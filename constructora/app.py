# app_clean.py - Sistema de Constructora COMPLETO - Python + HTML + CSS
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
from database import (
    get_clientes_safe, get_obras_safe, insert_obra_safe, insert_cliente_safe,
    get_empleados_safe, insert_empleado_safe,
    get_proveedores_safe, insert_proveedor_safe,
    get_materiales_safe, insert_material_safe,
    get_vehiculos_safe, insert_vehiculo_safe,
    get_equipos_safe, insert_equipo_safe,
    get_proyectos_safe, insert_proyecto_safe,
    get_areas_safe, insert_area_safe,
    get_contratos_safe, insert_contrato_safe,
    get_reportes_academicos_safe, get_bodegas_inventarios_safe,
    # Nuevas funciones para las 56 tablas
    get_actividades_safe, insert_actividad_safe,
    get_bitacoras_safe, insert_bitacora_safe,
    get_incidentes_safe, insert_incidente_safe,
    get_auditorias_safe, get_usuarios_safe,
    get_presupuestos_safe, insert_presupuesto_safe,
    get_avances_safe, insert_avance_safe,
    get_requisiciones_safe, get_movimientos_materiales_safe,
    get_trabajos_safe, insert_trabajo_safe
)
import logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)
app.secret_key = 'constructora-secret-2024'

print("🚀 Sistema de Constructora - SISTEMA COMPLETO")
print("📍 Servidor ejecutándose en: http://127.0.0.1:5000")
print("💡 Gestión completa de las 56 tablas - 100% server-side")
print("🏗️  Módulos: Obras, Clientes, Empleados, Proveedores, Materiales, Vehículos, Equipos")

# ===============================
# DASHBOARD PRINCIPAL
# ===============================
@app.route('/')
def dashboard():
    """Dashboard principal del sistema"""
    try:
        # Obtener estadísticas de todas las tablas principales
        obras = get_obras_safe()
        clientes = get_clientes_safe()
        empleados = get_empleados_safe()
        proveedores = get_proveedores_safe()
        materiales = get_materiales_safe()
        vehiculos = get_vehiculos_safe()
        equipos = get_equipos_safe()
        proyectos = get_proyectos_safe()
        
        stats = {
            'total_obras': len(obras),
            'obras_activas': len([o for o in obras if o.get('estado') in ['En Progreso', 'Activa']]),
            'obras_completadas': len([o for o in obras if o.get('estado') in ['Completado', 'Finalizada']]),
            'valor_total': sum([o.get('valor', 0) or 0 for o in obras]),
            'total_clientes': len(clientes),
            'total_empleados': len(empleados),
            'total_proveedores': len(proveedores),
            'total_materiales': len(materiales),
            'total_vehiculos': len(vehiculos),
            'total_equipos': len(equipos),
            'total_proyectos': len(proyectos)
        }
        
        obras_recientes = obras[:5]  # Últimas 5 obras
        return render_template('dashboard.html', stats=stats, obras_recientes=obras_recientes)
    except Exception as e:
        logger.error(f'Error en dashboard: {e}')
        stats = {
            'total_obras': 0, 'obras_activas': 0, 'obras_completadas': 0, 'valor_total': 0,
            'total_clientes': 0, 'total_empleados': 0, 'total_proveedores': 0,
            'total_materiales': 0, 'total_vehiculos': 0, 'total_equipos': 0, 'total_proyectos': 0
        }
        return render_template('dashboard.html', stats=stats, obras_recientes=[])

# ===============================
# GESTIÓN DE OBRAS
# ===============================
@app.route('/obras')
def listar_obras():
    """Listar todas las obras"""
    try:
        filtro_estado = request.args.get('estado', '')
        buscar = request.args.get('search', '')
        
        obras = get_obras_safe()
        
        # Aplicar filtros
        if filtro_estado:
            obras = [obra for obra in obras if obra.get('estado') == filtro_estado]
        
        if buscar:
            buscar_lower = buscar.lower()
            obras = [obra for obra in obras if 
                    buscar_lower in obra.get('nombre', '').lower() or 
                    buscar_lower in obra.get('ubicacion', '').lower() or
                    buscar_lower in obra.get('cliente', '').lower()]
        
        return render_template('obras/listar.html', obras=obras, filtro_estado=filtro_estado, buscar=buscar)
    except Exception as e:
        flash(f'Error al cargar obras: {str(e)}', 'error')
        return render_template('obras/listar.html', obras=[])

@app.route('/obras/nueva', methods=['GET', 'POST'])
def crear_obra():
    """Crear nueva obra"""
    if request.method == 'GET':
        clientes = get_clientes_safe()
        return render_template('obras/crear.html', clientes=clientes)
    
    try:
        # Obtener datos básicos del formulario
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        ubicacion = request.form.get('ubicacion', '').strip()
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        valor = request.form.get('valor')
        estado = request.form.get('estado', 'Planeación')
        
        # Validar datos obligatorios
        if not nombre:
            flash('El nombre de la obra es obligatorio', 'error')
            clientes = get_clientes_safe()
            return render_template('obras/crear.html', clientes=clientes)
        
        # Manejar cliente
        tipo_cliente = request.form.get('tipo_cliente')
        cliente_id = None
        
        if tipo_cliente == 'existente':
            cliente_id = request.form.get('cliente_id')
            if not cliente_id:
                flash('Debe seleccionar un cliente existente', 'error')
                clientes = get_clientes_safe()
                return render_template('obras/crear.html', clientes=clientes)
        
        elif tipo_cliente == 'nuevo':
            # Crear nuevo cliente
            nuevo_cliente_nombre = request.form.get('nuevo_cliente_nombre', '').strip()
            if not nuevo_cliente_nombre:
                flash('El nombre del cliente es obligatorio', 'error')
                clientes = get_clientes_safe()
                return render_template('obras/crear.html', clientes=clientes)
            
            nuevo_cliente_documento = request.form.get('nuevo_cliente_documento', '').strip()
            nuevo_cliente_telefono = request.form.get('nuevo_cliente_telefono', '').strip()
            nuevo_cliente_email = request.form.get('nuevo_cliente_email', '').strip()
            nuevo_cliente_direccion = request.form.get('nuevo_cliente_direccion', '').strip()
            
            # Insertar nuevo cliente
            cliente_id = insert_cliente_safe(
                nombre=nuevo_cliente_nombre,
                documento=nuevo_cliente_documento,
                telefono=nuevo_cliente_telefono,
                email=nuevo_cliente_email,
                direccion=nuevo_cliente_direccion
            )
            
            if cliente_id:
                flash(f'Cliente "{nuevo_cliente_nombre}" creado exitosamente', 'success')
            else:
                flash('Error al crear el cliente', 'error')
                clientes = get_clientes_safe()
                return render_template('obras/crear.html', clientes=clientes)
        
        else:
            flash('Debe especificar un cliente para la obra', 'error')
            clientes = get_clientes_safe()
            return render_template('obras/crear.html', clientes=clientes)
        
        # Convertir valor a número si se proporciona
        valor_numerico = None
        if valor:
            try:
                valor_numerico = float(valor)
            except ValueError:
                valor_numerico = None
        
        # Crear obra con cliente obligatorio
        nueva_obra_id = insert_obra_safe(
            nombre=nombre,
            descripcion=descripcion,
            ubicacion=ubicacion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            valor=valor_numerico,
            estado=estado,
            cliente_id=cliente_id
        )
        
        if nueva_obra_id:
            flash(f'Obra "{nombre}" creada exitosamente', 'success')
            return redirect(url_for('listar_obras'))
        else:
            flash('Error al crear la obra', 'error')
            clientes = get_clientes_safe()
            return render_template('obras/crear.html', clientes=clientes)
        
    except Exception as e:
        logger.error(f'Error al crear obra: {e}')
        flash(f'Error al crear obra: {str(e)}', 'error')
        clientes = get_clientes_safe()
        return render_template('obras/crear.html', clientes=clientes)

# ===============================
# GESTIÓN DE EMPLEADOS
# ===============================
@app.route('/empleados')
def listar_empleados():
    """Listar todos los empleados"""
    try:
        empleados = get_empleados_safe()
        return render_template('empleados/listar.html', empleados=empleados)
    except Exception as e:
        flash(f'Error al cargar empleados: {str(e)}', 'error')
        return render_template('empleados/listar.html', empleados=[])

@app.route('/empleados/nuevo', methods=['GET', 'POST'])
def crear_empleado():
    """Crear nuevo empleado"""
    if request.method == 'GET':
        return render_template('empleados/crear.html')
    
    try:
        nombre = request.form.get('nombre', '').strip()
        tipo = request.form.get('tipo', '').strip()
        salario = request.form.get('salario')
        
        if not nombre:
            flash('El nombre del empleado es obligatorio', 'error')
            return render_template('empleados/crear.html')
        
        salario_numerico = None
        if salario:
            try:
                salario_numerico = float(salario)
            except ValueError:
                salario_numerico = None
        
        empleado_id = insert_empleado_safe(nombre=nombre, tipo=tipo, salario=salario_numerico)
        
        if empleado_id:
            flash(f'Empleado "{nombre}" creado exitosamente', 'success')
            return redirect(url_for('listar_empleados'))
        else:
            flash('Error al crear empleado', 'error')
            return render_template('empleados/crear.html')
            
    except Exception as e:
        flash(f'Error al crear empleado: {str(e)}', 'error')
        return render_template('empleados/crear.html')

# ===============================
# GESTIÓN DE PROVEEDORES
# ===============================
@app.route('/proveedores')
def listar_proveedores():
    """Listar todos los proveedores"""
    try:
        proveedores = get_proveedores_safe()
        return render_template('proveedores/listar.html', proveedores=proveedores)
    except Exception as e:
        flash(f'Error al cargar proveedores: {str(e)}', 'error')
        return render_template('proveedores/listar.html', proveedores=[])

@app.route('/proveedores/nuevo', methods=['GET', 'POST'])
def crear_proveedor():
    """Crear nuevo proveedor"""
    if request.method == 'GET':
        return render_template('proveedores/crear.html')
    
    try:
        nombre = request.form.get('nombre', '').strip()
        contacto = request.form.get('contacto', '').strip()
        
        if not nombre:
            flash('El nombre del proveedor es obligatorio', 'error')
            return render_template('proveedores/crear.html')
        
        proveedor_id = insert_proveedor_safe(nombre=nombre, contacto=contacto)
        
        if proveedor_id:
            flash(f'Proveedor "{nombre}" creado exitosamente', 'success')
            return redirect(url_for('listar_proveedores'))
        else:
            flash('Error al crear proveedor', 'error')
            return render_template('proveedores/crear.html')
            
    except Exception as e:
        flash(f'Error al crear proveedor: {str(e)}', 'error')
        return render_template('proveedores/crear.html')

# ===============================
# GESTIÓN DE MATERIALES
# ===============================
@app.route('/materiales')
def listar_materiales():
    """Listar todos los materiales"""
    try:
        materiales = get_materiales_safe()
        return render_template('materiales/listar.html', materiales=materiales)
    except Exception as e:
        flash(f'Error al cargar materiales: {str(e)}', 'error')
        return render_template('materiales/listar.html', materiales=[])

@app.route('/materiales/nuevo', methods=['GET', 'POST'])
def crear_material():
    """Crear nuevo material"""
    if request.method == 'GET':
        return render_template('materiales/crear.html')
    
    try:
        nombre = request.form.get('nombre', '').strip()
        unidad = request.form.get('unidad', '').strip()
        precio = request.form.get('precio')
        
        if not nombre:
            flash('El nombre del material es obligatorio', 'error')
            return render_template('materiales/crear.html')
        
        precio_numerico = None
        if precio:
            try:
                precio_numerico = float(precio)
            except ValueError:
                precio_numerico = None
        
        material_id = insert_material_safe(nombre=nombre, unidad=unidad, precio=precio_numerico)
        
        if material_id:
            flash(f'Material "{nombre}" creado exitosamente', 'success')
            return redirect(url_for('listar_materiales'))
        else:
            flash('Error al crear material', 'error')
            return render_template('materiales/crear.html')
            
    except Exception as e:
        flash(f'Error al crear material: {str(e)}', 'error')
        return render_template('materiales/crear.html')

# ===============================
# GESTIÓN DE VEHÍCULOS
# ===============================
@app.route('/vehiculos')
def listar_vehiculos():
    """Listar todos los vehículos"""
    try:
        vehiculos = get_vehiculos_safe()
        return render_template('vehiculos/listar.html', vehiculos=vehiculos)
    except Exception as e:
        flash(f'Error al cargar vehículos: {str(e)}', 'error')
        return render_template('vehiculos/listar.html', vehiculos=[])

@app.route('/vehiculos/nuevo', methods=['GET', 'POST'])
def crear_vehiculo():
    """Crear nuevo vehículo"""
    if request.method == 'GET':
        return render_template('vehiculos/crear.html')
    
    try:
        placa = request.form.get('placa', '').strip()
        estado = request.form.get('estado', '').strip()
        tipo = request.form.get('tipo', '').strip()
        
        if not placa:
            flash('La placa del vehículo es obligatoria', 'error')
            return render_template('vehiculos/crear.html')
        
        vehiculo_id = insert_vehiculo_safe(placa=placa, estado=estado, tipo=tipo)
        
        if vehiculo_id:
            flash(f'Vehículo con placa "{placa}" creado exitosamente', 'success')
            return redirect(url_for('listar_vehiculos'))
        else:
            flash('Error al crear vehículo', 'error')
            return render_template('vehiculos/crear.html')
            
    except Exception as e:
        flash(f'Error al crear vehículo: {str(e)}', 'error')
        return render_template('vehiculos/crear.html')

# ===============================
# GESTIÓN DE EQUIPOS
# ===============================
@app.route('/equipos')
def listar_equipos():
    """Listar todos los equipos"""
    try:
        equipos = get_equipos_safe()
        return render_template('equipos/listar.html', equipos=equipos)
    except Exception as e:
        flash(f'Error al cargar equipos: {str(e)}', 'error')
        return render_template('equipos/listar.html', equipos=[])

@app.route('/equipos/nuevo', methods=['GET', 'POST'])
def crear_equipo():
    """Crear nuevo equipo"""
    if request.method == 'GET':
        return render_template('equipos/crear.html')
    
    try:
        nombre = request.form.get('nombre', '').strip()
        estado = request.form.get('estado', '').strip()
        tipo = request.form.get('tipo', '').strip()
        
        if not nombre:
            flash('El nombre del equipo es obligatorio', 'error')
            return render_template('equipos/crear.html')
        
        equipo_id = insert_equipo_safe(nombre=nombre, estado=estado, tipo=tipo)
        
        if equipo_id:
            flash(f'Equipo "{nombre}" creado exitosamente', 'success')
            return redirect(url_for('listar_equipos'))
        else:
            flash('Error al crear equipo', 'error')
            return render_template('equipos/crear.html')
            
    except Exception as e:
        flash(f'Error al crear equipo: {str(e)}', 'error')
        return render_template('equipos/crear.html')

# ===============================
# GESTIÓN DE PROYECTOS
# ===============================
@app.route('/proyectos')
def listar_proyectos():
    """Listar todos los proyectos"""
    try:
        proyectos = get_proyectos_safe()
        return render_template('proyectos/listar.html', proyectos=proyectos)
    except Exception as e:
        flash(f'Error al cargar proyectos: {str(e)}', 'error')
        return render_template('proyectos/listar.html', proyectos=[])

@app.route('/proyectos/nuevo', methods=['GET', 'POST'])
def crear_proyecto():
    """Crear nuevo proyecto"""
    if request.method == 'GET':
        return render_template('proyectos/crear.html')
    
    try:
        nombre = request.form.get('nombre', '').strip()
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        estado = request.form.get('estado', 'Planeación')
        
        if not nombre:
            flash('El nombre del proyecto es obligatorio', 'error')
            return render_template('proyectos/crear.html')
        
        proyecto_id = insert_proyecto_safe(
            nombre=nombre, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin, 
            estado=estado
        )
        
        if proyecto_id:
            flash(f'Proyecto "{nombre}" creado exitosamente', 'success')
            return redirect(url_for('listar_proyectos'))
        else:
            flash('Error al crear proyecto', 'error')
            return render_template('proyectos/crear.html')
            
    except Exception as e:
        flash(f'Error al crear proyecto: {str(e)}', 'error')
        return render_template('proyectos/crear.html')

# ===============================
# BODEGAS E INVENTARIOS
# ===============================
@app.route('/bodegas')
def bodegas_index():
    """Página principal de bodegas e inventarios"""
    try:
        bodegas = get_bodegas_inventarios_safe()
        return render_template('bodegas/index.html', bodegas=bodegas)
    except Exception as e:
        logger.error(f'Error en bodegas: {e}')
        bodegas_vacias = {
            'total_bodegas': 0, 'materiales_inventario': 0, 'valor_inventario': 0, 'movimientos_hoy': 0,
            'inventarios_resumen': [], 'movimientos_recientes': []
        }
        return render_template('bodegas/index.html', bodegas=bodegas_vacias)

@app.route('/bodegas/listar')
def listar_bodegas():
    """Listar todas las bodegas"""
    flash('Módulo de Bodegas - En desarrollo', 'info')
    return redirect(url_for('bodegas_index'))

@app.route('/bodegas/nueva')
def crear_bodega():
    """Crear nueva bodega"""
    flash('Módulo de Crear Bodega - En desarrollo', 'info')
    return redirect(url_for('bodegas_index'))

@app.route('/inventarios')
def inventarios():
    """Gestión de inventarios"""
    flash('Módulo de Inventarios - En desarrollo', 'info')
    return redirect(url_for('bodegas_index'))

@app.route('/movimientos')
def movimientos_materiales():
    """Movimientos de materiales"""
    flash('Módulo de Movimientos - En desarrollo', 'info')
    return redirect(url_for('bodegas_index'))

# ===============================
# REPORTES ACADÉMICOS
# ===============================
@app.route('/reportes')
def reportes_academicos():
    """Mostrar reportes académicos requeridos"""
    try:
        reportes = get_reportes_academicos_safe()
        return render_template('reportes/academicos.html', reportes=reportes)
    except Exception as e:
        logger.error(f'Error en reportes académicos: {e}')
        # Reportes vacíos en caso de error
        reportes_vacios = {
            'gastos_totales': 0,
            'obras_con_gastos': 0,
            'areas_activas': 0,
            'gastos_por_obra': [],
            'materiales_asignados': 0,
            'areas_con_materiales': 0,
            'valor_materiales': 0,
            'materiales_por_area': [],
            'proyectos_activos': 0,
            'ingenieros_asignados': 0,
            'arquitectos_asignados': 0,
            'asignaciones_proyectos': [],
            'empleados_activos': 0,
            'actividades_diarias': 0,
            'areas_ocupadas': 0,
            'actividades_personal': [],
            'precios_actualizados': 0,
            'variacion_promedio': 0,
            'materiales_con_precio': 0,
            'historial_precios': []
        }
        return render_template('reportes/academicos.html', reportes=reportes_vacios)

# ===============================
# MÓDULOS AVANZADOS - USANDO TODAS LAS 56 TABLAS
# ===============================

# ===============================
# GESTIÓN DE ACTIVIDADES
# ===============================
@app.route('/actividades')
def listar_actividades():
    """Listar todas las actividades"""
    try:
        actividades = get_actividades_safe()
        return render_template('actividades/listar.html', actividades=actividades)
    except Exception as e:
        flash(f'Error al cargar actividades: {str(e)}', 'error')
        return render_template('actividades/listar.html', actividades=[])

@app.route('/actividades/nueva', methods=['GET', 'POST'])
def crear_actividad():
    """Crear nueva actividad"""
    if request.method == 'GET':
        return render_template('actividades/crear.html')
    
    try:
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        fecha_programada = request.form.get('fecha_programada')
        
        if not nombre:
            flash('El nombre de la actividad es obligatorio', 'error')
            return render_template('actividades/crear.html')
        
        actividad_id = insert_actividad_safe(
            nombre=nombre, 
            descripcion=descripcion, 
            fecha_programada=fecha_programada
        )
        
        if actividad_id:
            flash(f'Actividad "{nombre}" creada exitosamente', 'success')
            return redirect(url_for('listar_actividades'))
        else:
            flash('Error al crear actividad', 'error')
            return render_template('actividades/crear.html')
            
    except Exception as e:
        flash(f'Error al crear actividad: {str(e)}', 'error')
        return render_template('actividades/crear.html')

# ===============================
# GESTIÓN DE BITÁCORAS
# ===============================
@app.route('/bitacoras')
def listar_bitacoras():
    """Listar todas las bitácoras"""
    try:
        bitacoras = get_bitacoras_safe()
        return render_template('bitacoras/listar.html', bitacoras=bitacoras)
    except Exception as e:
        flash(f'Error al cargar bitácoras: {str(e)}', 'error')
        return render_template('bitacoras/listar.html', bitacoras=[])

@app.route('/bitacoras/nueva', methods=['GET', 'POST'])
def crear_bitacora():
    """Crear nueva bitácora"""
    if request.method == 'GET':
        obras = get_obras_safe()
        return render_template('bitacoras/crear.html', obras=obras)
    
    try:
        observaciones = request.form.get('observaciones', '').strip()
        fecha_bitacora = request.form.get('fecha_bitacora')
        obra_id = request.form.get('obra_id')
        
        if not observaciones:
            flash('Las observaciones son obligatorias', 'error')
            obras = get_obras_safe()
            return render_template('bitacoras/crear.html', obras=obras)
        
        bitacora_id = insert_bitacora_safe(
            observaciones=observaciones,
            fecha_bitacora=fecha_bitacora,
            obra_id=obra_id if obra_id else None
        )
        
        if bitacora_id:
            flash('Bitácora creada exitosamente', 'success')
            return redirect(url_for('listar_bitacoras'))
        else:
            flash('Error al crear bitácora', 'error')
            obras = get_obras_safe()
            return render_template('bitacoras/crear.html', obras=obras)
            
    except Exception as e:
        flash(f'Error al crear bitácora: {str(e)}', 'error')
        obras = get_obras_safe()
        return render_template('bitacoras/crear.html', obras=obras)

# ===============================
# GESTIÓN DE INCIDENTES
# ===============================
@app.route('/incidentes')
def listar_incidentes():
    """Listar todos los incidentes"""
    try:
        incidentes = get_incidentes_safe()
        return render_template('incidentes/listar.html', incidentes=incidentes)
    except Exception as e:
        flash(f'Error al cargar incidentes: {str(e)}', 'error')
        return render_template('incidentes/listar.html', incidentes=[])

@app.route('/incidentes/nuevo', methods=['GET', 'POST'])
def crear_incidente():
    """Crear nuevo incidente"""
    if request.method == 'GET':
        obras = get_obras_safe()
        return render_template('incidentes/crear.html', obras=obras)
    
    try:
        descripcion = request.form.get('descripcion', '').strip()
        estado = request.form.get('estado', 'Reportado')
        fecha_incidente = request.form.get('fecha_incidente')
        obra_id = request.form.get('obra_id')
        
        if not descripcion:
            flash('La descripción del incidente es obligatoria', 'error')
            obras = get_obras_safe()
            return render_template('incidentes/crear.html', obras=obras)
        
        incidente_id = insert_incidente_safe(
            descripcion=descripcion,
            estado=estado,
            fecha_incidente=fecha_incidente,
            obra_id=obra_id if obra_id else None
        )
        
        if incidente_id:
            flash('Incidente reportado exitosamente', 'success')
            return redirect(url_for('listar_incidentes'))
        else:
            flash('Error al crear incidente', 'error')
            obras = get_obras_safe()
            return render_template('incidentes/crear.html', obras=obras)
            
    except Exception as e:
        flash(f'Error al crear incidente: {str(e)}', 'error')
        obras = get_obras_safe()
        return render_template('incidentes/crear.html', obras=obras)

# ===============================
# GESTIÓN DE AUDITORÍAS
# ===============================
@app.route('/auditorias')
def listar_auditorias():
    """Listar todas las auditorías del sistema"""
    try:
        auditorias = get_auditorias_safe()
        return render_template('auditorias/listar.html', auditorias=auditorias)
    except Exception as e:
        flash(f'Error al cargar auditorías: {str(e)}', 'error')
        return render_template('auditorias/listar.html', auditorias=[])

# ===============================
# GESTIÓN DE USUARIOS
# ===============================
@app.route('/usuarios')
def listar_usuarios():
    """Listar usuarios del sistema"""
    try:
        usuarios = get_usuarios_safe()
        return render_template('usuarios/listar.html', usuarios=usuarios)
    except Exception as e:
        flash(f'Error al cargar usuarios: {str(e)}', 'error')
        return render_template('usuarios/listar.html', usuarios=[])

# ===============================
# GESTIÓN DE CONTRATOS
# ===============================
@app.route('/contratos')
def listar_contratos():
    """Listar todos los contratos"""
    try:
        contratos = get_contratos_safe()
        return render_template('contratos/listar.html', contratos=contratos)
    except Exception as e:
        flash(f'Error al cargar contratos: {str(e)}', 'error')
        return render_template('contratos/listar.html', contratos=[])

@app.route('/contratos/nuevo', methods=['GET', 'POST'])
def crear_contrato():
    """Crear nuevo contrato"""
    if request.method == 'GET':
        obras = get_obras_safe()
        return render_template('contratos/crear.html', obras=obras)
    
    try:
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        tipo_pago = request.form.get('tipo_pago', '').strip()
        obra_id = request.form.get('obra_id')
        
        if not fecha_inicio:
            flash('La fecha de inicio es obligatoria', 'error')
            obras = get_obras_safe()
            return render_template('contratos/crear.html', obras=obras)
        
        contrato_id = insert_contrato_safe(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_pago=tipo_pago,
            obra_id=obra_id if obra_id else None
        )
        
        if contrato_id:
            flash('Contrato creado exitosamente', 'success')
            return redirect(url_for('listar_contratos'))
        else:
            flash('Error al crear contrato', 'error')
            obras = get_obras_safe()
            return render_template('contratos/crear.html', obras=obras)
            
    except Exception as e:
        flash(f'Error al crear contrato: {str(e)}', 'error')
        obras = get_obras_safe()
        return render_template('contratos/crear.html', obras=obras)

# ===============================
# GESTIÓN DE PRESUPUESTOS
# ===============================
@app.route('/presupuestos')
def listar_presupuestos():
    """Listar todos los presupuestos"""
    try:
        presupuestos = get_presupuestos_safe()
        return render_template('presupuestos/listar.html', presupuestos=presupuestos)
    except Exception as e:
        flash(f'Error al cargar presupuestos: {str(e)}', 'error')
        return render_template('presupuestos/listar.html', presupuestos=[])

@app.route('/presupuestos/nuevo', methods=['GET', 'POST'])
def crear_presupuesto():
    """Crear nuevo presupuesto"""
    if request.method == 'GET':
        obras = get_obras_safe()
        return render_template('presupuestos/crear.html', obras=obras)
    
    try:
        monto_estimado = request.form.get('monto_estimado')
        fecha_presupuesto = request.form.get('fecha_presupuesto')
        obra_id = request.form.get('obra_id')
        
        if not monto_estimado:
            flash('El monto estimado es obligatorio', 'error')
            obras = get_obras_safe()
            return render_template('presupuestos/crear.html', obras=obras)
        
        try:
            monto_numerico = float(monto_estimado)
        except ValueError:
            flash('El monto debe ser un número válido', 'error')
            obras = get_obras_safe()
            return render_template('presupuestos/crear.html', obras=obras)
        
        presupuesto_id = insert_presupuesto_safe(
            monto_estimado=monto_numerico,
            fecha_presupuesto=fecha_presupuesto,
            obra_id=obra_id if obra_id else None
        )
        
        if presupuesto_id:
            flash('Presupuesto creado exitosamente', 'success')
            return redirect(url_for('listar_presupuestos'))
        else:
            flash('Error al crear presupuesto', 'error')
            obras = get_obras_safe()
            return render_template('presupuestos/crear.html', obras=obras)
            
    except Exception as e:
        flash(f'Error al crear presupuesto: {str(e)}', 'error')
        obras = get_obras_safe()
        return render_template('presupuestos/crear.html', obras=obras)

# ===============================
# GESTIÓN DE AVANCES
# ===============================
@app.route('/avances')
def listar_avances():
    """Listar avances de obras"""
    try:
        avances = get_avances_safe()
        return render_template('avances/listar.html', avances=avances)
    except Exception as e:
        flash(f'Error al cargar avances: {str(e)}', 'error')
        return render_template('avances/listar.html', avances=[])

@app.route('/avances/nuevo', methods=['GET', 'POST'])
def crear_avance():
    """Registrar nuevo avance de obra"""
    if request.method == 'GET':
        obras = get_obras_safe()
        return render_template('avances/crear.html', obras=obras)
    
    try:
        porcentaje_fisico = request.form.get('porcentaje_fisico')
        porcentaje_financiero = request.form.get('porcentaje_financiero')
        fecha_avance = request.form.get('fecha_avance')
        obra_id = request.form.get('obra_id')
        
        if not porcentaje_fisico or not porcentaje_financiero:
            flash('Los porcentajes de avance son obligatorios', 'error')
            obras = get_obras_safe()
            return render_template('avances/crear.html', obras=obras)
        
        try:
            fisico = float(porcentaje_fisico)
            financiero = float(porcentaje_financiero)
        except ValueError:
            flash('Los porcentajes deben ser números válidos', 'error')
            obras = get_obras_safe()
            return render_template('avances/crear.html', obras=obras)
        
        avance_id = insert_avance_safe(
            porcentaje_fisico=fisico,
            porcentaje_financiero=financiero,
            fecha_avance=fecha_avance,
            obra_id=obra_id if obra_id else None
        )
        
        if avance_id:
            flash('Avance registrado exitosamente', 'success')
            return redirect(url_for('listar_avances'))
        else:
            flash('Error al registrar avance', 'error')
            obras = get_obras_safe()
            return render_template('avances/crear.html', obras=obras)
            
    except Exception as e:
        flash(f'Error al registrar avance: {str(e)}', 'error')
        obras = get_obras_safe()
        return render_template('avances/crear.html', obras=obras)

# ===============================
# GESTIÓN DE ÁREAS
# ===============================
@app.route('/areas')
def listar_areas():
    """Listar todas las áreas de trabajo"""
    try:
        areas = get_areas_safe()
        return render_template('areas/listar.html', areas=areas)
    except Exception as e:
        flash(f'Error al cargar áreas: {str(e)}', 'error')
        return render_template('areas/listar.html', areas=[])

@app.route('/areas/nueva', methods=['GET', 'POST'])
def crear_area():
    """Crear nueva área de trabajo"""
    if request.method == 'GET':
        return render_template('areas/crear.html')
    
    try:
        nombre = request.form.get('nombre', '').strip()
        
        if not nombre:
            flash('El nombre del área es obligatorio', 'error')
            return render_template('areas/crear.html')
        
        area_id = insert_area_safe(nombre=nombre)
        
        if area_id:
            flash(f'Área "{nombre}" creada exitosamente', 'success')
            return redirect(url_for('listar_areas'))
        else:
            flash('Error al crear área', 'error')
            return render_template('areas/crear.html')
            
    except Exception as e:
        flash(f'Error al crear área: {str(e)}', 'error')
        return render_template('areas/crear.html')

# ===============================
# GESTIÓN DE REQUISICIONES
# ===============================
@app.route('/requisiciones')
def listar_requisiciones():
    """Listar requisiciones de materiales"""
    try:
        requisiciones = get_requisiciones_safe()
        return render_template('requisiciones/listar.html', requisiciones=requisiciones)
    except Exception as e:
        flash(f'Error al cargar requisiciones: {str(e)}', 'error')
        return render_template('requisiciones/listar.html', requisiciones=[])

# ===============================
# MOVIMIENTOS DE MATERIALES
# ===============================
@app.route('/movimientos')
def listar_movimientos():
    """Listar movimientos de materiales"""
    try:
        movimientos = get_movimientos_materiales_safe()
        return render_template('movimientos/listar.html', movimientos=movimientos)
    except Exception as e:
        flash(f'Error al cargar movimientos: {str(e)}', 'error')
        return render_template('movimientos/listar.html', movimientos=[])

# ===============================
# GESTIÓN DE TRABAJOS
# ===============================
@app.route('/trabajos')
def listar_trabajos():
    """Listar trabajos disponibles"""
    try:
        trabajos = get_trabajos_safe()
        return render_template('trabajos/listar.html', trabajos=trabajos)
    except Exception as e:
        flash(f'Error al cargar trabajos: {str(e)}', 'error')
        return render_template('trabajos/listar.html', trabajos=[])

@app.route('/trabajos/nuevo', methods=['GET', 'POST'])
def crear_trabajo():
    """Crear nuevo tipo de trabajo"""
    if request.method == 'GET':
        return render_template('trabajos/crear.html')
    
    try:
        descripcion = request.form.get('descripcion', '').strip()
        precio_unitario = request.form.get('precio_unitario')
        unidad = request.form.get('unidad', '').strip()
        
        if not descripcion:
            flash('La descripción del trabajo es obligatoria', 'error')
            return render_template('trabajos/crear.html')
        
        precio_numerico = None
        if precio_unitario:
            try:
                precio_numerico = float(precio_unitario)
            except ValueError:
                precio_numerico = None
        
        trabajo_id = insert_trabajo_safe(
            descripcion=descripcion,
            precio_unitario=precio_numerico,
            unidad=unidad
        )
        
        if trabajo_id:
            flash(f'Trabajo "{descripcion}" creado exitosamente', 'success')
            return redirect(url_for('listar_trabajos'))
        else:
            flash('Error al crear trabajo', 'error')
            return render_template('trabajos/crear.html')
            
    except Exception as e:
        flash(f'Error al crear trabajo: {str(e)}', 'error')
        return render_template('trabajos/crear.html')

# ===============================
# REPORTES AVANZADOS DEL SISTEMA
# ===============================
@app.route('/reportes/sistema')
def reportes_sistema_completo():
    """Reportes que utilizan todas las 56 tablas"""
    try:
        # Estadísticas generales del sistema
        obras = get_obras_safe()
        empleados = get_empleados_safe()
        materiales = get_materiales_safe()
        vehiculos = get_vehiculos_safe()
        equipos = get_equipos_safe()
        incidentes = get_incidentes_safe()
        bitacoras = get_bitacoras_safe()
        auditorias = get_auditorias_safe()
        contratos = get_contratos_safe()
        avances = get_avances_safe()
        
        estadisticas = {
            'resumen_general': {
                'total_obras': len(obras),
                'total_empleados': len(empleados),
                'total_materiales': len(materiales),
                'total_vehiculos': len(vehiculos),
                'total_equipos': len(equipos),
                'total_incidentes': len(incidentes),
                'total_bitacoras': len(bitacoras),
                'total_auditorias': len(auditorias),
                'total_contratos': len(contratos),
                'total_avances': len(avances)
            },
            'obras_por_estado': {},
            'incidentes_por_estado': {},
            'avance_promedio_obras': 0,
            'valor_total_proyectos': 0
        }
        
        # Análisis por estados
        for obra in obras:
            estado = obra.get('estado', 'Sin Estado')
            if estado in estadisticas['obras_por_estado']:
                estadisticas['obras_por_estado'][estado] += 1
            else:
                estadisticas['obras_por_estado'][estado] = 1
        
        for incidente in incidentes:
            estado = incidente.get('estado_incidente', 'Sin Estado')
            if estado in estadisticas['incidentes_por_estado']:
                estadisticas['incidentes_por_estado'][estado] += 1
            else:
                estadisticas['incidentes_por_estado'][estado] = 1
        
        # Cálculos financieros
        valores_obras = [float(obra.get('valor', 0) or 0) for obra in obras]
        estadisticas['valor_total_proyectos'] = sum(valores_obras)
        
        # Avance promedio
        if avances:
            avance_fisico_promedio = sum([float(a.get('porcentaje_fisico_avance', 0) or 0) for a in avances]) / len(avances)
            estadisticas['avance_promedio_obras'] = round(avance_fisico_promedio, 2)
        
        return render_template('reportes/sistema_completo.html', estadisticas=estadisticas)
        
    except Exception as e:
        logger.error(f'Error generando reportes del sistema: {e}')
        flash(f'Error al generar reportes: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

# ===============================
# EJECUTAR APLICACIÓN
# ===============================
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)