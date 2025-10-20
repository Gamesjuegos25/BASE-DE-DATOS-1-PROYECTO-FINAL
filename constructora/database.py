# database_clean.py - Conexión PostgreSQL simplificada con manejo UTF-8
import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor
import os
import logging

logger = logging.getLogger(__name__)

# Configuración de conexión
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '123'),
    'database': os.getenv('DB_NAME', 'PROYECTO_FINAL_BD1'),
    'client_encoding': 'LATIN1'  # LATIN1 funciona mejor que UTF8 para esta BD
}

def get_connection():
    """Obtener conexión a PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)

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
# CONSULTAS SEGURAS PARA OBRAS
# ===============================
def get_obras_safe():
    """Obtener obras de forma segura manejando errores UTF-8"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        o.id_obra,
                        CASE 
                            WHEN o.nombre_obra IS NULL THEN 'Sin nombre'
                            WHEN LENGTH(TRIM(o.nombre_obra)) = 0 THEN 'Sin nombre'
                            ELSE REPLACE(REPLACE(REPLACE(TRIM(o.nombre_obra), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                        END as nombre,
                        CASE 
                            WHEN o.descripcion_obra IS NULL THEN ''
                            ELSE REPLACE(REPLACE(REPLACE(TRIM(o.descripcion_obra), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                        END as descripcion,
                        CASE 
                            WHEN o.ubicacion_obra IS NULL THEN ''
                            ELSE REPLACE(REPLACE(REPLACE(TRIM(o.ubicacion_obra), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                        END as ubicacion,
                        o.fecha_inicio,
                        o.fecha_fin,
                        o.valor_obra as valor,
                        COALESCE(o.estado_obra, 'Sin estado') as estado,
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

def insert_obra_safe(nombre, descripcion=None, ubicacion=None, fecha_inicio=None, fecha_fin=None, valor=None, estado='Planeación', cliente_id=None):
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
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    # Verificar que el cliente existe
                    cursor.execute("SELECT id_cliente FROM CLIENTES WHERE id_cliente = %s", (cliente_id,))
                    if not cursor.fetchone():
                        raise ValueError(f"El cliente con ID {cliente_id} no existe")
                    
                    # Insertar obra
                    cursor.execute("""
                        INSERT INTO OBRAS (nombre_obra, descripcion_obra, ubicacion_obra, fecha_inicio, fecha_fin, valor_obra, estado_obra, id_cliente)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_obra
                    """, (nombre_clean, descripcion_clean, ubicacion_clean, fecha_inicio, fecha_fin, valor, estado, cliente_id))
                    
                    obra_id = cursor.fetchone()['id_obra']
                    conn.commit()
                    
                    logger.info(f"Obra creada exitosamente: ID {obra_id} para cliente {cliente_id}")
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
                        CASE 
                            WHEN nombre_empleado IS NULL THEN 'Sin nombre'
                            ELSE REPLACE(REPLACE(REPLACE(TRIM(nombre_empleado), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                        END as nombre,
                        tipo_empleado as tipo,
                        salario_fijo_empleado as salario
                    FROM EMPLEADOS 
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

def insert_empleado_safe(nombre, tipo=None, salario=None):
    """Insertar empleado de forma segura"""
    try:
        nombre_clean = str(nombre).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('ñ', 'n')
        
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO EMPLEADOS (nombre_empleado, tipo_empleado, salario_fijo_empleado)
                    VALUES (%s, %s, %s) RETURNING id_empleado
                """, (nombre_clean, tipo, salario))
                
                empleado_id = cursor.fetchone()['id_empleado']
                conn.commit()
                
                logger.info(f"Empleado creado: ID {empleado_id}")
                return empleado_id
                
    except Exception as e:
        logger.error(f"Error insertando empleado: {e}")
        return None

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

# ===============================
# CONSULTAS SEGURAS PARA MATERIALES
# ===============================
def get_materiales_safe():
    """Obtener materiales de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        id_material,
                        CASE 
                            WHEN nombre_material IS NULL THEN 'Sin nombre'
                            ELSE REPLACE(REPLACE(REPLACE(TRIM(nombre_material), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                        END as nombre,
                        unidad_material as unidad,
                        precio_unitario_material as precio
                    FROM MATERIALES 
                    ORDER BY nombre_material
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
                        placa_vehiculo as placa,
                        estado_vehiculo as estado,
                        tipo_vehiculo as tipo
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

# ===============================
# CONSULTAS SEGURAS PARA ÁREAS
# ===============================
def get_areas_safe():
    """Obtener áreas de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        id_area,
                        CASE 
                            WHEN nombre_area IS NULL THEN 'Sin nombre'
                            ELSE REPLACE(REPLACE(REPLACE(TRIM(nombre_area), 'ó', 'o'), 'á', 'a'), 'é', 'e')
                        END as nombre
                    FROM AREAS 
                    ORDER BY nombre_area
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
        logger.error(f"Error obteniendo áreas: {e}")
        return []

def insert_area_safe(nombre):
    """Insertar área de forma segura"""
    try:
        nombre_clean = str(nombre).replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('ñ', 'n')
        
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    INSERT INTO AREAS (nombre_area)
                    VALUES (%s) RETURNING id_area
                """, (nombre_clean,))
                
                area_id = cursor.fetchone()['id_area']
                conn.commit()
                
                logger.info(f"Área creada: ID {area_id}")
                return area_id
                
    except Exception as e:
        logger.error(f"Error insertando área: {e}")
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
    """Obtener actividades de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        id_actividad,
                        nombre_actividad,
                        descripcion_actividad,
                        fecha_programada_actividad
                    FROM ACTIVIDADES
                    ORDER BY fecha_programada_actividad DESC
                    LIMIT 50
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo actividades: {e}")
        return []

def insert_actividad_safe(nombre, descripcion=None, fecha_programada=None):
    """Insertar nueva actividad"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO ACTIVIDADES (nombre_actividad, descripcion_actividad, fecha_programada_actividad)
                    VALUES (%s, %s, %s) RETURNING id_actividad
                """, (nombre, descripcion, fecha_programada))
                return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Error insertando actividad: {e}")
        return None

# BITACORAS
def get_bitacoras_safe():
    """Obtener bitácoras de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        b.id_bitacora,
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

# AUDITORIAS
def get_auditorias_safe():
    """Obtener auditorías de forma segura"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        a.id_auditoria,
                        a.accion_auditoria,
                        a.fecha_auditoria,
                        a.detalle_auditoria,
                        u.nombre_usuario
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

def insert_contrato_safe(fecha_inicio, fecha_fin=None, tipo_pago=None, obra_id=None):
    """Insertar nuevo contrato"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO CONTRATOS (fecha_inicio_contrato, fecha_fin_contrato, tipo_pago_contrato)
                    VALUES (%s, %s, %s) RETURNING id_contrato
                """, (fecha_inicio, fecha_fin, tipo_pago))
                contrato_id = cursor.fetchone()[0]
                
                # Asociar con obra si se especifica
                if obra_id:
                    cursor.execute("""
                        INSERT INTO CONTRATO_OBRA (id_contrato, id_obra) VALUES (%s, %s)
                    """, (contrato_id, obra_id))
                
                return contrato_id
    except Exception as e:
        logger.error(f"Error insertando contrato: {e}")
        return None

# PRESUPUESTOS
def get_presupuestos_safe():
    """Obtener presupuestos de obra"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        p.id_presupuesto,
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
                cursor.execute("""
                    INSERT INTO PRESUPUESTOS_OBRA (monto_estimado_presupuesto, fecha_presupuesto)
                    VALUES (%s, COALESCE(%s, CURRENT_DATE)) RETURNING id_presupuesto
                """, (monto_estimado, fecha_presupuesto))
                presupuesto_id = cursor.fetchone()[0]
                
                # Asociar con obra si se especifica
                if obra_id:
                    cursor.execute("""
                        INSERT INTO OBRA_PRESUPUESTO (id_obra, id_presupuesto) VALUES (%s, %s)
                    """, (obra_id, presupuesto_id))
                
                return presupuesto_id
    except Exception as e:
        logger.error(f"Error insertando presupuesto: {e}")
        return None

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
                return cursor.fetchall()
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

# REQUISICIONES Y MOVIMIENTOS
def get_requisiciones_safe():
    """Obtener requisiciones de materiales"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        r.id_requisicion,
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

def get_movimientos_materiales_safe():
    """Obtener movimientos de materiales"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        mm.id_movimiento_material,
                        mm.tipo_movimiento,
                        mm.fecha_movimiento,
                        mm.origen_movimiento,
                        mm.destino_movimiento,
                        m.nombre_material
                    FROM MOVIMIENTOS_MATERIAL mm
                    LEFT JOIN MATERIAL_MOVIMIENTO mat_mov ON mm.id_movimiento_material = mat_mov.id_movimiento_material
                    LEFT JOIN MATERIALES m ON mat_mov.id_material = m.id_material
                    ORDER BY mm.fecha_movimiento DESC
                    LIMIT 50
                """)
                return cursor.fetchall()
    except Exception as e:
        logger.error(f"Error obteniendo movimientos: {e}")
        return []

# TRABAJOS Y DETALLES
def get_trabajos_safe():
    """Obtener trabajos disponibles"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT 
                        t.id_trabajo,
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

# Probar conexión al importar
test_connection()