# database.py - Conexión PostgreSQL con codificación LATIN1 para sistema de construcción
import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor
import os
import logging
import time
from datetime import datetime

logger = logging.getLogger(__name__)

# Configuración de conexión
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '123654'),
    'database': os.getenv('DB_NAME', 'constructora'),  # Corregido el nombre de la base de datos
    'client_encoding': 'LATIN1'
}

def get_connection():
    """Obtener conexión a PostgreSQL"""
    try:
        # Establecer variables de entorno para la conexión
        os.environ['PGCLIENTENCODING'] = 'LATIN1'
        os.environ['LC_ALL'] = 'C'
        
        # Crear la conexión
        conn = psycopg2.connect(**DB_CONFIG)
        
        # Configurar la codificación de la conexión
        conn.set_client_encoding('LATIN1')
        
        return conn
    except Exception as e:
        logger.error(f"Error conectando a PostgreSQL: {e}")
        return None

def test_connection():
    """Probar conexión a la base de datos"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT 1')
                logger.info(f"✅ Conectado a PostgreSQL -> {DB_CONFIG['database']}")
                return True
    except Exception as e:
        logger.error(f"❌ Error conectando a PostgreSQL: {e}")
        return False

# ===============================
# FUNCIONES DE FACTURACIÓN
# ===============================
def get_facturas_safe():
    """Obtener todas las facturas"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        f.id_factura as id,
                        f.id_factura as factura_id,
                        f.id_factura as id_factura,
                        f.numero_factura,
                        f.fecha_factura,
                        f.fecha_vencimiento,
                        f.subtotal,
                        f.impuestos,
                        f.descuento,
                        f.total,
                        f.estado_factura,
                        f.observaciones,
                        f.fecha_creacion,
                        c.nombre_cliente,
                        o.nombre_obra
                    FROM FACTURAS f
                    LEFT JOIN CLIENTES c ON f.id_cliente = c.id_cliente
                    LEFT JOIN FACTURA_OBRA fo ON f.id_factura = fo.id_factura
                    LEFT JOIN OBRAS o ON fo.id_obra = o.id_obra
                    ORDER BY f.fecha_factura DESC
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo facturas: {e}")
        return []

def get_contratos_facturables_safe():
    """Obtener contratos que pueden generar facturas"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM CONTRATOS_FACTURABLES
                    ORDER BY fecha_inicio DESC
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo contratos facturables: {e}")
        return []

def facturizar_contrato_safe(id_contrato: int):
    """Genera una factura a partir de un contrato.

    Intentará primero la función SQL facturizar_contrato(id).
    Si no existe o falla por incompatibilidades de esquema, hará un fallback en Python
    detectando columnas disponibles y generando la factura y sus detalles.

    Retorna el id_factura creado o None si falla.
    """
    # 1) Intento con función SQL
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT facturizar_contrato(%s)", (id_contrato,))
                result = cursor.fetchone()
                nuevo_id = None
                if result is None:
                    nuevo_id = None
                elif isinstance(result[0], (int,)):
                    nuevo_id = result[0]
                else:
                    try:
                        if hasattr(result[0], 'get'):
                            nuevo_id = result[0].get('id_factura') or result[0].get('factura_id')
                        else:
                            nuevo_id = int(result[0])
                    except Exception:
                        nuevo_id = None
                conn.commit()
                if nuevo_id:
                    logger.info(f"✅ Factura generada desde contrato %s: %s", id_contrato, nuevo_id)
                    return nuevo_id
    except Exception as e:
        logger.warning(f"No se pudo usar la función facturizar_contrato: {e}. Procediendo con fallback Python.")

    # 2) Fallback Python
    try:
        with get_connection() as conn:
            conn.autocommit = False
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Descubrir columnas actuales de FACTURAS
                cur.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'facturas' AND table_schema = current_schema()
                """)
                cols = {r['column_name'].lower() for r in cur.fetchall()}

                fecha_col = 'fecha_emision' if 'fecha_emision' in cols else ('fecha_factura' if 'fecha_factura' in cols else None)
                estado_col = 'estado' if 'estado' in cols else ('estado_factura' if 'estado_factura' in cols else None)
                iva_col = 'iva' if 'iva' in cols else ('impuestos' if 'impuestos' in cols else None)
                subtotal_col = 'subtotal' if 'subtotal' in cols else None
                total_col = 'total' if 'total' in cols else None
                tiene_id_cliente = 'id_cliente' in cols

                # Generar número de factura
                numero = generar_numero_factura_safe() or f"{int(time.time())}"

                # Obtener cliente: OBRA del contrato -> cliente (por OBRA_CLIENTE o columna directa en OBRAS)
                id_cliente = None
                try:
                    cur.execute(
                        """
                        SELECT oc.id_cliente
                        FROM CONTRATO_OBRA co
                        JOIN OBRA_CLIENTE oc ON oc.id_obra = co.id_obra
                        WHERE co.id_contrato = %s
                        LIMIT 1
                        """,
                        (id_contrato,),
                    )
                    r = cur.fetchone()
                    if r:
                        id_cliente = r['id_cliente']
                    else:
                        # Fallback: si OBRAS tiene id_cliente y hay relación en CONTRATO_OBRA
                        cur.execute(
                            """
                            SELECT o.id_cliente
                            FROM CONTRATO_OBRA co
                            JOIN OBRAS o ON o.id_obra = co.id_obra
                            WHERE co.id_contrato = %s
                            LIMIT 1
                            """,
                            (id_contrato,),
                        )
                        r2 = cur.fetchone()
                        if r2:
                            id_cliente = r2['id_cliente']
                except Exception:
                    pass

                # Armar INSERT dinámico
                campos = ["numero_factura", "id_contrato"]
                valores = [numero, id_contrato]
                if tiene_id_cliente:
                    campos.append("id_cliente")
                    valores.append(id_cliente)
                if fecha_col:
                    campos.append(fecha_col)
                    valores.append(datetime.now().date())
                # fecha_vencimiento si existe
                if 'fecha_vencimiento' in cols:
                    campos.append('fecha_vencimiento')
                    valores.append(None)
                if estado_col:
                    campos.append(estado_col)
                    valores.append('PENDIENTE')
                if 'observaciones' in cols:
                    campos.append('observaciones')
                    valores.append(None)

                placeholders = ','.join(['%s'] * len(valores))
                sql_insert = f"INSERT INTO FACTURAS ({', '.join(campos)}) VALUES ({placeholders}) RETURNING id_factura"
                cur.execute(sql_insert, tuple(valores))
                id_factura = cur.fetchone()['id_factura']

                # Insertar detalles desde trabajos del contrato
                cur.execute(
                    """
                    INSERT INTO DETALLES_FACTURA (id_factura, descripcion, cantidad, precio_unitario, subtotal)
                    SELECT 
                        %s AS id_factura,
                        'Detalle contrato #' || cdt.id_contrato || ' - ítem ' || dt.id_detalle_trabajo AS descripcion,
                        COALESCE(NULLIF(dt.cantidad_trabajo,0), 1) AS cantidad,
                        CASE 
                            WHEN COALESCE(NULLIF(dt.cantidad_trabajo,0), 1) = 0 THEN COALESCE(dt.total_trabajo,0)
                            WHEN dt.total_trabajo IS NOT NULL AND dt.cantidad_trabajo IS NOT NULL AND dt.cantidad_trabajo > 0 
                                THEN dt.total_trabajo / dt.cantidad_trabajo
                            ELSE 0
                        END AS precio_unitario,
                        COALESCE(dt.total_trabajo, 0) AS subtotal
                    FROM CONTRATO_DETALLE_TRABAJO cdt
                    JOIN DETALLES_TRABAJO dt ON dt.id_detalle_trabajo = cdt.id_detalle_trabajo
                    WHERE cdt.id_contrato = %s
                    """,
                    (id_factura, id_contrato),
                )

                # Calcular totales
                cur.execute("SELECT COALESCE(SUM(subtotal),0) AS sub FROM DETALLES_FACTURA WHERE id_factura=%s", (id_factura,))
                sub = cur.fetchone()['sub'] or 0
                iva_val = round(sub * 0.16, 2)
                total_val = sub + iva_val

                sets = []
                params = []
                if subtotal_col:
                    sets.append(f"{subtotal_col} = %s")
                    params.append(sub)
                if iva_col:
                    sets.append(f"{iva_col} = %s")
                    params.append(iva_val)
                if total_col:
                    sets.append(f"{total_col} = %s")
                    params.append(total_val)
                if sets:
                    params.append(id_factura)
                    cur.execute(f"UPDATE FACTURAS SET {', '.join(sets)} WHERE id_factura = %s", tuple(params))

                conn.commit()
                logger.info("✅ Factura generada (fallback) desde contrato %s: %s", id_contrato, id_factura)
                return id_factura
    except Exception as e:
        logger.error(f"Error en fallback de facturización para contrato {id_contrato}: {e}")
        try:
            conn.rollback()
        except Exception:
            pass
        return None

def insert_factura_safe(numero_factura, id_contrato, fecha_vencimiento, observaciones, metodo_pago):
    """Crear una nueva factura"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO FACTURAS (numero_factura, id_contrato, fecha_vencimiento, observaciones, metodo_pago)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id_factura
                """, (numero_factura, id_contrato, fecha_vencimiento, observaciones, metodo_pago))
                
                factura_id = cursor.fetchone()[0]
                conn.commit()
                logger.info(f"✅ Factura creada: {numero_factura}")
                return factura_id
    except Exception as e:
        logger.error(f"Error creando factura: {e}")
        return None

def get_factura_by_id_safe(factura_id: int):
    """Obtener factura por ID (usando datos de contratos)"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        c.id_contrato as id,
                        c.id_contrato as factura_id,
                        c.id_contrato as id_factura,
                        c.numero_factura,
                        c.fecha_emision_factura as fecha_emision,
                        c.fecha_fin_contrato as fecha_vencimiento,
                        c.subtotal_factura as subtotal,
                        c.iva_factura as iva,
                        c.total_factura as total,
                        c.estado_factura as estado,
                        c.tipo_pago_contrato as metodo_pago,
                        o.id_obra,
                        o.nombre_obra,
                        o.ubicacion_obra,
                        cl.id_cliente,
                        cl.nombre_cliente,
                        cl.documento_cliente,
                        cl.telefono_cliente,
                        cl.email_cliente,
                        cl.direccion_cliente
                    FROM CONTRATOS c
                    LEFT JOIN CONTRATO_OBRA co ON c.id_contrato = co.id_contrato
                    LEFT JOIN OBRAS o ON co.id_obra = o.id_obra
                    LEFT JOIN CLIENTES cl ON o.id_cliente = cl.id_cliente
                    WHERE c.id_contrato = %s
                """, (factura_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo factura por ID: {e}")
        return None

def update_factura_safe(factura_id: int, numero_factura=None, id_contrato=None, fecha_vencimiento=None, observaciones=None, metodo_pago=None, estado=None):
    """Actualizar factura existente"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE FACTURAS 
                    SET numero_factura = COALESCE(%s, numero_factura),
                        id_contrato = COALESCE(%s, id_contrato),
                        fecha_vencimiento = COALESCE(%s, fecha_vencimiento),
                        observaciones = COALESCE(%s, observaciones),
                        metodo_pago = COALESCE(%s, metodo_pago),
                        estado = COALESCE(%s, estado)
                    WHERE id_factura = %s
                """, (numero_factura, id_contrato, fecha_vencimiento, observaciones, metodo_pago, estado, factura_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error actualizando factura: {e}")
        return False

def delete_factura_safe(factura_id: int):
    """Eliminar factura"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM FACTURAS WHERE id_factura = %s", (factura_id,))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error eliminando factura: {e}")
        return False

def get_detalles_factura_safe(id_factura):
    """Obtener detalles de una factura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM DETALLES_FACTURA 
                    WHERE id_factura = %s
                    ORDER BY id_detalle
                """, (id_factura,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo detalles de factura: {e}")
        return []

def insert_detalle_factura_safe(id_factura, descripcion, cantidad, precio_unitario):
    """Agregar detalle a una factura"""
    try:
        subtotal = float(cantidad) * float(precio_unitario)
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO DETALLES_FACTURA (id_factura, descripcion, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_factura, descripcion, cantidad, precio_unitario, subtotal))
                conn.commit()
                logger.info(f"✅ Detalle agregado a factura {id_factura}")
                return True
    except Exception as e:
        logger.error(f"Error agregando detalle a factura: {e}")
        return False

def get_pagos_factura_safe(id_factura):
    """Obtener pagos de una factura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM PAGOS 
                    WHERE id_factura = %s
                    ORDER BY fecha_pago DESC
                """, (id_factura,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo pagos: {e}")
        return []

def generar_numero_factura_safe():
    """Generar un nuevo número de factura"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT generar_numero_factura()")
                numero = cursor.fetchone()[0]
                return numero
    except Exception as e:
        logger.error(f"Error generando número de factura: {e}")
        return f"2025-{str(int(time.time()))[6:]}"

# ===============================
# CONSULTAS SEGURAS PARA OBRAS
# ===============================
def get_obras_safe():
    """Obtener obras de forma segura manejando errores UTF-8"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                try:
                    # Intento extendido con campos de estimación
                    cursor.execute("""
                        SELECT 
                            o.id_obra,
                            o.id_obra as id,
                            o.id_obra as obra_id,
                            CASE 
                                WHEN o.nombre_obra IS NULL THEN 'Sin nombre'
                                WHEN LENGTH(TRIM(o.nombre_obra)) = 0 THEN 'Sin nombre'
                                ELSE REPLACE(REPLACE(REPLACE(TRIM(o.nombre_obra), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                            END as nombre,
                            CASE 
                                WHEN o.descripcion_obra IS NULL THEN ''
                                ELSE REPLACE(REPLACE(REPLACE(TRIM(o.descripcion_obra), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                            END as descripcion,
                            o.tipo_obra as tipo_obra,
                            CASE 
                                WHEN o.ubicacion_obra IS NULL THEN ''
                                ELSE REPLACE(REPLACE(REPLACE(TRIM(o.ubicacion_obra), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                            END as ubicacion,
                            o.fecha_inicio,
                            o.fecha_fin,
                            o.valor_obra as valor,
                            COALESCE(o.estado_obra, 'Sin estado') as estado,
                            o.id_tipo_obra,
                            o.es_precio_fijo,
                            o.area_m2,
                            o.cantidad_estimada,
                            o.unidad_estimacion,
                            o.precio_unitario_estimado,
                            o.valor_estimado,
                            CASE 
                                WHEN c.nombre_cliente IS NULL THEN 'Sin cliente'
                                ELSE REPLACE(REPLACE(REPLACE(TRIM(c.nombre_cliente), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                            END as cliente,
                            o.id_cliente
                        FROM OBRAS o
                        LEFT JOIN CLIENTES c ON o.id_cliente = c.id_cliente
                        WHERE o.id_obra IS NOT NULL
                        ORDER BY o.id_obra DESC
                        LIMIT 100
                    """)
                except Exception:
                    # Fallback sin columnas de estimación
                    cursor.execute("""
                        SELECT 
                            o.id_obra,
                            o.id_obra as id,
                            o.id_obra as obra_id,
                            CASE 
                                WHEN o.nombre_obra IS NULL THEN 'Sin nombre'
                                WHEN LENGTH(TRIM(o.nombre_obra)) = 0 THEN 'Sin nombre'
                                ELSE REPLACE(REPLACE(REPLACE(TRIM(o.nombre_obra), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                            END as nombre,
                            CASE 
                                WHEN o.descripcion_obra IS NULL THEN ''
                                ELSE REPLACE(REPLACE(REPLACE(TRIM(o.descripcion_obra), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                            END as descripcion,
                            o.tipo_obra as tipo_obra,
                            CASE 
                                WHEN o.ubicacion_obra IS NULL THEN ''
                                ELSE REPLACE(REPLACE(REPLACE(TRIM(o.ubicacion_obra), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                            END as ubicacion,
                            o.fecha_inicio,
                            o.fecha_fin,
                            o.valor_obra as valor,
                            COALESCE(o.estado_obra, 'Sin estado') as estado,
                            o.id_tipo_obra,
                            o.es_precio_fijo,
                            CASE 
                                WHEN c.nombre_cliente IS NULL THEN 'Sin cliente'
                                ELSE REPLACE(REPLACE(REPLACE(TRIM(c.nombre_cliente), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                            END as cliente,
                            o.id_cliente
                        FROM OBRAS o
                        LEFT JOIN CLIENTES c ON o.id_cliente = c.id_cliente
                        WHERE o.id_obra IS NOT NULL
                        ORDER BY o.id_obra DESC
                        LIMIT 100
                    """)
                
                results = cursor.fetchall()
                
                # Limpiar resultados
                clean_results = []
                for row in results:
                    clean_row = {}
                    for key, value in row.items():
                        if isinstance(value, str):
                            clean_row[key] = str(value).replace('ñ', 'n').replace('Ñ', 'N')
                        else:
                            clean_row[key] = value
                    clean_results.append(clean_row)
                
                return clean_results
                
    except Exception as e:
        logger.error(f"Error obteniendo obras: {e}")
        return []

def get_clientes_safe():
    """Obtener clientes de forma segura manejando errores UTF-8"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        id_cliente,
                        CASE 
                            WHEN nombre_cliente IS NULL THEN 'Sin nombre'
                            WHEN LENGTH(TRIM(nombre_cliente)) = 0 THEN 'Sin nombre'
                            ELSE REPLACE(REPLACE(REPLACE(TRIM(nombre_cliente), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                        END as nombre_cliente,
                        documento_cliente,
                        telefono_cliente,
                        email_cliente,
                        direccion_cliente
                    FROM CLIENTES 
                    WHERE id_cliente IS NOT NULL
                    ORDER BY nombre_cliente
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                
                # Limpiar resultados
                clean_results = []
                for row in results:
                    clean_row = {
                        'id': row['id_cliente'],
                        'nombre': str(row['nombre_cliente']).replace('ñ', 'n').replace('Ñ', 'N'),
                        'documento': row.get('documento_cliente'),
                        'telefono': row.get('telefono_cliente'),
                        'email': row.get('email_cliente'),
                        'direccion': row.get('direccion_cliente')
                    }
                    clean_results.append(clean_row)
                
                return clean_results
                
    except Exception as e:
        logger.error(f"Error obteniendo clientes: {e}")
        return []

def get_cliente_by_id_safe(cliente_id):
    """Obtener un cliente específico por ID con información disponible"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        c.id_cliente,
                        c.nombre_cliente,
                        c.documento_cliente,
                        c.telefono_cliente,
                        c.email_cliente,
                        c.direccion_cliente,
                        c.contacto_cliente,
                        c.tipo_cliente,
                        COUNT(o.id_obra) as total_proyectos,
                        COALESCE(SUM(o.valor_obra), 0) as valor_total_proyectos,
                        MAX(o.fecha_inicio) as ultimo_proyecto
                    FROM CLIENTES c
                    LEFT JOIN OBRAS o ON c.id_cliente = o.id_cliente
                    WHERE c.id_cliente = %s
                    GROUP BY c.id_cliente, c.nombre_cliente, 
                             c.documento_cliente, c.telefono_cliente, c.email_cliente,
                             c.direccion_cliente, c.contacto_cliente, c.tipo_cliente
                """, (cliente_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo cliente {cliente_id}: {e}")
        return None

def get_tipos_obra_safe(activos_only: bool = True):
    """Obtener catálogo de TIPOS_OBRA de forma segura.
    Devuelve: lista de dicts con id, nombre, unidad, rango, notas, precio_min, precio_max, precio_base, activo.
    """
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                base_sql = """
                    SELECT 
                        id_tipo_obra AS id,
                        id_tipo_obra,
                        nombre_tipo,
                        COALESCE(unidad_medida, '') AS unidad_medida,
                        COALESCE(rango_precio, '') AS rango_precio,
                        COALESCE(notas, '') AS notas,
                        precio_min,
                        precio_max,
                        precio_base,
                        activo
                    FROM TIPOS_OBRA
                """
                if activos_only:
                    base_sql += " WHERE activo = TRUE"
                base_sql += " ORDER BY nombre_tipo"
                cursor.execute(base_sql)
                rows = cursor.fetchall()
                # Normalizar strings evitando problemas de acentos
                clean = []
                for r in rows:
                    d = {}
                    for k, v in r.items():
                        if isinstance(v, str):
                            d[k] = v.replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ú', 'u').replace('ñ', 'n').replace('Ñ', 'N')
                        else:
                            d[k] = v
                    clean.append(d)
                return clean
    except Exception as e:
        logger.error(f"Error obteniendo TIPOS_OBRA: {e}")
        return []

def get_tipo_obra_by_id_safe(id_tipo_obra: int):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT id_tipo_obra, nombre_tipo, descripcion_base, unidad_medida, rango_precio, notas,
                           precio_min, precio_max, precio_base, activo
                    FROM TIPOS_OBRA WHERE id_tipo_obra = %s
                    """,
                    (id_tipo_obra,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error obteniendo tipo_obra por id: {e}")
        return None

def insert_tipo_obra_safe(nombre_tipo: str, descripcion_base=None, unidad_medida=None, rango_precio=None,
                          notas=None, precio_min=None, precio_max=None, precio_base: float = 0.0, activo: bool = True):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO TIPOS_OBRA (nombre_tipo, descripcion_base, unidad_medida, rango_precio, notas,
                                             precio_min, precio_max, precio_base, activo)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    RETURNING id_tipo_obra
                    """,
                    (nombre_tipo, descripcion_base, unidad_medida, rango_precio, notas,
                     precio_min, precio_max, precio_base, activo)
                )
                new_id = cursor.fetchone()[0]
                conn.commit()
                return new_id
    except Exception as e:
        logger.error(f"Error insertando tipo_obra: {e}")
        return None

def update_tipo_obra_safe(id_tipo_obra: int, nombre_tipo=None, descripcion_base=None, unidad_medida=None,
                          rango_precio=None, notas=None, precio_min=None, precio_max=None,
                          precio_base=None, activo=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE TIPOS_OBRA
                    SET nombre_tipo = COALESCE(%s, nombre_tipo),
                        descripcion_base = COALESCE(%s, descripcion_base),
                        unidad_medida = COALESCE(%s, unidad_medida),
                        rango_precio = COALESCE(%s, rango_precio),
                        notas = COALESCE(%s, notas),
                        precio_min = COALESCE(%s, precio_min),
                        precio_max = COALESCE(%s, precio_max),
                        precio_base = COALESCE(%s, precio_base),
                        activo = COALESCE(%s, activo)
                    WHERE id_tipo_obra = %s
                    """,
                    (nombre_tipo, descripcion_base, unidad_medida, rango_precio, notas,
                     precio_min, precio_max, precio_base, activo, id_tipo_obra)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error actualizando tipo_obra: {e}")
        return False

def toggle_tipo_obra_activo_safe(id_tipo_obra: int, activo: bool):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE TIPOS_OBRA SET activo = %s WHERE id_tipo_obra = %s",
                    (activo, id_tipo_obra)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error cambiando estado activo de tipo_obra: {e}")
        return False

def insert_cliente_safe(nombre, documento=None, telefono=None, email=None, direccion=None):
    """Insertar cliente de forma segura"""
    try:
        # Limpiar datos de entrada
        nombre_clean = str(nombre).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ú', 'u').replace('ñ', 'n')
        
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO CLIENTES (nombre_cliente, documento_cliente, telefono_cliente, email_cliente, direccion_cliente)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id_cliente
                """, (nombre_clean, documento, telefono, email, direccion))
                
                cliente_id = cursor.fetchone()['id_cliente']
                conn.commit()
                
                logger.info(f"Cliente creado exitosamente: ID {cliente_id}")
                return cliente_id
                
    except Exception as e:
        logger.error(f"Error insertando cliente: {e}")
        return None

def update_cliente_safe(cliente_id: int, nombre=None, documento=None, telefono=None, email=None, direccion=None, tipo_cliente=None):
    """Actualizar cliente de forma segura"""
    try:
        # Construir dinámicamente la consulta UPDATE
        campos = []
        valores = []
        
        if nombre is not None:
            nombre_clean = str(nombre).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ú', 'u').replace('ñ', 'n')
            campos.append("nombre_cliente = %s")
            valores.append(nombre_clean)
        
        if documento is not None:
            campos.append("documento_cliente = %s")
            valores.append(documento)
            
        if telefono is not None:
            campos.append("telefono_cliente = %s")
            valores.append(telefono)
            
        if email is not None:
            campos.append("email_cliente = %s")
            valores.append(email)
            
        if direccion is not None:
            direccion_clean = str(direccion).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ú', 'u').replace('ñ', 'n')
            campos.append("direccion_cliente = %s")
            valores.append(direccion_clean)
        
        if not campos:
            logger.warning(f"No hay campos para actualizar en cliente {cliente_id}")
            return True
        
        # Agregar ID al final de los valores
        valores.append(cliente_id)
        
        with get_connection() as conn:
            with conn.cursor() as cursor:
                consulta = f"UPDATE CLIENTES SET {', '.join(campos)} WHERE id_cliente = %s"
                cursor.execute(consulta, valores)
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Cliente {cliente_id} actualizado exitosamente")
                    return True
                else:
                    logger.warning(f"Cliente {cliente_id} no encontrado para actualizar")
                    return False
                    
    except Exception as e:
        logger.error(f"Error actualizando cliente {cliente_id}: {e}")
        return False

def delete_cliente_safe(cliente_id: int):
    """Eliminar cliente de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM CLIENTES WHERE id_cliente = %s", (cliente_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Cliente {cliente_id} eliminado exitosamente")
                    return True
                else:
                    logger.warning(f"Cliente {cliente_id} no encontrado para eliminar")
                    return False
                    
    except Exception as e:
        logger.error(f"Error eliminando cliente {cliente_id}: {e}")
        return False

def insert_obra_safe(nombre, descripcion=None, ubicacion=None, fecha_inicio=None, fecha_fin=None, valor=None, estado='Planeación', cliente_id=None, id_tipo_obra=None, es_precio_fijo=None,
                    area_m2=None, cantidad_estimada=None, unidad_estimacion=None, precio_unitario_estimado=None, valor_estimado=None):
    """Insertar obra de forma segura con cliente obligatorio"""
    try:
        # Validar que se proporcione cliente
        if not cliente_id:
            raise ValueError("El cliente es obligatorio para crear una obra")
        
        # Limpiar datos de entrada
        nombre_clean = str(nombre).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ú', 'u').replace('ñ', 'n')
        descripcion_clean = None
        if descripcion:
            descripcion_clean = str(descripcion).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ú', 'u').replace('ñ', 'n')
        ubicacion_clean = None
        if ubicacion:
            ubicacion_clean = str(ubicacion).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ú', 'u').replace('ñ', 'n')
        
        with get_connection() as conn:
            conn.autocommit = False

            try:
                # Verificar que el cliente existe (fuera de los intentos de insert)
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    cursor.execute("SELECT id_cliente FROM CLIENTES WHERE id_cliente = %s", (cliente_id,))
                    if not cursor.fetchone():
                        raise ValueError(f"El cliente con ID {cliente_id} no existe")

                last_error = None
                # Intento 1: obra fija + estimación
                try:
                    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                        cursor.execute(
                            """
                            INSERT INTO OBRAS (
                                nombre_obra, descripcion_obra, ubicacion_obra,
                                fecha_inicio, fecha_fin, valor_obra, estado_obra,
                                id_cliente, id_tipo_obra, es_precio_fijo,
                                area_m2, cantidad_estimada, unidad_estimacion,
                                precio_unitario_estimado, valor_estimado
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            RETURNING id_obra
                            """,
                            (nombre_clean, descripcion_clean, ubicacion_clean,
                             fecha_inicio, fecha_fin, valor, estado,
                             cliente_id, id_tipo_obra, es_precio_fijo,
                             area_m2, cantidad_estimada, unidad_estimacion,
                             precio_unitario_estimado, valor_estimado)
                        )
                        obra_id = cursor.fetchone()['id_obra']
                        conn.commit()
                        logger.info(f"Obra creada exitosamente: ID {obra_id} para cliente {cliente_id}")
                        return obra_id
                except Exception as e1:
                    last_error = e1
                    logger.debug(f"Fallback insert obra sin columnas de estimación: {e1}")
                    conn.rollback()

                # Intento 2: solo obra fija
                try:
                    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                        cursor.execute(
                            """
                            INSERT INTO OBRAS (
                                nombre_obra, descripcion_obra, ubicacion_obra,
                                fecha_inicio, fecha_fin, valor_obra, estado_obra,
                                id_cliente, id_tipo_obra, es_precio_fijo
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            RETURNING id_obra
                            """,
                            (nombre_clean, descripcion_clean, ubicacion_clean,
                             fecha_inicio, fecha_fin, valor, estado,
                             cliente_id, id_tipo_obra, es_precio_fijo)
                        )
                        obra_id = cursor.fetchone()['id_obra']
                        conn.commit()
                        logger.info(f"Obra creada exitosamente (fallback fijo): ID {obra_id} para cliente {cliente_id}")
                        return obra_id
                except Exception as e2:
                    last_error = e2
                    logger.debug(f"Fallback insert obra básico tras error en fijo: {e2}")
                    conn.rollback()

                # Intento 3: base mínima
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        INSERT INTO OBRAS (
                            nombre_obra, descripcion_obra, ubicacion_obra,
                            fecha_inicio, fecha_fin, valor_obra, estado_obra,
                            id_cliente
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id_obra
                        """,
                        (nombre_clean, descripcion_clean, ubicacion_clean,
                         fecha_inicio, fecha_fin, valor, estado, cliente_id)
                    )
                    obra_id = cursor.fetchone()['id_obra']
                    conn.commit()
                    logger.info(f"Obra creada exitosamente (fallback básico): ID {obra_id} para cliente {cliente_id}")
                    return obra_id

            except Exception as e:
                conn.rollback()
                raise e
                
    except Exception as e:
        logger.error(f"Error insertando obra: {e}")
        raise Exception(f"No se pudo crear la obra: {str(e)}")

# ===============================
# CONSULTAS SEGURAS PARA EMPLEADOS
# ===============================
def get_empleados_safe():
    """Obtener empleados de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        id_empleado,
                        nombre_empleado,
                        apellido_empleado,
                        tipo_empleado,
                        salario_fijo_empleado,
                        telefono,
                        email,
                        fecha_ingreso
                    FROM empleados 
                    ORDER BY nombre_empleado
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                clean_results = []
                for row in results:
                    clean_row = {}
                    for key, value in row.items():
                        if isinstance(value, str):
                            clean_row[key] = str(value).replace('ñ', 'n').replace('Ñ', 'N')
                        else:
                            clean_row[key] = value
                    clean_results.append(clean_row)
                
                return clean_results
                
    except Exception as e:
        logger.error(f"Error obteniendo empleados: {e}")
        return []

def insert_empleado_safe(nombre, apellido=None, tipo=None, salario=None, telefono=None, email=None, fecha_ingreso=None):
    """Insertar empleado de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO empleados (nombre_empleado, apellido_empleado, tipo_empleado, salario_fijo_empleado, telefono, email, fecha_ingreso)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_empleado
                """, (nombre, apellido, tipo, salario, telefono, email, fecha_ingreso))
                
                empleado_id = cursor.fetchone()['id_empleado']
                conn.commit()
                
                logger.info(f"Empleado creado: ID {empleado_id}")
                return empleado_id
                
    except Exception as e:
        logger.error(f"Error insertando empleado: {e}")
        return None

# ===== CRUD Empleados adicionales =====
def get_empleado_by_id_safe(empleado_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT 
                        id_empleado,
                        nombre_empleado,
                        apellido_empleado,
                        tipo_empleado,
                        salario_fijo_empleado,
                        telefono,
                        email,
                        fecha_ingreso
                    FROM empleados
                    WHERE id_empleado = %s
                    """,
                    (empleado_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error obteniendo empleado por id: {e}")
        return None

def update_empleado_safe(empleado_id: int, nombre=None, apellido=None, tipo=None, salario=None, telefono=None, email=None, fecha_ingreso=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE empleados
                    SET nombre_empleado = COALESCE(%s, nombre_empleado),
                        apellido_empleado = COALESCE(%s, apellido_empleado),
                        tipo_empleado = COALESCE(%s, tipo_empleado),
                        salario_fijo_empleado = COALESCE(%s, salario_fijo_empleado),
                        telefono = COALESCE(%s, telefono),
                        email = COALESCE(%s, email),
                        fecha_ingreso = COALESCE(%s, fecha_ingreso)
                    WHERE id_empleado = %s
                    """,
                    (nombre, apellido, tipo, salario, telefono, email, fecha_ingreso, empleado_id)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error actualizando empleado: {e}")
        return False

def delete_empleado_safe(empleado_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM empleados WHERE id_empleado = %s", (empleado_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error eliminando empleado: {e}")
        return False

# ===============================
# CONSULTAS SEGURAS PARA PROVEEDORES
# ===============================
def get_proveedores_safe():
    """Obtener proveedores de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        id_proveedor,
                        CASE 
                            WHEN nombre_proveedor IS NULL THEN 'Sin nombre'
                            ELSE REPLACE(REPLACE(REPLACE(TRIM(nombre_proveedor), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                        END as nombre,
                        contacto_proveedor as contacto
                    FROM PROVEEDORES 
                    ORDER BY nombre_proveedor
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                clean_results = []
                for row in results:
                    clean_row = {}
                    for key, value in row.items():
                        if isinstance(value, str):
                            clean_row[key] = str(value).replace('ñ', 'n').replace('Ñ', 'N')
                        else:
                            clean_row[key] = value
                    clean_results.append(clean_row)
                
                return clean_results
                
    except Exception as e:
        logger.error(f"Error obteniendo proveedores: {e}")
        return []

def insert_proveedor_safe(nombre, contacto=None):
    """Insertar proveedor de forma segura"""
    try:
        nombre_clean = str(nombre).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('ñ', 'n')
        
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO PROVEEDORES (nombre_proveedor, contacto_proveedor)
                    VALUES (%s, %s) RETURNING id_proveedor
                """, (nombre_clean, contacto))
                
                proveedor_id = cursor.fetchone()['id_proveedor']
                conn.commit()
                
                logger.info(f"Proveedor creado: ID {proveedor_id}")
                return proveedor_id
                
    except Exception as e:
        logger.error(f"Error insertando proveedor: {e}")
        return None

# ===== CRUD Proveedores adicionales =====
def get_proveedor_by_id_safe(proveedor_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT 
                        id_proveedor,
                        id_proveedor as proveedor_id,
                        nombre_proveedor AS nombre,
                        contacto_proveedor AS contacto,
                        contacto_proveedor AS telefono,
                        '' as email,
                        '' as direccion,
                        'Comercial' as tipo,
                        'Activo' as estado
                    FROM PROVEEDORES
                    WHERE id_proveedor = %s
                    """,
                    (proveedor_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error obteniendo proveedor por id: {e}")
        return None

def update_proveedor_safe(proveedor_id: int, nombre=None, contacto=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE PROVEEDORES
                    SET nombre_proveedor = COALESCE(%s, nombre_proveedor),
                        contacto_proveedor = COALESCE(%s, contacto_proveedor)
                    WHERE id_proveedor = %s
                    """,
                    (nombre, contacto, proveedor_id)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error actualizando proveedor: {e}")
        return False

def delete_proveedor_safe(proveedor_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM PROVEEDORES WHERE id_proveedor = %s", (proveedor_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error eliminando proveedor: {e}")
        return False

# ===============================
# CONSULTAS SEGURAS PARA MATERIALES
# ===============================
def get_materiales_safe():
    """Obtener materiales de forma segura con información completa de proveedores y stock"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        m.id_material,
                        m.id_material as id,
                        m.id_material as material_id,
                        CASE 
                            WHEN m.nombre_material IS NULL THEN 'Sin nombre'
                            ELSE REPLACE(REPLACE(REPLACE(TRIM(m.nombre_material), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                        END as nombre,
                        m.unidad_material as unidad,
                        m.unidad_material as unidad_medida,
                        m.precio_unitario_material as precio,
                        m.precio_unitario_material as precio_unitario,
                        COALESCE(i.cantidad_inventario, 0) as stock,
                        COALESCE(i.cantidad_inventario, 0) as stock_actual,
                        50 as stock_minimo,
                        p.nombre_proveedor as proveedor_nombre,
                        p.contacto_proveedor as proveedor_contacto,
                        COALESCE(m.descripcion_material, 'Sin descripción') as descripcion,
                        COALESCE(m.categoria_material, 'Sin categoría') as categoria,
                        'Activo' as estado
                    FROM MATERIALES m
                    LEFT JOIN proveedor_material pm ON m.id_material = pm.id_material
                    LEFT JOIN proveedores p ON pm.id_proveedor = p.id_proveedor
                    LEFT JOIN inventario_material im ON m.id_material = im.id_material
                    LEFT JOIN inventarios i ON im.id_inventario = i.id_inventario
                    ORDER BY m.nombre_material
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                clean_results = []
                for row in results:
                    clean_row = {}
                    for key, value in row.items():
                        if isinstance(value, str):
                            clean_row[key] = str(value).replace('ñ', 'n').replace('Ñ', 'N')
                        else:
                            clean_row[key] = value
                    clean_results.append(clean_row)
                
                return clean_results
                
    except Exception as e:
        logger.error(f"Error obteniendo materiales: {e}")
        return []

def insert_material_safe(nombre, unidad=None, precio=None):
    """Insertar material de forma segura"""
    try:
        nombre_clean = str(nombre).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('ñ', 'n')
        
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO MATERIALES (nombre_material, unidad_material, precio_unitario_material)
                    VALUES (%s, %s, %s) RETURNING id_material
                """, (nombre_clean, unidad, precio))
                
                material_id = cursor.fetchone()['id_material']
                conn.commit()
                
                logger.info(f"Material creado: ID {material_id}")
                return material_id
                
    except Exception as e:
        logger.error(f"Error insertando material: {e}")
        return None

# ===== CRUD Materiales adicionales =====
def get_material_by_id_safe(material_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT 
                        m.id_material,
                        m.id_material as id,
                        m.id_material as material_id,
                        m.nombre_material AS nombre,
                        m.unidad_material AS unidad,
                        m.precio_unitario_material AS precio,
                        m.precio_unitario_material AS precio_unitario,
                        COALESCE(i.cantidad_inventario, 0) as stock,
                        COALESCE(i.cantidad_inventario, 0) as stock_actual,
                        50 as stock_minimo,
                        p.nombre_proveedor as proveedor_nombre,
                        p.contacto_proveedor as proveedor_contacto,
                        COALESCE(m.descripcion_material, 'Sin descripción') as descripcion,
                        COALESCE(m.categoria_material, 'Sin categoría') as categoria,
                        'Activo' as estado
                    FROM MATERIALES m
                    LEFT JOIN proveedor_material pm ON m.id_material = pm.id_material
                    LEFT JOIN proveedores p ON pm.id_proveedor = p.id_proveedor
                    LEFT JOIN inventario_material im ON m.id_material = im.id_material
                    LEFT JOIN inventarios i ON im.id_inventario = i.id_inventario
                    WHERE m.id_material = %s
                    """,
                    (material_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error obteniendo material por id: {e}")
        return None

def update_material_safe(material_id: int, nombre=None, unidad=None, precio=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE MATERIALES
                    SET nombre_material = COALESCE(%s, nombre_material),
                        unidad_material = COALESCE(%s, unidad_material),
                        precio_unitario_material = COALESCE(%s, precio_unitario_material)
                    WHERE id_material = %s
                    """,
                    (nombre, unidad, precio, material_id)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error actualizando material: {e}")
        return False

def update_material_completo_safe(material_id: int, nombre=None, unidad=None, precio=None, descripcion=None, categoria=None, stock=None):
    """Actualizar material completo incluyendo stock en inventario"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # 1. Actualizar datos básicos del material
                cursor.execute(
                    """
                    UPDATE MATERIALES
                    SET nombre_material = COALESCE(%s, nombre_material),
                        unidad_material = COALESCE(%s, unidad_material),
                        precio_unitario_material = COALESCE(%s, precio_unitario_material),
                        descripcion_material = COALESCE(%s, descripcion_material),
                        categoria_material = COALESCE(%s, categoria_material)
                    WHERE id_material = %s
                    """,
                    (nombre, unidad, precio, descripcion, categoria, material_id)
                )
                
                # 2. Actualizar stock si se proporcionó
                if stock is not None:
                    # Buscar el inventario asociado al material
                    cursor.execute("""
                        SELECT i.id_inventario
                        FROM inventario_material im
                        JOIN inventarios i ON im.id_inventario = i.id_inventario
                        WHERE im.id_material = %s
                    """, (material_id,))
                    
                    inventario_result = cursor.fetchone()
                    
                    if inventario_result:
                        # Actualizar inventario existente
                        inventario_id = inventario_result[0]
                        cursor.execute("""
                            UPDATE inventarios 
                            SET cantidad_inventario = %s
                            WHERE id_inventario = %s
                        """, (stock, inventario_id))
                    else:
                        # Crear nuevo inventario si no existe
                        cursor.execute("""
                            INSERT INTO inventarios (cantidad_inventario)
                            VALUES (%s)
                            RETURNING id_inventario
                        """, (stock,))
                        inventario_id = cursor.fetchone()[0]
                        
                        # Asociar con el material
                        cursor.execute("""
                            INSERT INTO inventario_material (id_inventario, id_material)
                            VALUES (%s, %s)
                        """, (inventario_id, material_id))
                
                conn.commit()
                return True
                
    except Exception as e:
        logger.error(f"Error actualizando material completo: {e}")
        return False

def delete_material_safe(material_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM MATERIALES WHERE id_material = %s", (material_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error eliminando material: {e}")
        return False

# ===============================
# CONSULTAS SEGURAS PARA VEHÍCULOS
# ===============================
def get_vehiculos_safe():
    """Obtener vehículos de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        id_vehiculo,
                        placa_vehiculo,
                        estado_vehiculo,
                        tipo_vehiculo
                    FROM VEHICULOS 
                    ORDER BY placa_vehiculo
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                return [dict(row) for row in results]
                
    except Exception as e:
        logger.error(f"Error obteniendo vehículos: {e}")
        return []

def insert_vehiculo_safe(placa, estado=None, tipo=None):
    """Insertar vehículo de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO VEHICULOS (placa_vehiculo, estado_vehiculo, tipo_vehiculo)
                    VALUES (%s, %s, %s) RETURNING id_vehiculo
                """, (placa, estado, tipo))
                
                vehiculo_id = cursor.fetchone()['id_vehiculo']
                conn.commit()
                
                logger.info(f"Vehículo creado: ID {vehiculo_id}")
                return vehiculo_id
                
    except Exception as e:
        logger.error(f"Error insertando vehículo: {e}")
        return None

# ===== CRUD Vehículos adicionales =====
def get_vehiculo_by_id_safe(vehiculo_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT 
                        id_vehiculo,
                        placa_vehiculo AS placa,
                        estado_vehiculo AS estado,
                        tipo_vehiculo AS tipo
                    FROM VEHICULOS
                    WHERE id_vehiculo = %s
                    """,
                    (vehiculo_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error obteniendo vehículo por id: {e}")
        return None

def update_vehiculo_safe(vehiculo_id: int, placa=None, estado=None, tipo=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE VEHICULOS
                    SET placa_vehiculo = COALESCE(%s, placa_vehiculo),
                        estado_vehiculo = COALESCE(%s, estado_vehiculo),
                        tipo_vehiculo = COALESCE(%s, tipo_vehiculo)
                    WHERE id_vehiculo = %s
                    """,
                    (placa, estado, tipo, vehiculo_id)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error actualizando vehículo: {e}")
        return False

def delete_vehiculo_safe(vehiculo_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM VEHICULOS WHERE id_vehiculo = %s", (vehiculo_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error eliminando vehículo: {e}")
        return False

# ===============================
# CONSULTAS SEGURAS PARA EQUIPOS
# ===============================
def get_equipos_safe():
    """Obtener equipos de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        id_equipo,
                        CASE 
                            WHEN nombre_equipo IS NULL THEN 'Sin nombre'
                            ELSE REPLACE(REPLACE(REPLACE(TRIM(nombre_equipo), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                        END as nombre,
                        estado_equipo as estado,
                        tipo_equipo as tipo
                    FROM EQUIPOS 
                    ORDER BY nombre_equipo
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                clean_results = []
                for row in results:
                    clean_row = {}
                    for key, value in row.items():
                        if isinstance(value, str):
                            clean_row[key] = str(value).replace('ñ', 'n').replace('Ñ', 'N')
                        else:
                            clean_row[key] = value
                    clean_results.append(clean_row)
                
                return clean_results
                
    except Exception as e:
        logger.error(f"Error obteniendo equipos: {e}")
        return []

def insert_equipo_safe(nombre, estado=None, tipo=None):
    """Insertar equipo de forma segura"""
    try:
        nombre_clean = str(nombre).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('ñ', 'n')
        
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO EQUIPOS (nombre_equipo, estado_equipo, tipo_equipo)
                    VALUES (%s, %s, %s) RETURNING id_equipo
                """, (nombre_clean, estado, tipo))
                
                equipo_id = cursor.fetchone()['id_equipo']
                conn.commit()
                
                logger.info(f"Equipo creado: ID {equipo_id}")
                return equipo_id
                
    except Exception as e:
        logger.error(f"Error insertando equipo: {e}")
        return None

# ===== CRUD Equipos adicionales =====
def get_equipo_by_id_safe(equipo_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT 
                        id_equipo,
                        id_equipo as equipo_id,
                        nombre_equipo AS nombre,
                        estado_equipo AS estado,
                        tipo_equipo AS tipo,
                        '' as marca,
                        '' as modelo,
                        '' as ubicacion,
                        null as ultimo_mantenimiento,
                        '' as capacidad,
                        'Disponible' as estado_actual
                    FROM EQUIPOS
                    WHERE id_equipo = %s
                    """,
                    (equipo_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error obteniendo equipo por id: {e}")
        return None

def update_equipo_safe(equipo_id: int, nombre=None, estado=None, tipo=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE EQUIPOS
                    SET nombre_equipo = COALESCE(%s, nombre_equipo),
                        estado_equipo = COALESCE(%s, estado_equipo),
                        tipo_equipo = COALESCE(%s, tipo_equipo)
                    WHERE id_equipo = %s
                    """,
                    (nombre, estado, tipo, equipo_id)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error actualizando equipo: {e}")
        return False

def delete_equipo_safe(equipo_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM EQUIPOS WHERE id_equipo = %s", (equipo_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error eliminando equipo: {e}")
        return False

# ===============================
# CONSULTAS SEGURAS PARA PROYECTOS
# ===============================
def get_proyectos_safe():
    """Obtener proyectos de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        id_proyecto,
                        id_proyecto as id,
                        id_proyecto as proyecto_id,
                        CASE 
                            WHEN nombre_proyecto IS NULL THEN 'Sin nombre'
                            ELSE REPLACE(REPLACE(REPLACE(TRIM(nombre_proyecto), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                        END as nombre,
                        fecha_inicio_proyecto as fecha_inicio,
                        fecha_fin_proyecto as fecha_fin,
                        estado_proyecto as estado
                    FROM PROYECTOS 
                    ORDER BY nombre_proyecto
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                clean_results = []
                for row in results:
                    clean_row = {}
                    for key, value in row.items():
                        if isinstance(value, str):
                            clean_row[key] = str(value).replace('ñ', 'n').replace('Ñ', 'N')
                        else:
                            clean_row[key] = value
                    clean_results.append(clean_row)
                
                return clean_results
                
    except Exception as e:
        logger.error(f"Error obteniendo proyectos: {e}")
        return []

def insert_proyecto_safe(nombre, fecha_inicio=None, fecha_fin=None, estado='Planeación'):
    """Insertar proyecto de forma segura"""
    try:
        nombre_clean = str(nombre).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('ñ', 'n')
        
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO PROYECTOS (nombre_proyecto, fecha_inicio_proyecto, fecha_fin_proyecto, estado_proyecto)
                    VALUES (%s, %s, %s, %s) RETURNING id_proyecto
                """, (nombre_clean, fecha_inicio, fecha_fin, estado))
                
                proyecto_id = cursor.fetchone()['id_proyecto']
                conn.commit()
                
                logger.info(f"Proyecto creado: ID {proyecto_id}")
                return proyecto_id
                
    except Exception as e:
        logger.error(f"Error insertando proyecto: {e}")
        return None

# ===== CRUD Proyectos adicionales =====
def get_proyecto_by_id_safe(proyecto_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT 
                        id_proyecto,
                        id_proyecto as id,
                        id_proyecto as proyecto_id,
                        nombre_proyecto AS nombre,
                        fecha_inicio_proyecto AS fecha_inicio,
                        fecha_fin_proyecto AS fecha_fin,
                        estado_proyecto AS estado
                    FROM PROYECTOS
                    WHERE id_proyecto = %s
                    """,
                    (proyecto_id,)
                )
                row = cursor.fetchone()
                return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error obteniendo proyecto por id: {e}")
        return None

def update_proyecto_safe(proyecto_id: int, nombre=None, fecha_inicio=None, fecha_fin=None, estado=None):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE PROYECTOS
                    SET nombre_proyecto = COALESCE(%s, nombre_proyecto),
                        fecha_inicio_proyecto = COALESCE(%s, fecha_inicio_proyecto),
                        fecha_fin_proyecto = COALESCE(%s, fecha_fin_proyecto),
                        estado_proyecto = COALESCE(%s, estado_proyecto)
                    WHERE id_proyecto = %s
                    """,
                    (nombre, fecha_inicio, fecha_fin, estado, proyecto_id)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error actualizando proyecto: {e}")
        return False

def delete_proyecto_safe(proyecto_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM PROYECTOS WHERE id_proyecto = %s", (proyecto_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error eliminando proyecto: {e}")
        return False

# ===== CRUD Obras adicionales =====
def get_obra_by_id_safe(obra_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                try:
                    cursor.execute(
                        """
                        SELECT 
                            o.id_obra,
                            o.id_obra as id,
                            o.id_obra as obra_id,
                            o.nombre_obra AS nombre,
                            o.descripcion_obra AS descripcion,
                            o.tipo_obra AS tipo_obra,
                            o.ubicacion_obra AS ubicacion,
                            o.fecha_inicio,
                            o.fecha_fin,
                            o.valor_obra AS valor,
                            o.estado_obra AS estado,
                            o.id_cliente,
                            o.id_tipo_obra,
                            o.es_precio_fijo,
                            o.area_m2,
                            o.cantidad_estimada,
                            o.unidad_estimacion,
                            o.precio_unitario_estimado,
                            o.valor_estimado,
                            c.nombre_cliente,
                            c.telefono_cliente,
                            c.email_cliente,
                            c.direccion_cliente,
                            c.documento_cliente
                        FROM OBRAS o
                        LEFT JOIN CLIENTES c ON o.id_cliente = c.id_cliente
                        WHERE o.id_obra = %s
                        """,
                        (obra_id,)
                    )
                except Exception:
                    cursor.execute(
                        """
                        SELECT 
                            o.id_obra,
                            o.id_obra as id,
                            o.id_obra as obra_id,
                            o.nombre_obra AS nombre,
                            o.descripcion_obra AS descripcion,
                            o.tipo_obra AS tipo_obra,
                            o.ubicacion_obra AS ubicacion,
                            o.fecha_inicio,
                            o.fecha_fin,
                            o.valor_obra AS valor,
                            o.estado_obra AS estado,
                            o.id_cliente,
                            o.id_tipo_obra,
                            o.es_precio_fijo,
                            c.nombre_cliente,
                            c.telefono_cliente,
                            c.email_cliente,
                            c.direccion_cliente,
                            c.documento_cliente
                        FROM OBRAS o
                        LEFT JOIN CLIENTES c ON o.id_cliente = c.id_cliente
                        WHERE o.id_obra = %s
                        """,
                        (obra_id,)
                    )
                row = cursor.fetchone()
                return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error obteniendo obra por id: {e}")
        return None

def update_obra_safe(obra_id: int, nombre=None, descripcion=None, ubicacion=None, fecha_inicio=None, fecha_fin=None, valor=None, estado=None, id_cliente=None, id_tipo_obra=None, es_precio_fijo=None,
                    area_m2=None, cantidad_estimada=None, unidad_estimacion=None, precio_unitario_estimado=None, valor_estimado=None):
    try:
        with get_connection() as conn:
            conn.autocommit = False
            try:
                # Intento 1: actualizar con obra fija + estimación
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE OBRAS
                        SET nombre_obra = COALESCE(%s, nombre_obra),
                            descripcion_obra = COALESCE(%s, descripcion_obra),
                            ubicacion_obra = COALESCE(%s, ubicacion_obra),
                            fecha_inicio = COALESCE(%s, fecha_inicio),
                            fecha_fin = COALESCE(%s, fecha_fin),
                            valor_obra = COALESCE(%s, valor_obra),
                            estado_obra = COALESCE(%s, estado_obra),
                            id_cliente = COALESCE(%s, id_cliente),
                            id_tipo_obra = COALESCE(%s, id_tipo_obra),
                            es_precio_fijo = COALESCE(%s, es_precio_fijo),
                            area_m2 = COALESCE(%s, area_m2),
                            cantidad_estimada = COALESCE(%s, cantidad_estimada),
                            unidad_estimacion = COALESCE(%s, unidad_estimacion),
                            precio_unitario_estimado = COALESCE(%s, precio_unitario_estimado),
                            valor_estimado = COALESCE(%s, valor_estimado)
                        WHERE id_obra = %s
                        """,
                        (nombre, descripcion, ubicacion, fecha_inicio, fecha_fin, valor, estado, id_cliente, id_tipo_obra, es_precio_fijo,
                         area_m2, cantidad_estimada, unidad_estimacion, precio_unitario_estimado, valor_estimado, obra_id)
                    )
                    conn.commit()
                    return cursor.rowcount > 0
            except Exception as e1:
                logger.debug(f"Fallback update obra sin columnas de estimación: {e1}")
                conn.rollback()

            try:
                # Intento 2: sin columnas de estimación
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE OBRAS
                        SET nombre_obra = COALESCE(%s, nombre_obra),
                            descripcion_obra = COALESCE(%s, descripcion_obra),
                            ubicacion_obra = COALESCE(%s, ubicacion_obra),
                            fecha_inicio = COALESCE(%s, fecha_inicio),
                            fecha_fin = COALESCE(%s, fecha_fin),
                            valor_obra = COALESCE(%s, valor_obra),
                            estado_obra = COALESCE(%s, estado_obra),
                            id_cliente = COALESCE(%s, id_cliente),
                            id_tipo_obra = COALESCE(%s, id_tipo_obra),
                            es_precio_fijo = COALESCE(%s, es_precio_fijo)
                        WHERE id_obra = %s
                        """,
                        (nombre, descripcion, ubicacion, fecha_inicio, fecha_fin, valor, estado, id_cliente, id_tipo_obra, es_precio_fijo, obra_id)
                    )
                    conn.commit()
                    return cursor.rowcount > 0
            except Exception as e2:
                logger.debug(f"Fallback update obra básico: {e2}")
                conn.rollback()

            # Intento 3: básico
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE OBRAS
                    SET nombre_obra = COALESCE(%s, nombre_obra),
                        descripcion_obra = COALESCE(%s, descripcion_obra),
                        ubicacion_obra = COALESCE(%s, ubicacion_obra),
                        fecha_inicio = COALESCE(%s, fecha_inicio),
                        fecha_fin = COALESCE(%s, fecha_fin),
                        valor_obra = COALESCE(%s, valor_obra),
                        estado_obra = COALESCE(%s, estado_obra),
                        id_cliente = COALESCE(%s, id_cliente)
                    WHERE id_obra = %s
                    """,
                    (nombre, descripcion, ubicacion, fecha_inicio, fecha_fin, valor, estado, id_cliente, obra_id)
                )
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error actualizando obra: {e}")
        return False

def delete_obra_safe(obra_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM OBRAS WHERE id_obra = %s", (obra_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error eliminando obra: {e}")
        return False

# ===============================
# CONSULTAS SEGURAS PARA ÁREAS
# ===============================
def get_areas_safe():
    """Obtener áreas de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Usamos bytea para evitar problemas de codificación
                cursor.execute("""
                    SELECT id_area, encode(nombre_area::bytea, 'escape') as nombre_area 
                    FROM AREAS 
                    ORDER BY nombre_area
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                return [
                    {
                        'id_area': row[0],
                        'nombre': row[1]
                    }
                    for row in results
                ]
                
    except Exception as e:
        logger.error(f"Error obteniendo áreas: {e}")
        return []
                
    except Exception as e:
        # Intento fallback: leer los bytes de la columna con convert_to(...) y
        # decodificarlos en Python usando LATIN1 para evitar errores de UTF-8
        logger.warning(f"Error obteniendo áreas con la consulta estándar: {e}. Intentando fallback de codificación.")
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_area, convert_to(nombre_area, 'LATIN1') AS nombre_bytes
                        FROM AREAS
                        ORDER BY nombre_area
                        LIMIT 100
                    """)
                    rows = cursor.fetchall()
                    clean_results = []
                    for r in rows:
                        # r[0] = id_area, r[1] = bytes
                        id_area = r[0]
                        nombre_bytes = r[1]
                        if hasattr(nombre_bytes, 'tobytes'):
                            nb = nombre_bytes.tobytes()
                        else:
                            nb = nombre_bytes
                        try:
                            nombre = nb.decode('latin-1') if nb is not None else 'Sin nombre'
                        except Exception:
                            nombre = 'Sin nombre'
                        clean_results.append({'id_area': id_area, 'nombre': nombre})
                    return clean_results
        except Exception as e2:
            logger.error(f"Fallback falló obteniendo áreas: {e2}")
            return []

def insert_area_safe(nombre):
    """Insertar área de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Insertamos el nombre directamente, confiando en la configuración LATIN1
                cursor.execute("""
                    INSERT INTO AREAS (nombre_area)
                    VALUES (%s) RETURNING id_area
                """, (nombre,))
                
                area_id = cursor.fetchone()[0]
                conn.commit()
                
                logger.info(f"Área creada: ID {area_id}")
                return area_id
                
    except Exception as e:
        logger.warning(f"Error insertando área con método estándar: {e}. Intentando fallback binario.")
        # Fallback: enviar bytes LATIN1 y usar convert_from(%s,'LATIN1') para insertar
        try:
            raw = None
            try:
                raw = str(nombre).encode('latin-1', errors='replace')
            except Exception:
                raw = str(nombre).encode('utf-8', errors='replace')

            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO AREAS (nombre_area)
                        VALUES (convert_from(%s, 'LATIN1')) RETURNING id_area
                    """, (psycopg2.Binary(raw),))
                    area_id = cursor.fetchone()[0]
                    conn.commit()
                    logger.info(f"Área creada con fallback binario: ID {area_id}")
                    return area_id
        except Exception as e2:
            logger.error(f"Fallback falló insertando área: {e2}")
            return None

# ===============================
# CONSULTAS SEGURAS PARA CONTRATOS
# ===============================
def get_contratos_safe():
    """Obtener contratos de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        id_contrato,
                        fecha_inicio_contrato as fecha_inicio,
                        fecha_fin_contrato as fecha_fin,
                        tipo_pago_contrato as tipo_pago
                    FROM CONTRATOS 
                    ORDER BY fecha_inicio_contrato DESC
                    LIMIT 100
                """)
                
                results = cursor.fetchall()
                return [dict(row) for row in results]
                
    except Exception as e:
        logger.error(f"Error obteniendo contratos: {e}")
        return []

def insert_contrato_safe(fecha_inicio, fecha_fin=None, tipo_pago=None):
    """Insertar contrato de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO CONTRATOS (fecha_inicio_contrato, fecha_fin_contrato, tipo_pago_contrato)
                    VALUES (%s, %s, %s) RETURNING id_contrato
                """, (fecha_inicio, fecha_fin, tipo_pago))
                
                contrato_id = cursor.fetchone()['id_contrato']
                conn.commit()
                
                logger.info(f"Contrato creado: ID {contrato_id}")
                return contrato_id
                
    except Exception as e:
        logger.error(f"Error insertando contrato: {e}")
        return None

# ===============================
# REPORTES ACADÉMICOS
# ===============================
def get_reportes_academicos_safe():
    """Obtener todos los reportes académicos requeridos"""
    try:
        reportes = {
            # Reporte 1: Control de gastos
            'gastos_totales': 0,
            'obras_con_gastos': 0,
            'areas_activas': 0,
            'gastos_por_obra': [],
            
            # Reporte 2: Control de materiales
            'materiales_asignados': 0,
            'areas_con_materiales': 0,
            'valor_materiales': 0,
            'materiales_por_area': [],
            
            # Reporte 3: Asignaciones de proyectos
            'proyectos_activos': 0,
            'ingenieros_asignados': 0,
            'arquitectos_asignados': 0,
            'asignaciones_proyectos': [],
            
            # Reporte 4: Control de personal
            'empleados_activos': 0,
            'actividades_diarias': 0,
            'areas_ocupadas': 0,
            'actividades_personal': [],
            
            # Reporte 5: Precios automáticos
            'precios_actualizados': 0,
            'variacion_promedio': 0,
            'materiales_con_precio': 0,
            'historial_precios': []
        }
        
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                
                # REPORTE 1: Control de gastos por obra
                cursor.execute("""
                    SELECT 
                        COUNT(DISTINCT o.id_obra) as obras_con_gastos,
                        COALESCE(SUM(o.valor_obra), 0) as gastos_totales
                    FROM OBRAS o 
                    WHERE o.valor_obra IS NOT NULL AND o.valor_obra > 0
                """)
                gastos_result = cursor.fetchone()
                if gastos_result:
                    reportes['gastos_totales'] = float(gastos_result['gastos_totales'] or 0)
                    reportes['obras_con_gastos'] = gastos_result['obras_con_gastos'] or 0
                
                # Gastos detallados por obra
                cursor.execute("""
                    SELECT 
                        COALESCE(o.nombre_obra, 'Sin nombre') as obra,
                        'General' as area,
                        'Obra' as tipo_gasto,
                        COALESCE(o.valor_obra, 0) as monto,
                        COALESCE(o.fecha_inicio::text, 'N/A') as fecha
                    FROM OBRAS o 
                    WHERE o.valor_obra IS NOT NULL AND o.valor_obra > 0
                    ORDER BY o.valor_obra DESC
                    LIMIT 10
                """)
                reportes['gastos_por_obra'] = cursor.fetchall()
                
                # REPORTE 2: Control de materiales 
                cursor.execute("""
                    SELECT 
                        COUNT(*) as materiales_asignados,
                        COALESCE(SUM(precio), 0) as valor_materiales
                    FROM MATERIALES 
                    WHERE precio IS NOT NULL AND precio > 0
                """)
                materiales_result = cursor.fetchone()
                if materiales_result:
                    reportes['materiales_asignados'] = materiales_result['materiales_asignados'] or 0
                    reportes['valor_materiales'] = float(materiales_result['valor_materiales'] or 0)
                
                # Materiales por área (simulado)
                cursor.execute("""
                    SELECT 
                        'Área General' as area,
                        COALESCE(nombre, 'Sin nombre') as material,
                        1 as cantidad,
                        COALESCE(unidad, 'Unidad') as unidad,
                        COALESCE(precio, 0) as valor_total,
                        'Disponible' as estado
                    FROM MATERIALES 
                    WHERE precio IS NOT NULL
                    ORDER BY precio DESC
                    LIMIT 10
                """)
                reportes['materiales_por_area'] = cursor.fetchall()
                reportes['areas_con_materiales'] = 1
                
                # REPORTE 3: Asignaciones de proyectos
                cursor.execute("""
                    SELECT COUNT(*) as proyectos_activos
                    FROM PROYECTOS 
                    WHERE estado_proyecto IN ('En Progreso', 'Activo', 'En Ejecución')
                """)
                proyectos_result = cursor.fetchone()
                reportes['proyectos_activos'] = proyectos_result['proyectos_activos'] if proyectos_result else 0
                
                # Asignaciones de proyectos (simulado con empleados)
                cursor.execute("""
                    SELECT 
                        p.nombre_proyecto as proyecto,
                        'Sin asignar' as responsable,
                        'Supervisor' as cargo,
                        p.fecha_inicio_proyecto::text as fecha_asignacion,
                        COALESCE(p.estado_proyecto, 'Planeación') as estado,
                        CASE 
                            WHEN p.estado_proyecto = 'Completado' THEN 100
                            WHEN p.estado_proyecto = 'En Progreso' THEN 60
                            ELSE 20
                        END as progreso
                    FROM PROYECTOS p
                    ORDER BY p.fecha_inicio_proyecto DESC NULLS LAST
                    LIMIT 5
                """)
                reportes['asignaciones_proyectos'] = cursor.fetchall()
                
                # Contar ingenieros y arquitectos
                cursor.execute("""
                    SELECT 
                        COUNT(CASE WHEN tipo = 'Ingeniero' THEN 1 END) as ingenieros,
                        COUNT(CASE WHEN tipo = 'Arquitecto' THEN 1 END) as arquitectos
                    FROM EMPLEADOS
                """)
                profesionales = cursor.fetchone()
                if profesionales:
                    reportes['ingenieros_asignados'] = profesionales['ingenieros'] or 0
                    reportes['arquitectos_asignados'] = profesionales['arquitectos'] or 0
                
                # REPORTE 4: Control de personal
                cursor.execute("""
                    SELECT COUNT(*) as empleados_activos
                    FROM EMPLEADOS
                """)
                empleados_result = cursor.fetchone()
                reportes['empleados_activos'] = empleados_result['empleados_activos'] if empleados_result else 0
                
                # Actividades del personal (simulado)
                cursor.execute("""
                    SELECT 
                        COALESCE(nombre, 'Sin nombre') as empleado,
                        'Área General' as area,
                        CASE 
                            WHEN tipo = 'Operario' THEN 'Trabajo de Campo'
                            WHEN tipo = 'Supervisor' THEN 'Supervisión'
                            WHEN tipo = 'Ingeniero' THEN 'Diseño y Planificación'
                            ELSE 'Actividades Varias'
                        END as actividad,
                        '08:00 - 17:00' as horario,
                        'Activo' as estado
                    FROM EMPLEADOS
                    ORDER BY nombre
                    LIMIT 10
                """)
                reportes['actividades_personal'] = cursor.fetchall()
                reportes['actividades_diarias'] = len(reportes['actividades_personal'])
                reportes['areas_ocupadas'] = 1
                
                # REPORTE 5: Precios automáticos
                cursor.execute("""
                    SELECT COUNT(*) as materiales_con_precio
                    FROM MATERIALES 
                    WHERE precio IS NOT NULL AND precio > 0
                """)
                precios_result = cursor.fetchone()
                reportes['materiales_con_precio'] = precios_result['materiales_con_precio'] if precios_result else 0
                
                # Historial de precios (simulado)
                cursor.execute("""
                    SELECT 
                        COALESCE(nombre, 'Sin nombre') as material,
                        COALESCE(precio * 0.9, 0) as precio_anterior,
                        COALESCE(precio, 0) as precio_actual,
                        10 as variacion,
                        CURRENT_DATE::text as fecha_actualizacion
                    FROM MATERIALES 
                    WHERE precio IS NOT NULL AND precio > 0
                    ORDER BY precio DESC
                    LIMIT 5
                """)
                reportes['historial_precios'] = cursor.fetchall()
                reportes['precios_actualizados'] = len(reportes['historial_precios'])
                reportes['variacion_promedio'] = 10
        
        return reportes
        
    except Exception as e:
        logger.error(f'Error obteniendo reportes académicos: {e}')
        # Retornar estructura vacía
        return {
            'gastos_totales': 0, 'obras_con_gastos': 0, 'areas_activas': 0, 'gastos_por_obra': [],
            'materiales_asignados': 0, 'areas_con_materiales': 0, 'valor_materiales': 0, 'materiales_por_area': [],
            'proyectos_activos': 0, 'ingenieros_asignados': 0, 'arquitectos_asignados': 0, 'asignaciones_proyectos': [],
            'empleados_activos': 0, 'actividades_diarias': 0, 'areas_ocupadas': 0, 'actividades_personal': [],
            'precios_actualizados': 0, 'variacion_promedio': 0, 'materiales_con_precio': 0, 'historial_precios': []
        }

# ===============================
# BODEGAS E INVENTARIOS
# ===============================
def get_bodegas_inventarios_safe():
    """Obtener información de bodegas e inventarios"""
    try:
        bodegas = {
            'total_bodegas': 1,  # Simulado
            'materiales_inventario': 0,
            'valor_inventario': 0,
            'movimientos_hoy': 0,
            'inventarios_resumen': [],
            'movimientos_recientes': []
        }
        
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                
                # Inventarios basados en materiales existentes
                cursor.execute("""
                    SELECT 
                        'Bodega Principal' as bodega,
                        COALESCE(nombre, 'Sin nombre') as material,
                        FLOOR(RANDOM() * 100 + 10) as stock_actual,
                        COALESCE(unidad, 'Unidad') as unidad,
                        COALESCE(precio, 0) as valor_unitario,
                        COALESCE(precio, 0) * FLOOR(RANDOM() * 100 + 10) as valor_total
                    FROM MATERIALES 
                    WHERE precio IS NOT NULL AND precio > 0
                    ORDER BY precio DESC
                    LIMIT 10
                """)
                inventarios = cursor.fetchall()
                bodegas['inventarios_resumen'] = inventarios
                bodegas['materiales_inventario'] = len(inventarios)
                
                # Calcular valor total del inventario
                valor_total = sum([float(inv['valor_total']) for inv in inventarios if inv['valor_total']])
                bodegas['valor_inventario'] = valor_total
                
                # Movimientos simulados
                cursor.execute("""
                    SELECT 
                        CURRENT_DATE::text as fecha,
                        CASE WHEN RANDOM() < 0.5 THEN 'Entrada' ELSE 'Salida' END as tipo,
                        COALESCE(nombre, 'Material') as material,
                        FLOOR(RANDOM() * 20 + 1) as cantidad,
                        'Bodega Principal' as bodega,
                        'Sistema Automático' as responsable
                    FROM MATERIALES 
                    ORDER BY RANDOM()
                    LIMIT 5
                """)
                bodegas['movimientos_recientes'] = cursor.fetchall()
                bodegas['movimientos_hoy'] = len(bodegas['movimientos_recientes'])
        
        return bodegas
        
    except Exception as e:
        logger.error(f'Error obteniendo bodegas: {e}')
        return {
            'total_bodegas': 0, 'materiales_inventario': 0, 'valor_inventario': 0, 'movimientos_hoy': 0,
            'inventarios_resumen': [], 'movimientos_recientes': []
        }

# ===============================
# FUNCIONES PARA TODAS LAS 56 TABLAS - SISTEMA COMPLETO
# ===============================

# ACTIVIDADES
def get_actividades_safe():
    """Obtener actividades con calendarización completa"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        a.id_actividad,
                        a.id_actividad as id,
                        a.id_actividad as actividad_id,
                        a.nombre_actividad,
                        a.descripcion_actividad,
                        a.fecha_programada_actividad,
                        a.hora_inicio,
                        a.hora_fin,
                        a.frecuencia,
                        a.notas_calendario,
                        a.area_id,
                        a.duracion_estimada,
                        a.prioridad,
                        a.estado,
                        a.fecha_creacion,
                        a.fecha_actualizacion,
                        ar.nombre_area
                    FROM ACTIVIDADES a
                    LEFT JOIN areas ar ON a.area_id = ar.id_area
                    ORDER BY a.fecha_programada_actividad DESC NULLS LAST, 
                             a.prioridad DESC, 
                             a.id_actividad DESC
                    LIMIT 100
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo actividades: {e}")
        return []

def insert_actividad_safe(nombre, descripcion=None, fecha_programada=None, area_id=None, 
                         duracion_estimada=None, prioridad=None, hora_inicio=None, hora_fin=None, 
                         frecuencia=None, notas_calendario=None):
    """Insertar nueva actividad con calendarización completa"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ACTIVIDADES (
                        nombre_actividad, 
                        descripcion_actividad, 
                        fecha_programada_actividad,
                        area_id,
                        duracion_estimada,
                        prioridad,
                        hora_inicio,
                        hora_fin,
                        frecuencia,
                        notas_calendario,
                        estado,
                        fecha_creacion,
                        fecha_actualizacion
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) 
                    RETURNING id_actividad
                """, (
                    nombre, 
                    descripcion, 
                    fecha_programada,
                    area_id,
                    duracion_estimada,
                    prioridad or 'media',
                    hora_inicio or '08:00',
                    hora_fin or '17:00',
                    frecuencia or 'unica',
                    notas_calendario,
                    'pendiente'
                ))
                
                return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Error insertando actividad: {e}")
        return None

def get_actividad_by_id_safe(actividad_id: int):
    """Obtener una actividad por ID"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        id_actividad,
                        id_actividad as id,
                        id_actividad as actividad_id,
                        nombre_actividad as nombre,
                        descripcion_actividad as descripcion,
                        fecha_programada_actividad as fecha_programada
                    FROM ACTIVIDADES
                    WHERE id_actividad = %s
                """, (actividad_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo actividad por id: {e}")
        return None

def update_actividad_safe(actividad_id: int, nombre=None, descripcion=None, fecha_programada=None):
    """Actualizar actividad"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE ACTIVIDADES
                    SET nombre_actividad = COALESCE(%s, nombre_actividad),
                        descripcion_actividad = COALESCE(%s, descripcion_actividad),
                        fecha_programada_actividad = COALESCE(%s, fecha_programada_actividad)
                    WHERE id_actividad = %s
                """, (nombre, descripcion, fecha_programada, actividad_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error actualizando actividad: {e}")
        return False

def delete_actividad_safe(actividad_id: int):
    """Eliminar actividad"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM ACTIVIDADES WHERE id_actividad = %s", (actividad_id,))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error eliminando actividad: {e}")
        return False

# BITACORAS
def get_bitacoras_safe():
    """Obtener bitácoras de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        b.id_bitacora as id,
                        b.id_bitacora as bitacora_id,
                        b.id_bitacora as id_bitacora,
                        b.fecha_bitacora,
                        b.observaciones_bitacora,
                        o.nombre_obra
                    FROM BITACORAS b
                    LEFT JOIN OBRA_BITACORA ob ON b.id_bitacora = ob.id_bitacora
                    LEFT JOIN OBRAS o ON ob.id_obra = o.id_obra
                    ORDER BY b.fecha_bitacora DESC
                    LIMIT 50
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo bitácoras: {e}")
        return []

def insert_bitacora_safe(observaciones, fecha_bitacora=None, obra_id=None):
    """Insertar nueva bitácora"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Insertar bitácora
                cursor.execute("""
                    INSERT INTO BITACORAS (fecha_bitacora, observaciones_bitacora)
                    VALUES (COALESCE(%s, CURRENT_DATE), %s) RETURNING id_bitacora
                """, (fecha_bitacora, observaciones))
                bitacora_id = cursor.fetchone()[0]
                
                # Asociar con obra si se especifica
                if obra_id:
                    cursor.execute("""
                        INSERT INTO OBRA_BITACORA (id_obra, id_bitacora) VALUES (%s, %s)
                    """, (obra_id, bitacora_id))
                
                return bitacora_id
    except Exception as e:
        logger.error(f"Error insertando bitácora: {e}")
        return None

def get_bitacora_by_id_safe(bitacora_id: int):
    """Obtener bitácora por ID con información disponible"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        b.id_bitacora as id,
                        b.id_bitacora as bitacora_id,
                        b.id_bitacora as id_bitacora,
                        b.fecha_bitacora,
                        b.observaciones_bitacora,
                        o.id_obra,
                        o.nombre_obra,
                        o.ubicacion_obra,
                        o.estado_obra
                    FROM BITACORAS b
                    LEFT JOIN OBRA_BITACORA ob ON b.id_bitacora = ob.id_bitacora
                    LEFT JOIN OBRAS o ON ob.id_obra = o.id_obra
                    WHERE b.id_bitacora = %s
                """, (bitacora_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo bitácora por ID: {e}")
        return None

def update_bitacora_safe(bitacora_id: int, observaciones=None, fecha_bitacora=None, obra_id=None):
    """Actualizar bitácora existente"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Actualizar bitácora
                cursor.execute("""
                    UPDATE BITACORAS 
                    SET observaciones_bitacora = COALESCE(%s, observaciones_bitacora),
                        fecha_bitacora = COALESCE(%s, fecha_bitacora)
                    WHERE id_bitacora = %s
                """, (observaciones, fecha_bitacora, bitacora_id))
                
                # Actualizar obra asociada si se especifica
                if obra_id is not None:
                    # Primero eliminar asociación anterior
                    cursor.execute("DELETE FROM OBRA_BITACORA WHERE id_bitacora = %s", (bitacora_id,))
                    # Luego insertar nueva asociación
                    if obra_id:  # Si obra_id no es vacío
                        cursor.execute("""
                            INSERT INTO OBRA_BITACORA (id_obra, id_bitacora) VALUES (%s, %s)
                        """, (obra_id, bitacora_id))
                
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error actualizando bitácora: {e}")
        return False

def delete_bitacora_safe(bitacora_id: int):
    """Eliminar bitácora"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Primero eliminar asociaciones en OBRA_BITACORA
                cursor.execute("DELETE FROM OBRA_BITACORA WHERE id_bitacora = %s", (bitacora_id,))
                # Luego eliminar la bitácora
                cursor.execute("DELETE FROM BITACORAS WHERE id_bitacora = %s", (bitacora_id,))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error eliminando bitácora: {e}")
        return False

# INCIDENTES
def get_incidentes_safe():
    """Obtener incidentes de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        i.id_incidente,
                        i.fecha_incidente,
                        i.descripcion_incidente,
                        i.estado_incidente,
                        o.nombre_obra
                    FROM INCIDENTES i
                    LEFT JOIN OBRA_INCIDENTE oi ON i.id_incidente = oi.id_incidente
                    LEFT JOIN OBRAS o ON oi.id_obra = o.id_obra
                    ORDER BY i.fecha_incidente DESC
                    LIMIT 50
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo incidentes: {e}")
        return []

def insert_incidente_safe(descripcion, estado='Reportado', fecha_incidente=None, obra_id=None):
    """Insertar nuevo incidente"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO INCIDENTES (fecha_incidente, descripcion_incidente, estado_incidente)
                    VALUES (COALESCE(%s, CURRENT_DATE), %s, %s) RETURNING id_incidente
                """, (fecha_incidente, descripcion, estado))
                incidente_id = cursor.fetchone()[0]
                
                # Asociar con obra si se especifica
                if obra_id:
                    cursor.execute("""
                        INSERT INTO OBRA_INCIDENTE (id_obra, id_incidente) VALUES (%s, %s)
                    """, (obra_id, incidente_id))
                
                return incidente_id
    except Exception as e:
        logger.error(f"Error insertando incidente: {e}")
        return None

def get_incidente_by_id_safe(incidente_id):
    """Obtener un incidente específico por ID"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT 
                        i.id_incidente,
                        i.id_incidente AS id,
                        i.fecha_incidente,
                        i.descripcion_incidente,
                        i.estado_incidente,
                        o.id_obra,
                        o.nombre_obra
                    FROM INCIDENTES i
                    LEFT JOIN OBRA_INCIDENTE oi ON i.id_incidente = oi.id_incidente
                    LEFT JOIN OBRAS o ON oi.id_obra = o.id_obra
                    WHERE i.id_incidente = %s
                    """,
                    (incidente_id,),
                )
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo incidente {incidente_id}: {e}")
        return None

def update_incidente_safe(incidente_id, descripcion=None, estado=None, fecha_incidente=None, obra_id=None):
    """Actualizar los datos de un incidente y su relación con obra"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE INCIDENTES
                    SET descripcion_incidente = COALESCE(%s, descripcion_incidente),
                        estado_incidente = COALESCE(%s, estado_incidente),
                        fecha_incidente = COALESCE(%s, fecha_incidente)
                    WHERE id_incidente = %s
                    """,
                    (descripcion, estado, fecha_incidente, incidente_id),
                )
                # Actualizar relación con obra
                cursor.execute("DELETE FROM OBRA_INCIDENTE WHERE id_incidente = %s", (incidente_id,))
                if obra_id:
                    cursor.execute(
                        "INSERT INTO OBRA_INCIDENTE (id_obra, id_incidente) VALUES (%s, %s)",
                        (obra_id, incidente_id),
                    )
                return True
    except Exception as e:
        logger.error(f"Error actualizando incidente {incidente_id}: {e}")
        return False

def delete_incidente_safe(incidente_id):
    """Eliminar un incidente y su relación con obra"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM OBRA_INCIDENTE WHERE id_incidente = %s", (incidente_id,))
                cursor.execute("DELETE FROM INCIDENTES WHERE id_incidente = %s", (incidente_id,))
                return True
    except Exception as e:
        logger.error(f"Error eliminando incidente {incidente_id}: {e}")
        return False

# AUDITORIAS
def get_auditorias_safe():
    """Obtener auditorías de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        a.id_auditoria,
                        a.id_auditoria as id,
                        a.id_auditoria as auditoria_id,
                        a.accion_auditoria,
                        a.fecha_auditoria,
                        a.detalle_auditoria,
                        u.nombre_usuario,
                        u.id_usuario
                    FROM AUDITORIAS a
                    LEFT JOIN USUARIO_AUDITORIA ua ON a.id_auditoria = ua.id_auditoria
                    LEFT JOIN USUARIOS_SISTEMA u ON ua.id_usuario = u.id_usuario
                    ORDER BY a.fecha_auditoria DESC
                    LIMIT 100
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo auditorías: {e}")
        return []

def get_auditoria_by_id_safe(auditoria_id: int):
    """Obtener auditoría por ID con aliases para templates"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        a.id_auditoria,
                        a.id_auditoria as id,
                        a.id_auditoria as auditoria_id,
                        a.accion_auditoria,
                        a.fecha_auditoria,
                        a.detalle_auditoria,
                        u.nombre_usuario,
                        u.id_usuario,
                        u.correo_usuario as email_usuario
                    FROM AUDITORIAS a
                    LEFT JOIN USUARIO_AUDITORIA ua ON a.id_auditoria = ua.id_auditoria
                    LEFT JOIN USUARIOS_SISTEMA u ON ua.id_usuario = u.id_usuario
                    WHERE a.id_auditoria = %s
                """, (auditoria_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo auditoría por ID: {e}")
        return None

# PERMISOS_ACCESO
def get_permisos_acceso_safe():
    """Obtener todos los permisos de acceso"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        p.id_permiso,
                        p.id_permiso as id,
                        p.id_permiso as permiso_id,
                        p.modulo_permiso,
                        p.nivel_acceso_permiso,
                        COUNT(DISTINCT up.id_usuario) as usuarios_asignados
                    FROM PERMISOS_ACCESO p
                    LEFT JOIN USUARIO_PERMISO up ON p.id_permiso = up.id_permiso
                    GROUP BY p.id_permiso, p.modulo_permiso, p.nivel_acceso_permiso
                    ORDER BY p.modulo_permiso, p.nivel_acceso_permiso
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo permisos de acceso: {e}")
        return []

def get_permiso_by_id_safe(permiso_id: int):
    """Obtener permiso por ID con aliases para templates"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        p.id_permiso,
                        p.id_permiso as id,
                        p.id_permiso as permiso_id,
                        p.modulo_permiso,
                        p.nivel_acceso_permiso,
                        COUNT(DISTINCT up.id_usuario) as usuarios_asignados
                    FROM PERMISOS_ACCESO p
                    LEFT JOIN USUARIO_PERMISO up ON p.id_permiso = up.id_permiso
                    WHERE p.id_permiso = %s
                    GROUP BY p.id_permiso, p.modulo_permiso, p.nivel_acceso_permiso
                """, (permiso_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo permiso por ID: {e}")
        return None

def insert_permiso_safe(modulo_permiso: str, nivel_acceso_permiso: str = None):
    """Insertar nuevo permiso de acceso"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO PERMISOS_ACCESO 
                        (modulo_permiso, nivel_acceso_permiso)
                    VALUES (%s, %s)
                    RETURNING id_permiso
                """, (modulo_permiso, nivel_acceso_permiso))
                result = cursor.fetchone()
                conn.commit()
                return result['id_permiso'] if result else None
    except Exception as e:
        logger.error(f"Error insertando permiso: {e}")
        return None

def update_permiso_safe(permiso_id: int, modulo_permiso: str = None, nivel_acceso_permiso: str = None):
    """Actualizar permiso de acceso"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                updates = []
                params = []
                
                if modulo_permiso is not None:
                    updates.append("modulo_permiso = %s")
                    params.append(modulo_permiso)
                
                if nivel_acceso_permiso is not None:
                    updates.append("nivel_acceso_permiso = %s")
                    params.append(nivel_acceso_permiso)
                
                if not updates:
                    return False
                
                params.append(permiso_id)
                query = f"UPDATE PERMISOS_ACCESO SET {', '.join(updates)} WHERE id_permiso = %s"
                
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error actualizando permiso: {e}")
        return False

def delete_permiso_safe(permiso_id: int):
    """Eliminar permiso de acceso"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # CASCADE eliminará automáticamente registros en USUARIO_PERMISO
                cursor.execute("DELETE FROM PERMISOS_ACCESO WHERE id_permiso = %s", (permiso_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error eliminando permiso: {e}")
        return False

def get_usuarios_con_permiso(permiso_id: int):
    """Obtener usuarios que tienen asignado un permiso específico"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        u.id_usuario,
                        u.nombre_usuario,
                        u.correo_usuario,
                        u.rol_usuario,
                        up.fecha_asignacion_usuario_permiso
                    FROM USUARIOS_SISTEMA u
                    INNER JOIN USUARIO_PERMISO up ON u.id_usuario = up.id_usuario
                    WHERE up.id_permiso = %s
                    ORDER BY u.nombre_usuario
                """, (permiso_id,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo usuarios con permiso: {e}")
        return []

def asignar_permiso_usuario(permiso_id: int, usuario_id: int):
    """Asignar permiso a un usuario"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Verificar si ya existe la asignación
                cursor.execute("""
                    SELECT 1 FROM USUARIO_PERMISO 
                    WHERE id_permiso = %s AND id_usuario = %s
                """, (permiso_id, usuario_id))
                
                if cursor.fetchone():
                    return False  # Ya existe
                
                cursor.execute("""
                    INSERT INTO USUARIO_PERMISO (id_permiso, id_usuario)
                    VALUES (%s, %s)
                """, (permiso_id, usuario_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error asignando permiso a usuario: {e}")
        return False

def revocar_permiso_usuario(permiso_id: int, usuario_id: int):
    """Revocar permiso de un usuario"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM USUARIO_PERMISO 
                    WHERE id_permiso = %s AND id_usuario = %s
                """, (permiso_id, usuario_id))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error revocando permiso de usuario: {e}")
        return False

# BODEGAS
def get_bodegas_safe():
    """Obtener todas las bodegas con información completa"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        b.id_bodega,
                        b.id_bodega as id,
                        b.id_bodega as bodega_id,
                        b.responsable_bodega,
                        b.ubicacion_bodega,
                        b.capacidad_bodega,
                        b.telefono_bodega,
                        b.estado_bodega,
                        b.fecha_creacion,
                        b.observaciones_bodega,
                        COUNT(DISTINCT ob.id_obra) as obras_asignadas,
                        COUNT(DISTINCT bi.id_inventario) as inventarios_asignados
                    FROM BODEGAS b
                    LEFT JOIN OBRA_BODEGA ob ON b.id_bodega = ob.id_bodega
                    LEFT JOIN BODEGA_INVENTARIO bi ON b.id_bodega = bi.id_bodega
                    GROUP BY b.id_bodega, b.responsable_bodega, b.ubicacion_bodega, 
                             b.capacidad_bodega, b.telefono_bodega, b.estado_bodega,
                             b.fecha_creacion, b.observaciones_bodega
                    ORDER BY b.id_bodega
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo bodegas: {e}")
        return []

def get_bodega_by_id_safe(bodega_id: int):
    """Obtener bodega por ID con información completa"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        b.id_bodega,
                        b.id_bodega as id,
                        b.id_bodega as bodega_id,
                        b.responsable_bodega,
                        b.ubicacion_bodega,
                        b.capacidad_bodega,
                        b.telefono_bodega,
                        b.estado_bodega,
                        b.fecha_creacion,
                        b.observaciones_bodega,
                        COUNT(DISTINCT ob.id_obra) as obras_asignadas,
                        COUNT(DISTINCT bi.id_inventario) as inventarios_asignados
                    FROM BODEGAS b
                    LEFT JOIN OBRA_BODEGA ob ON b.id_bodega = ob.id_bodega
                    LEFT JOIN BODEGA_INVENTARIO bi ON b.id_bodega = bi.id_bodega
                    WHERE b.id_bodega = %s
                    GROUP BY b.id_bodega, b.responsable_bodega, b.ubicacion_bodega, 
                             b.capacidad_bodega, b.telefono_bodega, b.estado_bodega,
                             b.fecha_creacion, b.observaciones_bodega
                """, (bodega_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo bodega por ID: {e}")
        return None

def insert_bodega_safe(responsable_bodega: str = None, ubicacion_bodega: str = None, 
                      capacidad_bodega: str = None, telefono_bodega: str = None, 
                      estado_bodega: str = 'Activa', observaciones_bodega: str = None):
    """Insertar nueva bodega con información completa"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO BODEGAS (
                        responsable_bodega, ubicacion_bodega, capacidad_bodega, 
                        telefono_bodega, estado_bodega, observaciones_bodega
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id_bodega
                """, (responsable_bodega, ubicacion_bodega, capacidad_bodega, 
                      telefono_bodega, estado_bodega, observaciones_bodega))
                result = cursor.fetchone()
                conn.commit()
                return result['id_bodega'] if result else None
    except Exception as e:
        logger.error(f"Error insertando bodega: {e}")
        return None

def update_bodega_safe(bodega_id: int, responsable_bodega: str = None, 
                      ubicacion_bodega: str = None, capacidad_bodega: str = None, 
                      telefono_bodega: str = None, estado_bodega: str = None, 
                      observaciones_bodega: str = None):
    """Actualizar bodega con información completa"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Construir la consulta dinámicamente según los campos proporcionados
                fields = []
                values = []
                
                if responsable_bodega is not None:
                    fields.append("responsable_bodega = %s")
                    values.append(responsable_bodega)
                if ubicacion_bodega is not None:
                    fields.append("ubicacion_bodega = %s")
                    values.append(ubicacion_bodega)
                if capacidad_bodega is not None:
                    fields.append("capacidad_bodega = %s")
                    values.append(capacidad_bodega)
                if telefono_bodega is not None:
                    fields.append("telefono_bodega = %s")
                    values.append(telefono_bodega)
                if estado_bodega is not None:
                    fields.append("estado_bodega = %s")
                    values.append(estado_bodega)
                if observaciones_bodega is not None:
                    fields.append("observaciones_bodega = %s")
                    values.append(observaciones_bodega)
                
                if fields:
                    values.append(bodega_id)
                    sql = f"UPDATE BODEGAS SET {', '.join(fields)} WHERE id_bodega = %s"
                    cursor.execute(sql, values)
                    conn.commit()
                    return cursor.rowcount > 0
                return False
    except Exception as e:
        logger.error(f"Error actualizando bodega: {e}")
        return False

def delete_bodega_safe(bodega_id: int):
    """Eliminar bodega"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # CASCADE eliminará automáticamente registros en OBRA_BODEGA y BODEGA_INVENTARIO
                cursor.execute("DELETE FROM BODEGAS WHERE id_bodega = %s", (bodega_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error eliminando bodega: {e}")
        return False

def get_obras_de_bodega(bodega_id: int):
    """Obtener obras asociadas a una bodega"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        o.id_obra,
                        o.nombre_obra,
                        o.ubicacion_obra,
                        o.fecha_inicio_obra
                    FROM OBRAS o
                    INNER JOIN OBRA_BODEGA ob ON o.id_obra = ob.id_obra
                    WHERE ob.id_bodega = %s
                    ORDER BY o.nombre_obra
                """, (bodega_id,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo obras de bodega: {e}")
        return []

def asignar_bodega_a_obra(bodega_id: int, obra_id: int):
    """Asignar bodega a una obra"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Verificar si ya existe la asignación
                cursor.execute("""
                    SELECT 1 FROM OBRA_BODEGA 
                    WHERE id_bodega = %s AND id_obra = %s
                """, (bodega_id, obra_id))
                
                if cursor.fetchone():
                    return False  # Ya existe
                
                cursor.execute("""
                    INSERT INTO OBRA_BODEGA (id_bodega, id_obra)
                    VALUES (%s, %s)
                """, (bodega_id, obra_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error asignando bodega a obra: {e}")
        return False

def remover_bodega_de_obra(bodega_id: int, obra_id: int):
    """Remover bodega de una obra"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM OBRA_BODEGA 
                    WHERE id_bodega = %s AND id_obra = %s
                """, (bodega_id, obra_id))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error removiendo bodega de obra: {e}")
        return False

# USUARIOS Y PERMISOS
def get_usuarios_safe():
    """Obtener usuarios del sistema"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        u.id_usuario,
                        u.nombre_usuario,
                        u.rol_usuario,
                        u.correo_usuario,
                        COUNT(p.id_permiso) as total_permisos
                    FROM USUARIOS_SISTEMA u
                    LEFT JOIN USUARIO_PERMISO up ON u.id_usuario = up.id_usuario
                    LEFT JOIN PERMISOS_ACCESO p ON up.id_permiso = p.id_permiso
                    GROUP BY u.id_usuario, u.nombre_usuario, u.rol_usuario, u.correo_usuario
                    ORDER BY u.nombre_usuario
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo usuarios: {e}")
        return []

# CONTRATOS
def get_contratos_safe():
    """Obtener contratos de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        c.id_contrato,
                        c.id_contrato as id,
                        c.id_contrato as contrato_id,
                        c.fecha_inicio_contrato,
                        c.fecha_fin_contrato,
                        c.tipo_pago_contrato,
                        o.nombre_obra
                    FROM CONTRATOS c
                    LEFT JOIN CONTRATO_OBRA co ON c.id_contrato = co.id_contrato
                    LEFT JOIN OBRAS o ON co.id_obra = o.id_obra
                    ORDER BY c.fecha_inicio_contrato DESC
                    LIMIT 50
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo contratos: {e}")
        return []

def insert_contrato_safe(fecha_inicio, fecha_fin=None, tipo_pago=None, obra_id=None, 
                        numero_contrato=None, cliente_id=None, valor_total=None, estado=None):
    """Insertar nuevo contrato con todos los campos del formulario"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Verificar qué columnas existen en la tabla CONTRATOS
                cursor.execute("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'contratos' AND table_schema = 'public'
                """)
                cols = [row[0] for row in cursor.fetchall()]
                
                # Construir query dinámicamente según campos disponibles
                base_fields = ['fecha_inicio_contrato', 'fecha_fin_contrato', 'tipo_pago_contrato']
                base_values = [fecha_inicio, fecha_fin, tipo_pago]
                
                # Agregar campos opcionales si existen en la tabla
                if 'numero_contrato' in cols and numero_contrato:
                    base_fields.append('numero_contrato')
                    base_values.append(numero_contrato)
                
                if 'id_cliente' in cols and cliente_id:
                    base_fields.append('id_cliente')
                    base_values.append(cliente_id)
                
                if 'valor_total' in cols and valor_total:
                    base_fields.append('valor_total')
                    base_values.append(valor_total)
                
                if 'estado' in cols and estado:
                    base_fields.append('estado')
                    base_values.append(estado)
                elif 'estado_contrato' in cols and estado:
                    base_fields.append('estado_contrato')
                    base_values.append(estado)
                
                # Ejecutar inserción
                placeholders = ', '.join(['%s'] * len(base_values))
                field_names = ', '.join(base_fields)
                
                cursor.execute(f"""
                    INSERT INTO CONTRATOS ({field_names})
                    VALUES ({placeholders}) RETURNING id_contrato
                """, base_values)
                contrato_id = cursor.fetchone()[0]
                
                # Asociar con obra si se especifica
                if obra_id:
                    try:
                        cursor.execute("""
                            INSERT INTO CONTRATO_OBRA (id_contrato, id_obra) VALUES (%s, %s)
                        """, (contrato_id, obra_id))
                    except Exception:
                        # Si no existe tabla CONTRATO_OBRA, intentar actualizar directamente en CONTRATOS
                        if 'id_obra' in cols:
                            cursor.execute("""
                                UPDATE CONTRATOS SET id_obra = %s WHERE id_contrato = %s
                            """, (obra_id, contrato_id))
                
                return contrato_id
    except Exception as e:
        logger.error(f"Error insertando contrato: {e}")
        return None

def get_contrato_by_id_safe(contrato_id):
    """Obtener un contrato específico por ID con información disponible"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        c.id_contrato,
                        c.id_contrato as id,
                        c.id_contrato as contrato_id,
                        c.fecha_inicio_contrato,
                        c.fecha_fin_contrato,
                        c.tipo_pago_contrato,
                        c.numero_factura,
                        c.fecha_emision_factura,
                        c.estado_factura,
                        c.subtotal_factura,
                        c.iva_factura,
                        c.total_factura,
                        o.id_obra,
                        o.nombre_obra,
                        o.ubicacion_obra,
                        o.estado_obra,
                        cl.id_cliente,
                        cl.nombre_cliente,
                        cl.telefono_cliente,
                        cl.email_cliente
                    FROM CONTRATOS c
                    LEFT JOIN CONTRATO_OBRA co ON c.id_contrato = co.id_contrato
                    LEFT JOIN OBRAS o ON co.id_obra = o.id_obra
                    LEFT JOIN CLIENTES cl ON o.id_cliente = cl.id_cliente
                    WHERE c.id_contrato = %s
                """, (contrato_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo contrato {contrato_id}: {e}")
        return None

def update_contrato_safe(contrato_id, fecha_inicio, fecha_fin=None, tipo_pago=None, obra_id=None):
    """Actualizar un contrato existente"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE CONTRATOS 
                    SET fecha_inicio_contrato = %s,
                        fecha_fin_contrato = %s,
                        tipo_pago_contrato = %s
                    WHERE id_contrato = %s
                """, (fecha_inicio, fecha_fin, tipo_pago, contrato_id))
                
                # Actualizar relación con obra
                cursor.execute("DELETE FROM CONTRATO_OBRA WHERE id_contrato = %s", (contrato_id,))
                if obra_id:
                    cursor.execute("""
                        INSERT INTO CONTRATO_OBRA (id_contrato, id_obra) VALUES (%s, %s)
                    """, (contrato_id, obra_id))
                
                return True
    except Exception as e:
        logger.error(f"Error actualizando contrato {contrato_id}: {e}")
        return False

def delete_contrato_safe(contrato_id):
    """Eliminar un contrato y sus relaciones"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Eliminar relaciones primero
                cursor.execute("DELETE FROM CONTRATO_OBRA WHERE id_contrato = %s", (contrato_id,))
                # Eliminar el contrato
                cursor.execute("DELETE FROM CONTRATOS WHERE id_contrato = %s", (contrato_id,))
                return True
    except Exception as e:
        logger.error(f"Error eliminando contrato {contrato_id}: {e}")
        return False

# PRESUPUESTOS
def get_presupuestos_safe():
    """Obtener presupuestos de obra"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        p.id_presupuesto,
                        p.id_presupuesto as id,
                        p.id_presupuesto as presupuesto_id,
                        p.monto_estimado_presupuesto,
                        p.fecha_presupuesto,
                        o.nombre_obra
                    FROM PRESUPUESTOS_OBRA p
                    LEFT JOIN OBRA_PRESUPUESTO op ON p.id_presupuesto = op.id_presupuesto
                    LEFT JOIN OBRAS o ON op.id_obra = o.id_obra
                    ORDER BY p.fecha_presupuesto DESC
                    LIMIT 50
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo presupuestos: {e}")
        return []

def insert_presupuesto_safe(monto_estimado, fecha_presupuesto=None, obra_id=None):
    """Insertar nuevo presupuesto"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("""
                        INSERT INTO PRESUPUESTOS_OBRA (monto_estimado_presupuesto, fecha_presupuesto)
                        VALUES (%s, COALESCE(%s, CURRENT_DATE)) RETURNING id_presupuesto
                    """, (monto_estimado, fecha_presupuesto))
                    presupuesto_id = cursor.fetchone()[0]
                    
                except Exception as seq_error:
                    # Si hay error de secuencia, intentar arreglarla
                    if "llave duplicada" in str(seq_error) or "duplicate key" in str(seq_error):
                        logger.warning("Arreglando secuencia de presupuestos_obra...")
                        cursor.execute("SELECT MAX(id_presupuesto) FROM presupuestos_obra;")
                        max_id = cursor.fetchone()[0] or 0
                        next_val = max_id + 1
                        cursor.execute(f"SELECT setval('presupuestos_obra_id_presupuesto_seq', {next_val}, false);")
                        
                        # Reintentar inserción
                        cursor.execute("""
                            INSERT INTO PRESUPUESTOS_OBRA (monto_estimado_presupuesto, fecha_presupuesto)
                            VALUES (%s, COALESCE(%s, CURRENT_DATE)) RETURNING id_presupuesto
                        """, (monto_estimado, fecha_presupuesto))
                        presupuesto_id = cursor.fetchone()[0]
                        logger.info(f"Secuencia arreglada, presupuesto creado con ID: {presupuesto_id}")
                    else:
                        raise seq_error
                
                # Asociar con obra si se especifica
                if obra_id:
                    cursor.execute("""
                        INSERT INTO OBRA_PRESUPUESTO (id_obra, id_presupuesto) VALUES (%s, %s)
                    """, (obra_id, presupuesto_id))
                
                return presupuesto_id
    except Exception as e:
        logger.error(f"Error insertando presupuesto: {e}")
        return None

def get_presupuesto_by_id_safe(presupuesto_id):
    """Obtener un presupuesto específico por ID con aliases"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        p.id_presupuesto,
                        p.id_presupuesto as id,
                        p.id_presupuesto as presupuesto_id,
                        p.monto_estimado_presupuesto,
                        p.fecha_presupuesto,
                        o.id_obra,
                        o.nombre_obra
                    FROM PRESUPUESTOS_OBRA p
                    LEFT JOIN OBRA_PRESUPUESTO op ON p.id_presupuesto = op.id_presupuesto
                    LEFT JOIN OBRAS o ON op.id_obra = o.id_obra
                    WHERE p.id_presupuesto = %s
                """, (presupuesto_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo presupuesto {presupuesto_id}: {e}")
        return None

def update_presupuesto_safe(presupuesto_id, monto_estimado, fecha_presupuesto=None, obra_id=None):
    """Actualizar un presupuesto existente"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE PRESUPUESTOS_OBRA 
                    SET monto_estimado_presupuesto = %s,
                        fecha_presupuesto = COALESCE(%s, fecha_presupuesto)
                    WHERE id_presupuesto = %s
                """, (monto_estimado, fecha_presupuesto, presupuesto_id))
                
                # Actualizar relación con obra
                cursor.execute("DELETE FROM OBRA_PRESUPUESTO WHERE id_presupuesto = %s", (presupuesto_id,))
                if obra_id:
                    cursor.execute("""
                        INSERT INTO OBRA_PRESUPUESTO (id_obra, id_presupuesto) VALUES (%s, %s)
                    """, (obra_id, presupuesto_id))
                
                return True
    except Exception as e:
        logger.error(f"Error actualizando presupuesto {presupuesto_id}: {e}")
        return False

def delete_presupuesto_safe(presupuesto_id):
    """Eliminar un presupuesto y sus relaciones"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Eliminar relaciones primero
                cursor.execute("DELETE FROM OBRA_PRESUPUESTO WHERE id_presupuesto = %s", (presupuesto_id,))
                # Eliminar el presupuesto
                cursor.execute("DELETE FROM PRESUPUESTOS_OBRA WHERE id_presupuesto = %s", (presupuesto_id,))
                return True
    except Exception as e:
        logger.error(f"Error eliminando presupuesto {presupuesto_id}: {e}")
        return False

# AVANCES DE OBRA
def get_avances_safe():
    """Obtener avances de obra"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        a.id_avance,
                        a.porcentaje_fisico_avance,
                        a.porcentaje_financiero_avance,
                        a.fecha_avance,
                        o.nombre_obra
                    FROM AVANCES_OBRA a
                    LEFT JOIN OBRA_AVANCE oa ON a.id_avance = oa.id_avance
                    LEFT JOIN OBRAS o ON oa.id_obra = o.id_obra
                    ORDER BY a.fecha_avance DESC
                    LIMIT 50
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo avances: {e}")
        return []

def insert_avance_safe(porcentaje_fisico, porcentaje_financiero, fecha_avance=None, obra_id=None):
    """Insertar nuevo avance"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO AVANCES_OBRA (porcentaje_fisico_avance, porcentaje_financiero_avance, fecha_avance)
                    VALUES (%s, %s, COALESCE(%s, CURRENT_DATE)) RETURNING id_avance
                """, (porcentaje_fisico, porcentaje_financiero, fecha_avance))
                avance_id = cursor.fetchone()[0]
                
                # Asociar con obra si se especifica
                if obra_id:
                    cursor.execute("""
                        INSERT INTO OBRA_AVANCE (id_obra, id_avance) VALUES (%s, %s)
                    """, (obra_id, avance_id))
                
                return avance_id
    except Exception as e:
        logger.error(f"Error insertando avance: {e}")
        return None

def get_avance_by_id_safe(avance_id):
    """Obtener un avance específico por ID, incluyendo nombre de obra relacionada si existe"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT 
                        a.id_avance,
                        a.id_avance AS id,
                        a.porcentaje_fisico_avance,
                        a.porcentaje_financiero_avance,
                        a.fecha_avance,
                        o.id_obra,
                        o.nombre_obra
                    FROM AVANCES_OBRA a
                    LEFT JOIN OBRA_AVANCE oa ON a.id_avance = oa.id_avance
                    LEFT JOIN OBRAS o ON oa.id_obra = o.id_obra
                    WHERE a.id_avance = %s
                    """,
                    (avance_id,),
                )
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo avance {avance_id}: {e}")
        return None

def update_avance_safe(avance_id, porcentaje_fisico=None, porcentaje_financiero=None, fecha_avance=None, obra_id=None):
    """Actualizar un avance y su relación con obra"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE AVANCES_OBRA
                    SET porcentaje_fisico_avance = COALESCE(%s, porcentaje_fisico_avance),
                        porcentaje_financiero_avance = COALESCE(%s, porcentaje_financiero_avance),
                        fecha_avance = COALESCE(%s, fecha_avance)
                    WHERE id_avance = %s
                    """,
                    (porcentaje_fisico, porcentaje_financiero, fecha_avance, avance_id),
                )
                # Actualizar relación obra- avance
                cursor.execute("DELETE FROM OBRA_AVANCE WHERE id_avance = %s", (avance_id,))
                if obra_id:
                    cursor.execute(
                        "INSERT INTO OBRA_AVANCE (id_obra, id_avance) VALUES (%s, %s)",
                        (obra_id, avance_id),
                    )
                return True
    except Exception as e:
        logger.error(f"Error actualizando avance {avance_id}: {e}")
        return False

def delete_avance_safe(avance_id):
    """Eliminar un avance y sus relaciones"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM OBRA_AVANCE WHERE id_avance = %s", (avance_id,))
                cursor.execute("DELETE FROM AVANCES_OBRA WHERE id_avance = %s", (avance_id,))
                return True
    except Exception as e:
        logger.error(f"Error eliminando avance {avance_id}: {e}")
        return False

# AREAS
def get_areas_safe():
    """Obtener áreas de trabajo"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        a.id_area,
                        a.nombre_area,
                        COUNT(DISTINCT oa.id_obra) as obras_asignadas,
                        COUNT(DISTINCT aa.id_actividad) as actividades_asignadas,
                        COUNT(DISTINCT ae.id_empleado) as empleados_asignados
                    FROM AREAS a
                    LEFT JOIN OBRA_AREA oa ON a.id_area = oa.id_area
                    LEFT JOIN AREA_ACTIVIDAD aa ON a.id_area = aa.id_area
                    LEFT JOIN AREA_EMPLEADO ae ON a.id_area = ae.id_area
                    GROUP BY a.id_area, a.nombre_area
                    ORDER BY a.nombre_area
                """)
                rows = cursor.fetchall()
                # Normalizar claves para que las plantillas esperen 'id' y 'nombre'
                normalized = []
                for r in rows:
                    normalized.append({
                        'id': r.get('id_area'),
                        'nombre': r.get('nombre_area'),
                        'obras_asignadas': int(r.get('obras_asignadas') or 0),
                        'actividades_asignadas': int(r.get('actividades_asignadas') or 0),
                        'empleados_asignados': int(r.get('empleados_asignados') or 0)
                    })
                return normalized
    except Exception as e:
        logger.error(f"Error obteniendo áreas: {e}")
        return []

def insert_area_safe(nombre):
    """Insertar nueva área"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO AREAS (nombre_area) VALUES (%s) RETURNING id_area
                """, (nombre,))
                return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Error insertando área: {e}")
        return None

def get_area_by_id_safe(area_id):
    """Obtener detalle de un área por ID, con conteos de relaciones"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT 
                        a.id_area,
                        a.id_area AS id,
                        a.id_area AS area_id,
                        a.nombre_area,
                        COUNT(DISTINCT oa.id_obra) AS obras_asignadas,
                        COUNT(DISTINCT aa.id_actividad) AS actividades_asignadas,
                        COUNT(DISTINCT ae.id_empleado) AS empleados_asignados
                    FROM AREAS a
                    LEFT JOIN OBRA_AREA oa ON a.id_area = oa.id_area
                    LEFT JOIN AREA_ACTIVIDAD aa ON a.id_area = aa.id_area
                    LEFT JOIN AREA_EMPLEADO ae ON a.id_area = ae.id_area
                    WHERE a.id_area = %s
                    GROUP BY a.id_area, a.nombre_area
                    """,
                    (area_id,),
                )
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo área {area_id}: {e}")
        return None

def update_area_safe(area_id, nombre):
    """Actualizar nombre de un área"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE AREAS
                    SET nombre_area = %s
                    WHERE id_area = %s
                    """,
                    (nombre, area_id),
                )
                return True
    except Exception as e:
        logger.error(f"Error actualizando área {area_id}: {e}")
        return False

def delete_area_safe(area_id):
    """Eliminar un área y sus relaciones N:M"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Eliminar relaciones en tablas puente primero
                cursor.execute("DELETE FROM OBRA_AREA WHERE id_area = %s", (area_id,))
                cursor.execute("DELETE FROM AREA_ACTIVIDAD WHERE id_area = %s", (area_id,))
                cursor.execute("DELETE FROM AREA_EMPLEADO WHERE id_area = %s", (area_id,))
                cursor.execute("DELETE FROM AREA_REQUISICION WHERE id_area = %s", (area_id,))
                # Finalmente eliminar el área
                cursor.execute("DELETE FROM AREAS WHERE id_area = %s", (area_id,))
                return True
    except Exception as e:
        logger.error(f"Error eliminando área {area_id}: {e}")
        return False

# ===============================
# HELPERS PARA RELACIONES AREA_* (N:M)
# ===============================
def assign_area_to_obra(area_id, obra_id):
    """Asociar un área a una obra (OBRA_AREA)"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO OBRA_AREA (id_obra, id_area) VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, (obra_id, area_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error asignando área a obra: {e}")
        return False

def remove_area_from_obra(area_id, obra_id):
    """Quitar asociación área-obra"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM OBRA_AREA WHERE id_obra = %s AND id_area = %s", (obra_id, area_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error removiendo área de obra: {e}")
        return False

def get_areas_for_obra(obra_id):
    """Obtener áreas asociadas a una obra"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT a.id_area, a.nombre_area
                    FROM AREAS a
                    JOIN OBRA_AREA oa ON a.id_area = oa.id_area
                    WHERE oa.id_obra = %s
                    ORDER BY a.nombre_area
                """, (obra_id,))
                rows = cursor.fetchall()
                return [{'id': r['id_area'], 'nombre': r['nombre_area']} for r in rows]
    except Exception as e:
        logger.error(f"Error obteniendo áreas de obra: {e}")
        return []

def get_obras_for_area(area_id):
    """Obtener obras asociadas a un área"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT o.id_obra, o.nombre_obra
                    FROM OBRAS o
                    JOIN OBRA_AREA oa ON o.id_obra = oa.id_obra
                    WHERE oa.id_area = %s
                    ORDER BY o.nombre_obra
                """, (area_id,))
                rows = cursor.fetchall()
                return [{'id': r['id_obra'], 'nombre': r.get('nombre_obra') or ''} for r in rows]
    except Exception as e:
        logger.error(f"Error obteniendo obras de área: {e}")
        return []

# AREA_ACTIVIDAD
def assign_activity_to_area(area_id, actividad_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO AREA_ACTIVIDAD (id_area, id_actividad) VALUES (%s, %s) ON CONFLICT DO NOTHING", (area_id, actividad_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error asignando actividad a área: {e}")
        return False

def get_activities_for_area(area_id):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("SELECT a.id_actividad, a.nombre_actividad FROM ACTIVIDADES a JOIN AREA_ACTIVIDAD aa ON a.id_actividad = aa.id_actividad WHERE aa.id_area = %s ORDER BY a.nombre_actividad", (area_id,))
                return [{'id': r['id_actividad'], 'nombre': r['nombre_actividad']} for r in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error obteniendo actividades de área: {e}")
        return []

def remove_activity_from_area(area_id, actividad_id):
    """Quitar asociación actividad-área"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM AREA_ACTIVIDAD WHERE id_area = %s AND id_actividad = %s", (area_id, actividad_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error removiendo actividad de área: {e}")
        return False

# AREA_EMPLEADO
def assign_employee_to_area(area_id, empleado_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO AREA_EMPLEADO (id_area, id_empleado) VALUES (%s, %s) ON CONFLICT DO NOTHING", (area_id, empleado_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error asignando empleado a área: {e}")
        return False

def get_employees_for_area(area_id):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("SELECT e.id_empleado, e.nombre_empleado FROM EMPLEADOS e JOIN AREA_EMPLEADO ae ON e.id_empleado = ae.id_empleado WHERE ae.id_area = %s ORDER BY e.nombre_empleado", (area_id,))
                return [{'id': r['id_empleado'], 'nombre': r['nombre_empleado']} for r in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error obteniendo empleados de área: {e}")
        return []

def remove_employee_from_area(area_id, empleado_id):
    """Quitar asociación empleado-área"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM AREA_EMPLEADO WHERE id_area = %s AND id_empleado = %s", (area_id, empleado_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error removiendo empleado de área: {e}")
        return False

# AREA_REQUISICION
def assign_requisicion_to_area(area_id, requisicion_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO AREA_REQUISICION (id_area, id_requisicion) VALUES (%s, %s) ON CONFLICT DO NOTHING", (area_id, requisicion_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error asignando requisición a área: {e}")
        return False

def get_requisiciones_for_area(area_id):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("SELECT r.id_requisicion, r.fecha_requisicion FROM REQUISICIONES r JOIN AREA_REQUISICION ar ON r.id_requisicion = ar.id_requisicion WHERE ar.id_area = %s ORDER BY r.fecha_requisicion DESC", (area_id,))
                return [{'id': r['id_requisicion'], 'fecha': r['fecha_requisicion']} for r in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Error obteniendo requisiciones de área: {e}")
        return []

def remove_requisicion_from_area(area_id, requisicion_id):
    """Quitar asociación requisición-área"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM AREA_REQUISICION WHERE id_area = %s AND id_requisicion = %s", (area_id, requisicion_id))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error removiendo requisición de área: {e}")
        return False

# REQUISICIONES Y MOVIMIENTOS
def get_requisiciones_safe():
    """Obtener requisiciones de materiales"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        r.id_requisicion,
                        r.id_requisicion as id,
                        r.id_requisicion as requisicion_id,
                        r.fecha_requisicion,
                        r.estado_requisicion,
                        a.nombre_area,
                        COUNT(rd.id_detalle_requisicion) as items_solicitados
                    FROM REQUISICIONES r
                    LEFT JOIN AREA_REQUISICION ar ON r.id_requisicion = ar.id_requisicion
                    LEFT JOIN AREAS a ON ar.id_area = a.id_area
                    LEFT JOIN REQUISICION_DETALLE rd_rel ON r.id_requisicion = rd_rel.id_requisicion
                    LEFT JOIN DETALLES_REQUISICION rd ON rd_rel.id_detalle_requisicion = rd.id_detalle_requisicion
                    GROUP BY r.id_requisicion, r.fecha_requisicion, r.estado_requisicion, a.nombre_area
                    ORDER BY r.fecha_requisicion DESC
                    LIMIT 50
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo requisiciones: {e}")
        return []

def insert_requisicion_safe(fecha_requisicion=None, estado_requisicion='Pendiente', area_id=None):
    """Insertar nueva requisición"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO REQUISICIONES (fecha_requisicion, estado_requisicion)
                    VALUES (COALESCE(%s, CURRENT_DATE), %s) RETURNING id_requisicion
                """, (fecha_requisicion, estado_requisicion))
                requisicion_id = cursor.fetchone()[0]
                
                # Asociar con área si se especifica
                if area_id:
                    cursor.execute("""
                        INSERT INTO AREA_REQUISICION (id_area, id_requisicion) VALUES (%s, %s)
                    """, (area_id, requisicion_id))
                
                return requisicion_id
    except Exception as e:
        logger.error(f"Error insertando requisición: {e}")
        return None

def get_requisicion_by_id_safe(requisicion_id):
    """Obtener una requisición específica por ID"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        r.id_requisicion,
                        r.id_requisicion as id,
                        r.id_requisicion as requisicion_id,
                        r.fecha_requisicion,
                        r.estado_requisicion,
                        a.id_area,
                        a.nombre_area,
                        COUNT(rd.id_detalle_requisicion) as items_solicitados
                    FROM REQUISICIONES r
                    LEFT JOIN AREA_REQUISICION ar ON r.id_requisicion = ar.id_requisicion
                    LEFT JOIN AREAS a ON ar.id_area = a.id_area
                    LEFT JOIN REQUISICION_DETALLE rd_rel ON r.id_requisicion = rd_rel.id_requisicion
                    LEFT JOIN DETALLES_REQUISICION rd ON rd_rel.id_detalle_requisicion = rd.id_detalle_requisicion
                    WHERE r.id_requisicion = %s
                    GROUP BY r.id_requisicion, r.fecha_requisicion, r.estado_requisicion, a.id_area, a.nombre_area
                """, (requisicion_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo requisición {requisicion_id}: {e}")
        return None

def update_requisicion_safe(requisicion_id, fecha_requisicion=None, estado_requisicion='Pendiente', area_id=None):
    """Actualizar una requisición existente"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE REQUISICIONES 
                    SET fecha_requisicion = COALESCE(%s, fecha_requisicion),
                        estado_requisicion = %s
                    WHERE id_requisicion = %s
                """, (fecha_requisicion, estado_requisicion, requisicion_id))
                
                # Actualizar relación con área
                cursor.execute("DELETE FROM AREA_REQUISICION WHERE id_requisicion = %s", (requisicion_id,))
                if area_id:
                    cursor.execute("""
                        INSERT INTO AREA_REQUISICION (id_area, id_requisicion) VALUES (%s, %s)
                    """, (area_id, requisicion_id))
                
                return True
    except Exception as e:
        logger.error(f"Error actualizando requisición {requisicion_id}: {e}")
        return False

def delete_requisicion_safe(requisicion_id):
    """Eliminar una requisición y sus relaciones"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Eliminar relaciones primero
                cursor.execute("DELETE FROM AREA_REQUISICION WHERE id_requisicion = %s", (requisicion_id,))
                cursor.execute("DELETE FROM REQUISICION_DETALLE WHERE id_requisicion = %s", (requisicion_id,))
                # Eliminar la requisición
                cursor.execute("DELETE FROM REQUISICIONES WHERE id_requisicion = %s", (requisicion_id,))
                return True
    except Exception as e:
        logger.error(f"Error eliminando requisición {requisicion_id}: {e}")
        return False

def get_movimientos_materiales_safe():
    """Obtener movimientos de materiales"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        mm.id_movimiento_material,
                        mm.id_movimiento_material as id,
                        mm.id_movimiento_material as movimiento_id,
                        mm.tipo_movimiento,
                        mm.fecha_movimiento,
                        mm.origen_movimiento,
                        mm.destino_movimiento,
                        mm.cantidad,
                        mm.id_material,
                        m.nombre_material
                    FROM MOVIMIENTOS_MATERIAL mm
                    LEFT JOIN MATERIALES m ON mm.id_material = m.id_material
                    ORDER BY mm.fecha_movimiento DESC
                    LIMIT 100
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo movimientos: {e}")
        return []

def get_movimiento_material_by_id_safe(movimiento_id: int):
    """Obtener movimiento de material por ID"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        mm.id_movimiento_material,
                        mm.id_movimiento_material as id,
                        mm.id_movimiento_material as movimiento_id,
                        mm.tipo_movimiento,
                        mm.fecha_movimiento,
                        mm.origen_movimiento,
                        mm.destino_movimiento,
                        mm.cantidad,
                        mm.id_material,
                        m.nombre_material
                    FROM MOVIMIENTOS_MATERIAL mm
                    LEFT JOIN MATERIALES m ON mm.id_material = m.id_material
                    WHERE mm.id_movimiento_material = %s
                """, (movimiento_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo movimiento por ID: {e}")
        return None

def insert_movimiento_material_safe(tipo_movimiento, cantidad, id_material=None, fecha_movimiento=None, origen=None, destino=None):
    """Insertar nuevo movimiento de material"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO MOVIMIENTOS_MATERIAL 
                    (tipo_movimiento, cantidad, id_material, fecha_movimiento, origen_movimiento, destino_movimiento)
                    VALUES (%s, %s, %s, COALESCE(%s, CURRENT_TIMESTAMP), %s, %s)
                    RETURNING id_movimiento_material
                """, (tipo_movimiento, cantidad, id_material, fecha_movimiento, origen, destino))
                movimiento_id = cursor.fetchone()[0]
                conn.commit()
                logger.info(f"Movimiento de material creado: ID {movimiento_id}")
                return movimiento_id
    except Exception as e:
        logger.error(f"Error insertando movimiento: {e}")
        return None

def update_movimiento_material_safe(movimiento_id: int, tipo_movimiento=None, cantidad=None, id_material=None, 
                                     fecha_movimiento=None, origen=None, destino=None):
    """Actualizar movimiento de material existente"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE MOVIMIENTOS_MATERIAL
                    SET tipo_movimiento = COALESCE(%s, tipo_movimiento),
                        cantidad = COALESCE(%s, cantidad),
                        id_material = COALESCE(%s, id_material),
                        fecha_movimiento = COALESCE(%s, fecha_movimiento),
                        origen_movimiento = COALESCE(%s, origen_movimiento),
                        destino_movimiento = COALESCE(%s, destino_movimiento)
                    WHERE id_movimiento_material = %s
                """, (tipo_movimiento, cantidad, id_material, fecha_movimiento, origen, destino, movimiento_id))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error actualizando movimiento: {e}")
        return False

def delete_movimiento_material_safe(movimiento_id: int):
    """Eliminar movimiento de material"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM MOVIMIENTOS_MATERIAL WHERE id_movimiento_material = %s", (movimiento_id,))
                conn.commit()
                return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Error eliminando movimiento: {e}")
        return False

# TRABAJOS Y DETALLES
def get_trabajos_safe():
    """Obtener trabajos disponibles"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        t.id_trabajo,
                        t.id_trabajo as id,
                        t.id_trabajo as trabajo_id,
                        t.descripcion_trabajo,
                        t.precio_unitario_trabajo,
                        t.unidad_trabajo,
                        COUNT(DISTINCT at.id_actividad) as actividades_asignadas
                    FROM TRABAJOS t
                    LEFT JOIN ACTIVIDAD_TRABAJO at ON t.id_trabajo = at.id_trabajo
                    GROUP BY t.id_trabajo, t.descripcion_trabajo, t.precio_unitario_trabajo, t.unidad_trabajo
                    ORDER BY t.descripcion_trabajo
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo trabajos: {e}")
        return []

def insert_trabajo_safe(descripcion, precio_unitario=None, unidad=None):
    """Insertar nuevo trabajo"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO TRABAJOS (descripcion_trabajo, precio_unitario_trabajo, unidad_trabajo)
                    VALUES (%s, %s, %s) RETURNING id_trabajo
                """, (descripcion, precio_unitario, unidad))
                return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Error insertando trabajo: {e}")
        return None

def get_trabajo_by_id_safe(trabajo_id):
    """Obtener un trabajo específico por ID"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        t.id_trabajo,
                        t.id_trabajo as id,
                        t.id_trabajo as trabajo_id,
                        t.descripcion_trabajo,
                        t.precio_unitario_trabajo,
                        t.unidad_trabajo,
                        COUNT(DISTINCT at.id_actividad) as actividades_asignadas
                    FROM TRABAJOS t
                    LEFT JOIN ACTIVIDAD_TRABAJO at ON t.id_trabajo = at.id_trabajo
                    WHERE t.id_trabajo = %s
                    GROUP BY t.id_trabajo, t.descripcion_trabajo, t.precio_unitario_trabajo, t.unidad_trabajo
                """, (trabajo_id,))
                return cursor.fetchone()
    except Exception as e:
        logger.error(f"Error obteniendo trabajo {trabajo_id}: {e}")
        return None

def update_trabajo_safe(trabajo_id, descripcion, precio_unitario=None, unidad=None):
    """Actualizar un trabajo existente"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE TRABAJOS 
                    SET descripcion_trabajo = %s,
                        precio_unitario_trabajo = %s,
                        unidad_trabajo = %s
                    WHERE id_trabajo = %s
                """, (descripcion, precio_unitario, unidad, trabajo_id))
                return True
    except Exception as e:
        logger.error(f"Error actualizando trabajo {trabajo_id}: {e}")
        return False

def delete_trabajo_safe(trabajo_id):
    """Eliminar un trabajo"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Eliminar relaciones primero
                cursor.execute("DELETE FROM ACTIVIDAD_TRABAJO WHERE id_trabajo = %s", (trabajo_id,))
                # Eliminar el trabajo
                cursor.execute("DELETE FROM TRABAJOS WHERE id_trabajo = %s", (trabajo_id,))
                return True
    except Exception as e:
        logger.error(f"Error eliminando trabajo {trabajo_id}: {e}")
        return False

# =====================================================
# FUNCIONES EXTENDIDAS PARA 30 NUEVAS TABLAS
# =====================================================

# MÓDULO FACTURACIÓN Y PAGOS
def obtener_facturas():
    """Obtiene todas las facturas"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT f.*, c.nombre as nombre_cliente
                    FROM FACTURAS f
                    LEFT JOIN CLIENTES c ON f.id_cliente = c.id_cliente
                    ORDER BY f.fecha_factura DESC
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo facturas: {e}")
        return []

def crear_factura(numero_factura, fecha_factura, fecha_vencimiento, 
                  subtotal, impuestos, descuento, total, id_cliente, observaciones=""):
    """Crea una nueva factura"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO FACTURAS (numero_factura, fecha_factura, fecha_vencimiento,
                                        subtotal, impuestos, descuento, total, id_cliente, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_factura
                """, (numero_factura, fecha_factura, fecha_vencimiento, 
                      subtotal, impuestos, descuento, total, id_cliente, observaciones))
                return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Error creando factura: {e}")
        return None

def obtener_metodos_pago():
    """Obtiene todos los métodos de pago activos"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM METODOS_PAGO WHERE activo = true ORDER BY nombre_metodo")
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo métodos de pago: {e}")
        return []

def crear_pago(numero_recibo, fecha_pago, monto_pago, id_metodo_pago, 
               referencia_pago="", observaciones_pago=""):
    """Crea un nuevo pago"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO PAGOS (numero_recibo, fecha_pago, monto_pago, id_metodo_pago,
                                      referencia_pago, observaciones_pago)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id_pago
                """, (numero_recibo, fecha_pago, monto_pago, id_metodo_pago, 
                      referencia_pago, observaciones_pago))
                return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Error creando pago: {e}")
        return None

def obtener_cuentas_por_cobrar():
    """Obtiene todas las cuentas por cobrar pendientes"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT cc.*, f.numero_factura, c.nombre as nombre_cliente
                    FROM CUENTAS_COBRAR cc
                    JOIN FACTURAS f ON cc.id_factura = f.id_factura
                    JOIN CLIENTES c ON f.id_cliente = c.id_cliente
                    WHERE cc.monto_pendiente > 0
                    ORDER BY cc.fecha_vencimiento
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo cuentas por cobrar: {e}")
        return []

# MÓDULO CONTABILIDAD AVANZADA
def obtener_cuentas_contables():
    """Obtiene todas las cuentas contables"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM CUENTAS_CONTABLES
                    WHERE activa = true
                    ORDER BY codigo_cuenta
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo cuentas contables: {e}")
        return []

def obtener_gastos_obra(id_obra=None):
    """Obtiene gastos de obras"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                if id_obra:
                    cursor.execute("""
                        SELECT go.*, o.nombre as nombre_obra, cc.nombre_centro
                        FROM GASTOS_OBRA go
                        JOIN OBRAS o ON go.id_obra = o.id_obra
                        LEFT JOIN CENTROS_COSTO cc ON go.id_centro_costo = cc.id_centro_costo
                        WHERE go.id_obra = %s
                        ORDER BY go.fecha_gasto DESC
                    """, (id_obra,))
                else:
                    cursor.execute("""
                        SELECT go.*, o.nombre as nombre_obra, cc.nombre_centro
                        FROM GASTOS_OBRA go
                        JOIN OBRAS o ON go.id_obra = o.id_obra
                        LEFT JOIN CENTROS_COSTO cc ON go.id_centro_costo = cc.id_centro_costo
                        ORDER BY go.fecha_gasto DESC
                    """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo gastos de obra: {e}")
        return []

def obtener_flujo_caja(fecha_inicio=None, fecha_fin=None):
    """Obtiene el flujo de caja"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM FLUJO_CAJA"
                params = []
                
                if fecha_inicio and fecha_fin:
                    query += " WHERE fecha_flujo BETWEEN %s AND %s"
                    params = [fecha_inicio, fecha_fin]
                
                query += " ORDER BY fecha_flujo DESC"
                cursor.execute(query, params)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo flujo de caja: {e}")
        return []

# MÓDULO MANTENIMIENTO
def obtener_mantenimientos():
    """Obtiene todos los mantenimientos"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT m.*, 
                           e.nombre as nombre_equipo,
                           v.marca as marca_vehiculo, v.modelo as modelo_vehiculo
                    FROM MANTENIMIENTOS m
                    LEFT JOIN EQUIPOS e ON m.id_equipo = e.id_equipo
                    LEFT JOIN VEHICULOS v ON m.id_vehiculo = v.id_vehiculo
                    ORDER BY m.fecha_programada DESC
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo mantenimientos: {e}")
        return []

def crear_mantenimiento(id_equipo, id_vehiculo, tipo_mantenimiento, descripcion_mantenimiento,
                       fecha_programada, costo_estimado, responsable_mantenimiento):
    """Crea un nuevo mantenimiento"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO MANTENIMIENTOS (id_equipo, id_vehiculo, tipo_mantenimiento,
                                              descripcion_mantenimiento, fecha_programada,
                                              costo_estimado, responsable_mantenimiento)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_mantenimiento
                """, (id_equipo, id_vehiculo, tipo_mantenimiento, descripcion_mantenimiento,
                      fecha_programada, costo_estimado, responsable_mantenimiento))
                return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Error creando mantenimiento: {e}")
        return None

def obtener_repuestos():
    """Obtiene todos los repuestos"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT *, 
                           CASE 
                               WHEN stock_actual <= stock_minimo THEN 'Bajo Stock'
                               WHEN stock_actual = 0 THEN 'Sin Stock'
                               ELSE 'Disponible'
                           END as estado_stock
                    FROM REPUESTOS
                    WHERE activo = true
                    ORDER BY codigo_repuesto
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo repuestos: {e}")
        return []

# MÓDULO COMPRAS EXTENDIDO
def obtener_ordenes_compra():
    """Obtiene todas las órdenes de compra"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT oc.*, p.nombre as nombre_proveedor
                    FROM ORDENES_COMPRA oc
                    JOIN PROVEEDORES p ON oc.id_proveedor = p.id_proveedor
                    ORDER BY oc.fecha_orden DESC
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo órdenes de compra: {e}")
        return []

def crear_orden_compra(numero_orden, id_proveedor, fecha_entrega_solicitada,
                      subtotal, impuestos, total, observaciones=""):
    """Crea una nueva orden de compra"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ORDENES_COMPRA (numero_orden, id_proveedor, fecha_entrega_solicitada,
                                              subtotal, impuestos, total, observaciones)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_orden_compra
                """, (numero_orden, id_proveedor, fecha_entrega_solicitada,
                      subtotal, impuestos, total, observaciones))
                return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Error creando orden de compra: {e}")
        return None

# MÓDULO NÓMINA EXTENDIDO
def obtener_nomina(periodo_mes=None, periodo_ano=None):
    """Obtiene registros de nómina"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT n.*, e.nombre as nombre_empleado, e.cargo
                    FROM NOMINA n
                    JOIN EMPLEADOS e ON n.id_empleado = e.id_empleado
                """
                params = []
                
                if periodo_mes and periodo_ano:
                    query += " WHERE n.periodo_mes = %s AND n.periodo_ano = %s"
                    params = [periodo_mes, periodo_ano]
                
                query += " ORDER BY e.nombre"
                cursor.execute(query, params)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo nómina: {e}")
        return []

def obtener_asistencia(id_empleado=None, fecha_inicio=None, fecha_fin=None):
    """Obtiene registros de asistencia"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    SELECT a.*, e.nombre as nombre_empleado
                    FROM ASISTENCIA a
                    JOIN EMPLEADOS e ON a.id_empleado = e.id_empleado
                """
                params = []
                conditions = []
                
                if id_empleado:
                    conditions.append("a.id_empleado = %s")
                    params.append(id_empleado)
                
                if fecha_inicio and fecha_fin:
                    conditions.append("a.fecha_asistencia BETWEEN %s AND %s")
                    params.extend([fecha_inicio, fecha_fin])
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                
                query += " ORDER BY a.fecha_asistencia DESC, e.nombre"
                cursor.execute(query, params)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo asistencia: {e}")
        return []

def obtener_capacitaciones():
    """Obtiene todas las capacitaciones"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT c.*,
                           COUNT(ec.id_empleado) as empleados_inscritos
                    FROM CAPACITACIONES c
                    LEFT JOIN EMPLEADO_CAPACITACION ec ON c.id_capacitacion = ec.id_capacitacion
                    GROUP BY c.id_capacitacion
                    ORDER BY c.fecha_inicio DESC
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo capacitaciones: {e}")
        return []

# MÓDULO REPORTES AVANZADOS
def obtener_metricas_kpi():
    """Obtiene todas las métricas KPI"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT *,
                           CASE 
                               WHEN valor_objetivo > 0 THEN 
                                   ROUND((valor_actual / valor_objetivo * 100), 2)
                               ELSE 0
                           END as porcentaje_cumplimiento
                    FROM METRICAS_KPI
                    ORDER BY categoria_kpi, nombre_metrica
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo métricas KPI: {e}")
        return []

def obtener_alertas_sistema(id_usuario=None, solo_no_leidas=False):
    """Obtiene alertas del sistema"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM ALERTAS_SISTEMA"
                params = []
                conditions = []
                
                if id_usuario:
                    conditions.append("id_usuario_destinatario = %s")
                    params.append(id_usuario)
                
                if solo_no_leidas:
                    conditions.append("leida = false")
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                
                query += " ORDER BY fecha_creacion DESC"
                cursor.execute(query, params)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo alertas del sistema: {e}")
        return []

def obtener_dashboard_completo():
    """Obtiene datos para el dashboard principal con métricas del sistema completo"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                
                dashboard = {}
                
                # Métricas financieras
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_facturas,
                        COALESCE(SUM(total), 0) as facturacion_total,
                        COALESCE(SUM(CASE WHEN estado_factura = 'Pendiente' THEN total ELSE 0 END), 0) as pendiente_cobro
                    FROM FACTURAS
                """)
                finanzas = cursor.fetchone()
                dashboard['finanzas'] = finanzas if finanzas else {}
                
                # Métricas de obras
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_obras,
                        COUNT(CASE WHEN estado = 'En Progreso' THEN 1 END) as obras_activas,
                        COUNT(CASE WHEN estado = 'Completado' THEN 1 END) as obras_completadas
                    FROM OBRAS
                """)
                obras = cursor.fetchone()
                dashboard['obras'] = obras if obras else {}
                
                # Métricas de mantenimiento
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_mantenimientos,
                        COUNT(CASE WHEN estado_mantenimiento = 'Programado' THEN 1 END) as programados,
                        COUNT(CASE WHEN estado_mantenimiento = 'Realizado' THEN 1 END) as realizados
                    FROM MANTENIMIENTOS
                """)
                mantenimiento = cursor.fetchone()
                dashboard['mantenimiento'] = mantenimiento if mantenimiento else {}
                
                # Alertas pendientes
                cursor.execute("""
                    SELECT COUNT(*) as alertas_pendientes
                    FROM ALERTAS_SISTEMA
                    WHERE leida = false
                """)
                alertas = cursor.fetchone()
                dashboard['alertas_pendientes'] = alertas['alertas_pendientes'] if alertas else 0
                
                return dashboard
    except Exception as e:
        logger.error(f"Error obteniendo dashboard completo: {e}")
        return {}

# ===============================
# FUNCIONES DE AUTENTICACIÓN
# ===============================
def validar_usuario_login(username, password):
    """Validar credenciales de usuario para login"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        u.id_usuario,
                        u.nombre_usuario,
                        u.password_hash,
                        u.email,
                        u.nombre_completo,
                        u.activo,
                        u.fecha_ultimo_acceso,
                        u.intentos_fallidos,
                        u.bloqueado,
                        e.nombre as empleado_nombre,
                        e.cargo,
                        r.nombre_rol,
                        r.descripcion_rol
                    FROM USUARIOS_SISTEMA u
                    LEFT JOIN EMPLEADOS e ON u.id_empleado = e.id_empleado
                    LEFT JOIN ROLES r ON u.id_rol = r.id_rol
                    WHERE u.nombre_usuario = %s AND u.activo = true AND u.bloqueado = false
                """, (username,))
                
                usuario = cursor.fetchone()
                
                if usuario:
                    # En producción, usar bcrypt para verificar password hash
                    # Por ahora, comparación simple (SOLO PARA DESARROLLO)
                    if usuario['password_hash'] == password:
                        # Actualizar último acceso
                        cursor.execute("""
                            UPDATE USUARIOS_SISTEMA 
                            SET fecha_ultimo_acceso = CURRENT_TIMESTAMP,
                                intentos_fallidos = 0
                            WHERE id_usuario = %s
                        """, (usuario['id_usuario'],))
                        conn.commit()
                        
                        return dict(usuario)
                    else:
                        # Incrementar intentos fallidos
                        nuevo_intentos = (usuario['intentos_fallidos'] or 0) + 1
                        bloqueado = nuevo_intentos >= 5
                        
                        cursor.execute("""
                            UPDATE USUARIOS_SISTEMA 
                            SET intentos_fallidos = %s,
                                bloqueado = %s
                            WHERE id_usuario = %s
                        """, (nuevo_intentos, bloqueado, usuario['id_usuario']))
                        conn.commit()
                        
                        return None
                else:
                    return None
                    
    except Exception as e:
        logger.error(f"Error validando usuario: {e}")
        return None

def obtener_permisos_usuario(id_usuario):
    """Obtener permisos del usuario"""
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Intentar con sistema completo de permisos
        try:
            cursor.execute("""
                SELECT DISTINCT
                    p.codigo_permiso,
                    p.nombre_permiso,
                    p.descripcion,
                    p.modulo
                FROM PERMISOS_SISTEMA p
                INNER JOIN ROLES_PERMISOS rp ON p.id_permiso = rp.id_permiso
                INNER JOIN USUARIOS_SISTEMA u ON rp.id_rol = u.id_rol
                WHERE u.id_usuario = %s AND p.activo = true
                ORDER BY p.modulo, p.codigo_permiso
            """, (id_usuario,))
            
            permisos = cursor.fetchall()
            conn.close()
            return [dict(p) for p in permisos] if permisos else []
        except Exception as e:
            # Si falla, hacer rollback y usar esquema simplificado basado en rol
            logger.debug(f"Sistema de permisos complejo no disponible, usando roles simples: {e}")
            conn.rollback()
            
            cursor.execute("""
                SELECT rol_usuario
                FROM USUARIOS_SISTEMA
                WHERE id_usuario = %s
            """, (id_usuario,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if not resultado:
                return []
            
            rol = resultado['rol_usuario'] if isinstance(resultado, dict) else resultado[0]
            
            # Mapeo de permisos por rol
            permisos_por_rol = {
                'ADMINISTRADOR': [
                    {'codigo_permiso': 'ADMIN_USUARIOS', 'nombre_permiso': 'Administrar Usuarios', 'modulo': 'Administración'},
                    {'codigo_permiso': 'ADMIN_SISTEMA', 'nombre_permiso': 'Administrar Sistema', 'modulo': 'Administración'},
                    {'codigo_permiso': 'VER_REPORTES', 'nombre_permiso': 'Ver Reportes', 'modulo': 'Reportes'},
                    {'codigo_permiso': 'GESTIONAR_OBRAS', 'nombre_permiso': 'Gestionar Obras', 'modulo': 'Obras'}
                ],
                'SUPERVISOR': [
                    {'codigo_permiso': 'VER_REPORTES', 'nombre_permiso': 'Ver Reportes', 'modulo': 'Reportes'},
                    {'codigo_permiso': 'GESTIONAR_OBRAS', 'nombre_permiso': 'Gestionar Obras', 'modulo': 'Obras'}
                ],
                'TECNICO': [
                    {'codigo_permiso': 'GESTIONAR_OBRAS', 'nombre_permiso': 'Gestionar Obras', 'modulo': 'Obras'}
                ],
                'CONTADOR': [
                    {'codigo_permiso': 'VER_REPORTES', 'nombre_permiso': 'Ver Reportes', 'modulo': 'Reportes'}
                ],
                'OPERADOR': []
            }
            
            return permisos_por_rol.get(rol.upper() if rol else '', [])
            
    except Exception as e:
        logger.error(f"Error obteniendo permisos: {e}")
        try:
            if conn:
                conn.close()
        except:
            pass
        return []

def crear_usuario_sistema(nombre_usuario, password, email, nombre_completo, id_empleado=None, id_rol=None):
    """Crear nuevo usuario del sistema"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Insertar en la tabla usuarios_sistema con la estructura real
                cursor.execute("""
                    INSERT INTO usuarios_sistema 
                    (nombre_usuario, contrasena_usuario, correo_usuario, rol_usuario)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_usuario
                """, (nombre_usuario, password, email, id_rol))
                
                usuario_id = cursor.fetchone()[0]
                conn.commit()
                logger.info(f"Usuario creado: {nombre_usuario} con rol {id_rol}")
                return usuario_id
                
    except Exception as e:
        logger.error(f"Error creando usuario: {e}")
        return None

def obtener_roles_disponibles():
    """Obtener todos los roles disponibles desde la tabla roles"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Intentar obtener roles de la nueva tabla 'roles'
                cursor.execute("""
                    SELECT id_rol, nombre_rol, descripcion_rol, activo
                    FROM roles
                    WHERE activo = true
                    ORDER BY id_rol
                """)
                
                roles = cursor.fetchall()
                return [dict(r) for r in roles] if roles else []
                
    except Exception as e:
        logger.error(f"Error obteniendo roles desde tabla roles: {e}")
        
        # Fallback: intentar obtener roles únicos de usuarios_sistema
        try:
            with get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute("""
                        SELECT DISTINCT rol_usuario as nombre_rol
                        FROM usuarios_sistema
                        WHERE rol_usuario IS NOT NULL AND rol_usuario != ''
                        ORDER BY rol_usuario
                    """)
                    
                    roles = cursor.fetchall()
                    # Convertir a formato compatible con el template
                    roles_list = []
                    for i, rol in enumerate(roles or []):
                        roles_list.append({
                            'id_rol': i + 1,
                            'nombre_rol': rol['nombre_rol'],
                            'descripcion_rol': rol['nombre_rol'],
                            'activo': True
                        })
                    
                    if roles_list:
                        return roles_list
                        
        except Exception as e2:
            logger.error(f"Error obteniendo roles desde usuarios_sistema: {e2}")
        
        # Último recurso: retornar roles predeterminados
        logger.info("Usando roles predeterminados como fallback")
        return [
            {'id_rol': 1, 'nombre_rol': 'ADMINISTRADOR', 'descripcion_rol': 'Administrador del sistema', 'activo': True},
            {'id_rol': 2, 'nombre_rol': 'Ingeniero Civil', 'descripcion_rol': 'Ingeniero Civil', 'activo': True},
            {'id_rol': 3, 'nombre_rol': 'Arquitecto', 'descripcion_rol': 'Arquitecto', 'activo': True},
            {'id_rol': 4, 'nombre_rol': 'Supervisor de Obra', 'descripcion_rol': 'Supervisor de Obra', 'activo': True},
            {'id_rol': 5, 'nombre_rol': 'Jefe de Proyecto', 'descripcion_rol': 'Jefe de Proyecto', 'activo': True},
            {'id_rol': 6, 'nombre_rol': 'Contador', 'descripcion_rol': 'Contador', 'activo': True},
            {'id_rol': 7, 'nombre_rol': 'Operador de Equipo', 'descripcion_rol': 'Operador de Equipo', 'activo': True},
            {'id_rol': 8, 'nombre_rol': 'Almacenista', 'descripcion_rol': 'Almacenista', 'activo': True},
            {'id_rol': 9, 'nombre_rol': 'Asistente', 'descripcion_rol': 'Asistente', 'activo': True},
            {'id_rol': 10, 'nombre_rol': 'Otro', 'descripcion_rol': 'Otro cargo no especificado', 'activo': True}
        ]

def _cols_usuarios_sistema(cursor):
    """Helper: devuelve el set de columnas existentes en USUARIOS_SISTEMA."""
    try:
        cursor.execute("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'usuarios_sistema'
        """)
        return {row[0] for row in cursor.fetchall()}
    except Exception:
        return set()

def get_usuario_by_id_safe(id_usuario):
    """Obtiene un usuario por id adaptándose al esquema existente."""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as rcursor:
                with conn.cursor() as cursor:
                    cols = _cols_usuarios_sistema(cursor)

                # Campos obligatorios mínimos
                select_parts = [
                    "u.id_usuario",
                    "u.nombre_usuario"
                ]

                # Email
                if 'correo_usuario' in cols:
                    select_parts.append("u.correo_usuario AS email")
                elif 'email' in cols:
                    select_parts.append("u.email AS email")

                # Nombre completo
                if 'nombre_completo' in cols:
                    select_parts.append("u.nombre_completo")

                # Empleado
                join_empleado = False
                if 'id_empleado' in cols:
                    select_parts.append("u.id_empleado")
                    select_parts.append("e.nombre AS empleado_nombre")
                    select_parts.append("e.cargo")
                    join_empleado = True

                # Rol
                join_rol = False
                if 'id_rol' in cols:
                    select_parts.append("u.id_rol")
                    select_parts.append("r.nombre_rol")
                    join_rol = True
                elif 'rol_usuario' in cols:
                    select_parts.append("u.rol_usuario AS nombre_rol")

                # Estado
                for c in ['activo', 'bloqueado', 'intentos_fallidos', 'fecha_creacion', 'fecha_ultimo_acceso']:
                    if c in cols:
                        select_parts.append(f"u.{c}")

                query = "SELECT " + ", ".join(select_parts) + " FROM USUARIOS_SISTEMA u"
                if join_empleado:
                    query += " LEFT JOIN EMPLEADOS e ON u.id_empleado = e.id_empleado"
                if join_rol:
                    query += " LEFT JOIN ROLES r ON u.id_rol = r.id_rol"
                query += " WHERE u.id_usuario = %s"

                rcursor.execute(query, (id_usuario,))
                row = rcursor.fetchone()
                return dict(row) if row else None
    except Exception as e:
        logger.error(f"Error obteniendo usuario por id: {e}")
        return None

def update_usuario_safe(id_usuario, datos):
    """Actualiza un usuario de forma segura solo en columnas existentes.
    datos: dict con posibles llaves: nombre_usuario, email, nombre_completo, id_empleado, id_rol, rol_usuario
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cols = _cols_usuarios_sistema(cursor)

                sets = []
                params = []

                # nombre_usuario
                if 'nombre_usuario' in datos and 'nombre_usuario' in cols:
                    sets.append('nombre_usuario = %s')
                    params.append(datos['nombre_usuario'])

                # correo/email
                if 'email' in datos:
                    if 'correo_usuario' in cols:
                        sets.append('correo_usuario = %s')
                        params.append(datos['email'])
                    elif 'email' in cols:
                        sets.append('email = %s')
                        params.append(datos['email'])

                # nombre_completo
                if 'nombre_completo' in datos and 'nombre_completo' in cols:
                    sets.append('nombre_completo = %s')
                    params.append(datos['nombre_completo'])

                # empleado
                if 'id_empleado' in datos and 'id_empleado' in cols:
                    sets.append('id_empleado = %s')
                    params.append(datos['id_empleado'])

                # rol (id_rol o rol_usuario)
                if 'id_rol' in datos and 'id_rol' in cols:
                    sets.append('id_rol = %s')
                    params.append(datos['id_rol'])
                elif 'rol_usuario' in datos and 'rol_usuario' in cols:
                    sets.append('rol_usuario = %s')
                    params.append(datos['rol_usuario'])

                if not sets:
                    return False

                params.append(id_usuario)
                query = f"UPDATE USUARIOS_SISTEMA SET {', '.join(sets)} WHERE id_usuario = %s"
                cursor.execute(query, tuple(params))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f"Error actualizando usuario: {e}")
        return False

def cambiar_password_usuario(id_usuario, password_actual, password_nuevo):
    """Cambiar contraseña de usuario"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Verificar password actual
                cursor.execute("""
                    SELECT password_hash FROM USUARIOS_SISTEMA 
                    WHERE id_usuario = %s
                """, (id_usuario,))
                
                usuario = cursor.fetchone()
                
                if usuario and usuario['password_hash'] == password_actual:
                    cursor.execute("""
                        UPDATE USUARIOS_SISTEMA 
                        SET password_hash = %s,
                            fecha_cambio_password = CURRENT_TIMESTAMP
                        WHERE id_usuario = %s
                    """, (password_nuevo, id_usuario))
                    conn.commit()
                    
                    logger.info(f"Password cambiado para usuario ID: {id_usuario}")
                    return True
                else:
                    return False
                    
    except Exception as e:
        logger.error(f"Error cambiando password: {e}")
        return False

def registrar_auditoria_login(id_usuario, accion, ip_address=None, user_agent=None):
    """Registrar eventos de login en auditoría"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO AUDITORIA 
                    (tabla_afectada, accion, id_usuario, fecha_operacion, 
                     detalles_operacion, ip_address)
                    VALUES ('USUARIOS_SISTEMA', %s, %s, CURRENT_TIMESTAMP, %s, %s)
                """, (accion, id_usuario, f"Login desde {user_agent or 'Unknown'}", ip_address))
                conn.commit()
                
    except Exception as e:
        logger.error(f"Error registrando auditoría: {e}")

def verificar_permiso_usuario(id_usuario, codigo_permiso):
    """Verificar si usuario tiene un permiso específico"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Primero intentar con el sistema completo de permisos
        try:
            cursor.execute("""
                SELECT COUNT(*) as tiene_permiso
                FROM PERMISOS_SISTEMA p
                INNER JOIN ROLES_PERMISOS rp ON p.id_permiso = rp.id_permiso
                INNER JOIN USUARIOS_SISTEMA u ON rp.id_rol = u.id_rol
                WHERE u.id_usuario = %s 
                  AND p.codigo_permiso = %s 
                  AND p.activo = true
                  AND u.activo = true
            """, (id_usuario, codigo_permiso))
            
            resultado = cursor.fetchone()
            conn.close()
            return resultado[0] > 0 if resultado else False
        except Exception as e:
            # Si falla, hacer rollback y usar el esquema simplificado
            logger.debug(f"Sistema de permisos complejo no disponible, usando rol simple: {e}")
            conn.rollback()
            
            # Verificar por rol de usuario simple
            cursor.execute("""
                SELECT rol_usuario
                FROM USUARIOS_SISTEMA
                WHERE id_usuario = %s
            """, (id_usuario,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if not resultado:
                return False
            
            rol = resultado[0]
            
            # Mapeo de permisos basado en roles simples
            permisos_por_rol = {
                'ADMINISTRADOR': ['ADMIN_USUARIOS', 'ADMIN_SISTEMA', 'VER_REPORTES', 'GESTIONAR_OBRAS'],
                'SUPERVISOR': ['VER_REPORTES', 'GESTIONAR_OBRAS'],
                'TECNICO': ['GESTIONAR_OBRAS'],
                'CONTADOR': ['VER_REPORTES'],
                'OPERADOR': []
            }
            
            # Si el rol es ADMINISTRADOR, tiene todos los permisos
            if rol and rol.upper() == 'ADMINISTRADOR':
                return True
            
            # Verificar si el rol tiene el permiso específico
            permisos = permisos_por_rol.get(rol.upper() if rol else '', [])
            return codigo_permiso in permisos
            
    except Exception as e:
        logger.error(f"Error verificando permiso: {e}")
        try:
            if conn:
                conn.close()
        except:
            pass
        return False

def obtener_usuarios_sistema():
    """Obtener todos los usuarios del sistema"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        u.id_usuario,
                        u.nombre_usuario,
                        u.correo_usuario as email,
                        u.nombre_usuario as nombre_completo,
                        CASE WHEN u.rol_usuario IS NOT NULL THEN true ELSE false END as activo,
                        false as bloqueado,
                        NOW() as fecha_creacion,
                        NULL as fecha_ultimo_acceso,
                        0 as intentos_fallidos,
                        CONCAT(e.nombre_empleado, ' ', e.apellido_empleado) as empleado_nombre,
                        e.tipo_empleado as cargo,
                        u.rol_usuario as nombre_rol
                    FROM usuarios_sistema u
                    LEFT JOIN empleados e ON u.id_usuario = e.id_empleado
                    ORDER BY u.id_usuario DESC
                """)
                
                usuarios = cursor.fetchall()
                return [dict(u) for u in usuarios] if usuarios else []
                
    except Exception as e:
        logger.error(f"Error obteniendo usuarios: {e}")
        return []

def bloquear_desbloquear_usuario(id_usuario, bloquear=True):
    """Bloquear o desbloquear usuario"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE USUARIOS_SISTEMA 
                    SET bloqueado = %s,
                        intentos_fallidos = 0
                    WHERE id_usuario = %s
                """, (bloquear, id_usuario))
                conn.commit()
                
                accion = "BLOQUEO" if bloquear else "DESBLOQUEO"
                logger.info(f"Usuario {accion}: {id_usuario}")
                return True
                
    except Exception as e:
        logger.error(f"Error {'bloqueando' if bloquear else 'desbloqueando'} usuario: {e}")
        return False

def eliminar_usuario_sistema(id_usuario):
    """Eliminar usuario del sistema"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    DELETE FROM usuarios_sistema 
                    WHERE id_usuario = %s
                """, (id_usuario,))
                
                filas_afectadas = cursor.rowcount
                conn.commit()
                
                if filas_afectadas > 0:
                    logger.info(f"Usuario eliminado: {id_usuario}")
                    return True
                else:
                    logger.warning(f"Usuario no encontrado para eliminar: {id_usuario}")
                    return False
                
    except Exception as e:
        logger.error(f"Error eliminando usuario: {e}")
        return False

# Funciones de autenticación ajustadas a la estructura real
def validar_usuario_login_real(username, password):
    """Validar credenciales de usuario usando la estructura real de USUARIOS_SISTEMA"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        u.id_usuario,
                        u.nombre_usuario,
                        u.contrasena_usuario as password_hash,
                        u.correo_usuario as email,
                        u.nombre_usuario as nombre_completo,
                        u.rol_usuario as nombre_rol,
                        true as activo
                    FROM USUARIOS_SISTEMA u
                    WHERE u.nombre_usuario = %s
                """, (username,))
                
                usuario = cursor.fetchone()
                
                if usuario:
                    # En desarrollo usamos comparación simple, en producción usar bcrypt
                    if usuario['password_hash'] == password:
                        # Registrar auditoría de login exitoso
                        accion_exitoso = f'LOGIN_EXITOSO: Usuario {username} inició sesión'
                        cursor.execute("""
                            INSERT INTO AUDITORIAS (accion_auditoria, fecha_auditoria)
                            VALUES (%s, CURRENT_TIMESTAMP)
                        """, (accion_exitoso,))
                        conn.commit()
                        
                        return dict(usuario)
                    else:
                        # Registrar intento fallido
                        accion_fallido = f'LOGIN_FALLIDO: Intento fallido para usuario {username}'
                        cursor.execute("""
                            INSERT INTO AUDITORIAS (accion_auditoria, fecha_auditoria)
                            VALUES (%s, CURRENT_TIMESTAMP)
                        """, (accion_fallido,))
                        conn.commit()
                        
                        logger.warning(f"Intento de login fallido para usuario: {username}")
                        return None
                else:
                    # Usuario no encontrado
                    accion_no_encontrado = f'LOGIN_FALLIDO: Usuario {username} no encontrado'
                    cursor.execute("""
                        INSERT INTO AUDITORIAS (accion_auditoria, fecha_auditoria)
                        VALUES (%s, CURRENT_TIMESTAMP)
                    """, (accion_no_encontrado,))
                    conn.commit()
                    
                    logger.warning(f"Intento de login con usuario inexistente: {username}")
                    return None
                    
    except Exception as e:
        logger.error(f"Error validando usuario: {e}")
        return None

# Funciones para registro de usuarios
def registrar_nuevo_usuario(datos_usuario):
    """Registra un nuevo usuario en el sistema con validaciones y asigna rol/permisos por defecto"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Validar que el nombre de usuario no exista
        try:
            cursor.execute("SELECT id_usuario FROM USUARIOS_SISTEMA WHERE nombre_usuario = %s", 
                          (datos_usuario['nombre_usuario'],))
            if cursor.fetchone():
                conn.close()
                return False, "El nombre de usuario ya existe"
        except Exception as e:
            logger.error(f"Error verificando nombre de usuario: {e}")
            conn.rollback()
            conn.close()
            return False, f"Error verificando usuario: {str(e)}"

        # Validar que el email no exista (columna correo_usuario)
        try:
            cursor.execute("SELECT id_usuario FROM USUARIOS_SISTEMA WHERE correo_usuario = %s", 
                          (datos_usuario['email'],))
            if cursor.fetchone():
                conn.close()
                return False, "El correo electrónico ya está registrado"
        except Exception as e:
            logger.error(f"Error verificando email: {e}")
            conn.rollback()
            conn.close()
            return False, f"Error verificando email: {str(e)}"

        # Determinar el rol basado en el cargo
        rol_nombre = determinar_rol_por_cargo(datos_usuario.get('cargo', ''))

        # Resolver id_rol si la tabla ROLES existe - usar conexión separada para no afectar transacción principal
        rol_id = None
        try:
            with get_connection() as conn_check:
                with conn_check.cursor() as cursor_check:
                    cursor_check.execute("SELECT id_rol FROM ROLES WHERE UPPER(nombre_rol) = UPPER(%s) LIMIT 1", (rol_nombre,))
                    res = cursor_check.fetchone()
                    if res:
                        rol_id = res[0]
        except Exception as e:
            # Si no existe la tabla ROLES o la consulta falla, continuamos sin id_rol
            logger.debug(f"No se pudo obtener id_rol: {e}")
            rol_id = None

        # Verificar si la columna id_rol existe en USUARIOS_SISTEMA - usar conexión separada
        tiene_col_id_rol = False
        try:
            with get_connection() as conn_check:
                with conn_check.cursor() as cursor_check:
                    cursor_check.execute("""
                        SELECT 1 FROM information_schema.columns 
                        WHERE table_name = 'usuarios_sistema' AND column_name = 'id_rol'
                    """)
                    tiene_col_id_rol = cursor_check.fetchone() is not None
        except Exception as e:
            logger.debug(f"No se pudo verificar columna id_rol: {e}")
            tiene_col_id_rol = False

        # Para desarrollo usamos texto plano, en producción usar bcrypt
        password_plano = datos_usuario['password']

        # Construir INSERT con las columnas seguras conocidas
        columnas = [
            'nombre_usuario',
            'rol_usuario',
            'correo_usuario',
            'contrasena_usuario'
        ]
        valores = [
            datos_usuario['nombre_usuario'],
            rol_nombre,
            datos_usuario['email'],
            password_plano
        ]

        # Si existe columna id_rol y tenemos rol_id, la incluimos
        if tiene_col_id_rol and rol_id is not None:
            columnas.append('id_rol')
            valores.append(rol_id)

        # Preparar consulta dinámica
        cols_sql = ", ".join(columnas)
        params_sql = ", ".join(["%s"] * len(valores))

        try:
            cursor.execute(
                f"""
                INSERT INTO USUARIOS_SISTEMA ({cols_sql})
                VALUES ({params_sql})
                RETURNING id_usuario
                """,
                tuple(valores)
            )
            usuario_id = cursor.fetchone()[0]
            conn.commit()
        except Exception as e:
            logger.error(f"Error insertando usuario: {e}")
            conn.rollback()
            conn.close()
            return False, f"Error al crear usuario: {str(e)}"

        # Registrar auditoría en tabla AUDITORIAS - usar conexión separada para no afectar transacción principal
        try:
            with get_connection() as conn_audit:
                with conn_audit.cursor() as cursor_audit:
                    accion_auditoria = (
                        f"REGISTRO: Usuario {datos_usuario['nombre_usuario']} "
                        f"registrado con rol {rol_nombre}"
                    )
                    cursor_audit.execute(
                        """
                        INSERT INTO AUDITORIAS (accion_auditoria, fecha_auditoria)
                        VALUES (%s, CURRENT_TIMESTAMP)
                        """,
                        (accion_auditoria,)
                    )
                    conn_audit.commit()
        except Exception as e:
            # Si no existe la tabla AUDITORIAS, no interrumpir el registro
            logger.debug(f"No se pudo registrar auditoría: {e}")
            pass

        conn.close()
        return True, f"Usuario {datos_usuario['nombre_usuario']} registrado exitosamente"

    except Exception as e:
        if conn:
            try:
                conn.rollback()
                conn.close()
            except:
                pass
        logger.error(f"Error al registrar usuario: {e}")
        return False, f"Error al registrar usuario: {str(e)}"

def determinar_rol_por_cargo(cargo):
    """Determina el rol del usuario basado en su cargo"""
    roles_por_cargo = {
        'Administrador': 'ADMINISTRADOR',
        'Jefe de Proyecto': 'SUPERVISOR',
        'Supervisor de Obra': 'SUPERVISOR',
        'Ingeniero Civil': 'TECNICO',
        'Arquitecto': 'TECNICO',
        'Contador': 'CONTADOR',
        'Operador de Equipo': 'OPERADOR',
        'Almacenista': 'OPERADOR',
        'Asistente': 'OPERADOR'
    }
    
    return roles_por_cargo.get(cargo, 'OPERADOR')

def obtener_permisos_por_rol(rol):
    """Obtiene los permisos básicos según el rol del usuario - simplificado"""
    # Como no tenemos tabla de permisos, solo retornamos lista vacía
    # En el futuro se puede expandir con una tabla de permisos real
    return []

def validar_datos_registro(datos):
    """Valida los datos del formulario de registro"""
    import re
    errores = []
    
    # Validar nombre completo
    if not datos.get('nombre_completo') or len(datos['nombre_completo'].strip()) < 3:
        errores.append("El nombre completo debe tener al menos 3 caracteres")
    
    # Validar nombre de usuario
    nombre_usuario = datos.get('nombre_usuario', '').strip()
    if not nombre_usuario or len(nombre_usuario) < 4:
        errores.append("El nombre de usuario debe tener al menos 4 caracteres")
    elif not re.match(r'^[a-zA-Z0-9_]+$', nombre_usuario):
        errores.append("El nombre de usuario solo puede contener letras, números y guiones bajos")
    
    # Validar email
    email = datos.get('email', '').strip()
    if not email or not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        errores.append("Debe proporcionar un correo electrónico válido")
    
    # Validar contraseña
    password = datos.get('password', '')
    if not password or len(password) < 6:
        errores.append("La contraseña debe tener al menos 6 caracteres")
    
    # Validar confirmación de contraseña
    if password != datos.get('confirmar_password', ''):
        errores.append("Las contraseñas no coinciden")
    
    # Validar campos requeridos
    if not datos.get('cargo'):
        errores.append("Debe seleccionar un cargo")
    
    if not datos.get('departamento'):
        errores.append("Debe seleccionar un departamento")
    
    if not datos.get('terminos'):
        errores.append("Debe aceptar los términos y condiciones")
    
    return errores

# ===============================
# FUNCIONES ADICIONALES FALTANTES
# ===============================

def get_bodegas_inventarios_safe():
    """Obtener listado de bodegas e inventarios de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT b.id_bodega as id, b.nombre, b.ubicacion, b.responsable,
                       COUNT(i.id_inventario) as total_items
                FROM BODEGAS b
                LEFT JOIN INVENTARIOS i ON b.id_bodega = i.id_bodega
                GROUP BY b.id_bodega, b.nombre, b.ubicacion, b.responsable
                ORDER BY b.nombre
                """
                cursor.execute(query)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f'Error obteniendo bodegas: {e}')
        return []

def insert_bodega_safe(nombre, ubicacion, responsable=None):
    """Insertar nueva bodega de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                INSERT INTO BODEGAS (nombre, ubicacion, responsable)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (nombre, ubicacion, responsable))
                conn.commit()
                return True
    except Exception as e:
        logger.error(f'Error insertando bodega: {e}')
        return False

def get_inventarios_por_bodega_safe(id_bodega):
    """Obtener inventarios de una bodega específica"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT i.*, m.nombre as material_nombre, m.unidad
                FROM INVENTARIOS i
                JOIN MATERIALES m ON i.id_material = m.id_material
                WHERE i.id_bodega = %s
                ORDER BY m.nombre
                """
                cursor.execute(query, (id_bodega,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f'Error obteniendo inventarios de bodega {id_bodega}: {e}')
        return []

def actualizar_stock_material_safe(id_material, nueva_cantidad, tipo_movimiento='Ajuste'):
    """Actualizar stock de material de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Actualizar o crear inventario
                query_update = """
                INSERT INTO INVENTARIOS (id_material, cantidad_inventario, fecha_actualizacion)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (id_material) 
                DO UPDATE SET cantidad_inventario = %s, fecha_actualizacion = CURRENT_TIMESTAMP
                """
                cursor.execute(query_update, (id_material, nueva_cantidad, nueva_cantidad))
                
                # Registrar movimiento
                query_movimiento = """
                INSERT INTO MOVIMIENTOS_MATERIAL (id_material, tipo_movimiento, cantidad, fecha_movimiento)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
                """
                cursor.execute(query_movimiento, (id_material, tipo_movimiento, nueva_cantidad))
                
                conn.commit()
                return True
    except Exception as e:
        logger.error(f'Error actualizando stock de material {id_material}: {e}')
        return False

def get_movimientos_materiales_recientes_safe(limite=50):
    """Obtener movimientos recientes de materiales"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT mm.*, m.nombre_material as material_nombre, m.unidad_material as unidad
                FROM MOVIMIENTOS_MATERIAL mm
                LEFT JOIN MATERIALES m ON mm.id_material = m.id_material
                ORDER BY mm.fecha_movimiento DESC
                LIMIT %s
                """
                cursor.execute(query, (limite,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f'Error obteniendo movimientos de materiales: {e}')
        return []

def generar_reporte_inventario_valorizado_safe():
    """Generar reporte de inventario valorizado"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT 
                    m.nombre as material,
                    m.unidad,
                    COALESCE(i.cantidad, 0) as stock_actual,
                    m.precio_unitario,
                    (COALESCE(i.cantidad, 0) * COALESCE(m.precio_unitario, 0)) as valor_total,
                    b.nombre as bodega
                FROM MATERIALES m
                LEFT JOIN INVENTARIOS i ON m.id_material = i.id_material
                LEFT JOIN BODEGAS b ON i.id_bodega = b.id_bodega
                ORDER BY valor_total DESC
                """
                cursor.execute(query)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f'Error generando reporte de inventario valorizado: {e}')
        return []

def get_alertas_stock_bajo_safe():
    """Obtener alertas de stock bajo"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT 
                    m.nombre as material,
                    m.unidad,
                    COALESCE(i.cantidad, 0) as stock_actual,
                    m.stock_minimo,
                    b.nombre as bodega
                FROM MATERIALES m
                LEFT JOIN INVENTARIOS i ON m.id_material = i.id_material
                LEFT JOIN BODEGAS b ON i.id_bodega = b.id_bodega
                WHERE m.stock_minimo IS NOT NULL 
                AND COALESCE(i.cantidad, 0) <= m.stock_minimo
                ORDER BY stock_actual ASC
                """
                cursor.execute(query)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f'Error obteniendo alertas de stock bajo: {e}')
        return []

def validar_disponibilidad_material_safe(id_material, cantidad_requerida):
    """Validar si hay suficiente material disponible"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = """
                SELECT COALESCE(SUM(cantidad), 0) as stock_total
                FROM INVENTARIOS
                WHERE id_material = %s
                """
                cursor.execute(query, (id_material,))
                resultado = cursor.fetchone()
                stock_disponible = resultado[0] if resultado else 0
                return stock_disponible >= cantidad_requerida
    except Exception as e:
        logger.error(f'Error validando disponibilidad de material {id_material}: {e}')
        return False

def get_empleados_asignados_obra_safe(id_obra):
    """Obtener empleados asignados a una obra específica"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT 
                    oe.id_empleado,
                    oe.tipo_asignacion,
                    oe.fecha_asignacion,
                    oe.fecha_fin_asignacion,
                    oe.salario_obra,
                    oe.horas_asignadas,
                    oe.observaciones,
                    e.nombre_empleado,
                    e.apellido_empleado,
                    e.tipo_empleado,
                    e.salario_fijo_empleado,
                    e.telefono,
                    e.email
                FROM obra_empleado oe
                INNER JOIN empleados e ON oe.id_empleado = e.id_empleado
                WHERE oe.id_obra = %s
                ORDER BY oe.tipo_asignacion, e.nombre_empleado
                """
                cursor.execute(query, (id_obra,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f'Error obteniendo empleados asignados a obra {id_obra}: {e}')
        return []

def get_materiales_asignados_obra_safe(id_obra):
    """Obtener materiales asignados a una obra específica"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT 
                    om.id_material,
                    om.cantidad_asignada,
                    om.cantidad_utilizada,
                    om.fecha_asignacion,
                    om.precio_unitario_obra,
                    om.observaciones,
                    m.nombre_material,
                    m.unidad_material,
                    m.precio_unitario_material,
                    COALESCE(om.precio_unitario_obra, m.precio_unitario_material) as precio_final,
                    (COALESCE(om.precio_unitario_obra, m.precio_unitario_material) * om.cantidad_asignada) as valor_total,
                    (om.cantidad_asignada - COALESCE(om.cantidad_utilizada, 0)) as cantidad_restante
                FROM obra_material om
                INNER JOIN materiales m ON om.id_material = m.id_material
                WHERE om.id_obra = %s
                ORDER BY m.nombre_material
                """
                cursor.execute(query, (id_obra,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f'Error obteniendo materiales asignados a obra {id_obra}: {e}')
        return []

def get_vehiculos_asignados_obra_safe(id_obra):
    """Obtener vehículos asignados a una obra específica"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT 
                    ov.id_vehiculo,
                    v.placa_vehiculo,
                    v.tipo_vehiculo,
                    v.estado_vehiculo
                FROM obra_vehiculo ov
                INNER JOIN vehiculos v ON ov.id_vehiculo = v.id_vehiculo
                WHERE ov.id_obra = %s
                ORDER BY v.tipo_vehiculo, v.placa_vehiculo
                """
                cursor.execute(query, (id_obra,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f'Error obteniendo vehículos asignados a obra {id_obra}: {e}')
        return []

def get_resumen_asignaciones_obra_safe(id_obra):
    """Obtener resumen completo de asignaciones de una obra"""
    try:
        empleados = get_empleados_asignados_obra_safe(id_obra)
        materiales = get_materiales_asignados_obra_safe(id_obra)
        vehiculos = get_vehiculos_asignados_obra_safe(id_obra)
        
        # Calcular estadísticas
        total_empleados = len(empleados)
        total_materiales = len(materiales)
        total_vehiculos = len(vehiculos)
        
        # Agrupar empleados por tipo
        empleados_por_tipo = {}
        for emp in empleados:
            tipo = emp['tipo_asignacion']
            if tipo not in empleados_por_tipo:
                empleados_por_tipo[tipo] = []
            empleados_por_tipo[tipo].append(emp)
        
        # Calcular valor total de materiales
        valor_total_materiales = sum(
            float(mat.get('valor_total', 0) or 0) 
            for mat in materiales
        )
        
        return {
            'empleados': empleados,
            'materiales': materiales,
            'vehiculos': vehiculos,
            'estadisticas': {
                'total_empleados': total_empleados,
                'total_materiales': total_materiales,
                'total_vehiculos': total_vehiculos,
                'valor_total_materiales': valor_total_materiales,
                'empleados_por_tipo': empleados_por_tipo
            }
        }
    except Exception as e:
        logger.error(f'Error obteniendo resumen de asignaciones para obra {id_obra}: {e}')
        return {
            'empleados': [],
            'materiales': [],
            'vehiculos': [],
            'estadisticas': {
                'total_empleados': 0,
                'total_materiales': 0,
                'total_vehiculos': 0,
                'valor_total_materiales': 0,
                'empleados_por_tipo': {}
            }
        }

def get_obras_asignadas_proyecto_safe(id_proyecto):
    """Obtener obras asignadas a un proyecto específico"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT 
                    po.id_obra,
                    po.fecha_asignacion,
                    po.observaciones as observaciones_asignacion,
                    o.nombre_obra,
                    o.descripcion_obra,
                    o.tipo_obra,
                    o.estado_obra,
                    o.ubicacion_obra,
                    o.fecha_inicio,
                    o.fecha_fin,
                    o.valor_obra
                FROM proyecto_obra po
                INNER JOIN obras o ON po.id_obra = o.id_obra
                WHERE po.id_proyecto = %s
                ORDER BY po.fecha_asignacion DESC
                """
                cursor.execute(query, (id_proyecto,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f'Error obteniendo obras asignadas a proyecto {id_proyecto}: {e}')
        return []

def get_empleados_asignados_proyecto_safe(id_proyecto):
    """Obtener empleados asignados a un proyecto específico"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT 
                    pe.id_empleado,
                    pe.tipo_asignacion,
                    pe.fecha_asignacion,
                    pe.fecha_fin_asignacion,
                    pe.responsabilidad,
                    pe.observaciones,
                    e.nombre_empleado,
                    e.apellido_empleado,
                    e.tipo_empleado,
                    e.salario_fijo_empleado,
                    e.telefono,
                    e.email
                FROM proyecto_empleado pe
                INNER JOIN empleados e ON pe.id_empleado = e.id_empleado
                WHERE pe.id_proyecto = %s
                ORDER BY pe.tipo_asignacion, e.nombre_empleado
                """
                cursor.execute(query, (id_proyecto,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f'Error obteniendo empleados asignados a proyecto {id_proyecto}: {e}')
        return []

def get_vehiculos_asignados_proyecto_safe(id_proyecto):
    """Obtener vehículos asignados a un proyecto específico"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                SELECT 
                    pv.id_vehiculo,
                    pv.fecha_asignacion,
                    pv.fecha_fin_asignacion,
                    pv.proposito,
                    pv.observaciones,
                    v.placa_vehiculo,
                    v.tipo_vehiculo,
                    v.estado_vehiculo
                FROM proyecto_vehiculo pv
                INNER JOIN vehiculos v ON pv.id_vehiculo = v.id_vehiculo
                WHERE pv.id_proyecto = %s
                ORDER BY v.tipo_vehiculo, v.placa_vehiculo
                """
                cursor.execute(query, (id_proyecto,))
                return cursor.fetchall()
    except Exception as e:
        logger.error(f'Error obteniendo vehículos asignados a proyecto {id_proyecto}: {e}')
        return []

def get_resumen_asignaciones_proyecto_safe(id_proyecto):
    """Obtener resumen completo de asignaciones de un proyecto"""
    try:
        obras = get_obras_asignadas_proyecto_safe(id_proyecto)
        empleados = get_empleados_asignados_proyecto_safe(id_proyecto)
        vehiculos = get_vehiculos_asignados_proyecto_safe(id_proyecto)
        
        # Calcular estadísticas
        total_obras = len(obras)
        total_empleados = len(empleados)
        total_vehiculos = len(vehiculos)
        
        # Agrupar empleados por tipo de asignación
        empleados_por_tipo = {}
        arquitectos = []
        ingenieros = []
        
        for emp in empleados:
            tipo = emp['tipo_asignacion']
            if tipo not in empleados_por_tipo:
                empleados_por_tipo[tipo] = []
            empleados_por_tipo[tipo].append(emp)
            
            # Clasificar arquitectos e ingenieros específicamente
            if tipo == 'ARQUITECTO':
                arquitectos.append(emp)
            elif tipo == 'INGENIERO':
                ingenieros.append(emp)
        
        # Calcular valor total de obras asignadas
        valor_total_obras = sum(
            float(obra.get('valor_obra', 0) or 0) 
            for obra in obras
        )
        
        return {
            'obras': obras,
            'empleados': empleados,
            'vehiculos': vehiculos,
            'arquitectos': arquitectos,
            'ingenieros': ingenieros,
            'estadisticas': {
                'total_obras': total_obras,
                'total_empleados': total_empleados,
                'total_vehiculos': total_vehiculos,
                'total_arquitectos': len(arquitectos),
                'total_ingenieros': len(ingenieros),
                'valor_total_obras': valor_total_obras,
                'empleados_por_tipo': empleados_por_tipo
            }
        }
    except Exception as e:
        logger.error(f'Error obteniendo resumen de asignaciones para proyecto {id_proyecto}: {e}')
        return {
            'obras': [],
            'empleados': [],
            'vehiculos': [],
            'arquitectos': [],
            'ingenieros': [],
            'estadisticas': {
                'total_obras': 0,
                'total_empleados': 0,
                'total_vehiculos': 0,
                'total_arquitectos': 0,
                'total_ingenieros': 0,
                'valor_total_obras': 0,
                'empleados_por_tipo': {}
            }
        }

# =============================================
# GESTIÓN DE INVENTARIOS COMPLETA
# =============================================

def get_inventarios_safe():
    """Obtener todos los inventarios con información detallada"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        i.id_inventario,
                        i.cantidad_inventario,
                        COUNT(DISTINCT bi.id_bodega) as bodegas_asignadas,
                        COUNT(DISTINCT im.id_material) as materiales_incluidos,
                        COALESCE(SUM(m.precio_unitario_material * i.cantidad_inventario), 0) as valor_estimado
                    FROM INVENTARIOS i
                    LEFT JOIN BODEGA_INVENTARIO bi ON i.id_inventario = bi.id_inventario
                    LEFT JOIN INVENTARIO_MATERIAL im ON i.id_inventario = im.id_inventario
                    LEFT JOIN MATERIALES m ON im.id_material = m.id_material
                    GROUP BY i.id_inventario, i.cantidad_inventario
                    ORDER BY i.id_inventario
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo inventarios: {e}")
        return []

def get_inventario_by_id_safe(inventario_id: int):
    """Obtener inventario por ID con detalles completos"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                # Información básica del inventario
                cursor.execute("""
                    SELECT 
                        i.id_inventario,
                        i.cantidad_inventario,
                        COUNT(DISTINCT bi.id_bodega) as bodegas_asignadas,
                        COUNT(DISTINCT im.id_material) as materiales_incluidos
                    FROM INVENTARIOS i
                    LEFT JOIN BODEGA_INVENTARIO bi ON i.id_inventario = bi.id_inventario
                    LEFT JOIN INVENTARIO_MATERIAL im ON i.id_inventario = im.id_inventario
                    WHERE i.id_inventario = %s
                    GROUP BY i.id_inventario, i.cantidad_inventario
                """, (inventario_id,))
                
                inventario = cursor.fetchone()
                if not inventario:
                    return None
                
                # Bodegas asociadas
                cursor.execute("""
                    SELECT b.id_bodega, b.responsable_bodega
                    FROM BODEGAS b
                    JOIN BODEGA_INVENTARIO bi ON b.id_bodega = bi.id_bodega
                    WHERE bi.id_inventario = %s
                """, (inventario_id,))
                inventario['bodegas'] = cursor.fetchall()
                
                # Materiales incluidos
                cursor.execute("""
                    SELECT m.id_material, m.nombre_material, m.unidad_material, m.precio_unitario_material
                    FROM MATERIALES m
                    JOIN INVENTARIO_MATERIAL im ON m.id_material = im.id_material
                    WHERE im.id_inventario = %s
                """, (inventario_id,))
                inventario['materiales'] = cursor.fetchall()
                
                return inventario
                
    except Exception as e:
        logger.error(f"Error obteniendo inventario {inventario_id}: {e}")
        return None

def insert_inventario_safe(cantidad_inventario: int, materiales_ids=None, bodegas_ids=None):
    """Insertar nuevo inventario con relaciones"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Insertar inventario base
                cursor.execute("""
                    INSERT INTO INVENTARIOS (cantidad_inventario)
                    VALUES (%s)
                    RETURNING id_inventario
                """, (cantidad_inventario,))
                
                inventario_id = cursor.fetchone()[0]
                
                # Asociar materiales si se especifican
                if materiales_ids:
                    for material_id in materiales_ids:
                        cursor.execute("""
                            INSERT INTO INVENTARIO_MATERIAL (id_inventario, id_material)
                            VALUES (%s, %s)
                        """, (inventario_id, material_id))
                
                # Asociar bodegas si se especifican
                if bodegas_ids:
                    for bodega_id in bodegas_ids:
                        cursor.execute("""
                            INSERT INTO BODEGA_INVENTARIO (id_bodega, id_inventario)
                            VALUES (%s, %s)
                        """, (bodega_id, inventario_id))
                
                conn.commit()
                logger.info(f"Inventario creado: ID {inventario_id}")
                return inventario_id
                
    except Exception as e:
        logger.error(f"Error insertando inventario: {e}")
        return None

def update_inventario_safe(inventario_id: int, cantidad_inventario=None):
    """Actualizar inventario"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                if cantidad_inventario is not None:
                    cursor.execute("""
                        UPDATE INVENTARIOS 
                        SET cantidad_inventario = %s
                        WHERE id_inventario = %s
                    """, (cantidad_inventario, inventario_id))
                    
                    conn.commit()
                    logger.info(f"Inventario {inventario_id} actualizado")
                    return True
        return False
    except Exception as e:
        logger.error(f"Error actualizando inventario {inventario_id}: {e}")
        return False

def delete_inventario_safe(inventario_id: int):
    """Eliminar inventario (las relaciones se eliminan por CASCADE)"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM INVENTARIOS WHERE id_inventario = %s", (inventario_id,))
                conn.commit()
                logger.info(f"Inventario {inventario_id} eliminado")
                return True
    except Exception as e:
        logger.error(f"Error eliminando inventario {inventario_id}: {e}")
        return False

def asignar_materiales_inventario_safe(inventario_id: int, materiales_ids: list):
    """Asignar materiales a un inventario (reemplaza asignaciones existentes)"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Eliminar asignaciones existentes
                cursor.execute("DELETE FROM INVENTARIO_MATERIAL WHERE id_inventario = %s", (inventario_id,))
                
                # Agregar nuevas asignaciones
                for material_id in materiales_ids:
                    cursor.execute("""
                        INSERT INTO INVENTARIO_MATERIAL (id_inventario, id_material)
                        VALUES (%s, %s)
                    """, (inventario_id, material_id))
                
                conn.commit()
                logger.info(f"Materiales asignados a inventario {inventario_id}")
                return True
    except Exception as e:
        logger.error(f"Error asignando materiales a inventario {inventario_id}: {e}")
        return False

def asignar_bodegas_inventario_safe(inventario_id: int, bodegas_ids: list):
    """Asignar bodegas a un inventario (reemplaza asignaciones existentes)"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Eliminar asignaciones existentes
                cursor.execute("DELETE FROM BODEGA_INVENTARIO WHERE id_inventario = %s", (inventario_id,))
                
                # Agregar nuevas asignaciones
                for bodega_id in bodegas_ids:
                    cursor.execute("""
                        INSERT INTO BODEGA_INVENTARIO (id_bodega, id_inventario)
                        VALUES (%s, %s)
                    """, (bodega_id, inventario_id))
                
                conn.commit()
                logger.info(f"Bodegas asignadas a inventario {inventario_id}")
                return True
    except Exception as e:
        logger.error(f"Error asignando bodegas a inventario {inventario_id}: {e}")
        return False

# ===============================
# FUNCIONES PARA MÓDULO DE COMPRAS
# ===============================

def get_compras_safe():
    """Obtener todas las órdenes de compra (compras)"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT oc.*, p.nombre_proveedor, p.contacto_proveedor
                    FROM ORDENES_COMPRA oc
                    LEFT JOIN PROVEEDORES p ON oc.id_proveedor = p.id_proveedor
                    ORDER BY oc.fecha_orden DESC, oc.id_orden_compra DESC
                """)
                compras = cursor.fetchall()
                logger.info(f"Obtenidas {len(compras)} órdenes de compra")
                return compras
    except Exception as e:
        logger.error(f"Error obteniendo compras: {e}")
        return []

def get_compra_by_id_safe(compra_id: int):
    """Obtener orden de compra específica por ID"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT oc.*, p.nombre_proveedor, p.contacto_proveedor
                    FROM ORDENES_COMPRA oc
                    LEFT JOIN PROVEEDORES p ON oc.id_proveedor = p.id_proveedor
                    WHERE oc.id_orden_compra = %s
                """, (compra_id,))
                compra = cursor.fetchone()
                
                if compra:
                    logger.info(f"Obtenida compra {compra_id}")
                return compra
    except Exception as e:
        logger.error(f"Error obteniendo compra {compra_id}: {e}")
        return None

def insert_compra_safe(numero_orden, id_proveedor, fecha_entrega_solicitada=None, observaciones=None):
    """Insertar nueva orden de compra"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO ORDENES_COMPRA 
                    (numero_orden, id_proveedor, fecha_entrega_solicitada, observaciones)
                    VALUES (%s, %s, %s, %s) 
                    RETURNING id_orden_compra
                """, (numero_orden, id_proveedor, fecha_entrega_solicitada, observaciones))
                
                compra_id = cursor.fetchone()['id_orden_compra']
                conn.commit()
                
                logger.info(f"Orden de compra creada exitosamente: ID {compra_id}")
                return compra_id
    except Exception as e:
        logger.error(f"Error insertando compra: {e}")
        return None

def update_compra_safe(compra_id: int, numero_orden=None, id_proveedor=None, 
                      fecha_entrega_solicitada=None, fecha_entrega_real=None,
                      estado_orden=None, observaciones=None):
    """Actualizar orden de compra"""
    try:
        campos = []
        valores = []
        
        if numero_orden is not None:
            campos.append("numero_orden = %s")
            valores.append(numero_orden)
        if id_proveedor is not None:
            campos.append("id_proveedor = %s")
            valores.append(id_proveedor)
        if fecha_entrega_solicitada is not None:
            campos.append("fecha_entrega_solicitada = %s")
            valores.append(fecha_entrega_solicitada)
        if fecha_entrega_real is not None:
            campos.append("fecha_entrega_real = %s")
            valores.append(fecha_entrega_real)
        if estado_orden is not None:
            campos.append("estado_orden = %s")
            valores.append(estado_orden)
        if observaciones is not None:
            campos.append("observaciones = %s")
            valores.append(observaciones)
        
        if not campos:
            logger.warning(f"No hay campos para actualizar en compra {compra_id}")
            return True
        
        valores.append(compra_id)
        
        with get_connection() as conn:
            with conn.cursor() as cursor:
                consulta = f"UPDATE ORDENES_COMPRA SET {', '.join(campos)} WHERE id_orden_compra = %s"
                cursor.execute(consulta, valores)
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Compra {compra_id} actualizada exitosamente")
                    return True
                else:
                    logger.warning(f"Compra {compra_id} no encontrada para actualizar")
                    return False
    except Exception as e:
        logger.error(f"Error actualizando compra {compra_id}: {e}")
        return False

def delete_compra_safe(compra_id: int):
    """Eliminar orden de compra"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM ORDENES_COMPRA WHERE id_orden_compra = %s", (compra_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Compra {compra_id} eliminada exitosamente")
                    return True
                else:
                    logger.warning(f"Compra {compra_id} no encontrada para eliminar")
                    return False
    except Exception as e:
        logger.error(f"Error eliminando compra {compra_id}: {e}")
        return False

# ===============================
# FUNCIONES PARA MÓDULO DE PAGOS
# ===============================

def get_pagos_safe():
    """Obtener todos los pagos"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT p.*, mp.nombre_metodo
                    FROM PAGOS p
                    LEFT JOIN METODOS_PAGO mp ON p.id_metodo_pago = mp.id_metodo_pago
                    ORDER BY p.fecha_pago DESC, p.id_pago DESC
                """)
                pagos = cursor.fetchall()
                logger.info(f"Obtenidos {len(pagos)} pagos")
                return pagos
    except Exception as e:
        logger.error(f"Error obteniendo pagos: {e}")
        return []

def get_pago_by_id_safe(pago_id: int):
    """Obtener pago específico por ID"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT p.*, mp.nombre_metodo
                    FROM PAGOS p
                    LEFT JOIN METODOS_PAGO mp ON p.id_metodo_pago = mp.id_metodo_pago
                    WHERE p.id_pago = %s
                """, (pago_id,))
                pago = cursor.fetchone()
                
                if pago:
                    logger.info(f"Obtenido pago {pago_id}")
                return pago
    except Exception as e:
        logger.error(f"Error obteniendo pago {pago_id}: {e}")
        return None

def insert_pago_safe(numero_recibo, monto_pago, id_metodo_pago=None, referencia_pago=None, observaciones_pago=None):
    """Insertar nuevo pago"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO PAGOS 
                    (numero_recibo, monto_pago, id_metodo_pago, referencia_pago, observaciones_pago)
                    VALUES (%s, %s, %s, %s, %s) 
                    RETURNING id_pago
                """, (numero_recibo, monto_pago, id_metodo_pago, referencia_pago, observaciones_pago))
                
                pago_id = cursor.fetchone()['id_pago']
                conn.commit()
                
                logger.info(f"Pago creado exitosamente: ID {pago_id}")
                return pago_id
    except Exception as e:
        logger.error(f"Error insertando pago: {e}")
        return None

def update_pago_safe(pago_id: int, numero_recibo=None, monto_pago=None, 
                     id_metodo_pago=None, referencia_pago=None, 
                     observaciones_pago=None, estado_pago=None):
    """Actualizar pago"""
    try:
        campos = []
        valores = []
        
        if numero_recibo is not None:
            campos.append("numero_recibo = %s")
            valores.append(numero_recibo)
        if monto_pago is not None:
            campos.append("monto_pago = %s")
            valores.append(monto_pago)
        if id_metodo_pago is not None:
            campos.append("id_metodo_pago = %s")
            valores.append(id_metodo_pago)
        if referencia_pago is not None:
            campos.append("referencia_pago = %s")
            valores.append(referencia_pago)
        if observaciones_pago is not None:
            campos.append("observaciones_pago = %s")
            valores.append(observaciones_pago)
        if estado_pago is not None:
            campos.append("estado_pago = %s")
            valores.append(estado_pago)
        
        if not campos:
            logger.warning(f"No hay campos para actualizar en pago {pago_id}")
            return True
        
        valores.append(pago_id)
        
        with get_connection() as conn:
            with conn.cursor() as cursor:
                consulta = f"UPDATE PAGOS SET {', '.join(campos)} WHERE id_pago = %s"
                cursor.execute(consulta, valores)
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Pago {pago_id} actualizado exitosamente")
                    return True
                else:
                    logger.warning(f"Pago {pago_id} no encontrado para actualizar")
                    return False
    except Exception as e:
        logger.error(f"Error actualizando pago {pago_id}: {e}")
        return False

def delete_pago_safe(pago_id: int):
    """Eliminar pago"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM PAGOS WHERE id_pago = %s", (pago_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Pago {pago_id} eliminado exitosamente")
                    return True
                else:
                    logger.warning(f"Pago {pago_id} no encontrado para eliminar")
                    return False
    except Exception as e:
        logger.error(f"Error eliminando pago {pago_id}: {e}")
        return False

# ===============================
# FUNCIONES PARA MÓDULO DE NÓMINA
# ===============================

def get_nominas_safe():
    """Obtener todas las nóminas"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT n.*, e.nombre_empleado, e.apellido_empleado
                    FROM NOMINA n
                    LEFT JOIN EMPLEADOS e ON n.id_empleado = e.id_empleado
                    ORDER BY n.periodo_ano DESC, n.periodo_mes DESC, n.id_nomina DESC
                """)
                nominas = cursor.fetchall()
                logger.info(f"Obtenidas {len(nominas)} nóminas")
                return nominas
    except Exception as e:
        logger.error(f"Error obteniendo nóminas: {e}")
        return []

def get_nomina_by_id_safe(nomina_id: int):
    """Obtener nómina específica por ID"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT n.*, e.nombre_empleado, e.apellido_empleado, e.salario_empleado
                    FROM NOMINA n
                    LEFT JOIN EMPLEADOS e ON n.id_empleado = e.id_empleado
                    WHERE n.id_nomina = %s
                """, (nomina_id,))
                nomina = cursor.fetchone()
                
                if nomina:
                    logger.info(f"Obtenida nómina {nomina_id}")
                return nomina
    except Exception as e:
        logger.error(f"Error obteniendo nómina {nomina_id}: {e}")
        return None

def insert_nomina_safe(id_empleado, periodo_mes, periodo_ano, salario_base, 
                      horas_extras=0, valor_horas_extras=0, bonificaciones=0, deducciones=0):
    """Insertar nueva nómina"""
    try:
        # Calcular salario neto
        salario_neto = salario_base + valor_horas_extras + bonificaciones - deducciones
        
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO NOMINA 
                    (id_empleado, periodo_mes, periodo_ano, salario_base, horas_extras, 
                     valor_horas_extras, bonificaciones, deducciones, salario_neto)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    RETURNING id_nomina
                """, (id_empleado, periodo_mes, periodo_ano, salario_base, horas_extras,
                      valor_horas_extras, bonificaciones, deducciones, salario_neto))
                
                nomina_id = cursor.fetchone()['id_nomina']
                conn.commit()
                
                logger.info(f"Nómina creada exitosamente: ID {nomina_id}")
                return nomina_id
    except Exception as e:
        logger.error(f"Error insertando nómina: {e}")
        return None

def calcular_nomina_safe(id_empleado, periodo_mes, periodo_ano, horas_extras=0, bonificaciones=0, deducciones=0):
    """Calcular nómina automáticamente basada en salario del empleado"""
    try:
        # Obtener datos del empleado
        empleado = get_empleado_by_id_safe(id_empleado)
        if not empleado:
            logger.error(f"Empleado {id_empleado} no encontrado para calcular nómina")
            return None
        
        salario_base = float(empleado.get('salario_empleado', 0))
        valor_horas_extras = horas_extras * (salario_base / 160) * 1.25  # 25% extra por hora extra
        
        return insert_nomina_safe(
            id_empleado=id_empleado,
            periodo_mes=periodo_mes,
            periodo_ano=periodo_ano,
            salario_base=salario_base,
            horas_extras=horas_extras,
            valor_horas_extras=valor_horas_extras,
            bonificaciones=bonificaciones,
            deducciones=deducciones
        )
    except Exception as e:
        logger.error(f"Error calculando nómina: {e}")
        return None

def update_nomina_safe(nomina_id: int, salario_base=None, horas_extras=None, 
                      valor_horas_extras=None, bonificaciones=None, deducciones=None,
                      fecha_pago=None, estado_nomina=None, observaciones_nomina=None):
    """Actualizar nómina"""
    try:
        campos = []
        valores = []
        
        if salario_base is not None:
            campos.append("salario_base = %s")
            valores.append(salario_base)
        if horas_extras is not None:
            campos.append("horas_extras = %s")
            valores.append(horas_extras)
        if valor_horas_extras is not None:
            campos.append("valor_horas_extras = %s")
            valores.append(valor_horas_extras)
        if bonificaciones is not None:
            campos.append("bonificaciones = %s")
            valores.append(bonificaciones)
        if deducciones is not None:
            campos.append("deducciones = %s")
            valores.append(deducciones)
        if fecha_pago is not None:
            campos.append("fecha_pago = %s")
            valores.append(fecha_pago)
        if estado_nomina is not None:
            campos.append("estado_nomina = %s")
            valores.append(estado_nomina)
        if observaciones_nomina is not None:
            campos.append("observaciones_nomina = %s")
            valores.append(observaciones_nomina)
        
        # Recalcular salario neto si hay cambios en componentes salariales
        if any(x is not None for x in [salario_base, valor_horas_extras, bonificaciones, deducciones]):
            # Obtener valores actuales
            nomina_actual = get_nomina_by_id_safe(nomina_id)
            if nomina_actual:
                nuevo_base = salario_base if salario_base is not None else float(nomina_actual['salario_base'])
                nuevo_extras = valor_horas_extras if valor_horas_extras is not None else float(nomina_actual['valor_horas_extras'])
                nuevas_bonif = bonificaciones if bonificaciones is not None else float(nomina_actual['bonificaciones'])
                nuevas_deduc = deducciones if deducciones is not None else float(nomina_actual['deducciones'])
                
                nuevo_neto = nuevo_base + nuevo_extras + nuevas_bonif - nuevas_deduc
                campos.append("salario_neto = %s")
                valores.append(nuevo_neto)
        
        if not campos:
            logger.warning(f"No hay campos para actualizar en nómina {nomina_id}")
            return True
        
        valores.append(nomina_id)
        
        with get_connection() as conn:
            with conn.cursor() as cursor:
                consulta = f"UPDATE NOMINA SET {', '.join(campos)} WHERE id_nomina = %s"
                cursor.execute(consulta, valores)
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Nómina {nomina_id} actualizada exitosamente")
                    return True
                else:
                    logger.warning(f"Nómina {nomina_id} no encontrada para actualizar")
                    return False
    except Exception as e:
        logger.error(f"Error actualizando nómina {nomina_id}: {e}")
        return False

def delete_nomina_safe(nomina_id: int):
    """Eliminar nómina"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM NOMINA WHERE id_nomina = %s", (nomina_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    logger.info(f"Nómina {nomina_id} eliminada exitosamente")
                    return True
                else:
                    logger.warning(f"Nómina {nomina_id} no encontrada para eliminar")
                    return False
    except Exception as e:
        logger.error(f"Error eliminando nómina {nomina_id}: {e}")
        return False

# Probar conexión manualmente ejecutando database.test_connection() desde un script o desde __main__
if __name__ == '__main__':
    test_connection()