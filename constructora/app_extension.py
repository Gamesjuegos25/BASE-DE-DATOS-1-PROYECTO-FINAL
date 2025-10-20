# Extensión de rutas para app.py - Sistema Completo 86 Tablas
# Este código se añadirá al archivo app.py existente

# =====================================================
# RUTAS MÓDULO FACTURACIÓN Y PAGOS
# =====================================================

@app.route('/facturas')
def facturas():
    """Lista todas las facturas"""
    facturas = obtener_facturas()
    return render_template('facturas/listar.html', facturas=facturas)

@app.route('/facturas/crear', methods=['GET', 'POST'])
def crear_factura_route():
    """Crear nueva factura"""
    if request.method == 'POST':
        data = request.get_json()
        id_factura = crear_factura(
            data['numero_factura'],
            data['fecha_factura'],
            data['fecha_vencimiento'],
            data['subtotal'],
            data['impuestos'],
            data['descuento'],
            data['total'],
            data['id_cliente'],
            data.get('observaciones', '')
        )
        if id_factura:
            return jsonify({'success': True, 'id_factura': id_factura})
        return jsonify({'success': False})
    
    clientes = obtener_clientes()
    return render_template('facturas/crear.html', clientes=clientes)

@app.route('/facturas/<int:id_factura>/detalle')
def detalle_factura(id_factura):
    """Ver detalle de factura"""
    detalles = obtener_detalle_factura(id_factura)
    return render_template('facturas/detalle.html', detalles=detalles, id_factura=id_factura)

@app.route('/pagos')
def pagos():
    """Lista todos los pagos"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT p.*, mp.nombre_metodo
                    FROM PAGOS p
                    LEFT JOIN METODOS_PAGO mp ON p.id_metodo_pago = mp.id_metodo_pago
                    ORDER BY p.fecha_pago DESC
                """)
                pagos = cursor.fetchall()
    except Exception as e:
        pagos = []
    
    return render_template('pagos/listar.html', pagos=pagos)

@app.route('/pagos/crear', methods=['GET', 'POST'])
def crear_pago_route():
    """Crear nuevo pago"""
    if request.method == 'POST':
        data = request.get_json()
        id_pago = crear_pago(
            data['numero_recibo'],
            data['fecha_pago'],
            data['monto_pago'],
            data['id_metodo_pago'],
            data.get('referencia_pago', ''),
            data.get('observaciones_pago', '')
        )
        if id_pago:
            return jsonify({'success': True, 'id_pago': id_pago})
        return jsonify({'success': False})
    
    metodos_pago = obtener_metodos_pago()
    return render_template('pagos/crear.html', metodos_pago=metodos_pago)

@app.route('/cuentas-por-cobrar')
def cuentas_por_cobrar():
    """Lista cuentas por cobrar"""
    cuentas = obtener_cuentas_por_cobrar()
    return render_template('cuentas_cobrar/listar.html', cuentas=cuentas)

# =====================================================
# RUTAS MÓDULO CONTABILIDAD AVANZADA
# =====================================================

@app.route('/contabilidad')
def contabilidad_dashboard():
    """Dashboard de contabilidad"""
    cuentas = obtener_cuentas_contables()
    flujo_caja = obtener_flujo_caja()
    gastos_obra = obtener_gastos_obra()
    
    return render_template('contabilidad/dashboard.html', 
                         cuentas=cuentas, 
                         flujo_caja=flujo_caja[:10],  # Últimos 10 registros
                         gastos_obra=gastos_obra[:10])

@app.route('/contabilidad/cuentas')
def cuentas_contables():
    """Lista cuentas contables"""
    cuentas = obtener_cuentas_contables()
    return render_template('contabilidad/cuentas.html', cuentas=cuentas)

@app.route('/contabilidad/gastos-obra')
def gastos_obra_route():
    """Lista gastos de obra"""
    id_obra = request.args.get('id_obra')
    gastos = obtener_gastos_obra(id_obra)
    obras = obtener_obras()
    return render_template('contabilidad/gastos_obra.html', gastos=gastos, obras=obras)

@app.route('/contabilidad/flujo-caja')
def flujo_caja_route():
    """Flujo de caja"""
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    flujo = obtener_flujo_caja(fecha_inicio, fecha_fin)
    return render_template('contabilidad/flujo_caja.html', flujo=flujo)

# =====================================================
# RUTAS MÓDULO MANTENIMIENTO
# =====================================================

@app.route('/mantenimiento')
def mantenimiento_dashboard():
    """Dashboard de mantenimiento"""
    mantenimientos = obtener_mantenimientos()
    repuestos = obtener_repuestos()
    
    # Estadísticas
    total_mantenimientos = len(mantenimientos)
    programados = len([m for m in mantenimientos if m.get('estado_mantenimiento') == 'Programado'])
    repuestos_bajo_stock = len([r for r in repuestos if r.get('estado_stock') == 'Bajo Stock'])
    
    return render_template('mantenimiento/dashboard.html',
                         mantenimientos=mantenimientos[:10],
                         repuestos=repuestos[:10],
                         total_mantenimientos=total_mantenimientos,
                         programados=programados,
                         repuestos_bajo_stock=repuestos_bajo_stock)

@app.route('/mantenimiento/mantenimientos')
def mantenimientos_lista():
    """Lista todos los mantenimientos"""
    mantenimientos = obtener_mantenimientos()
    return render_template('mantenimiento/listar.html', mantenimientos=mantenimientos)

@app.route('/mantenimiento/crear', methods=['GET', 'POST'])
def crear_mantenimiento_route():
    """Crear nuevo mantenimiento"""
    if request.method == 'POST':
        data = request.get_json()
        id_mantenimiento = crear_mantenimiento(
            data.get('id_equipo'),
            data.get('id_vehiculo'),
            data['tipo_mantenimiento'],
            data['descripcion_mantenimiento'],
            data['fecha_programada'],
            data.get('costo_estimado'),
            data.get('responsable_mantenimiento', '')
        )
        if id_mantenimiento:
            return jsonify({'success': True, 'id_mantenimiento': id_mantenimiento})
        return jsonify({'success': False})
    
    equipos = obtener_equipos()
    vehiculos = obtener_vehiculos()
    return render_template('mantenimiento/crear.html', equipos=equipos, vehiculos=vehiculos)

@app.route('/mantenimiento/repuestos')
def repuestos_lista():
    """Lista todos los repuestos"""
    repuestos = obtener_repuestos()
    return render_template('mantenimiento/repuestos.html', repuestos=repuestos)

# =====================================================
# RUTAS MÓDULO COMPRAS EXTENDIDO
# =====================================================

@app.route('/compras/ordenes')
def ordenes_compra():
    """Lista órdenes de compra"""
    ordenes = obtener_ordenes_compra()
    return render_template('compras/ordenes.html', ordenes=ordenes)

@app.route('/compras/ordenes/crear', methods=['GET', 'POST'])
def crear_orden_compra_route():
    """Crear nueva orden de compra"""
    if request.method == 'POST':
        data = request.get_json()
        id_orden = crear_orden_compra(
            data['numero_orden'],
            data['id_proveedor'],
            data['fecha_entrega_solicitada'],
            data['subtotal'],
            data['impuestos'],
            data['total'],
            data.get('observaciones', '')
        )
        if id_orden:
            return jsonify({'success': True, 'id_orden_compra': id_orden})
        return jsonify({'success': False})
    
    proveedores = obtener_proveedores()
    return render_template('compras/crear_orden.html', proveedores=proveedores)

@app.route('/compras/evaluaciones')
def evaluaciones_proveedores():
    """Evaluaciones de proveedores"""
    try:
        evaluaciones = obtener_evaluaciones_proveedores()
    except:
        evaluaciones = []
    
    return render_template('compras/evaluaciones.html', evaluaciones=evaluaciones)

# =====================================================
# RUTAS MÓDULO NÓMINA EXTENDIDO
# =====================================================

@app.route('/nomina')
def nomina_dashboard():
    """Dashboard de nómina"""
    import datetime
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    
    nomina_actual = obtener_nomina(current_month, current_year)
    capacitaciones = obtener_capacitaciones()
    
    return render_template('nomina/dashboard.html',
                         nomina=nomina_actual,
                         capacitaciones=capacitaciones[:5])

@app.route('/nomina/empleados')
def nomina_empleados():
    """Lista nómina de empleados"""
    periodo_mes = request.args.get('mes')
    periodo_ano = request.args.get('ano')
    
    nomina = obtener_nomina(periodo_mes, periodo_ano)
    return render_template('nomina/listar.html', nomina=nomina, mes=periodo_mes, ano=periodo_ano)

@app.route('/nomina/asistencia')
def asistencia_empleados():
    """Asistencia de empleados"""
    id_empleado = request.args.get('id_empleado')
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    asistencia = obtener_asistencia(id_empleado, fecha_inicio, fecha_fin)
    empleados = obtener_empleados()
    
    return render_template('nomina/asistencia.html', 
                         asistencia=asistencia, 
                         empleados=empleados)

@app.route('/nomina/capacitaciones')
def capacitaciones_lista():
    """Lista capacitaciones"""
    capacitaciones = obtener_capacitaciones()
    return render_template('nomina/capacitaciones.html', capacitaciones=capacitaciones)

# =====================================================
# RUTAS MÓDULO REPORTES AVANZADOS
# =====================================================

@app.route('/reportes/kpi')
def reportes_kpi():
    """Reportes KPI"""
    try:
        metricas = obtener_metricas_kpi()
    except:
        metricas = []
    
    return render_template('reportes/kpi.html', metricas=metricas)

@app.route('/reportes/completos')
def reportes_completos():
    """Reportes completos del sistema"""
    dashboard = obtener_dashboard_completo()
    
    return render_template('reportes/completos.html', dashboard=dashboard)

@app.route('/alertas')
def alertas_sistema():
    """Alertas del sistema"""
    try:
        alertas = obtener_alertas_sistema()
    except:
        alertas = []
    
    return render_template('alertas/listar.html', alertas=alertas)

# =====================================================
# API ENDPOINTS PARA INTEGRACIÓN
# =====================================================

@app.route('/api/dashboard')
def api_dashboard():
    """API para datos del dashboard"""
    dashboard = obtener_dashboard_completo()
    return jsonify(dashboard)

@app.route('/api/buscar')
def api_buscar():
    """API para búsqueda global"""
    termino = request.args.get('q', '')
    if not termino:
        return jsonify({'error': 'Término de búsqueda requerido'})
    
    try:
        # Función de búsqueda global simplificada
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                resultados = []
                
                # Buscar en clientes
                cursor.execute("""
                    SELECT 'cliente' as tipo, id_cliente as id, nombre, telefono as detalle
                    FROM CLIENTES
                    WHERE nombre ILIKE %s OR telefono ILIKE %s
                    LIMIT 5
                """, (f'%{termino}%', f'%{termino}%'))
                resultados.extend(cursor.fetchall())
                
                # Buscar en obras
                cursor.execute("""
                    SELECT 'obra' as tipo, id_obra as id, nombre, ubicacion as detalle
                    FROM OBRAS
                    WHERE nombre ILIKE %s OR ubicacion ILIKE %s
                    LIMIT 5
                """, (f'%{termino}%', f'%{termino}%'))
                resultados.extend(cursor.fetchall())
                
                return jsonify({'resultados': resultados})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/estadisticas')
def api_estadisticas():
    """API para estadísticas generales"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                estadisticas = {}
                
                # Contar registros en tablas principales
                tablas = ['CLIENTES', 'OBRAS', 'EMPLEADOS', 'EQUIPOS', 'VEHICULOS', 'MATERIALES']
                for tabla in tablas:
                    try:
                        cursor.execute(f"SELECT COUNT(*) as total FROM {tabla}")
                        resultado = cursor.fetchone()
                        estadisticas[tabla.lower()] = resultado['total'] if resultado else 0
                    except:
                        estadisticas[tabla.lower()] = 0
                
                return jsonify(estadisticas)
    except Exception as e:
        return jsonify({'error': str(e)})

# =====================================================
# RUTA PARA SISTEMA COMPLETO
# =====================================================

@app.route('/sistema-completo')
def sistema_completo():
    """Vista general del sistema completo con todas las funcionalidades"""
    
    # Obtener datos de resumen para cada módulo
    try:
        dashboard = obtener_dashboard_completo()
        
        # Datos adicionales para vista completa
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                
                # Contar tablas por módulo
                modulos_count = {}
                
                # Módulo Comercial
                cursor.execute("SELECT COUNT(*) as total FROM CLIENTES")
                clientes_count = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM OBRAS")
                obras_count = cursor.fetchone()['total']
                
                modulos_count['comercial'] = {
                    'clientes': clientes_count,
                    'obras': obras_count
                }
                
                # Módulo RRHH
                cursor.execute("SELECT COUNT(*) as total FROM EMPLEADOS")
                empleados_count = cursor.fetchone()['total']
                
                modulos_count['rrhh'] = {
                    'empleados': empleados_count
                }
                
                # Módulo Activos
                cursor.execute("SELECT COUNT(*) as total FROM EQUIPOS")
                equipos_count = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM VEHICULOS")
                vehiculos_count = cursor.fetchone()['total']
                
                modulos_count['activos'] = {
                    'equipos': equipos_count,
                    'vehiculos': vehiculos_count
                }
                
                # Módulo Inventarios
                cursor.execute("SELECT COUNT(*) as total FROM MATERIALES")
                materiales_count = cursor.fetchone()['total']
                
                cursor.execute("SELECT COUNT(*) as total FROM BODEGAS")
                bodegas_count = cursor.fetchone()['total']
                
                modulos_count['inventarios'] = {
                    'materiales': materiales_count,
                    'bodegas': bodegas_count
                }
                
                dashboard['modulos'] = modulos_count
        
    except Exception as e:
        dashboard = {}
        print(f"Error obteniendo datos del sistema completo: {e}")
    
    return render_template('sistema_completo.html', dashboard=dashboard)

# =====================================================
# WEBHOOK PARA ACTUALIZACIONES EN TIEMPO REAL
# =====================================================

@app.route('/webhook/actualizar-dashboard', methods=['POST'])
def webhook_actualizar_dashboard():
    """Webhook para actualizar dashboard en tiempo real"""
    try:
        # Aquí se pueden manejar actualizaciones en tiempo real
        # Por ejemplo, cuando se cree una nueva factura, orden de trabajo, etc.
        
        data = request.get_json()
        tipo_evento = data.get('tipo', '')
        
        # Lógica para diferentes tipos de eventos
        if tipo_evento == 'nueva_factura':
            # Crear alerta para nueva factura
            pass
        elif tipo_evento == 'mantenimiento_vencido':
            # Crear alerta para mantenimiento vencido
            pass
        
        return jsonify({'success': True, 'mensaje': 'Dashboard actualizado'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# =====================================================
# FUNCIONES DE UTILIDAD ADICIONALES
# =====================================================

@app.context_processor
def utility_processor():
    """Funciones de utilidad disponibles en todas las plantillas"""
    def format_currency(amount):
        """Formatear moneda"""
        if amount is None:
            return "$0.00"
        return f"${amount:,.2f}"
    
    def format_date(date):
        """Formatear fecha"""
        if date is None:
            return ""
        return date.strftime('%d/%m/%Y') if hasattr(date, 'strftime') else str(date)
    
    def get_alert_class(nivel):
        """Obtener clase CSS para alertas"""
        classes = {
            'Baja': 'alert-info',
            'Media': 'alert-warning',
            'Alta': 'alert-danger',
            'Crítica': 'alert-danger'
        }
        return classes.get(nivel, 'alert-info')
    
    return dict(
        format_currency=format_currency,
        format_date=format_date,
        get_alert_class=get_alert_class
    )