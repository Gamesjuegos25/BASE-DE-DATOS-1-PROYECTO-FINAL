# Extensión de funciones para las 30 nuevas tablas
# Este archivo se añadirá al final de database.py

# =====================================================
# MÓDULO FACTURACIÓN Y PAGOS
# =====================================================

def obtener_facturas():
    """Obtiene todas las facturas"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT f.*, c.nombre as nombre_cliente
            FROM FACTURAS f
            LEFT JOIN CLIENTES c ON f.id_cliente = c.id_cliente
            ORDER BY f.fecha_factura DESC
        """)
        facturas = cursor.fetchall()
        conn.close()
        return facturas
    except Exception as e:
        print(f"Error al obtener facturas: {e}")
        return []

def crear_factura(numero_factura, fecha_factura, fecha_vencimiento, 
                  subtotal, impuestos, descuento, total, id_cliente, observaciones=""):
    """Crea una nueva factura"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO FACTURAS (numero_factura, fecha_factura, fecha_vencimiento,
                                subtotal, impuestos, descuento, total, id_cliente, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_factura
        """, (numero_factura, fecha_factura, fecha_vencimiento, 
              subtotal, impuestos, descuento, total, id_cliente, observaciones))
        id_factura = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id_factura
    except Exception as e:
        print(f"Error al crear factura: {e}")
        return None

def obtener_detalle_factura(id_factura):
    """Obtiene el detalle de una factura específica"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM DETALLES_FACTURA
            WHERE id_factura = %s
            ORDER BY id_detalle_factura
        """, (id_factura,))
        detalles = cursor.fetchall()
        conn.close()
        return detalles
    except Exception as e:
        print(f"Error al obtener detalle de factura: {e}")
        return []

def crear_detalle_factura(id_factura, concepto, descripcion, cantidad, 
                         precio_unitario, subtotal_linea, impuesto_linea, total_linea):
    """Crea un detalle de factura"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO DETALLES_FACTURA (id_factura, concepto, descripcion, cantidad,
                                        precio_unitario, subtotal_linea, impuesto_linea, total_linea)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (id_factura, concepto, descripcion, cantidad, 
              precio_unitario, subtotal_linea, impuesto_linea, total_linea))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al crear detalle de factura: {e}")
        return False

def obtener_metodos_pago():
    """Obtiene todos los métodos de pago activos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM METODOS_PAGO WHERE activo = true ORDER BY nombre_metodo")
        metodos = cursor.fetchall()
        conn.close()
        return metodos
    except Exception as e:
        print(f"Error al obtener métodos de pago: {e}")
        return []

def crear_pago(numero_recibo, fecha_pago, monto_pago, id_metodo_pago, 
               referencia_pago="", observaciones_pago=""):
    """Crea un nuevo pago"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PAGOS (numero_recibo, fecha_pago, monto_pago, id_metodo_pago,
                              referencia_pago, observaciones_pago)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_pago
        """, (numero_recibo, fecha_pago, monto_pago, id_metodo_pago, 
              referencia_pago, observaciones_pago))
        id_pago = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id_pago
    except Exception as e:
        print(f"Error al crear pago: {e}")
        return None

def obtener_cuentas_por_cobrar():
    """Obtiene todas las cuentas por cobrar pendientes"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT cc.*, f.numero_factura, c.nombre as nombre_cliente
            FROM CUENTAS_COBRAR cc
            JOIN FACTURAS f ON cc.id_factura = f.id_factura
            JOIN CLIENTES c ON f.id_cliente = c.id_cliente
            WHERE cc.monto_pendiente > 0
            ORDER BY cc.fecha_vencimiento
        """)
        cuentas = cursor.fetchall()
        conn.close()
        return cuentas
    except Exception as e:
        print(f"Error al obtener cuentas por cobrar: {e}")
        return []

# =====================================================
# MÓDULO CONTABILIDAD AVANZADA
# =====================================================

def obtener_cuentas_contables():
    """Obtiene todas las cuentas contables"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM CUENTAS_CONTABLES
            WHERE activa = true
            ORDER BY codigo_cuenta
        """)
        cuentas = cursor.fetchall()
        conn.close()
        return cuentas
    except Exception as e:
        print(f"Error al obtener cuentas contables: {e}")
        return []

def crear_movimiento_contable(numero_asiento, fecha_movimiento, id_cuenta, 
                             debe, haber, concepto, documento_soporte="", id_obra=None):
    """Crea un movimiento contable"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO MOVIMIENTOS_CONTABLES (numero_asiento, fecha_movimiento, id_cuenta,
                                             debe, haber, concepto, documento_soporte, id_obra)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (numero_asiento, fecha_movimiento, id_cuenta, 
              debe, haber, concepto, documento_soporte, id_obra))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al crear movimiento contable: {e}")
        return False

def obtener_gastos_obra(id_obra=None):
    """Obtiene gastos de obras"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
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
        gastos = cursor.fetchall()
        conn.close()
        return gastos
    except Exception as e:
        print(f"Error al obtener gastos de obra: {e}")
        return []

def obtener_flujo_caja(fecha_inicio=None, fecha_fin=None):
    """Obtiene el flujo de caja"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM FLUJO_CAJA"
        params = []
        
        if fecha_inicio and fecha_fin:
            query += " WHERE fecha_flujo BETWEEN %s AND %s"
            params = [fecha_inicio, fecha_fin]
        
        query += " ORDER BY fecha_flujo DESC"
        cursor.execute(query, params)
        flujo = cursor.fetchall()
        conn.close()
        return flujo
    except Exception as e:
        print(f"Error al obtener flujo de caja: {e}")
        return []

# =====================================================
# MÓDULO MANTENIMIENTO
# =====================================================

def obtener_mantenimientos():
    """Obtiene todos los mantenimientos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT m.*, 
                   e.nombre as nombre_equipo,
                   v.marca as marca_vehiculo, v.modelo as modelo_vehiculo
            FROM MANTENIMIENTOS m
            LEFT JOIN EQUIPOS e ON m.id_equipo = e.id_equipo
            LEFT JOIN VEHICULOS v ON m.id_vehiculo = v.id_vehiculo
            ORDER BY m.fecha_programada DESC
        """)
        mantenimientos = cursor.fetchall()
        conn.close()
        return mantenimientos
    except Exception as e:
        print(f"Error al obtener mantenimientos: {e}")
        return []

def crear_mantenimiento(id_equipo, id_vehiculo, tipo_mantenimiento, descripcion_mantenimiento,
                       fecha_programada, costo_estimado, responsable_mantenimiento):
    """Crea un nuevo mantenimiento"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO MANTENIMIENTOS (id_equipo, id_vehiculo, tipo_mantenimiento,
                                      descripcion_mantenimiento, fecha_programada,
                                      costo_estimado, responsable_mantenimiento)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_mantenimiento
        """, (id_equipo, id_vehiculo, tipo_mantenimiento, descripcion_mantenimiento,
              fecha_programada, costo_estimado, responsable_mantenimiento))
        id_mantenimiento = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id_mantenimiento
    except Exception as e:
        print(f"Error al crear mantenimiento: {e}")
        return None

def obtener_repuestos():
    """Obtiene todos los repuestos"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
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
        repuestos = cursor.fetchall()
        conn.close()
        return repuestos
    except Exception as e:
        print(f"Error al obtener repuestos: {e}")
        return []

def crear_orden_trabajo(numero_orden, id_mantenimiento, descripcion_trabajo,
                       prioridad, asignado_a, tiempo_estimado):
    """Crea una nueva orden de trabajo"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ORDENES_TRABAJO (numero_orden, id_mantenimiento, descripcion_trabajo,
                                       prioridad, asignado_a, tiempo_estimado)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_orden_trabajo
        """, (numero_orden, id_mantenimiento, descripcion_trabajo,
              prioridad, asignado_a, tiempo_estimado))
        id_orden = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id_orden
    except Exception as e:
        print(f"Error al crear orden de trabajo: {e}")
        return None

# =====================================================
# MÓDULO COMPRAS EXTENDIDO
# =====================================================

def obtener_ordenes_compra():
    """Obtiene todas las órdenes de compra"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT oc.*, p.nombre as nombre_proveedor
            FROM ORDENES_COMPRA oc
            JOIN PROVEEDORES p ON oc.id_proveedor = p.id_proveedor
            ORDER BY oc.fecha_orden DESC
        """)
        ordenes = cursor.fetchall()
        conn.close()
        return ordenes
    except Exception as e:
        print(f"Error al obtener órdenes de compra: {e}")
        return []

def crear_orden_compra(numero_orden, id_proveedor, fecha_entrega_solicitada,
                      subtotal, impuestos, total, observaciones=""):
    """Crea una nueva orden de compra"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ORDENES_COMPRA (numero_orden, id_proveedor, fecha_entrega_solicitada,
                                      subtotal, impuestos, total, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_orden_compra
        """, (numero_orden, id_proveedor, fecha_entrega_solicitada,
              subtotal, impuestos, total, observaciones))
        id_orden = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id_orden
    except Exception as e:
        print(f"Error al crear orden de compra: {e}")
        return None

def obtener_evaluaciones_proveedores():
    """Obtiene evaluaciones de proveedores"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT ep.*, p.nombre as nombre_proveedor
            FROM EVALUACION_PROVEEDORES ep
            JOIN PROVEEDORES p ON ep.id_proveedor = p.id_proveedor
            ORDER BY ep.fecha_evaluacion DESC
        """)
        evaluaciones = cursor.fetchall()
        conn.close()
        return evaluaciones
    except Exception as e:
        print(f"Error al obtener evaluaciones de proveedores: {e}")
        return []

# =====================================================
# MÓDULO NÓMINA EXTENDIDO
# =====================================================

def obtener_nomina(periodo_mes=None, periodo_ano=None):
    """Obtiene registros de nómina"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
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
        nomina = cursor.fetchall()
        conn.close()
        return nomina
    except Exception as e:
        print(f"Error al obtener nómina: {e}")
        return []

def crear_registro_nomina(id_empleado, periodo_mes, periodo_ano, salario_base,
                         horas_extras, valor_horas_extras, bonificaciones, deducciones, salario_neto):
    """Crea un registro de nómina"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO NOMINA (id_empleado, periodo_mes, periodo_ano, salario_base,
                              horas_extras, valor_horas_extras, bonificaciones, deducciones, salario_neto)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (id_empleado, periodo_mes, periodo_ano, salario_base,
              horas_extras, valor_horas_extras, bonificaciones, deducciones, salario_neto))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al crear registro de nómina: {e}")
        return False

def obtener_asistencia(id_empleado=None, fecha_inicio=None, fecha_fin=None):
    """Obtiene registros de asistencia"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
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
        asistencia = cursor.fetchall()
        conn.close()
        return asistencia
    except Exception as e:
        print(f"Error al obtener asistencia: {e}")
        return []

def obtener_capacitaciones():
    """Obtiene todas las capacitaciones"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT c.*,
                   COUNT(ec.id_empleado) as empleados_inscritos
            FROM CAPACITACIONES c
            LEFT JOIN EMPLEADO_CAPACITACION ec ON c.id_capacitacion = ec.id_capacitacion
            GROUP BY c.id_capacitacion
            ORDER BY c.fecha_inicio DESC
        """)
        capacitaciones = cursor.fetchall()
        conn.close()
        return capacitaciones
    except Exception as e:
        print(f"Error al obtener capacitaciones: {e}")
        return []

# =====================================================
# MÓDULO REPORTES AVANZADOS
# =====================================================

def obtener_metricas_kpi():
    """Obtiene todas las métricas KPI"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
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
        metricas = cursor.fetchall()
        conn.close()
        return metricas
    except Exception as e:
        print(f"Error al obtener métricas KPI: {e}")
        return []

def obtener_alertas_sistema(id_usuario=None, solo_no_leidas=False):
    """Obtiene alertas del sistema"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
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
        alertas = cursor.fetchall()
        conn.close()
        return alertas
    except Exception as e:
        print(f"Error al obtener alertas del sistema: {e}")
        return []

def crear_alerta_sistema(tipo_alerta, titulo_alerta, mensaje_alerta, nivel_prioridad,
                        id_usuario_destinatario, fecha_vencimiento=None):
    """Crea una nueva alerta del sistema"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ALERTAS_SISTEMA (tipo_alerta, titulo_alerta, mensaje_alerta,
                                       nivel_prioridad, id_usuario_destinatario, fecha_vencimiento)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_alerta
        """, (tipo_alerta, titulo_alerta, mensaje_alerta, nivel_prioridad,
              id_usuario_destinatario, fecha_vencimiento))
        id_alerta = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        return id_alerta
    except Exception as e:
        print(f"Error al crear alerta del sistema: {e}")
        return None

# =====================================================
# FUNCIONES DE UTILIDAD PARA EL SISTEMA COMPLETO
# =====================================================

def obtener_dashboard_completo():
    """Obtiene datos para el dashboard principal con métricas del sistema completo"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
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
        dashboard['finanzas'] = finanzas
        
        # Métricas de obras
        cursor.execute("""
            SELECT 
                COUNT(*) as total_obras,
                COUNT(CASE WHEN estado = 'En Progreso' THEN 1 END) as obras_activas,
                COUNT(CASE WHEN estado = 'Completado' THEN 1 END) as obras_completadas
            FROM OBRAS
        """)
        obras = cursor.fetchone()
        dashboard['obras'] = obras
        
        # Métricas de mantenimiento
        cursor.execute("""
            SELECT 
                COUNT(*) as total_mantenimientos,
                COUNT(CASE WHEN estado_mantenimiento = 'Programado' THEN 1 END) as programados,
                COUNT(CASE WHEN estado_mantenimiento = 'Realizado' THEN 1 END) as realizados
            FROM MANTENIMIENTOS
        """)
        mantenimiento = cursor.fetchone()
        dashboard['mantenimiento'] = mantenimiento
        
        # Alertas pendientes
        cursor.execute("""
            SELECT COUNT(*) as alertas_pendientes
            FROM ALERTAS_SISTEMA
            WHERE leida = false
        """)
        alertas = cursor.fetchone()
        dashboard['alertas_pendientes'] = alertas['alertas_pendientes'] if alertas else 0
        
        conn.close()
        return dashboard
    except Exception as e:
        print(f"Error al obtener dashboard completo: {e}")
        return {}

def buscar_global(termino_busqueda):
    """Búsqueda global en todo el sistema"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        resultados = {
            'clientes': [],
            'obras': [],
            'empleados': [],
            'facturas': [],
            'proveedores': []
        }
        
        # Buscar en clientes
        cursor.execute("""
            SELECT 'cliente' as tipo, id_cliente as id, nombre, telefono
            FROM CLIENTES
            WHERE nombre ILIKE %s OR telefono ILIKE %s
            LIMIT 5
        """, (f'%{termino_busqueda}%', f'%{termino_busqueda}%'))
        resultados['clientes'] = cursor.fetchall()
        
        # Buscar en obras
        cursor.execute("""
            SELECT 'obra' as tipo, id_obra as id, nombre, ubicacion
            FROM OBRAS
            WHERE nombre ILIKE %s OR ubicacion ILIKE %s
            LIMIT 5
        """, (f'%{termino_busqueda}%', f'%{termino_busqueda}%'))
        resultados['obras'] = cursor.fetchall()
        
        # Buscar en empleados
        cursor.execute("""
            SELECT 'empleado' as tipo, id_empleado as id, nombre, cargo
            FROM EMPLEADOS
            WHERE nombre ILIKE %s OR cargo ILIKE %s
            LIMIT 5
        """, (f'%{termino_busqueda}%', f'%{termino_busqueda}%'))
        resultados['empleados'] = cursor.fetchall()
        
        # Buscar en facturas
        cursor.execute("""
            SELECT 'factura' as tipo, id_factura as id, numero_factura as nombre, 
                   CAST(total as VARCHAR) as detalle
            FROM FACTURAS
            WHERE numero_factura ILIKE %s
            LIMIT 5
        """, (f'%{termino_busqueda}%',))
        resultados['facturas'] = cursor.fetchall()
        
        conn.close()
        return resultados
    except Exception as e:
        print(f"Error en búsqueda global: {e}")
        return {}