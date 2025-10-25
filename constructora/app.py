# app_clean.py - Sistema de Constructora COMPLETO - Python + HTML + CSS
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import timedelta
from dotenv import load_dotenv
from functools import wraps

# Salarios fijos por cargo (en quetzales)
SALARIOS_POR_CARGO = {
    'ARQUITECTO': 9500.00,           
    'INGENIERO': 8500.00,            
    'ADMINISTRADOR': 7200.00,        
    'SUPERVISOR': 6200.00,           
    'ADMINISTRATIVO': 4800.00,       
    'ALMACENISTA': 4200.00,          
    'CONDUCTOR': 3800.00,            
    'OBRERO_ESPECIALIZADO': 3500.00, 
    'OPERARIO': 3200.00,             
    'OBRERO': 2800.00,               
    'SEGURIDAD': 2600.00             
}
from database import (
    get_connection,
    get_clientes_safe, get_cliente_by_id_safe, update_cliente_safe, delete_cliente_safe, get_obras_safe, insert_obra_safe, insert_cliente_safe,
    get_empleados_safe, insert_empleado_safe,
    get_proveedores_safe, insert_proveedor_safe,
    get_materiales_safe, insert_material_safe,
    get_vehiculos_safe, insert_vehiculo_safe,
    get_equipos_safe, insert_equipo_safe,
    get_proyectos_safe, insert_proyecto_safe,
    get_areas_safe, insert_area_safe, get_area_by_id_safe, update_area_safe, delete_area_safe,
    assign_area_to_obra, remove_area_from_obra, get_obras_for_area, get_areas_for_obra,
    assign_activity_to_area, get_activities_for_area,
    assign_employee_to_area, get_employees_for_area,
    assign_requisicion_to_area, get_requisiciones_for_area,
    remove_activity_from_area, remove_employee_from_area, remove_requisicion_from_area,
    get_contratos_safe, insert_contrato_safe, get_contrato_by_id_safe, update_contrato_safe, delete_contrato_safe,
    get_reportes_academicos_safe, get_bodegas_inventarios_safe,
    # Nuevas funciones para las 56 tablas
    get_actividades_safe, insert_actividad_safe, get_actividad_by_id_safe, update_actividad_safe, delete_actividad_safe,
    get_bitacoras_safe, insert_bitacora_safe, get_bitacora_by_id_safe, update_bitacora_safe, delete_bitacora_safe,
    get_incidentes_safe, insert_incidente_safe, get_incidente_by_id_safe, update_incidente_safe, delete_incidente_safe,
    get_auditorias_safe, get_auditoria_by_id_safe, get_usuarios_safe,
    get_permisos_acceso_safe, get_permiso_by_id_safe, insert_permiso_safe, update_permiso_safe, delete_permiso_safe,
    get_usuarios_con_permiso, asignar_permiso_usuario, revocar_permiso_usuario,
    get_bodegas_safe, get_bodega_by_id_safe, insert_bodega_safe, update_bodega_safe, delete_bodega_safe,
    get_obras_de_bodega, asignar_bodega_a_obra, remover_bodega_de_obra,
    get_presupuestos_safe, insert_presupuesto_safe, get_presupuesto_by_id_safe, update_presupuesto_safe, delete_presupuesto_safe,
    get_avances_safe, insert_avance_safe, get_avance_by_id_safe, update_avance_safe, delete_avance_safe,
    get_requisiciones_safe, get_requisicion_by_id_safe, insert_requisicion_safe, update_requisicion_safe, delete_requisicion_safe,
    get_movimientos_materiales_safe, get_movimiento_material_by_id_safe, insert_movimiento_material_safe, 
    update_movimiento_material_safe, delete_movimiento_material_safe,
    get_trabajos_safe, insert_trabajo_safe, get_trabajo_by_id_safe, update_trabajo_safe, delete_trabajo_safe,
    # Funciones de facturación
    get_facturas_safe, get_contratos_facturables_safe, insert_factura_safe,
    get_factura_by_id_safe, update_factura_safe, delete_factura_safe,
    get_detalles_factura_safe, insert_detalle_factura_safe, get_pagos_factura_safe,
    generar_numero_factura_safe, facturizar_contrato_safe,
    # Funciones de autenticación
    validar_usuario_login, obtener_permisos_usuario, crear_usuario_sistema,
    obtener_roles_disponibles, cambiar_password_usuario, registrar_auditoria_login,
    verificar_permiso_usuario, obtener_usuarios_sistema, bloquear_desbloquear_usuario,
    registrar_nuevo_usuario, validar_datos_registro, validar_usuario_login_real,
    get_usuario_by_id_safe, update_usuario_safe, eliminar_usuario_sistema,
    # CRUD extendidos
    get_empleado_by_id_safe, update_empleado_safe, delete_empleado_safe,
    get_vehiculo_by_id_safe, update_vehiculo_safe, delete_vehiculo_safe,
    # Nuevos CRUD de módulos
    get_proveedor_by_id_safe, update_proveedor_safe, delete_proveedor_safe,
    get_material_by_id_safe, update_material_safe, update_material_completo_safe, delete_material_safe,
    get_equipo_by_id_safe, update_equipo_safe, delete_equipo_safe,
    get_proyecto_by_id_safe, update_proyecto_safe, delete_proyecto_safe,
    get_obra_by_id_safe, update_obra_safe, delete_obra_safe,
    # Catálogo de tipos de obra
    get_tipos_obra_safe, get_tipo_obra_by_id_safe,
    insert_tipo_obra_safe, update_tipo_obra_safe, toggle_tipo_obra_activo_safe,
    # Funciones de asignaciones de obras
    get_empleados_asignados_obra_safe, get_materiales_asignados_obra_safe,
    get_vehiculos_asignados_obra_safe, get_resumen_asignaciones_obra_safe,
    # Funciones de asignaciones de proyectos
    get_obras_asignadas_proyecto_safe, get_empleados_asignados_proyecto_safe,
    get_vehiculos_asignados_proyecto_safe, get_resumen_asignaciones_proyecto_safe,
    # Funciones de inventario
    get_inventarios_safe, get_inventario_by_id_safe, insert_inventario_safe, 
    update_inventario_safe, delete_inventario_safe,
    asignar_materiales_inventario_safe, asignar_bodegas_inventario_safe,
    # Funciones de compras
    get_compras_safe, get_compra_by_id_safe, insert_compra_safe,
    update_compra_safe, delete_compra_safe,
    # Funciones de pagos
    get_pagos_safe, get_pago_by_id_safe, insert_pago_safe,
    update_pago_safe, delete_pago_safe,
    # Funciones de nómina
    get_nominas_safe, get_nomina_by_id_safe, insert_nomina_safe,
    calcular_nomina_safe, update_nomina_safe, delete_nomina_safe
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

# ===============================
# FILTROS JINJA2 PERSONALIZADOS
# ===============================
from datetime import datetime, date

@app.template_filter('strftime')
def strftime_filter(value, format='%Y-%m-%d'):
    """Filtro para formatear fechas con strftime"""
    if isinstance(value, str):
        if value.lower() == 'now':
            return date.today().strftime(format)
        try:
            # Intentar parsear string como fecha
            dt = datetime.strptime(value, '%Y-%m-%d')
            return dt.strftime(format)
        except:
            return value
    elif isinstance(value, (date, datetime)):
        return value.strftime(format)
    else:
        return str(value)

@app.template_filter('format_date')
def format_date_filter(value, format='%d/%m/%Y'):
    """Filtro para formatear fechas en español"""
    if isinstance(value, str):
        try:
            dt = datetime.strptime(value, '%Y-%m-%d')
            return dt.strftime(format)
        except:
            return value
    elif isinstance(value, (date, datetime)):
        return value.strftime(format)
    else:
        return str(value)

@app.template_filter('format_time')
def format_time_filter(value, format='%H:%M'):
    """Filtro para formatear horas"""
    if isinstance(value, str):
        try:
            dt = datetime.strptime(value, '%H:%M:%S')
            return dt.strftime(format)
        except:
            return value
    else:
        return str(value)

print("🚀 Sistema de Constructora - SISTEMA COMPLETO")
print("📍 Servidor ejecutándose en: http://127.0.0.1:5000")
print("💡 Gestión completa de las 56 tablas - 100% server-side")
print("🏗️  Módulos: Obras, Clientes, Empleados, Proveedores, Materiales, Vehículos, Equipos")

# ===============================
# DECORADORES Y FUNCIONES DE AUTENTICACIÓN
# ===============================
def login_requerido(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def permiso_requerido(codigo_permiso):
    """Decorador para rutas que requieren permisos específicos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'usuario_id' not in session:
                flash('Debes iniciar sesión', 'warning')
                return redirect(url_for('login'))
            
            usuario_id = session['usuario_id']
            if not verificar_permiso_usuario(usuario_id, codigo_permiso):
                flash('No tienes permisos suficientes para esta acción', 'error')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ===============================
# RUTAS DE AUTENTICACIÓN
# ===============================
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        recordar = request.form.get('recordar') == 'on'
        
        if not username or not password:
            flash('Usuario y contraseña son obligatorios', 'error')
            return render_template('auth/login.html')
        
        # Validar usuario usando la función que coincide con la estructura real
        usuario = validar_usuario_login_real(username, password)
        
        if usuario:
            # Login exitoso - crear sesión
            session['usuario_id'] = usuario['id_usuario']
            session['usuario_nombre'] = usuario['nombre_completo'] or usuario['nombre_usuario']
            session['usuario_rol'] = usuario['nombre_rol']
            session['usuario_email'] = usuario['email']
            
            # Configurar duración de sesión
            if recordar:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=30)
            else:
                session.permanent = False
                app.permanent_session_lifetime = timedelta(hours=8)
            
            # Obtener permisos del usuario
            permisos = obtener_permisos_usuario(usuario['id_usuario'])
            session['permisos'] = [p['codigo_permiso'] for p in permisos]
            
            # Registrar auditoría
            ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            user_agent = request.headers.get('User-Agent')
            registrar_auditoria_login(usuario['id_usuario'], 'LOGIN_EXITOSO', ip_address, user_agent)
            
            flash(f'¡Bienvenido, {usuario["nombre_completo"] or usuario["nombre_usuario"]}!', 'success')
            
            # Redireccionar a página solicitada o dashboard
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            # Login fallido
            registrar_auditoria_login(None, 'LOGIN_FALLIDO', 
                                    request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
                                    f'Usuario: {username}')
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('auth/login.html')

@app.route('/logout')
@login_requerido
def logout():
    """Cerrar sesión"""
    usuario_nombre = session.get('usuario_nombre', 'Usuario')
    usuario_id = session.get('usuario_id')
    
    # Registrar auditoría
    if usuario_id:
        registrar_auditoria_login(usuario_id, 'LOGOUT')
    
    # Limpiar sesión
    session.clear()
    
    flash(f'¡Hasta luego, {usuario_nombre}!', 'info')
    return redirect(url_for('login'))

@app.route('/recuperar-password', methods=['GET', 'POST'])
def recuperar_password():
    """Recuperación de contraseña"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('El email es obligatorio', 'error')
            return render_template('auth/recuperar_password.html')
        
        try:
            # Verificar si el email existe en el sistema
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, nombre FROM usuarios WHERE email = %s AND activo = true", (email,))
            usuario = cur.fetchone()
            
            if usuario:
                # Generar token único y seguro
                import secrets
                import hashlib
                from datetime import datetime, timedelta
                
                token = secrets.token_urlsafe(32)
                token_hash = hashlib.sha256(token.encode()).hexdigest()
                expiracion = datetime.now() + timedelta(hours=1)  # Token válido por 1 hora
                
                # Guardar token en base de datos (necesitaríamos crear tabla de tokens)
                # Por ahora, guardamos en sesión temporalmente
                session[f'recovery_token_{usuario[0]}'] = {
                    'token': token_hash,
                    'expiracion': expiracion.isoformat(),
                    'usuario_id': usuario[0],
                    'email': email
                }
                
                # En un entorno de producción, aquí se enviaría el email
                # Simulamos el envío creando un link de recuperación
                recovery_url = url_for('reset_password', token=token, _external=True)
                
                # Log del intento de recuperación para seguridad
                cur.execute("""
                    INSERT INTO auditorias (tabla_afectada, accion, usuario, descripcion, fecha) 
                    VALUES (%s, %s, %s, %s, NOW())
                """, ('usuarios', 'recuperacion_password', email, f'Solicitud de recuperación de contraseña para {email}'))
                
                conn.commit()
                
                # En desarrollo, mostramos el link en un mensaje
                flash(f'Se han enviado las instrucciones de recuperación a {email}. Link temporal: {recovery_url}', 'info')
                
            else:
                # Por seguridad, no revelar si el email existe o no
                flash(f'Si el email {email} está registrado, recibirá las instrucciones de recuperación.', 'info')
            
            cur.close()
            conn.close()
            
        except Exception as e:
            flash(f'Error al procesar la solicitud: {str(e)}', 'error')
        
        return redirect(url_for('login'))
    
    return render_template('auth/recuperar_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Resetear contraseña con token"""
    import hashlib
    from datetime import datetime
    
    # Buscar token válido en sesiones activas
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    token_data = None
    
    # Buscar el token en las sesiones
    for key in list(session.keys()):
        if key.startswith('recovery_token_'):
            data = session[key]
            if data.get('token') == token_hash:
                # Verificar si no ha expirado
                expiracion = datetime.fromisoformat(data['expiracion'])
                if datetime.now() < expiracion:
                    token_data = data
                    break
                else:
                    # Token expirado, eliminarlo
                    session.pop(key, None)
    
    if not token_data:
        flash('El enlace de recuperación es inválido o ha expirado.', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nueva_password = request.form.get('nueva_password', '').strip()
        confirmar_password = request.form.get('confirmar_password', '').strip()
        
        # Validaciones
        if not nueva_password or not confirmar_password:
            flash('Todos los campos son obligatorios', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if nueva_password != confirmar_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if len(nueva_password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        try:
            # Actualizar contraseña
            conn = get_connection()
            cur = conn.cursor()
            
            password_hash = generate_password_hash(nueva_password)
            cur.execute(
                "UPDATE usuarios SET password = %s WHERE id = %s AND activo = true",
                (password_hash, token_data['usuario_id'])
            )
            
            if cur.rowcount > 0:
                # Registrar cambio en auditoría
                cur.execute("""
                    INSERT INTO auditorias (tabla_afectada, accion, usuario, descripcion, fecha) 
                    VALUES (%s, %s, %s, %s, NOW())
                """, ('usuarios', 'reset_password', token_data['email'], 'Contraseña restablecida exitosamente'))
                
                conn.commit()
                
                # Limpiar token de la sesión
                for key in list(session.keys()):
                    if key.startswith('recovery_token_'):
                        data = session[key]
                        if data.get('usuario_id') == token_data['usuario_id']:
                            session.pop(key, None)
                
                flash('Tu contraseña ha sido restablecida exitosamente. Ya puedes iniciar sesión.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error al actualizar la contraseña. Intenta nuevamente.', 'error')
            
            cur.close()
            conn.close()
            
        except Exception as e:
            flash(f'Error al resetear la contraseña: {str(e)}', 'error')
        
        return render_template('auth/reset_password.html', token=token)
    
    return render_template('auth/reset_password.html', token=token, email=token_data.get('email'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de nuevos usuarios"""
    if request.method == 'POST':
        # Recopilar datos del formulario
        datos_usuario = {
            'nombre_completo': request.form.get('nombre_completo', '').strip(),
            'email': request.form.get('email', '').strip(),
            'nombre_usuario': request.form.get('nombre_usuario', '').strip(),
            'password': request.form.get('password', ''),
            'confirmar_password': request.form.get('confirmar_password', ''),
            'cargo': request.form.get('cargo', ''),
            'departamento': request.form.get('departamento', ''),
            'terminos': request.form.get('terminos') == 'on'
        }
        
        # Validar datos
        errores = validar_datos_registro(datos_usuario)
        
        if errores:
            for error in errores:
                flash(error, 'error')
            return render_template('auth/registro.html')
        
        # Intentar registrar el usuario
        exito, mensaje = registrar_nuevo_usuario(datos_usuario)
        
        if exito:
            flash(mensaje, 'success')
            flash('¡Bienvenido! Ahora puedes iniciar sesión con tus credenciales.', 'info')
            return redirect(url_for('login'))
        else:
            flash(mensaje, 'error')
            return render_template('auth/registro.html')
    
    return render_template('auth/registro.html')

@app.route('/cambiar-password', methods=['GET', 'POST'])
@login_requerido
def cambiar_password():
    """Cambiar contraseña del usuario actual"""
    if request.method == 'POST':
        password_actual = request.form.get('password_actual', '')
        password_nuevo = request.form.get('password_nuevo', '')
        password_confirmacion = request.form.get('password_confirmacion', '')
        
        if not all([password_actual, password_nuevo, password_confirmacion]):
            flash('Todos los campos son obligatorios', 'error')
            return render_template('auth/cambiar_password.html')
        
        if password_nuevo != password_confirmacion:
            flash('La nueva contraseña y su confirmación no coinciden', 'error')
            return render_template('auth/cambiar_password.html')
        
        if len(password_nuevo) < 8:
            flash('La nueva contraseña debe tener al menos 8 caracteres', 'error')
            return render_template('auth/cambiar_password.html')
        
        usuario_id = session['usuario_id']
        if cambiar_password_usuario(usuario_id, password_actual, password_nuevo):
            flash('Contraseña cambiada exitosamente', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Contraseña actual incorrecta', 'error')
    
    return render_template('auth/cambiar_password.html')

# ===============================
# GESTIÓN DE USUARIOS DEL SISTEMA
# ===============================
@app.route('/usuarios')
@login_requerido
@permiso_requerido('ADMIN_USUARIOS')
def listar_usuarios_sistema():
    """Listar usuarios del sistema"""
    try:
        usuarios = obtener_usuarios_sistema()
        roles = obtener_roles_disponibles()
        empleados = get_empleados_safe()
        return render_template('usuarios/listar.html', 
                             usuarios=usuarios, roles=roles, empleados=empleados)
    except Exception as e:
        flash(f'Error cargando usuarios: {e}', 'error')
        return render_template('usuarios/listar.html', 
                             usuarios=[], roles=[], empleados=[])

@app.route('/usuarios/nuevo', methods=['GET'])
@login_requerido
@permiso_requerido('ADMIN_USUARIOS')
def mostrar_crear_usuario():
    """Mostrar formulario para crear nuevo usuario"""
    try:
        roles = obtener_roles_disponibles()
        empleados = get_empleados_safe()
        return render_template('usuarios/crear.html', roles=roles, empleados=empleados)
    except Exception as e:
        flash(f'Error cargando datos del formulario: {e}', 'error')
        return redirect(url_for('listar_usuarios_sistema'))

@app.route('/usuarios/crear', methods=['POST'])
@login_requerido
@permiso_requerido('ADMIN_USUARIOS')
def crear_usuario_sistema_route():
    """Crear nuevo usuario del sistema"""
    try:
        nombre_usuario = request.form.get('nombre_usuario', '').strip()
        password = request.form.get('password', '').strip()
        email = request.form.get('email', '').strip()
        nombre_completo = request.form.get('nombre_completo', '').strip()
        id_empleado = request.form.get('id_empleado') or None
        id_rol = request.form.get('id_rol', '').strip() or None
        activo = request.form.get('activo') == 'on'
        
        # Validación de campos obligatorios
        if not all([nombre_usuario, password, email, nombre_completo, id_rol]):
            error_msg = 'Faltan campos obligatorios: nombre de usuario, contraseña, email, nombre completo y rol'
            
            # Si es AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': error_msg}), 400
            
            # Si es formulario HTML, mostrar flash y redirect
            flash(error_msg, 'error')
            return redirect(url_for('mostrar_crear_usuario'))
        
        # Crear usuario usando la función de database
        usuario_id = crear_usuario_sistema(nombre_usuario, password, email, nombre_completo, id_empleado, id_rol)
        
        if usuario_id:
            flash('Usuario creado exitosamente', 'success')
            
            # Si es AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': True, 'usuario_id': usuario_id})
            
            # Si es formulario HTML, redirect
            return redirect(url_for('listar_usuarios_sistema'))
        else:
            error_msg = 'Error al crear usuario'
            
            # Si es AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'error': error_msg}), 500
            
            # Si es formulario HTML, mostrar flash y redirect
            flash(error_msg, 'error')
            return redirect(url_for('mostrar_crear_usuario'))
            
    except Exception as e:
        logger.error(f'Error creando usuario: {e}')
        error_msg = f'Error al crear usuario: {str(e)}'
        
        # Si es AJAX, devolver JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'error': error_msg}), 500
        
        # Si es formulario HTML, mostrar flash y redirect
        flash(error_msg, 'error')
        return redirect(url_for('mostrar_crear_usuario'))

@app.route('/usuarios/<int:id>/bloquear', methods=['POST'])
@login_requerido
@permiso_requerido('ADMIN_USUARIOS')
def bloquear_usuario_route(id):
    """Bloquear usuario"""
    try:
        if bloquear_desbloquear_usuario(id, True):
            registrar_auditoria_login(session['usuario_id'], 'BLOQUEAR_USUARIO')
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Error bloqueando usuario'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/usuarios/<int:id>/desbloquear', methods=['POST'])
@login_requerido
@permiso_requerido('ADMIN_USUARIOS')
def desbloquear_usuario_route(id):
    """Desbloquear usuario"""
    try:
        if bloquear_desbloquear_usuario(id, False):
            registrar_auditoria_login(session['usuario_id'], 'DESBLOQUEAR_USUARIO')
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Error desbloqueando usuario'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_requerido
@permiso_requerido('ADMIN_USUARIOS')
def editar_usuario_sistema_route(id):
    """Ver/Editar un usuario del sistema (solo administradores)."""
    try:
        if request.method == 'POST':
            nombre_usuario = request.form.get('nombre_usuario', '').strip()
            email = request.form.get('email', '').strip()
            nombre_completo = request.form.get('nombre_completo', '').strip()
            id_empleado = request.form.get('id_empleado') or None
            id_rol = request.form.get('id_rol') or None

            datos = {
                'nombre_usuario': nombre_usuario,
                'email': email,
                'nombre_completo': nombre_completo,
                'id_empleado': int(id_empleado) if id_empleado else None,
                'id_rol': int(id_rol) if id_rol else None
            }

            # Limpiar claves None para evitar updates innecesarios
            datos = {k: v for k, v in datos.items() if v is not None and v != ''}

            if not datos.get('nombre_usuario'):
                flash('El nombre de usuario es obligatorio', 'error')
                return redirect(url_for('editar_usuario_sistema_route', id=id))

            if update_usuario_safe(id, datos):
                flash('Usuario actualizado correctamente', 'success')
                return redirect(url_for('listar_usuarios_sistema'))
            else:
                flash('No se pudieron aplicar los cambios', 'error')
                return redirect(url_for('editar_usuario_sistema_route', id=id))

        # GET: cargar datos
        usuario = get_usuario_by_id_safe(id)
        if not usuario:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('listar_usuarios_sistema'))

        roles = obtener_roles_disponibles()
        empleados = get_empleados_safe()
        return render_template('usuarios/editar.html', usuario=usuario, roles=roles, empleados=empleados)
    except Exception as e:
        flash(f'Error: {e}', 'error')
        return redirect(url_for('listar_usuarios_sistema'))

@app.route('/usuarios/<int:id>/eliminar', methods=['POST'])
@login_requerido
@permiso_requerido('ADMIN_USUARIOS')
def eliminar_usuario(id):
    """Eliminar un usuario del sistema"""
    try:
        # Verificar que el usuario existe
        usuario = get_usuario_by_id_safe(id)
        if not usuario:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('listar_usuarios_sistema'))
        
        # No permitir eliminar al propio usuario
        if session.get('usuario_id') == id:
            flash('No puedes eliminar tu propio usuario', 'error')
            return redirect(url_for('listar_usuarios_sistema'))
        
        # Eliminar el usuario
        if eliminar_usuario_sistema(id):
            flash(f'Usuario {usuario.get("nombre_usuario", "desconocido")} eliminado correctamente', 'success')
        else:
            flash('Error al eliminar el usuario', 'error')
            
    except Exception as e:
        flash(f'Error eliminando usuario: {str(e)}', 'error')
    
    return redirect(url_for('listar_usuarios_sistema'))

# Alias para compatibilidad con el diagnóstico
def listar_usuarios():
    """Alias de listar_usuarios_sistema"""
    return listar_usuarios_sistema()

def crear_usuario():
    """Alias de mostrar_crear_usuario"""
    return mostrar_crear_usuario()

def ver_usuario(id):
    """Ver detalle de usuario específico"""
    try:
        usuario = get_usuario_by_id_safe(id)
        if not usuario:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('listar_usuarios_sistema'))
        return render_template('usuarios/detalle.html', usuario=usuario)
    except Exception as e:
        flash(f'Error cargando usuario: {str(e)}', 'error')
        return redirect(url_for('listar_usuarios_sistema'))

def editar_usuario(id):
    """Editar usuario específico"""
    try:
        usuario = get_usuario_by_id_safe(id)
        if not usuario:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('listar_usuarios_sistema'))
        
        roles = obtener_roles_disponibles()
        return render_template('usuarios/editar.html', usuario=usuario, roles=roles)
    except Exception as e:
        flash(f'Error cargando usuario para edición: {str(e)}', 'error')
        return redirect(url_for('listar_usuarios_sistema'))

# ===============================
# DASHBOARD PRINCIPAL
# ===============================
@app.route('/')
@login_requerido
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
        facturas = get_facturas_safe()
        contratos = get_contratos_safe()
        actividades = get_actividades_safe()
        bitacoras = get_bitacoras_safe()
        
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
            'total_proyectos': len(proyectos),
            'total_facturas': len(facturas),
            'total_contratos': len(contratos),
            'total_actividades': len(actividades),
            'total_bitacoras': len(bitacoras)
        }
        
        obras_recientes = obras[:5]  # Últimas 5 obras
        return render_template('dashboard.html', stats=stats, obras_recientes=obras_recientes)
    except Exception as e:
        logger.error(f'Error en dashboard: {e}')
        stats = {
            'total_obras': 0, 'obras_activas': 0, 'obras_completadas': 0, 'valor_total': 0,
            'total_clientes': 0, 'total_empleados': 0, 'total_proveedores': 0,
            'total_materiales': 0, 'total_vehiculos': 0, 'total_equipos': 0, 'total_proyectos': 0,
            'total_facturas': 0, 'total_contratos': 0, 'total_actividades': 0, 'total_bitacoras': 0
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
        tipos_obra = get_tipos_obra_safe()
        return render_template('obras/crear.html', clientes=clientes, tipos_obra=tipos_obra)
    
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
            if not cliente_id or cliente_id.strip() == '' or cliente_id == 'None':
                flash('Debe seleccionar un cliente existente', 'error')
                clientes = get_clientes_safe()
                tipos_obra = get_tipos_obra_safe()
                return render_template('obras/crear.html', clientes=clientes, tipos_obra=tipos_obra)
            
            # Convertir cliente_id a entero para validación
            try:
                cliente_id = int(cliente_id)
            except (ValueError, TypeError):
                flash('ID de cliente inválido', 'error')
                clientes = get_clientes_safe()
                tipos_obra = get_tipos_obra_safe()
                return render_template('obras/crear.html', clientes=clientes, tipos_obra=tipos_obra)
        
        elif tipo_cliente == 'nuevo':
            # Crear nuevo cliente
            nuevo_cliente_nombre = request.form.get('nuevo_cliente_nombre', '').strip()
            if not nuevo_cliente_nombre:
                flash('El nombre del cliente es obligatorio', 'error')
                clientes = get_clientes_safe()
                tipos_obra = get_tipos_obra_safe()
                return render_template('obras/crear.html', clientes=clientes, tipos_obra=tipos_obra)
            
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
                tipos_obra = get_tipos_obra_safe()
                return render_template('obras/crear.html', clientes=clientes, tipos_obra=tipos_obra)
        
        else:
            flash('Debe especificar un cliente para la obra', 'error')
            clientes = get_clientes_safe()
            tipos_obra = get_tipos_obra_safe()
            return render_template('obras/crear.html', clientes=clientes, tipos_obra=tipos_obra)
        
        # Convertir valor a número si se proporciona
        valor_numerico = None
        if valor:
            try:
                valor_numerico = float(valor)
            except ValueError:
                valor_numerico = None
        
        # Campos opcionales: tipo de obra fijo
        id_tipo_obra_raw = request.form.get('id_tipo_obra')
        id_tipo_obra = int(id_tipo_obra_raw) if id_tipo_obra_raw not in (None, '', '0') else None
        es_precio_fijo = True if request.form.get('es_precio_fijo') == 'on' else None

        # Campos de estimación para cotización
        unidad_estimacion = request.form.get('unidad_estimacion') or None
        area_m2_raw = request.form.get('area_m2')
        cantidad_estimada_raw = request.form.get('cantidad_estimada')
        precio_unitario_estimado_raw = request.form.get('precio_unitario_estimado')
        area_m2 = None
        cantidad_estimada = None
        precio_unitario_estimado = None
        try:
            if area_m2_raw not in (None, ''):
                area_m2 = float(area_m2_raw)
        except ValueError:
            area_m2 = None
        try:
            if cantidad_estimada_raw not in (None, ''):
                cantidad_estimada = float(cantidad_estimada_raw)
        except ValueError:
            cantidad_estimada = None
        try:
            if precio_unitario_estimado_raw not in (None, ''):
                precio_unitario_estimado = float(precio_unitario_estimado_raw)
        except ValueError:
            precio_unitario_estimado = None

        # Crear obra con cliente obligatorio
        nueva_obra_id = insert_obra_safe(
            nombre=nombre,
            descripcion=descripcion,
            ubicacion=ubicacion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            valor=valor_numerico,
            estado=estado,
            cliente_id=cliente_id,
            id_tipo_obra=id_tipo_obra,
            es_precio_fijo=es_precio_fijo,
            unidad_estimacion=unidad_estimacion,
            area_m2=area_m2,
            cantidad_estimada=cantidad_estimada,
            precio_unitario_estimado=precio_unitario_estimado
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
    tipos_obra = get_tipos_obra_safe()
    return render_template('obras/crear.html', clientes=clientes, tipos_obra=tipos_obra)

# Detalle/Editar/Eliminar Obra
@app.route('/obras/<int:id>')
def ver_obra(id):
    try:
        o = get_obra_by_id_safe(id)
        if not o:
            flash('Obra no encontrada', 'error')
            return redirect(url_for('listar_obras'))
        
        # Obtener asignaciones de recursos para la obra
        asignaciones = get_resumen_asignaciones_obra_safe(id)
        
        return render_template('obras/detalle.html', obra=o, asignaciones=asignaciones)
    except Exception as e:
        flash(f'Error al cargar obra: {str(e)}', 'error')
        return redirect(url_for('listar_obras'))

@app.route('/obras/<int:id>/editar', methods=['GET', 'POST'])
def editar_obra(id):
    if request.method == 'GET':
        o = get_obra_by_id_safe(id)
        clientes = get_clientes_safe()
        tipos_obra = get_tipos_obra_safe()
        if not o:
            flash('Obra no encontrada', 'error')
            return redirect(url_for('listar_obras'))
        return render_template('obras/editar.html', obra=o, clientes=clientes, tipos_obra=tipos_obra)
    try:
        nombre = request.form.get('nombre') or None
        descripcion = request.form.get('descripcion') or None
        ubicacion = request.form.get('ubicacion') or None
        fecha_inicio = request.form.get('fecha_inicio') or None
        fecha_fin = request.form.get('fecha_fin') or None
        valor_raw = request.form.get('valor')
        valor = None
        if valor_raw not in (None, ''):
            try:
                valor = float(valor_raw)
            except ValueError:
                valor = None
        estado = request.form.get('estado') or None
        id_cliente = request.form.get('id_cliente') or None
        # Campos opcionales para obra fija
        id_tipo_obra_raw = request.form.get('id_tipo_obra')
        id_tipo_obra = int(id_tipo_obra_raw) if id_tipo_obra_raw not in (None, '', '0') else None
        es_precio_fijo = True if request.form.get('es_precio_fijo') == 'on' else None

        # Campos de estimación
        unidad_estimacion = request.form.get('unidad_estimacion') or None
        area_m2_raw = request.form.get('area_m2')
        cantidad_estimada_raw = request.form.get('cantidad_estimada')
        precio_unitario_estimado_raw = request.form.get('precio_unitario_estimado')
        area_m2 = None
        cantidad_estimada = None
        precio_unitario_estimado = None
        try:
            if area_m2_raw not in (None, ''):
                area_m2 = float(area_m2_raw)
        except ValueError:
            area_m2 = None
        try:
            if cantidad_estimada_raw not in (None, ''):
                cantidad_estimada = float(cantidad_estimada_raw)
        except ValueError:
            cantidad_estimada = None
        try:
            if precio_unitario_estimado_raw not in (None, ''):
                precio_unitario_estimado = float(precio_unitario_estimado_raw)
        except ValueError:
            precio_unitario_estimado = None

        ok = update_obra_safe(
            id,
            nombre=nombre,
            descripcion=descripcion,
            ubicacion=ubicacion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            valor=valor,
            estado=estado,
            id_cliente=id_cliente,
            id_tipo_obra=id_tipo_obra,
            es_precio_fijo=es_precio_fijo,
            unidad_estimacion=unidad_estimacion,
            area_m2=area_m2,
            cantidad_estimada=cantidad_estimada,
            precio_unitario_estimado=precio_unitario_estimado
        )
        if ok:
            flash('Obra actualizada', 'success')
            return redirect(url_for('ver_obra', id=id))
        flash('No se pudo actualizar la obra', 'error')
        return redirect(url_for('editar_obra', id=id))
    except Exception as e:
        flash(f'Error al actualizar obra: {str(e)}', 'error')
        return redirect(url_for('editar_obra', id=id))

@app.route('/obras/<int:id>/eliminar', methods=['POST'])
def eliminar_obra(id):
    try:
        ok = delete_obra_safe(id)
        if ok:
            flash('Obra eliminada', 'success')
        else:
            flash('No se pudo eliminar la obra', 'error')
    except Exception as e:
        flash(f'Error al eliminar obra: {str(e)}', 'error')
    return redirect(url_for('listar_obras'))

# ===============================
# CATÁLOGO TIPOS_OBRA
# ===============================
@app.route('/tipos-obra')
def tipos_obra_listar():
    try:
        mostrar_todos = request.args.get('todos') == '1'
        tipos = get_tipos_obra_safe(activos_only=not mostrar_todos)
        return render_template('tipos_obra/listar.html', tipos=tipos, mostrar_todos=mostrar_todos)
    except Exception as e:
        flash(f'Error al cargar tipos de obra: {e}', 'error')
        return render_template('tipos_obra/listar.html', tipos=[], mostrar_todos=False)

@app.route('/tipos-obra/nuevo', methods=['GET','POST'])
def tipos_obra_nuevo():
    if request.method == 'GET':
        return render_template('tipos_obra/crear.html')
    try:
        nombre = request.form.get('nombre_tipo')
        descripcion = request.form.get('descripcion_base')
        unidad = request.form.get('unidad_medida')
        rango = request.form.get('rango_precio')
        notas = request.form.get('notas')
        precio_min = request.form.get('precio_min') or None
        precio_max = request.form.get('precio_max') or None
        precio_base = request.form.get('precio_base') or 0
        # Convertir números
        precio_min = float(precio_min) if precio_min not in (None, '') else None
        precio_max = float(precio_max) if precio_max not in (None, '') else None
        precio_base = float(precio_base) if precio_base not in (None, '') else 0
        if not nombre:
            flash('El nombre del tipo es obligatorio', 'error')
            return render_template('tipos_obra/crear.html')
        new_id = insert_tipo_obra_safe(nombre, descripcion, unidad, rango, notas, precio_min, precio_max, precio_base, True)
        if new_id:
            flash('Tipo de obra creado', 'success')
            return redirect(url_for('tipos_obra_listar'))
        flash('No se pudo crear el tipo de obra', 'error')
        return render_template('tipos_obra/crear.html')
    except Exception as e:
        flash(f'Error creando tipo de obra: {e}', 'error')
        return render_template('tipos_obra/crear.html')

@app.route('/tipos-obra/<int:id>/editar', methods=['GET','POST'])
def tipos_obra_editar(id):
    if request.method == 'GET':
        t = get_tipo_obra_by_id_safe(id)
        if not t:
            flash('Tipo de obra no encontrado', 'error')
            return redirect(url_for('tipos_obra_listar'))
        return render_template('tipos_obra/editar.html', t=t)
    try:
        nombre = request.form.get('nombre_tipo') or None
        descripcion = request.form.get('descripcion_base') or None
        unidad = request.form.get('unidad_medida') or None
        rango = request.form.get('rango_precio') or None
        notas = request.form.get('notas') or None
        precio_min = request.form.get('precio_min')
        precio_max = request.form.get('precio_max')
        precio_base = request.form.get('precio_base')
        activo_raw = request.form.get('activo')
        precio_min = float(precio_min) if precio_min not in (None, '') else None
        precio_max = float(precio_max) if precio_max not in (None, '') else None
        precio_base = float(precio_base) if precio_base not in (None, '') else None
        activo = True if activo_raw == 'on' else None
        ok = update_tipo_obra_safe(id, nombre, descripcion, unidad, rango, notas, precio_min, precio_max, precio_base, activo)
        if ok:
            flash('Tipo de obra actualizado', 'success')
            return redirect(url_for('tipos_obra_listar'))
        flash('No se pudo actualizar el tipo de obra', 'error')
        return redirect(url_for('tipos_obra_editar', id=id))
    except Exception as e:
        flash(f'Error actualizando tipo de obra: {e}', 'error')
        return redirect(url_for('tipos_obra_editar', id=id))

@app.route('/tipos-obra/<int:id>/activar', methods=['POST'])
def tipos_obra_activar(id):
    try:
        ok = toggle_tipo_obra_activo_safe(id, True)
        flash('Tipo activado' if ok else 'No se pudo activar', 'success' if ok else 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('tipos_obra_listar', todos='1'))

@app.route('/tipos-obra/<int:id>/desactivar', methods=['POST'])
def tipos_obra_desactivar(id):
    try:
        ok = toggle_tipo_obra_activo_safe(id, False)
        flash('Tipo desactivado' if ok else 'No se pudo desactivar', 'success' if ok else 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    return redirect(url_for('tipos_obra_listar'))

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
        nombre = request.form.get('nombre_empleado', '').strip()
        apellido = request.form.get('apellido_empleado', '').strip()
        tipo = request.form.get('tipo_empleado', '').strip()
        salario_fijo = request.form.get('salario_fijo_empleado')
        telefono = request.form.get('telefono', '').strip()
        email = request.form.get('email', '').strip()
        fecha_ingreso = request.form.get('fecha_ingreso', '').strip()
        
        if not nombre:
            flash('El nombre del empleado es obligatorio', 'error')
            return render_template('empleados/crear.html')
        
        if not apellido:
            flash('El apellido del empleado es obligatorio', 'error')
            return render_template('empleados/crear.html')
        
        # Asignar salario automáticamente según el cargo
        salario_numerico = None
        if tipo and tipo in SALARIOS_POR_CARGO:
            salario_numerico = SALARIOS_POR_CARGO[tipo]
        elif salario_fijo:
            try:
                salario_numerico = float(salario_fijo)
            except ValueError:
                salario_numerico = None
        
        empleado_id = insert_empleado_safe(nombre=nombre, apellido=apellido, tipo=tipo, salario=salario_numerico, telefono=telefono, email=email, fecha_ingreso=fecha_ingreso)
        
        if empleado_id:
            flash(f'Empleado "{nombre} {apellido}" creado exitosamente', 'success')
            return redirect(url_for('listar_empleados'))
        else:
            flash('Error al crear empleado', 'error')
            return render_template('empleados/crear.html')
            
    except Exception as e:
        flash(f'Error al crear empleado: {str(e)}', 'error')
        return render_template('empleados/crear.html')

# Detalle/Editar/Eliminar Empleado
@app.route('/empleados/<int:id>')
def ver_empleado(id):
    try:
        emp = get_empleado_by_id_safe(id)
        if not emp:
            flash('Empleado no encontrado', 'error')
            return redirect(url_for('listar_empleados'))
        return render_template('empleados/detalle.html', empleado=emp)
    except Exception as e:
        flash(f'Error al cargar empleado: {str(e)}', 'error')
        return redirect(url_for('listar_empleados'))

@app.route('/empleados/<int:id>/editar', methods=['GET', 'POST'])
def editar_empleado(id):
    if request.method == 'GET':
        emp = get_empleado_by_id_safe(id)
        if not emp:
            flash('Empleado no encontrado', 'error')
            return redirect(url_for('listar_empleados'))
        return render_template('empleados/editar.html', empleado=emp)
    try:
        nombre = request.form.get('nombre_empleado') or None
        apellido = request.form.get('apellido_empleado') or None
        tipo = request.form.get('tipo_empleado') or None
        salario_fijo = request.form.get('salario_fijo_empleado')
        telefono = request.form.get('telefono') or None
        email = request.form.get('email') or None
        fecha_ingreso = request.form.get('fecha_ingreso') or None
        
        salario_val = None
        if salario_fijo not in (None, ''):
            try:
                salario_val = float(salario_fijo)
            except ValueError:
                salario_val = None
        ok = update_empleado_safe(id, nombre=nombre, apellido=apellido, tipo=tipo, salario=salario_val, telefono=telefono, email=email, fecha_ingreso=fecha_ingreso)
        if ok:
            flash('Empleado actualizado', 'success')
            return redirect(url_for('ver_empleado', id=id))
        flash('No se pudo actualizar el empleado', 'error')
        return redirect(url_for('editar_empleado', id=id))
    except Exception as e:
        flash(f'Error al actualizar empleado: {str(e)}', 'error')
        return redirect(url_for('editar_empleado', id=id))

@app.route('/empleados/<int:id>/eliminar', methods=['POST'])
def eliminar_empleado(id):
    try:
        ok = delete_empleado_safe(id)
        if ok:
            flash('Empleado eliminado', 'success')
        else:
            flash('No se pudo eliminar el empleado', 'error')
    except Exception as e:
        flash(f'Error al eliminar empleado: {str(e)}', 'error')
    return redirect(url_for('listar_empleados'))

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

# Detalle/Editar/Eliminar Proveedor
@app.route('/proveedores/<int:id>')
def ver_proveedor(id):
    try:
        p = get_proveedor_by_id_safe(id)
        if not p:
            flash('Proveedor no encontrado', 'error')
            return redirect(url_for('listar_proveedores'))
        return render_template('proveedores/detalle.html', proveedor=p)
    except Exception as e:
        flash(f'Error al cargar proveedor: {str(e)}', 'error')
        return redirect(url_for('listar_proveedores'))

@app.route('/proveedores/<int:id>/editar', methods=['GET', 'POST'])
def editar_proveedor(id):
    if request.method == 'GET':
        p = get_proveedor_by_id_safe(id)
        if not p:
            flash('Proveedor no encontrado', 'error')
            return redirect(url_for('listar_proveedores'))
        return render_template('proveedores/editar.html', proveedor=p)
    try:
        nombre = request.form.get('nombre') or None
        contacto = request.form.get('contacto') or None
        ok = update_proveedor_safe(id, nombre=nombre, contacto=contacto)
        if ok:
            flash('Proveedor actualizado', 'success')
            return redirect(url_for('ver_proveedor', id=id))
        flash('No se pudo actualizar el proveedor', 'error')
        return redirect(url_for('editar_proveedor', id=id))
    except Exception as e:
        flash(f'Error al actualizar proveedor: {str(e)}', 'error')
        return redirect(url_for('editar_proveedor', id=id))

@app.route('/proveedores/<int:id>/eliminar', methods=['POST'])
def eliminar_proveedor(id):
    try:
        ok = delete_proveedor_safe(id)
        if ok:
            flash('Proveedor eliminado', 'success')
        else:
            flash('No se pudo eliminar el proveedor', 'error')
    except Exception as e:
        flash(f'Error al eliminar proveedor: {str(e)}', 'error')
    return redirect(url_for('listar_proveedores'))

# ===============================
# GESTIÓN DE CLIENTES
# ===============================
@app.route('/clientes')
def listar_clientes():
    """Listar todos los clientes"""
    try:
        clientes = get_clientes_safe()
        return render_template('clientes/listar.html', clientes=clientes)
    except Exception as e:
        flash(f'Error al cargar clientes: {str(e)}', 'error')
        return render_template('clientes/listar.html', clientes=[])

@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def crear_cliente():
    """Crear nuevo cliente"""
    if request.method == 'GET':
        return render_template('clientes/crear.html')
    
    try:
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        telefono = request.form.get('telefono', '').strip()
        direccion = request.form.get('direccion', '').strip()
        tipo_cliente = request.form.get('tipo_cliente', '').strip()
        
        if not nombre:
            flash('El nombre del cliente es obligatorio', 'error')
            return render_template('clientes/crear.html')
        
        cliente_id = insert_cliente_safe(
            nombre=nombre,
            email=email,
            telefono=telefono,
            direccion=direccion,
            tipo_cliente=tipo_cliente
        )
        
        if cliente_id:
            flash(f'Cliente "{nombre}" creado exitosamente', 'success')
            return redirect(url_for('listar_clientes'))
        else:
            flash('Error al crear cliente', 'error')
            return render_template('clientes/crear.html')
            
    except Exception as e:
        flash(f'Error al crear cliente: {str(e)}', 'error')
        return render_template('clientes/crear.html')

@app.route('/clientes/<int:id>')
def ver_cliente(id):
    """Ver detalle de un cliente"""
    try:
        cliente = get_cliente_by_id_safe(id)
        if not cliente:
            flash('Cliente no encontrado', 'error')
            return redirect(url_for('listar_clientes'))
        return render_template('clientes/detalle.html', cliente=cliente)
    except Exception as e:
        flash(f'Error al cargar cliente: {str(e)}', 'error')
        return redirect(url_for('listar_clientes'))

@app.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_cliente(id):
    """Editar cliente"""
    if request.method == 'GET':
        try:
            cliente = get_cliente_by_id_safe(id)
            if not cliente:
                flash('Cliente no encontrado', 'error')
                return redirect(url_for('listar_clientes'))
            return render_template('clientes/editar.html', cliente=cliente)
        except Exception as e:
            flash(f'Error al cargar cliente: {str(e)}', 'error')
            return redirect(url_for('listar_clientes'))
    
    # POST - Actualizar
    try:
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        telefono = request.form.get('telefono', '').strip()
        direccion = request.form.get('direccion', '').strip()
        tipo_cliente = request.form.get('tipo_cliente', '').strip()
        
        if not nombre:
            flash('El nombre del cliente es obligatorio', 'error')
            cliente = get_cliente_by_id_safe(id)
            return render_template('clientes/editar.html', cliente=cliente)
        
        ok = update_cliente_safe(id, nombre=nombre, email=email, telefono=telefono, direccion=direccion, tipo_cliente=tipo_cliente)
        
        if ok:
            flash('Cliente actualizado exitosamente', 'success')
            return redirect(url_for('ver_cliente', id=id))
        else:
            flash('Error al actualizar el cliente', 'error')
            cliente = get_cliente_by_id_safe(id)
            return render_template('clientes/editar.html', cliente=cliente)
            
    except Exception as e:
        flash(f'Error al actualizar cliente: {str(e)}', 'error')
        cliente = get_cliente_by_id_safe(id)
        return render_template('clientes/editar.html', cliente=cliente)

@app.route('/clientes/<int:id>/eliminar', methods=['POST'])
def eliminar_cliente(id):
    """Eliminar cliente"""
    try:
        ok = delete_cliente_safe(id)
        if ok:
            flash('Cliente eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar el cliente', 'error')
    except Exception as e:
        flash(f'Error al eliminar cliente: {str(e)}', 'error')
    return redirect(url_for('listar_clientes'))

# ===============================
# GESTIÓN DE MATERIALES
# ===============================
@app.route('/materiales')
def listar_materiales():
    """Listar todos los materiales"""
    try:
        materiales = get_materiales_safe()
        return render_template('materiales/listar_modern.html', materiales=materiales)
    except Exception as e:
        flash(f'Error al cargar materiales: {str(e)}', 'error')
        return render_template('materiales/listar_modern.html', materiales=[])

@app.route('/materiales/nuevo', methods=['GET', 'POST'])
def crear_material():
    """Crear nuevo material"""
    if request.method == 'GET':
        proveedores = get_proveedores_safe()
        return render_template('materiales/crear_modern.html', proveedores=proveedores)
    
    try:
        nombre = request.form.get('nombre', '').strip()
        unidad = request.form.get('unidad_medida', '').strip()
        precio = request.form.get('precio_unitario')
        categoria = request.form.get('categoria', '').strip()
        
        if not nombre:
            flash('El nombre del material es obligatorio', 'error')
            proveedores = get_proveedores_safe()
            return render_template('materiales/crear_modern.html', proveedores=proveedores)
        
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
            proveedores = get_proveedores_safe()
            return render_template('materiales/crear_modern.html', proveedores=proveedores)
            
    except Exception as e:
        flash(f'Error al crear material: {str(e)}', 'error')
        proveedores = get_proveedores_safe()
        return render_template('materiales/crear_modern.html', proveedores=proveedores)

# Detalle/Editar/Eliminar Material
@app.route('/materiales/<int:id>')
def ver_material(id):
    try:
        m = get_material_by_id_safe(id)
        if not m:
            flash('Material no encontrado', 'error')
            return redirect(url_for('listar_materiales'))
        return render_template('materiales/detalle.html', material=m)
    except Exception as e:
        flash(f'Error al cargar material: {str(e)}', 'error')
        return redirect(url_for('listar_materiales'))

@app.route('/materiales/<int:id>/editar', methods=['GET', 'POST'])
def editar_material(id):
    if request.method == 'GET':
        m = get_material_by_id_safe(id)
        if not m:
            flash('Material no encontrado', 'error')
            return redirect(url_for('listar_materiales'))
        return render_template('materiales/editar.html', material=m)
    try:
        nombre = request.form.get('nombre') or None
        unidad = request.form.get('unidad') or request.form.get('unidad_medida') or None
        descripcion = request.form.get('descripcion') or None
        categoria = request.form.get('categoria') or None
        
        precio_raw = request.form.get('precio') or request.form.get('precio_unitario')
        precio = None
        if precio_raw not in (None, ''):
            try:
                precio = float(precio_raw)
            except ValueError:
                precio = None
        
        stock_raw = request.form.get('stock')
        stock = None
        if stock_raw not in (None, ''):
            try:
                stock = int(stock_raw)
            except ValueError:
                stock = None
        
        ok = update_material_completo_safe(id, nombre=nombre, unidad=unidad, precio=precio, 
                                         descripcion=descripcion, categoria=categoria, stock=stock)
        if ok:
            flash('Material actualizado completamente', 'success')
            return redirect(url_for('ver_material', id=id))
        flash('No se pudo actualizar el material', 'error')
        return redirect(url_for('editar_material', id=id))
    except Exception as e:
        flash(f'Error al actualizar material: {str(e)}', 'error')
        return redirect(url_for('editar_material', id=id))

@app.route('/materiales/<int:id>/eliminar', methods=['POST'])
def eliminar_material(id):
    try:
        ok = delete_material_safe(id)
        if ok:
            flash('Material eliminado', 'success')
        else:
            flash('No se pudo eliminar el material', 'error')
    except Exception as e:
        flash(f'Error al eliminar material: {str(e)}', 'error')
    return redirect(url_for('listar_materiales'))

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

# Detalle/Editar/Eliminar Vehículo
@app.route('/vehiculos/<int:id>')
def ver_vehiculo(id):
    try:
        v = get_vehiculo_by_id_safe(id)
        if not v:
            flash('Vehículo no encontrado', 'error')
            return redirect(url_for('listar_vehiculos'))
        return render_template('vehiculos/detalle.html', vehiculo=v)
    except Exception as e:
        flash(f'Error al cargar vehículo: {str(e)}', 'error')
        return redirect(url_for('listar_vehiculos'))

@app.route('/vehiculos/<int:id>/editar', methods=['GET', 'POST'])
def editar_vehiculo(id):
    if request.method == 'GET':
        v = get_vehiculo_by_id_safe(id)
        if not v:
            flash('Vehículo no encontrado', 'error')
            return redirect(url_for('listar_vehiculos'))
        return render_template('vehiculos/editar.html', vehiculo=v)
    try:
        placa = request.form.get('placa') or None
        estado = request.form.get('estado') or None
        tipo = request.form.get('tipo') or None
        ok = update_vehiculo_safe(id, placa=placa, estado=estado, tipo=tipo)
        if ok:
            flash('Vehículo actualizado', 'success')
            return redirect(url_for('ver_vehiculo', id=id))
        flash('No se pudo actualizar el vehículo', 'error')
        return redirect(url_for('editar_vehiculo', id=id))
    except Exception as e:
        flash(f'Error al actualizar vehículo: {str(e)}', 'error')
        return redirect(url_for('editar_vehiculo', id=id))

@app.route('/vehiculos/<int:id>/eliminar', methods=['POST'])
def eliminar_vehiculo(id):
    try:
        ok = delete_vehiculo_safe(id)
        if ok:
            flash('Vehículo eliminado', 'success')
        else:
            flash('No se pudo eliminar el vehículo', 'error')
    except Exception as e:
        flash(f'Error al eliminar vehículo: {str(e)}', 'error')
    return redirect(url_for('listar_vehiculos'))

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
        proveedores = get_proveedores_safe()
        return render_template('equipos/crear_modern.html', proveedores=proveedores)
    
    try:
        nombre = request.form.get('nombre', '').strip()
        estado = request.form.get('estado_actual', '').strip()
        tipo = request.form.get('tipo_equipo', '').strip()
        marca = request.form.get('marca', '').strip()
        modelo = request.form.get('modelo', '').strip()
        
        if not nombre:
            flash('El nombre del equipo es obligatorio', 'error')
            proveedores = get_proveedores_safe()
            return render_template('equipos/crear_modern.html', proveedores=proveedores)
        
        equipo_id = insert_equipo_safe(nombre=nombre, estado=estado, tipo=tipo)
        
        if equipo_id:
            flash(f'Equipo "{nombre}" creado exitosamente', 'success')
            return redirect(url_for('listar_equipos'))
        else:
            flash('Error al crear equipo', 'error')
            proveedores = get_proveedores_safe()
            return render_template('equipos/crear_modern.html', proveedores=proveedores)
            
    except Exception as e:
        flash(f'Error al crear equipo: {str(e)}', 'error')
        proveedores = get_proveedores_safe()
        return render_template('equipos/crear_modern.html', proveedores=proveedores)

# Detalle/Editar/Eliminar Equipo
@app.route('/equipos/<int:id>')
def ver_equipo(id):
    try:
        e = get_equipo_by_id_safe(id)
        if not e:
            flash('Equipo no encontrado', 'error')
            return redirect(url_for('listar_equipos'))
        return render_template('equipos/detalle.html', equipo=e)
    except Exception as e:
        flash(f'Error al cargar equipo: {str(e)}', 'error')
        return redirect(url_for('listar_equipos'))

@app.route('/equipos/<int:id>/editar', methods=['GET', 'POST'])
def editar_equipo(id):
    if request.method == 'GET':
        e = get_equipo_by_id_safe(id)
        if not e:
            flash('Equipo no encontrado', 'error')
            return redirect(url_for('listar_equipos'))
        return render_template('equipos/editar.html', equipo=e)
    try:
        nombre = request.form.get('nombre') or None
        estado = request.form.get('estado') or request.form.get('estado_actual') or None
        tipo = request.form.get('tipo') or request.form.get('tipo_equipo') or None
        ok = update_equipo_safe(id, nombre=nombre, estado=estado, tipo=tipo)
        if ok:
            flash('Equipo actualizado', 'success')
            return redirect(url_for('ver_equipo', id=id))
        flash('No se pudo actualizar el equipo', 'error')
        return redirect(url_for('editar_equipo', id=id))
    except Exception as e:
        flash(f'Error al actualizar equipo: {str(e)}', 'error')
        return redirect(url_for('editar_equipo', id=id))

@app.route('/equipos/<int:id>/eliminar', methods=['POST'])
def eliminar_equipo(id):
    try:
        ok = delete_equipo_safe(id)
        if ok:
            flash('Equipo eliminado', 'success')
        else:
            flash('No se pudo eliminar el equipo', 'error')
    except Exception as e:
        flash(f'Error al eliminar equipo: {str(e)}', 'error')
    return redirect(url_for('listar_equipos'))

# ===============================
# GESTIÓN DE HERRAMIENTAS (Alias de Equipos)
# ===============================
@app.route('/herramientas')
def listar_herramientas():
    """Listar todas las herramientas (equipos)"""
    try:
        herramientas = get_equipos_safe()
        return render_template('herramientas/listar.html', herramientas=herramientas)
    except Exception as e:
        flash(f'Error al cargar herramientas: {str(e)}', 'error')
        return render_template('herramientas/listar.html', herramientas=[])

@app.route('/herramientas/nueva', methods=['GET', 'POST'])
def crear_herramienta():
    """Crear nueva herramienta"""
    if request.method == 'GET':
        return render_template('herramientas/crear.html')
    
    try:
        nombre = request.form.get('nombre', '').strip()
        estado = request.form.get('estado', 'Disponible').strip()
        tipo = request.form.get('tipo', '').strip()
        
        if not nombre:
            flash('El nombre de la herramienta es obligatorio', 'error')
            return render_template('herramientas/crear.html')
        
        herramienta_id = insert_equipo_safe(nombre=nombre, estado=estado, tipo=tipo)
        
        if herramienta_id:
            flash(f'Herramienta "{nombre}" creada exitosamente', 'success')
            return redirect(url_for('listar_herramientas'))
        else:
            flash('Error al crear herramienta', 'error')
            return render_template('herramientas/crear.html')
            
    except Exception as e:
        flash(f'Error al crear herramienta: {str(e)}', 'error')
        return render_template('herramientas/crear.html')

@app.route('/herramientas/<int:id>')
def ver_herramienta(id):
    """Ver detalle de una herramienta"""
    try:
        herramienta = get_equipo_by_id_safe(id)
        if not herramienta:
            flash('Herramienta no encontrada', 'error')
            return redirect(url_for('listar_herramientas'))
        return render_template('herramientas/detalle.html', herramienta=herramienta)
    except Exception as e:
        flash(f'Error al cargar herramienta: {str(e)}', 'error')
        return redirect(url_for('listar_herramientas'))

@app.route('/herramientas/<int:id>/editar', methods=['GET', 'POST'])
def editar_herramienta(id):
    """Editar herramienta"""
    if request.method == 'GET':
        try:
            herramienta = get_equipo_by_id_safe(id)
            if not herramienta:
                flash('Herramienta no encontrada', 'error')
                return redirect(url_for('listar_herramientas'))
            return render_template('herramientas/editar.html', herramienta=herramienta)
        except Exception as e:
            flash(f'Error al cargar herramienta: {str(e)}', 'error')
            return redirect(url_for('listar_herramientas'))
    
    # POST - Actualizar
    try:
        nombre = request.form.get('nombre', '').strip()
        estado = request.form.get('estado', '').strip()
        tipo = request.form.get('tipo', '').strip()
        
        if not nombre:
            flash('El nombre de la herramienta es obligatorio', 'error')
            herramienta = get_equipo_by_id_safe(id)
            return render_template('herramientas/editar.html', herramienta=herramienta)
        
        ok = update_equipo_safe(id, nombre=nombre, estado=estado, tipo=tipo)
        
        if ok:
            flash('Herramienta actualizada exitosamente', 'success')
            return redirect(url_for('ver_herramienta', id=id))
        else:
            flash('Error al actualizar la herramienta', 'error')
            herramienta = get_equipo_by_id_safe(id)
            return render_template('herramientas/editar.html', herramienta=herramienta)
            
    except Exception as e:
        flash(f'Error al actualizar herramienta: {str(e)}', 'error')
        herramienta = get_equipo_by_id_safe(id)
        return render_template('herramientas/editar.html', herramienta=herramienta)

@app.route('/herramientas/<int:id>/eliminar', methods=['POST'])
def eliminar_herramienta(id):
    """Eliminar herramienta"""
    try:
        ok = delete_equipo_safe(id)
        if ok:
            flash('Herramienta eliminada exitosamente', 'success')
        else:
            flash('Error al eliminar la herramienta', 'error')
    except Exception as e:
        flash(f'Error al eliminar herramienta: {str(e)}', 'error')
    return redirect(url_for('listar_herramientas'))

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
        # Obtener datos necesarios para el formulario
        obras = get_obras_safe()
        empleados = get_empleados_safe() 
        vehiculos = get_vehiculos_safe()
        
        # Filtrar arquitectos e ingenieros y convertir a formato compatible
        arquitectos = []
        ingenieros = []
        
        for empleado in empleados:
            if empleado.get('tipo_empleado') == 'ARQUITECTO':
                arquitectos.append((
                    empleado['id_empleado'], 
                    empleado['nombre_empleado'], 
                    empleado['apellido_empleado']
                ))
            elif empleado.get('tipo_empleado') == 'INGENIERO':
                ingenieros.append((
                    empleado['id_empleado'], 
                    empleado['nombre_empleado'], 
                    empleado['apellido_empleado']
                ))
        
        # Convertir obras y vehiculos a tuplas también para consistencia
        obras_tuplas = [(obra['id_obra'], obra.get('nombre', 'Sin nombre')) for obra in obras]
        vehiculos_tuplas = [(v['id_vehiculo'], v.get('placa_vehiculo', 'Sin placa'), v.get('tipo_vehiculo', 'Sin tipo')) for v in vehiculos]
        
        return render_template('proyectos/crear.html', 
                             obras=obras_tuplas, 
                             arquitectos=arquitectos, 
                             ingenieros=ingenieros, 
                             vehiculos=vehiculos_tuplas)
    
    try:
        # Obtener datos básicos del proyecto
        nombre = request.form.get('nombre', '').strip()
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        estado = request.form.get('estado', 'PLANIFICACION')
        
        # Obtener asignaciones
        obra_id = request.form.get('obra_id')
        arquitecto_id = request.form.get('arquitecto_id')
        ingeniero_id = request.form.get('ingeniero_id')
        vehiculos_ids = request.form.getlist('vehiculos_ids')
        
        if not nombre:
            flash('El nombre del proyecto es obligatorio', 'error')
            obras = get_obras_safe()
            empleados = get_empleados_safe()
            vehiculos = get_vehiculos_safe()
            arquitectos = [e for e in empleados if e.get('tipo_empleado') == 'ARQUITECTO']
            ingenieros = [e for e in empleados if e.get('tipo_empleado') == 'INGENIERO']
            return render_template('proyectos/crear.html', obras=obras, arquitectos=arquitectos, ingenieros=ingenieros, vehiculos=vehiculos)
        
        # Crear el proyecto
        proyecto_id = insert_proyecto_safe(
            nombre=nombre, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin, 
            estado=estado
        )
        
        if proyecto_id:
            # Realizar asignaciones si el proyecto se creó correctamente
            conn = get_connection()
            cursor = conn.cursor()
            
            try:
                # Asignar obra si se seleccionó
                if obra_id:
                    cursor.execute("""
                    INSERT INTO proyecto_obra (id_proyecto, id_obra, observaciones)
                    VALUES (%s, %s, %s)
                    """, (proyecto_id, obra_id, f"Obra asignada al crear el proyecto {nombre}"))
                
                # Asignar arquitecto si se seleccionó
                if arquitecto_id:
                    cursor.execute("""
                    INSERT INTO proyecto_empleado (id_proyecto, id_empleado, tipo_asignacion, responsabilidad, observaciones)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (proyecto_id, arquitecto_id, 'ARQUITECTO', 'Arquitecto principal del proyecto', f'Arquitecto asignado al crear el proyecto {nombre}'))
                
                # Asignar ingeniero si se seleccionó  
                if ingeniero_id:
                    cursor.execute("""
                    INSERT INTO proyecto_empleado (id_proyecto, id_empleado, tipo_asignacion, responsabilidad, observaciones)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (proyecto_id, ingeniero_id, 'INGENIERO', 'Ingeniero principal del proyecto', f'Ingeniero asignado al crear el proyecto {nombre}'))
                
                # Asignar vehículos si se seleccionaron
                for vehiculo_id in vehiculos_ids:
                    if vehiculo_id:
                        cursor.execute("""
                        INSERT INTO proyecto_vehiculo (id_proyecto, id_vehiculo, proposito, observaciones)
                        VALUES (%s, %s, %s, %s)
                        """, (proyecto_id, vehiculo_id, f'Vehículo asignado para logística y transporte del proyecto', f'Vehículo asignado al crear el proyecto {nombre}'))
                
                conn.commit()
                flash(f'Proyecto "{nombre}" creado exitosamente con todas las asignaciones', 'success')
                return redirect(url_for('ver_proyecto', id=proyecto_id))
                
            except Exception as e:
                conn.rollback()
                flash(f'Proyecto creado pero error en asignaciones: {str(e)}', 'warning')
                return redirect(url_for('ver_proyecto', id=proyecto_id))
            finally:
                conn.close()
        else:
            flash('Error al crear proyecto', 'error')
            obras = get_obras_safe()
            empleados = get_empleados_safe()
            vehiculos = get_vehiculos_safe()
            arquitectos = [e for e in empleados if e.get('tipo_empleado') == 'ARQUITECTO']
            ingenieros = [e for e in empleados if e.get('tipo_empleado') == 'INGENIERO']
            return render_template('proyectos/crear.html', obras=obras, arquitectos=arquitectos, ingenieros=ingenieros, vehiculos=vehiculos)
            
    except Exception as e:
        flash(f'Error al crear proyecto: {str(e)}', 'error')
        obras = get_obras_safe()
        empleados = get_empleados_safe()
        vehiculos = get_vehiculos_safe()
        arquitectos = [e for e in empleados if e.get('tipo_empleado') == 'ARQUITECTO']
        ingenieros = [e for e in empleados if e.get('tipo_empleado') == 'INGENIERO']
        return render_template('proyectos/crear.html', obras=obras, arquitectos=arquitectos, ingenieros=ingenieros, vehiculos=vehiculos)

# Detalle/Editar/Eliminar Proyecto
@app.route('/proyectos/<int:id>')
def ver_proyecto(id):
    try:
        p = get_proyecto_by_id_safe(id)
        if not p:
            flash('Proyecto no encontrado', 'error')
            return redirect(url_for('listar_proyectos'))
        
        # Obtener asignaciones de recursos para el proyecto
        asignaciones = get_resumen_asignaciones_proyecto_safe(id)
        
        return render_template('proyectos/detalle.html', proyecto=p, asignaciones=asignaciones)
    except Exception as e:
        flash(f'Error al cargar proyecto: {str(e)}', 'error')
        return redirect(url_for('listar_proyectos'))

@app.route('/proyectos/<int:id>/editar', methods=['GET', 'POST'])
def editar_proyecto(id):
    if request.method == 'GET':
        p = get_proyecto_by_id_safe(id)
        if not p:
            flash('Proyecto no encontrado', 'error')
            return redirect(url_for('listar_proyectos'))
        return render_template('proyectos/editar.html', proyecto=p)
    try:
        nombre = request.form.get('nombre') or None
        fecha_inicio = request.form.get('fecha_inicio') or None
        fecha_fin = request.form.get('fecha_fin') or None
        estado = request.form.get('estado') or None
        ok = update_proyecto_safe(id, nombre=nombre, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, estado=estado)
        if ok:
            flash('Proyecto actualizado', 'success')
            return redirect(url_for('ver_proyecto', id=id))
        flash('No se pudo actualizar el proyecto', 'error')
        return redirect(url_for('editar_proyecto', id=id))
    except Exception as e:
        flash(f'Error al actualizar proyecto: {str(e)}', 'error')
        return redirect(url_for('editar_proyecto', id=id))

@app.route('/proyectos/<int:id>/eliminar', methods=['POST'])
def eliminar_proyecto(id):
    try:
        ok = delete_proyecto_safe(id)
        if ok:
            flash('Proyecto eliminado', 'success')
        else:
            flash('No se pudo eliminar el proyecto', 'error')
    except Exception as e:
        flash(f'Error al eliminar proyecto: {str(e)}', 'error')
    return redirect(url_for('listar_proyectos'))

# Función inventarios movida a la sección completa al final

# ===============================
# GESTIÓN DE MOVIMIENTOS DE MATERIALES
# ===============================
@app.route('/movimientos')
def listar_movimientos_materiales():
    """Listar movimientos de materiales"""
    try:
        movimientos = get_movimientos_materiales_safe()
        return render_template('movimientos/listar.html', movimientos=movimientos)
    except Exception as e:
        flash(f'Error al cargar movimientos: {str(e)}', 'error')
        return render_template('movimientos/listar.html', movimientos=[])

@app.route('/movimientos/nuevo', methods=['GET', 'POST'])
def crear_movimiento_material():
    """Crear nuevo movimiento de material"""
    if request.method == 'GET':
        materiales = get_materiales_safe()
        return render_template('movimientos/crear.html', materiales=materiales)
    
    try:
        tipo_movimiento = request.form.get('tipo_movimiento', '').strip()
        cantidad = request.form.get('cantidad')
        id_material = request.form.get('id_material')
        fecha_movimiento = request.form.get('fecha_movimiento')
        origen = request.form.get('origen', '').strip()
        destino = request.form.get('destino', '').strip()
        
        if not tipo_movimiento or not cantidad:
            flash('Tipo de movimiento y cantidad son obligatorios', 'error')
            materiales = get_materiales_safe()
            return render_template('movimientos/crear.html', materiales=materiales)
        
        try:
            cantidad_int = int(cantidad)
        except ValueError:
            flash('La cantidad debe ser un número válido', 'error')
            materiales = get_materiales_safe()
            return render_template('movimientos/crear.html', materiales=materiales)
        
        movimiento_id = insert_movimiento_material_safe(
            tipo_movimiento=tipo_movimiento,
            cantidad=cantidad_int,
            id_material=id_material if id_material else None,
            fecha_movimiento=fecha_movimiento,
            origen=origen if origen else None,
            destino=destino if destino else None
        )
        
        if movimiento_id:
            flash('Movimiento registrado exitosamente', 'success')
            return redirect(url_for('listar_movimientos_materiales'))
        else:
            flash('Error al registrar movimiento', 'error')
            materiales = get_materiales_safe()
            return render_template('movimientos/crear.html', materiales=materiales)
            
    except Exception as e:
        flash(f'Error al crear movimiento: {str(e)}', 'error')
        materiales = get_materiales_safe()
        return render_template('movimientos/crear.html', materiales=materiales)

@app.route('/movimientos/<int:id>')
def ver_movimiento_material(id):
    """Ver detalle de un movimiento"""
    try:
        movimiento = get_movimiento_material_by_id_safe(id)
        if not movimiento:
            flash('Movimiento no encontrado', 'error')
            return redirect(url_for('listar_movimientos_materiales'))
        return render_template('movimientos/detalle.html', movimiento=movimiento)
    except Exception as e:
        flash(f'Error al cargar movimiento: {str(e)}', 'error')
        return redirect(url_for('listar_movimientos_materiales'))

@app.route('/movimientos/<int:id>/editar', methods=['GET', 'POST'])
def editar_movimiento_material(id):
    """Editar movimiento de material"""
    if request.method == 'GET':
        try:
            movimiento = get_movimiento_material_by_id_safe(id)
            if not movimiento:
                flash('Movimiento no encontrado', 'error')
                return redirect(url_for('listar_movimientos_materiales'))
            materiales = get_materiales_safe()
            return render_template('movimientos/editar.html', movimiento=movimiento, materiales=materiales)
        except Exception as e:
            flash(f'Error al cargar movimiento: {str(e)}', 'error')
            return redirect(url_for('listar_movimientos_materiales'))
    
    try:
        tipo_movimiento = request.form.get('tipo_movimiento', '').strip()
        cantidad = request.form.get('cantidad')
        id_material = request.form.get('id_material')
        fecha_movimiento = request.form.get('fecha_movimiento')
        origen = request.form.get('origen', '').strip()
        destino = request.form.get('destino', '').strip()
        
        if not tipo_movimiento or not cantidad:
            flash('Tipo de movimiento y cantidad son obligatorios', 'error')
            movimiento = get_movimiento_material_by_id_safe(id)
            materiales = get_materiales_safe()
            return render_template('movimientos/editar.html', movimiento=movimiento, materiales=materiales)
        
        try:
            cantidad_int = int(cantidad)
        except ValueError:
            flash('La cantidad debe ser un número válido', 'error')
            movimiento = get_movimiento_material_by_id_safe(id)
            materiales = get_materiales_safe()
            return render_template('movimientos/editar.html', movimiento=movimiento, materiales=materiales)
        
        success = update_movimiento_material_safe(
            movimiento_id=id,
            tipo_movimiento=tipo_movimiento or None,
            cantidad=cantidad_int,
            id_material=id_material if id_material else None,
            fecha_movimiento=fecha_movimiento or None,
            origen=origen if origen else None,
            destino=destino if destino else None
        )
        
        if success:
            flash('Movimiento actualizado exitosamente', 'success')
            return redirect(url_for('ver_movimiento_material', id=id))
        else:
            flash('Error al actualizar movimiento', 'error')
            movimiento = get_movimiento_material_by_id_safe(id)
            materiales = get_materiales_safe()
            return render_template('movimientos/editar.html', movimiento=movimiento, materiales=materiales)
            
    except Exception as e:
        flash(f'Error al actualizar movimiento: {str(e)}', 'error')
        movimiento = get_movimiento_material_by_id_safe(id)
        materiales = get_materiales_safe()
        return render_template('movimientos/editar.html', movimiento=movimiento, materiales=materiales)

@app.route('/movimientos/<int:id>/eliminar', methods=['POST'])
def eliminar_movimiento_material(id):
    """Eliminar movimiento de material"""
    try:
        success = delete_movimiento_material_safe(id)
        if success:
            flash('Movimiento eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar movimiento', 'error')
    except Exception as e:
        flash(f'Error al eliminar movimiento: {str(e)}', 'error')
    return redirect(url_for('listar_movimientos_materiales'))

# Mantener alias antigua
@app.route('/movimientos-materiales')
def movimientos_materiales():
    """Redirección de alias antiguo"""
    return redirect(url_for('listar_movimientos_materiales'))

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
# MÓDULO DE FACTURACIÓN
# ===============================
@app.route('/facturas')
def listar_facturas():
    """Listar todas las facturas"""
    try:
        facturas = get_facturas_safe()
        return render_template('facturas/listar_modern.html', facturas=facturas)
    except Exception as e:
        flash(f'Error cargando facturas: {e}', 'error')
        return render_template('facturas/listar_modern.html', facturas=[])

@app.route('/facturas/crear', methods=['GET', 'POST'])
def crear_factura():
    """Crear nueva factura"""
    if request.method == 'POST':
        try:
            numero_factura = generar_numero_factura_safe()
            id_contrato = request.form.get('id_contrato')
            fecha_vencimiento = request.form.get('fecha_vencimiento')
            observaciones = request.form.get('observaciones')
            metodo_pago = request.form.get('metodo_pago', 'Transferencia')
            
            factura_id = insert_factura_safe(numero_factura, id_contrato, fecha_vencimiento, observaciones, metodo_pago)
            
            if factura_id:
                flash(f'Factura {numero_factura} creada exitosamente', 'success')
                return redirect(url_for('listar_facturas'))
            else:
                flash('Error al crear la factura', 'error')
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    # Obtener contratos facturables para el formulario
    try:
        contratos = get_contratos_facturables_safe()
    except:
        contratos = []
    
    return render_template('facturas/crear.html', contratos=contratos)

@app.route('/facturas/<int:id>')
def ver_factura(id):
    """Ver detalle de una factura"""
    try:
        factura = get_factura_by_id_safe(id)
        if not factura:
            flash('Factura no encontrada', 'error')
            return redirect(url_for('listar_facturas'))
        
        # Obtener detalles y pagos relacionados
        detalles = get_detalles_factura_safe(id)
        pagos = get_pagos_factura_safe(id)
        
        return render_template('facturas/detalle.html', factura=factura, detalles=detalles, pagos=pagos)
    except Exception as e:
        flash(f'Error al cargar factura: {e}', 'error')
        return redirect(url_for('listar_facturas'))

@app.route('/facturas/<int:id>/editar', methods=['GET', 'POST'])
def editar_factura(id):
    """Editar una factura existente"""
    if request.method == 'POST':
        try:
            numero_factura = request.form.get('numero_factura')
            id_contrato = request.form.get('id_contrato')
            fecha_vencimiento = request.form.get('fecha_vencimiento')
            observaciones = request.form.get('observaciones')
            metodo_pago = request.form.get('metodo_pago')
            estado = request.form.get('estado')
            
            success = update_factura_safe(id, numero_factura, id_contrato, fecha_vencimiento, observaciones, metodo_pago, estado)
            
            if success:
                flash('Factura actualizada exitosamente', 'success')
                return redirect(url_for('ver_factura', id=id))
            else:
                flash('Error al actualizar factura', 'error')
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    # GET: Mostrar formulario con datos actuales
    try:
        factura = get_factura_by_id_safe(id)
        if not factura:
            flash('Factura no encontrada', 'error')
            return redirect(url_for('listar_facturas'))
        
        contratos = get_contratos_facturables_safe()
        return render_template('facturas/editar.html', factura=factura, contratos=contratos)
    except Exception as e:
        flash(f'Error al cargar factura: {e}', 'error')
        return redirect(url_for('listar_facturas'))

@app.route('/facturas/<int:id>/eliminar', methods=['POST'])
def eliminar_factura(id):
    """Eliminar una factura"""
    try:
        success = delete_factura_safe(id)
        if success:
            flash('Factura eliminada exitosamente', 'success')
        else:
            flash('Error al eliminar factura', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    
    return redirect(url_for('listar_facturas'))

@app.route('/contratos/facturables')
def contratos_facturables():
    """Mostrar contratos que pueden generar facturas"""
    try:
        contratos = get_contratos_facturables_safe()
        return render_template('facturas/contratos_facturables.html', contratos=contratos)
    except Exception as e:
        flash(f'Error cargando contratos: {e}', 'error')
        return render_template('facturas/contratos_facturables.html', contratos=[])

@app.route('/facturas/<int:id_factura>/detalles')
def detalles_factura(id_factura):
    """Ver detalles de una factura"""
    try:
        detalles = get_detalles_factura_safe(id_factura)
        pagos = get_pagos_factura_safe(id_factura)
        return render_template('facturas/detalles.html', detalles=detalles, pagos=pagos, id_factura=id_factura)
    except Exception as e:
        flash(f'Error cargando detalles: {e}', 'error')
        return redirect(url_for('listar_facturas'))

@app.route('/facturas/<int:id_factura>/imprimir')
def imprimir_factura(id_factura):
    """Imprimir factura en PDF o vista de impresión"""
    try:
        # Aquí se implementaría la generación de PDF
        flash(f'Factura {id_factura} lista para imprimir', 'info')
        return redirect(url_for('listar_facturas'))
    except Exception as e:
        flash(f'Error al imprimir: {e}', 'error')
        return redirect(url_for('listar_facturas'))

# ===============================
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
    # Cargar áreas para el dropdown
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_area, nombre_area FROM areas ORDER BY nombre_area")
        areas = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error cargando áreas: {str(e)}")
        areas = []
    
    if request.method == 'GET':
        return render_template('actividades/crear.html', areas=areas)
    
    try:
        # Campos básicos
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        area_id = request.form.get('area_id')
        duracion_estimada = request.form.get('duracion_estimada')
        prioridad = request.form.get('prioridad')
        
        # Campos de calendarización
        fecha_programada = request.form.get('fecha_programada')
        hora_inicio = request.form.get('hora_inicio')
        hora_fin = request.form.get('hora_fin')
        frecuencia = request.form.get('frecuencia')
        notas_calendario = request.form.get('notas_calendario', '').strip()
        
        if not nombre:
            flash('El nombre de la actividad es obligatorio', 'error')
            return render_template('actividades/crear.html', areas=areas)
        
        if not descripcion:
            flash('La descripción de la actividad es obligatoria', 'error')
            return render_template('actividades/crear.html', areas=areas)
        
        if not area_id:
            flash('Debe seleccionar un área', 'error')
            return render_template('actividades/crear.html', areas=areas)
        
        actividad_id = insert_actividad_safe(
            nombre=nombre, 
            descripcion=descripcion, 
            fecha_programada=fecha_programada,
            area_id=area_id,
            duracion_estimada=duracion_estimada,
            prioridad=prioridad,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            frecuencia=frecuencia,
            notas_calendario=notas_calendario
        )
        
        if actividad_id:
            flash(f'Actividad "{nombre}" creada exitosamente', 'success')
            return redirect(url_for('listar_actividades'))
        else:
            flash('Error al crear actividad', 'error')
            return render_template('actividades/crear.html', areas=areas)
            
    except Exception as e:
        flash(f'Error al crear actividad: {str(e)}', 'error')
        return render_template('actividades/crear.html', areas=areas)

# Detalle/Editar/Eliminar Actividad
@app.route('/actividades/<int:id>')
def ver_actividad(id):
    """Ver detalle de una actividad"""
    try:
        actividad = get_actividad_by_id_safe(id)
        if not actividad:
            flash('Actividad no encontrada', 'error')
            return redirect(url_for('listar_actividades'))
        return render_template('actividades/detalle.html', actividad=actividad)
    except Exception as e:
        flash(f'Error al cargar actividad: {str(e)}', 'error')
        return redirect(url_for('listar_actividades'))

@app.route('/actividades/<int:id>/editar', methods=['GET', 'POST'])
def editar_actividad(id):
    """Editar actividad"""
    if request.method == 'GET':
        try:
            actividad = get_actividad_by_id_safe(id)
            if not actividad:
                flash('Actividad no encontrada', 'error')
                return redirect(url_for('listar_actividades'))
            return render_template('actividades/editar.html', actividad=actividad)
        except Exception as e:
            flash(f'Error al cargar actividad: {str(e)}', 'error')
            return redirect(url_for('listar_actividades'))
    
    # POST - Actualizar
    try:
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        fecha_programada = request.form.get('fecha_programada')
        
        if not nombre:
            flash('El nombre de la actividad es obligatorio', 'error')
            actividad = get_actividad_by_id_safe(id)
            return render_template('actividades/editar.html', actividad=actividad)
        
        ok = update_actividad_safe(id, nombre=nombre, descripcion=descripcion, fecha_programada=fecha_programada)
        
        if ok:
            flash('Actividad actualizada exitosamente', 'success')
            return redirect(url_for('ver_actividad', id=id))
        else:
            flash('Error al actualizar la actividad', 'error')
            actividad = get_actividad_by_id_safe(id)
            return render_template('actividades/editar.html', actividad=actividad)
            
    except Exception as e:
        flash(f'Error al actualizar actividad: {str(e)}', 'error')
        actividad = get_actividad_by_id_safe(id)
        return render_template('actividades/editar.html', actividad=actividad)

@app.route('/actividades/<int:id>/eliminar', methods=['POST'])
def eliminar_actividad(id):
    """Eliminar actividad"""
    try:
        ok = delete_actividad_safe(id)
        if ok:
            flash('Actividad eliminada exitosamente', 'success')
        else:
            flash('Error al eliminar la actividad', 'error')
    except Exception as e:
        flash(f'Error al eliminar actividad: {str(e)}', 'error')
    return redirect(url_for('listar_actividades'))

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
        from datetime import date
        obras = get_obras_safe()
        fecha_hoy = date.today().strftime('%Y-%m-%d')
        return render_template('bitacoras/crear.html', obras=obras, fecha_hoy=fecha_hoy)
    
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

@app.route('/bitacoras/<int:id>')
def ver_bitacora(id):
    """Ver detalle de una bitácora"""
    try:
        bitacora = get_bitacora_by_id_safe(id)
        if not bitacora:
            flash('Bitácora no encontrada', 'error')
            return redirect(url_for('listar_bitacoras'))
        
        return render_template('bitacoras/detalle.html', bitacora=bitacora)
    except Exception as e:
        flash(f'Error al cargar bitácora: {e}', 'error')
        return redirect(url_for('listar_bitacoras'))

@app.route('/bitacoras/<int:id>/editar', methods=['GET', 'POST'])
def editar_bitacora(id):
    """Editar una bitácora existente"""
    if request.method == 'POST':
        try:
            observaciones = request.form.get('observaciones')
            fecha_bitacora = request.form.get('fecha_bitacora')
            obra_id = request.form.get('obra_id')
            
            success = update_bitacora_safe(id, observaciones, fecha_bitacora, obra_id if obra_id else None)
            
            if success:
                flash('Bitácora actualizada exitosamente', 'success')
                return redirect(url_for('ver_bitacora', id=id))
            else:
                flash('Error al actualizar bitácora', 'error')
        except Exception as e:
            flash(f'Error: {e}', 'error')
    
    # GET: Mostrar formulario con datos actuales
    try:
        bitacora = get_bitacora_by_id_safe(id)
        if not bitacora:
            flash('Bitácora no encontrada', 'error')
            return redirect(url_for('listar_bitacoras'))
        
        obras = get_obras_safe()
        return render_template('bitacoras/editar.html', bitacora=bitacora, obras=obras)
    except Exception as e:
        flash(f'Error al cargar bitácora: {e}', 'error')
        return redirect(url_for('listar_bitacoras'))

@app.route('/bitacoras/<int:id>/eliminar', methods=['POST'])
def eliminar_bitacora(id):
    """Eliminar una bitácora"""
    try:
        success = delete_bitacora_safe(id)
        if success:
            flash('Bitácora eliminada exitosamente', 'success')
        else:
            flash('Error al eliminar bitácora', 'error')
    except Exception as e:
        flash(f'Error: {e}', 'error')
    
    return redirect(url_for('listar_bitacoras'))

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
        empleados = get_empleados_safe()
        return render_template('incidentes/crear.html', obras=obras, empleados=empleados)
    
    try:
        descripcion = request.form.get('descripcion', '').strip()
        tipo_incidente = request.form.get('tipo_incidente', 'otro')
        gravedad = request.form.get('gravedad', 'leve')
        empleado_id = request.form.get('empleado_id')
        fecha_incidente = request.form.get('fecha_incidente')
        obra_id = request.form.get('obra_id')
        
        if not descripcion:
            flash('La descripción del incidente es obligatoria', 'error')
            obras = get_obras_safe()
            empleados = get_empleados_safe()
            return render_template('incidentes/crear.html', obras=obras, empleados=empleados)
        
        incidente_id = insert_incidente_safe(
            descripcion=descripcion,
            tipo_incidente=tipo_incidente,
            gravedad=gravedad,
            empleado_id=empleado_id if empleado_id else None,
            fecha_incidente=fecha_incidente,
            obra_id=obra_id if obra_id else None
        )
        
        if incidente_id:
            flash('Incidente reportado exitosamente', 'success')
            return redirect(url_for('listar_incidentes'))
        else:
            flash('Error al crear incidente', 'error')
            obras = get_obras_safe()
            empleados = get_empleados_safe()
            return render_template('incidentes/crear.html', obras=obras, empleados=empleados)
            
    except Exception as e:
        flash(f'Error al crear incidente: {str(e)}', 'error')
        obras = get_obras_safe()
        empleados = get_empleados_safe()
        return render_template('incidentes/crear.html', obras=obras, empleados=empleados)

# ===============================
# GESTIÓN DE AUDITORÍAS
# ===============================
@app.route('/incidentes/<int:id>')
def ver_incidente(id):
    try:
        inc = get_incidente_by_id_safe(id)
        if not inc:
            flash('Incidente no encontrado', 'error')
            return redirect(url_for('listar_incidentes'))
        return render_template('incidentes/detalle.html', incidente=inc)
    except Exception as e:
        flash(f'Error cargando incidente: {e}', 'error')
        return redirect(url_for('listar_incidentes'))

@app.route('/incidentes/<int:id>/editar', methods=['GET', 'POST'])
def editar_incidente(id):
    if request.method == 'GET':
        inc = get_incidente_by_id_safe(id)
        if not inc:
            flash('Incidente no encontrado', 'error')
            return redirect(url_for('listar_incidentes'))
        obras = get_obras_safe()
        return render_template('incidentes/editar.html', incidente=inc, obras=obras)

    try:
        descripcion = request.form.get('descripcion', '').strip()
        estado = request.form.get('estado')
        fecha_incidente = request.form.get('fecha_incidente')
        obra_id = request.form.get('obra_id')

        ok = update_incidente_safe(
            id,
            descripcion=descripcion or None,
            estado=estado or None,
            fecha_incidente=fecha_incidente or None,
            obra_id=obra_id or None
        )
        if ok:
            flash('Incidente actualizado', 'success')
            return redirect(url_for('ver_incidente', id=id))
        else:
            flash('No se pudo actualizar el incidente', 'error')
            inc = get_incidente_by_id_safe(id)
            obras = get_obras_safe()
            return render_template('incidentes/editar.html', incidente=inc, obras=obras)
    except Exception as e:
        flash(f'Error actualizando incidente: {e}', 'error')
        inc = get_incidente_by_id_safe(id)
        obras = get_obras_safe()
        return render_template('incidentes/editar.html', incidente=inc, obras=obras)

@app.route('/incidentes/<int:id>/eliminar', methods=['POST'])
def eliminar_incidente(id):
    try:
        if delete_incidente_safe(id):
            flash('Incidente eliminado', 'success')
        else:
            flash('No se pudo eliminar el incidente', 'error')
    except Exception as e:
        flash(f'Error eliminando incidente: {e}', 'error')
    return redirect(url_for('listar_incidentes'))

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

@app.route('/auditorias/<int:id>')
def ver_auditoria(id):
    """Ver detalle de una auditoría"""
    try:
        auditoria = get_auditoria_by_id_safe(id)
        if not auditoria:
            flash('Auditoría no encontrada', 'error')
            return redirect(url_for('listar_auditorias'))
        return render_template('auditorias/detalle.html', auditoria=auditoria)
    except Exception as e:
        flash(f'Error al cargar auditoría: {str(e)}', 'error')
        return redirect(url_for('listar_auditorias'))

@app.route('/auditorias/nueva', methods=['GET', 'POST'])
def crear_auditoria():
    """Crear nueva auditoría (funcionalidad limitada - solo vista)"""
    if request.method == 'GET':
        return render_template('auditorias/crear.html')
    
    try:
        # Nota: Las auditorías se generan automáticamente por el sistema
        # Esta función existe para compatibilidad pero redirige con mensaje informativo
        flash('Las auditorías se generan automáticamente por el sistema', 'info')
        return redirect(url_for('listar_auditorias'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return render_template('auditorias/crear.html')

@app.route('/auditorias/<int:id>/editar', methods=['GET', 'POST'])
def editar_auditoria(id):
    """Editar auditoría (solo vista - las auditorías son de solo lectura)"""
    try:
        auditoria = get_auditoria_by_id_safe(id)
        if not auditoria:
            flash('Auditoría no encontrada', 'error')
            return redirect(url_for('listar_auditorias'))
        
        # Las auditorías son registros de solo lectura
        flash('Las auditorías son registros de solo lectura del sistema', 'info')
        return render_template('auditorias/detalle.html', auditoria=auditoria)
    except Exception as e:
        flash(f'Error al cargar auditoría: {str(e)}', 'error')
        return redirect(url_for('listar_auditorias'))

@app.route('/auditorias/<int:id>/eliminar', methods=['POST'])
def eliminar_auditoria(id):
    """Eliminar auditoría (no recomendado - son registros históricos)"""
    try:
        # Por seguridad, las auditorías no se eliminan
        flash('Por motivos de seguridad, las auditorías no pueden eliminarse', 'warning')
        return redirect(url_for('listar_auditorias'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('listar_auditorias'))

# ===============================
# GESTIÓN DE PERMISOS DE ACCESO
# ===============================
@app.route('/permisos')
def listar_permisos():
    """Listar todos los permisos de acceso"""
    try:
        permisos = get_permisos_acceso_safe()
        return render_template('permisos/listar.html', permisos=permisos)
    except Exception as e:
        flash(f'Error al cargar permisos: {str(e)}', 'error')
        return render_template('permisos/listar.html', permisos=[])

@app.route('/permisos/nuevo', methods=['GET', 'POST'])
def crear_permiso():
    """Crear nuevo permiso de acceso"""
    if request.method == 'POST':
        try:
            modulo = request.form.get('modulo_permiso')
            nivel = request.form.get('nivel_acceso_permiso')
            
            if not modulo:
                flash('El módulo es requerido', 'error')
                return render_template('permisos/crear.html')
            
            permiso_id = insert_permiso_safe(modulo, nivel)
            if permiso_id:
                flash('Permiso creado exitosamente', 'success')
                return redirect(url_for('ver_permiso', id=permiso_id))
            else:
                flash('Error al crear permiso', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('permisos/crear.html')

@app.route('/permisos/<int:id>')
def ver_permiso(id):
    """Ver detalle de un permiso"""
    try:
        permiso = get_permiso_by_id_safe(id)
        if not permiso:
            flash('Permiso no encontrado', 'error')
            return redirect(url_for('listar_permisos'))
        
        usuarios = get_usuarios_con_permiso(id)
        return render_template('permisos/detalle.html', permiso=permiso, usuarios_asignados=usuarios)
    except Exception as e:
        flash(f'Error al cargar permiso: {str(e)}', 'error')
        return redirect(url_for('listar_permisos'))

@app.route('/permisos/<int:id>/editar', methods=['GET', 'POST'])
def editar_permiso(id):
    """Editar un permiso de acceso"""
    if request.method == 'POST':
        try:
            modulo = request.form.get('modulo_permiso')
            nivel = request.form.get('nivel_acceso_permiso')
            
            if not modulo:
                flash('El módulo es requerido', 'error')
                return redirect(url_for('editar_permiso', id=id))
            
            if update_permiso_safe(id, modulo, nivel):
                flash('Permiso actualizado exitosamente', 'success')
                return redirect(url_for('ver_permiso', id=id))
            else:
                flash('Error al actualizar permiso', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    try:
        permiso = get_permiso_by_id_safe(id)
        if not permiso:
            flash('Permiso no encontrado', 'error')
            return redirect(url_for('listar_permisos'))
        return render_template('permisos/editar.html', permiso=permiso)
    except Exception as e:
        flash(f'Error al cargar permiso: {str(e)}', 'error')
        return redirect(url_for('listar_permisos'))

@app.route('/permisos/<int:id>/eliminar', methods=['POST'])
def eliminar_permiso(id):
    """Eliminar un permiso de acceso"""
    try:
        if delete_permiso_safe(id):
            flash('Permiso eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar permiso', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('listar_permisos'))

@app.route('/permisos/<int:id>/asignar', methods=['GET', 'POST'])
def asignar_permiso(id):
    """Asignar/revocar permiso a usuarios"""
    if request.method == 'POST':
        try:
            usuario_id = request.form.get('usuario_id')
            accion = request.form.get('accion')
            
            if not usuario_id:
                flash('Debe seleccionar un usuario', 'error')
                return redirect(url_for('asignar_permiso', id=id))
            
            if accion == 'asignar':
                if asignar_permiso_usuario(id, int(usuario_id)):
                    flash('Permiso asignado exitosamente', 'success')
                else:
                    flash('El usuario ya tiene este permiso o hubo un error', 'warning')
            elif accion == 'revocar':
                if revocar_permiso_usuario(id, int(usuario_id)):
                    flash('Permiso revocado exitosamente', 'success')
                else:
                    flash('Error al revocar permiso', 'error')
            
            return redirect(url_for('asignar_permiso', id=id))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    try:
        permiso = get_permiso_by_id_safe(id)
        if not permiso:
            flash('Permiso no encontrado', 'error')
            return redirect(url_for('listar_permisos'))
        
        usuarios_con_permiso = get_usuarios_con_permiso(id)
        todos_usuarios = get_usuarios_safe()
        
        # Filtrar usuarios que NO tienen el permiso
        usuarios_ids_con_permiso = {u['id_usuario'] for u in usuarios_con_permiso}
        usuarios_sin_permiso = [u for u in todos_usuarios if u['id_usuario'] not in usuarios_ids_con_permiso]
        
        return render_template('permisos/asignar.html', 
                             permiso=permiso, 
                             usuarios_con_permiso=usuarios_con_permiso,
                             usuarios_sin_permiso=usuarios_sin_permiso)
    except Exception as e:
        flash(f'Error al cargar datos: {str(e)}', 'error')
        return redirect(url_for('listar_permisos'))

# ===============================
# GESTIÓN DE BODEGAS
# ===============================
@app.route('/bodegas')
def listar_bodegas():
    """Listar todas las bodegas"""
    try:
        bodegas = get_bodegas_safe()
        return render_template('bodegas/listar.html', bodegas=bodegas)
    except Exception as e:
        flash(f'Error al cargar bodegas: {str(e)}', 'error')
        return render_template('bodegas/listar.html', bodegas=[])

@app.route('/bodegas/nueva', methods=['GET', 'POST'])
def crear_bodega():
    """Crear nueva bodega con información completa"""
    if request.method == 'POST':
        try:
            # Obtener todos los campos del formulario
            responsable = request.form.get('responsable_bodega', '').strip()
            ubicacion = request.form.get('ubicacion_bodega', '').strip()
            capacidad = request.form.get('capacidad_bodega', '').strip()
            telefono = request.form.get('telefono_bodega', '').strip()
            estado = request.form.get('estado_bodega', 'Activa')
            observaciones = request.form.get('observaciones_bodega', '').strip()
            
            # Validación básica
            if not responsable:
                flash('El responsable es requerido', 'error')
                return render_template('bodegas/crear.html')
            
            # Crear bodega con todos los campos
            bodega_id = insert_bodega_safe(
                responsable_bodega=responsable or None,
                ubicacion_bodega=ubicacion or None,
                capacidad_bodega=capacidad or None,
                telefono_bodega=telefono or None,
                estado_bodega=estado,
                observaciones_bodega=observaciones or None
            )
            
            if bodega_id:
                flash(f'Bodega #{bodega_id} creada exitosamente', 'success')
                return redirect(url_for('ver_bodega', id=bodega_id))
            else:
                flash('Error al crear bodega', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('bodegas/crear.html')

@app.route('/bodegas/<int:id>')
def ver_bodega(id):
    """Ver detalle de una bodega"""
    try:
        bodega = get_bodega_by_id_safe(id)
        if not bodega:
            flash('Bodega no encontrada', 'error')
            return redirect(url_for('listar_bodegas'))
        
        obras = get_obras_de_bodega(id)
        return render_template('bodegas/detalle.html', bodega=bodega, obras_asignadas=obras)
    except Exception as e:
        flash(f'Error al cargar bodega: {str(e)}', 'error')
        return redirect(url_for('listar_bodegas'))

@app.route('/bodegas/<int:id>/editar', methods=['GET', 'POST'])
def editar_bodega(id):
    """Editar una bodega"""
    if request.method == 'POST':
        try:
            responsable = request.form.get('responsable_bodega')
            
            if not responsable:
                flash('El responsable es requerido', 'error')
                return redirect(url_for('editar_bodega', id=id))
            
            if update_bodega_safe(id, responsable):
                flash('Bodega actualizada exitosamente', 'success')
                return redirect(url_for('ver_bodega', id=id))
            else:
                flash('Error al actualizar bodega', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    try:
        bodega = get_bodega_by_id_safe(id)
        if not bodega:
            flash('Bodega no encontrada', 'error')
            return redirect(url_for('listar_bodegas'))
        return render_template('bodegas/editar.html', bodega=bodega)
    except Exception as e:
        flash(f'Error al cargar bodega: {str(e)}', 'error')
        return redirect(url_for('listar_bodegas'))

@app.route('/bodegas/<int:id>/eliminar', methods=['POST'])
def eliminar_bodega(id):
    """Eliminar una bodega"""
    try:
        if delete_bodega_safe(id):
            flash('Bodega eliminada exitosamente', 'success')
        else:
            flash('Error al eliminar bodega', 'error')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('listar_bodegas'))

@app.route('/bodegas/<int:id>/asignar', methods=['GET', 'POST'])
def asignar_bodega_obras(id):
    """Asignar/remover bodega de obras"""
    if request.method == 'POST':
        try:
            obra_id = request.form.get('obra_id')
            accion = request.form.get('accion')
            
            if not obra_id:
                flash('Debe seleccionar una obra', 'error')
                return redirect(url_for('asignar_bodega_obras', id=id))
            
            if accion == 'asignar':
                if asignar_bodega_a_obra(id, int(obra_id)):
                    flash('Bodega asignada a obra exitosamente', 'success')
                else:
                    flash('La bodega ya está asignada a esta obra o hubo un error', 'warning')
            elif accion == 'remover':
                if remover_bodega_de_obra(id, int(obra_id)):
                    flash('Bodega removida de obra exitosamente', 'success')
                else:
                    flash('Error al remover bodega de obra', 'error')
            
            return redirect(url_for('asignar_bodega_obras', id=id))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    try:
        bodega = get_bodega_by_id_safe(id)
        if not bodega:
            flash('Bodega no encontrada', 'error')
            return redirect(url_for('listar_bodegas'))
        
        obras_con_bodega = get_obras_de_bodega(id)
        todas_obras = get_obras_safe()
        
        # Filtrar obras que NO tienen la bodega
        obras_ids_con_bodega = {o['id_obra'] for o in obras_con_bodega}
        obras_sin_bodega = [o for o in todas_obras if o['id_obra'] not in obras_ids_con_bodega]
        
        return render_template('bodegas/asignar.html', 
                             bodega=bodega, 
                             obras_con_bodega=obras_con_bodega,
                             obras_sin_bodega=obras_sin_bodega)
    except Exception as e:
        flash(f'Error al cargar datos: {str(e)}', 'error')
        return redirect(url_for('listar_bodegas'))

# ===============================
# (El bloque duplicado de gestión de usuarios fue removido para evitar conflictos de rutas)
# Las rutas oficiales del módulo USUARIOS están definidas arriba:
# - listar_usuarios_sistema (GET /usuarios)
# - crear_usuario_sistema_route (POST /usuarios/crear)
# - bloquear_usuario_route (POST /usuarios/<id>/bloquear)
# - desbloquear_usuario_route (POST /usuarios/<id>/desbloquear)

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
        # Obtener datos para los selects
        obras_data = get_obras_safe()
        clientes_data = get_clientes_safe()
        
        # Convertir a formato de tuplas para el template (id, nombre)
        obras = [(obra.get('id_obra') or obra.get('id'), 
                 f"{obra.get('nombre', 'Sin nombre')} - {obra.get('ubicacion', 'Sin ubicación')}")
                 for obra in obras_data]
        
        clientes = [(cliente.get('id') or cliente.get('id_cliente'), 
                    cliente.get('nombre', 'Sin nombre'))
                    for cliente in clientes_data]
        
        return render_template('contratos/crear.html', obras=obras, clientes=clientes)
    
    try:
        # Obtener todos los campos del formulario
        numero_contrato = request.form.get('numero_contrato', '').strip()
        cliente_id = request.form.get('cliente_id')
        obra_id = request.form.get('obra_id')
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        valor_total = request.form.get('valor_total')
        estado = request.form.get('estado', '').strip()
        tipo_pago = request.form.get('tipo_pago', '').strip()
        
        # Validaciones completas según el formulario
        errors = []
        
        if not numero_contrato:
            errors.append('El número de contrato es obligatorio')
        if not cliente_id:
            errors.append('Debe seleccionar un cliente')
        if not obra_id:
            errors.append('Debe seleccionar una obra')
        if not fecha_inicio:
            errors.append('La fecha de inicio es obligatoria')
        if not valor_total:
            errors.append('El valor total es obligatorio')
        if not tipo_pago:
            errors.append('Debe seleccionar un método de pago')
        if not estado:
            errors.append('Debe seleccionar un estado')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            # Obtener datos para los selects
            obras_data = get_obras_safe()
            clientes_data = get_clientes_safe()
            
            # Convertir a formato de tuplas para el template
            obras = [(obra.get('id_obra') or obra.get('id'), 
                     f"{obra.get('nombre', 'Sin nombre')} - {obra.get('ubicacion', 'Sin ubicación')}")
                     for obra in obras_data]
            
            clientes = [(cliente.get('id') or cliente.get('id_cliente'), 
                        cliente.get('nombre', 'Sin nombre'))
                        for cliente in clientes_data]
            
            return render_template('contratos/crear.html', obras=obras, clientes=clientes)
        
        # Intentamos crear el contrato con los campos disponibles
        contrato_id = insert_contrato_safe(
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_pago=tipo_pago,
            obra_id=obra_id,
            numero_contrato=numero_contrato,
            cliente_id=cliente_id,
            valor_total=valor_total,
            estado=estado
        )
        
        if contrato_id:
            flash('Contrato creado exitosamente', 'success')
            return redirect(url_for('listar_contratos'))
        else:
            flash('Error al crear contrato', 'error')
            # Obtener datos para los selects
            obras_data = get_obras_safe()
            clientes_data = get_clientes_safe()
            
            # Convertir a formato de tuplas para el template
            obras = [(obra.get('id_obra') or obra.get('id'), 
                     f"{obra.get('nombre', 'Sin nombre')} - {obra.get('ubicacion', 'Sin ubicación')}")
                     for obra in obras_data]
            
            clientes = [(cliente.get('id') or cliente.get('id_cliente'), 
                        cliente.get('nombre', 'Sin nombre'))
                        for cliente in clientes_data]
            
            return render_template('contratos/crear.html', obras=obras, clientes=clientes)
            
    except Exception as e:
        flash(f'Error al crear contrato: {str(e)}', 'error')
        # Obtener datos para los selects
        obras_data = get_obras_safe()
        clientes_data = get_clientes_safe()
        
        # Convertir a formato de tuplas para el template
        obras = [(obra.get('id_obra') or obra.get('id'), 
                 f"{obra.get('nombre', 'Sin nombre')} - {obra.get('ubicacion', 'Sin ubicación')}")
                 for obra in obras_data]
        
        clientes = [(cliente.get('id') or cliente.get('id_cliente'), 
                    cliente.get('nombre', 'Sin nombre'))
                    for cliente in clientes_data]
        
        return render_template('contratos/crear.html', obras=obras, clientes=clientes)

@app.route('/contratos/<int:id>')
def ver_contrato(id):
    """Ver detalle de un contrato"""
    try:
        contrato = get_contrato_by_id_safe(id)
        if not contrato:
            flash('Contrato no encontrado', 'error')
            return redirect(url_for('listar_contratos'))
        return render_template('contratos/detalle.html', contrato=contrato)
    except Exception as e:
        flash(f'Error al cargar contrato: {str(e)}', 'error')
        return redirect(url_for('listar_contratos'))

@app.route('/contratos/<int:id>/editar', methods=['GET', 'POST'])
def editar_contrato(id):
    """Editar un contrato existente"""
    if request.method == 'GET':
        try:
            contrato = get_contrato_by_id_safe(id)
            if not contrato:
                flash('Contrato no encontrado', 'error')
                return redirect(url_for('listar_contratos'))
            obras = get_obras_safe()
            return render_template('contratos/editar.html', contrato=contrato, obras=obras)
        except Exception as e:
            flash(f'Error al cargar contrato: {str(e)}', 'error')
            return redirect(url_for('listar_contratos'))
    
    try:
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        tipo_pago = request.form.get('tipo_pago', '').strip()
        obra_id = request.form.get('obra_id')
        
        if not fecha_inicio:
            flash('La fecha de inicio es obligatoria', 'error')
            contrato = get_contrato_by_id_safe(id)
            obras = get_obras_safe()
            return render_template('contratos/editar.html', contrato=contrato, obras=obras)
        
        success = update_contrato_safe(
            contrato_id=id,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tipo_pago=tipo_pago,
            obra_id=obra_id if obra_id else None
        )
        
        if success:
            flash('Contrato actualizado exitosamente', 'success')
            return redirect(url_for('ver_contrato', id=id))
        else:
            flash('Error al actualizar contrato', 'error')
            contrato = get_contrato_by_id_safe(id)
            obras = get_obras_safe()
            return render_template('contratos/editar.html', contrato=contrato, obras=obras)
            
    except Exception as e:
        flash(f'Error al actualizar contrato: {str(e)}', 'error')
        contrato = get_contrato_by_id_safe(id)
        obras = get_obras_safe()
        return render_template('contratos/editar.html', contrato=contrato, obras=obras)

@app.route('/contratos/<int:id>/eliminar', methods=['POST'])
def eliminar_contrato(id):
    """Eliminar un contrato"""
    try:
        success = delete_contrato_safe(id)
        if success:
            flash('Contrato eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar contrato', 'error')
    except Exception as e:
        flash(f'Error al eliminar contrato: {str(e)}', 'error')
    return redirect(url_for('listar_contratos'))

@app.route('/contratos/<int:id>/facturizar', methods=['GET', 'POST'])
def facturizar_contrato_route(id):
    """Generar una factura a partir de un contrato y redirigir a la factura creada."""
    try:
        nueva_factura_id = facturizar_contrato_safe(id)
        if nueva_factura_id:
            flash(f'Factura generada correctamente (ID {nueva_factura_id})', 'success')
            return redirect(url_for('ver_factura', id=nueva_factura_id))
        else:
            flash('No se pudo generar la factura para este contrato. Verifica que la función SQL esté instalada y que el contrato sea facturable.', 'error')
            return redirect(url_for('ver_contrato', id=id))
    except Exception as e:
        flash(f'Error al facturizar contrato: {str(e)}', 'error')
        return redirect(url_for('ver_contrato', id=id))

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

@app.route('/presupuestos/<int:id>')
def ver_presupuesto(id):
    """Ver detalle de un presupuesto"""
    try:
        presupuesto = get_presupuesto_by_id_safe(id)
        if not presupuesto:
            flash('Presupuesto no encontrado', 'error')
            return redirect(url_for('listar_presupuestos'))
        return render_template('presupuestos/detalle.html', presupuesto=presupuesto)
    except Exception as e:
        flash(f'Error al cargar presupuesto: {str(e)}', 'error')
        return redirect(url_for('listar_presupuestos'))

@app.route('/presupuestos/<int:id>/editar', methods=['GET', 'POST'])
def editar_presupuesto(id):
    """Editar un presupuesto existente"""
    if request.method == 'GET':
        try:
            presupuesto = get_presupuesto_by_id_safe(id)
            if not presupuesto:
                flash('Presupuesto no encontrado', 'error')
                return redirect(url_for('listar_presupuestos'))
            obras = get_obras_safe()
            return render_template('presupuestos/editar.html', presupuesto=presupuesto, obras=obras)
        except Exception as e:
            flash(f'Error al cargar presupuesto: {str(e)}', 'error')
            return redirect(url_for('listar_presupuestos'))
    
    try:
        monto_estimado = request.form.get('monto_estimado')
        fecha_presupuesto = request.form.get('fecha_presupuesto')
        obra_id = request.form.get('obra_id')
        
        if not monto_estimado:
            flash('El monto estimado es obligatorio', 'error')
            presupuesto = get_presupuesto_by_id_safe(id)
            obras = get_obras_safe()
            return render_template('presupuestos/editar.html', presupuesto=presupuesto, obras=obras)
        
        try:
            monto_numerico = float(monto_estimado)
        except ValueError:
            flash('El monto debe ser un número válido', 'error')
            presupuesto = get_presupuesto_by_id_safe(id)
            obras = get_obras_safe()
            return render_template('presupuestos/editar.html', presupuesto=presupuesto, obras=obras)
        
        success = update_presupuesto_safe(
            presupuesto_id=id,
            monto_estimado=monto_numerico,
            fecha_presupuesto=fecha_presupuesto,
            obra_id=obra_id if obra_id else None
        )
        
        if success:
            flash('Presupuesto actualizado exitosamente', 'success')
            return redirect(url_for('ver_presupuesto', id=id))
        else:
            flash('Error al actualizar presupuesto', 'error')
            presupuesto = get_presupuesto_by_id_safe(id)
            obras = get_obras_safe()
            return render_template('presupuestos/editar.html', presupuesto=presupuesto, obras=obras)
            
    except Exception as e:
        flash(f'Error al actualizar presupuesto: {str(e)}', 'error')
        presupuesto = get_presupuesto_by_id_safe(id)
        obras = get_obras_safe()
        return render_template('presupuestos/editar.html', presupuesto=presupuesto, obras=obras)

@app.route('/presupuestos/<int:id>/eliminar', methods=['POST'])
def eliminar_presupuesto(id):
    """Eliminar un presupuesto"""
    try:
        success = delete_presupuesto_safe(id)
        if success:
            flash('Presupuesto eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar presupuesto', 'error')
    except Exception as e:
        flash(f'Error al eliminar presupuesto: {str(e)}', 'error')
    return redirect(url_for('listar_presupuestos'))

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
@app.route('/avances/<int:id>')
def ver_avance(id):
    """Ver detalle de un avance"""
    try:
        avance = get_avance_by_id_safe(id)
        if not avance:
            flash('Avance no encontrado', 'error')
            return redirect(url_for('listar_avances'))
        return render_template('avances/detalle.html', avance=avance)
    except Exception as e:
        flash(f'Error cargando avance: {e}', 'error')
        return redirect(url_for('listar_avances'))

@app.route('/avances/<int:id>/editar', methods=['GET', 'POST'])
def editar_avance(id):
    """Editar un avance existente"""
    if request.method == 'GET':
        avance = get_avance_by_id_safe(id)
        if not avance:
            flash('Avance no encontrado', 'error')
            return redirect(url_for('listar_avances'))
        obras = get_obras_safe()
        return render_template('avances/editar.html', avance=avance, obras=obras)

    # POST
    try:
        porcentaje_fisico = request.form.get('porcentaje_fisico')
        porcentaje_financiero = request.form.get('porcentaje_financiero')
        fecha_avance = request.form.get('fecha_avance')
        obra_id = request.form.get('obra_id')

        fisico = float(porcentaje_fisico) if porcentaje_fisico else None
        financiero = float(porcentaje_financiero) if porcentaje_financiero else None

        ok = update_avance_safe(
            id,
            porcentaje_fisico=fisico,
            porcentaje_financiero=financiero,
            fecha_avance=fecha_avance or None,
            obra_id=obra_id or None
        )
        if ok:
            flash('Avance actualizado', 'success')
            return redirect(url_for('ver_avance', id=id))
        else:
            flash('No se pudo actualizar el avance', 'error')
            avance = get_avance_by_id_safe(id)
            obras = get_obras_safe()
            return render_template('avances/editar.html', avance=avance, obras=obras)
    except Exception as e:
        flash(f'Error actualizando avance: {e}', 'error')
        avance = get_avance_by_id_safe(id)
        obras = get_obras_safe()
        return render_template('avances/editar.html', avance=avance, obras=obras)

@app.route('/avances/<int:id>/eliminar', methods=['POST'])
def eliminar_avance(id):
    try:
        if delete_avance_safe(id):
            flash('Avance eliminado', 'success')
        else:
            flash('No se pudo eliminar el avance', 'error')
    except Exception as e:
        flash(f'Error eliminando avance: {e}', 'error')
    return redirect(url_for('listar_avances'))

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


# Detalle de área y gestión de relaciones
@app.route('/areas/<int:area_id>')
def detalle_area(area_id):
    try:
        # Preferimos una consulta directa por ID si está disponible
        area = get_area_by_id_safe(area_id)
        if not area:
            # Fallback: buscar en listado si no se encontró
            areas = get_areas_safe()
            area = next((a for a in areas if a.get('id') == area_id or a.get('id_area') == area_id), None)
        if not area:
            flash('Área no encontrada', 'error')
            return redirect(url_for('listar_areas'))

        obras = get_obras_for_area(area_id)
        actividades = get_activities_for_area(area_id)
        empleados = get_employees_for_area(area_id)
        requisiciones = get_requisiciones_for_area(area_id)

        # Para los selects de asignación, mostramos listas completas
        obras_all = get_obras_safe()
        actividades_all = get_actividades_safe()
        empleados_all = get_empleados_safe()

        return render_template('areas/detalle.html', area=area, obras=obras, actividades=actividades, empleados=empleados, requisiciones=requisiciones, obras_all=obras_all, actividades_all=actividades_all, empleados_all=empleados_all)
    except Exception as e:
        flash(f'Error cargando detalle de área: {e}', 'error')
        return redirect(url_for('listar_areas'))


@app.route('/areas/<int:area_id>/editar', methods=['GET', 'POST'])
def editar_area(area_id):
    """Editar nombre de un área"""
    if request.method == 'GET':
        area = get_area_by_id_safe(area_id)
        if not area:
            flash('Área no encontrada', 'error')
            return redirect(url_for('listar_areas'))
        return render_template('areas/editar.html', area=area)

    # POST
    try:
        nombre = request.form.get('nombre', '').strip()
        if not nombre:
            flash('El nombre del área es obligatorio', 'error')
            area = get_area_by_id_safe(area_id)
            return render_template('areas/editar.html', area=area)
        if update_area_safe(area_id, nombre):
            flash('Área actualizada exitosamente', 'success')
            return redirect(url_for('detalle_area', area_id=area_id))
        else:
            flash('No se pudo actualizar el área', 'error')
            area = get_area_by_id_safe(area_id)
            return render_template('areas/editar.html', area=area)
    except Exception as e:
        flash(f'Error al actualizar área: {e}', 'error')
        area = get_area_by_id_safe(area_id)
        return render_template('areas/editar.html', area=area)


@app.route('/areas/<int:area_id>/eliminar', methods=['POST'])
def eliminar_area(area_id):
    try:
        if delete_area_safe(area_id):
            flash('Área eliminada correctamente', 'success')
        else:
            flash('No se pudo eliminar el área', 'error')
    except Exception as e:
        flash(f'Error eliminando área: {e}', 'error')
    return redirect(url_for('listar_areas'))


@app.route('/areas/<int:area_id>/asignar/obra', methods=['POST'])
def asignar_obra_area(area_id):
    # Soportar uno o varios ids (múltiples campos 'obra_id')
    ids = request.form.getlist('obra_id') or []
    # Fallback a un único campo si el cliente envió solo uno
    if not ids:
        single = request.form.get('obra_id')
        if single:
            ids = [single]
    # Filtrar valores inválidos como '' o 'None'
    clean_ids = [s for s in ids if s and str(s).lower() != 'none']
    if not clean_ids:
        return jsonify({'error': 'Falta obra_id'}), 400
    assigned = 0
    for oid in clean_ids:
        try:
            if assign_area_to_obra(area_id, int(oid)):
                assigned += 1
        except Exception:
            # ignorar un id inválido y continuar
            continue
    return jsonify({'success': True, 'assigned': assigned})

@app.route('/areas/<int:area_id>/desasignar/obra', methods=['POST'])
def desasignar_obra_area(area_id):
    ids = request.form.getlist('obra_id') or []
    if not ids:
        single = request.form.get('obra_id')
        if single:
            ids = [single]
    clean_ids = [s for s in ids if s and str(s).lower() != 'none']
    if not clean_ids:
        return jsonify({'error': 'Falta obra_id'}), 400
    removed = 0
    for oid in clean_ids:
        try:
            if remove_area_from_obra(area_id, int(oid)):
                removed += 1
        except Exception:
            continue
    return jsonify({'success': True, 'removed': removed})

@app.route('/areas/<int:area_id>/asignar/actividad', methods=['POST'])
def asignar_actividad_area(area_id):
    ids = request.form.getlist('actividad_id') or []
    if not ids:
        single = request.form.get('actividad_id')
        if single:
            ids = [single]
    clean_ids = [s for s in ids if s and str(s).lower() != 'none']
    if not clean_ids:
        return jsonify({'error': 'Falta actividad_id'}), 400
    assigned = 0
    for aid in clean_ids:
        try:
            if assign_activity_to_area(area_id, int(aid)):
                assigned += 1
        except Exception:
            continue
    return jsonify({'success': True, 'assigned': assigned})


@app.route('/areas/<int:area_id>/desasignar/actividad', methods=['POST'])
def desasignar_actividad_area(area_id):
    ids = request.form.getlist('actividad_id') or []
    if not ids:
        single = request.form.get('actividad_id')
        if single:
            ids = [single]
    clean_ids = [s for s in ids if s and str(s).lower() != 'none']
    if not clean_ids:
        return jsonify({'error': 'Falta actividad_id'}), 400
    removed = 0
    for aid in clean_ids:
        try:
            if remove_activity_from_area(area_id, int(aid)):
                removed += 1
        except Exception:
            continue
    return jsonify({'success': True, 'removed': removed})

@app.route('/areas/<int:area_id>/asignar/empleado', methods=['POST'])
def asignar_empleado_area(area_id):
    ids = request.form.getlist('empleado_id') or []
    if not ids:
        single = request.form.get('empleado_id')
        if single:
            ids = [single]
    clean_ids = [s for s in ids if s and str(s).lower() != 'none']
    if not clean_ids:
        return jsonify({'error': 'Falta empleado_id'}), 400
    assigned = 0
    for eid in clean_ids:
        try:
            if assign_employee_to_area(area_id, int(eid)):
                assigned += 1
        except Exception:
            continue
    return jsonify({'success': True, 'assigned': assigned})


@app.route('/areas/<int:area_id>/desasignar/empleado', methods=['POST'])
def desasignar_empleado_area(area_id):
    ids = request.form.getlist('empleado_id') or []
    if not ids:
        single = request.form.get('empleado_id')
        if single:
            ids = [single]
    clean_ids = [s for s in ids if s and str(s).lower() != 'none']
    if not clean_ids:
        return jsonify({'error': 'Falta empleado_id'}), 400
    removed = 0
    for eid in clean_ids:
        try:
            if remove_employee_from_area(area_id, int(eid)):
                removed += 1
        except Exception:
            continue
    return jsonify({'success': True, 'removed': removed})

@app.route('/areas/<int:area_id>/asignar/requisicion', methods=['POST'])
def asignar_requisicion_area(area_id):
    ids = request.form.getlist('requisicion_id') or []
    if not ids:
        single = request.form.get('requisicion_id')
        if single:
            ids = [single]
    clean_ids = [s for s in ids if s and str(s).lower() != 'none']
    if not clean_ids:
        return jsonify({'error': 'Falta requisicion_id'}), 400
    assigned = 0
    for rid in clean_ids:
        try:
            if assign_requisicion_to_area(area_id, int(rid)):
                assigned += 1
        except Exception:
            continue
    return jsonify({'success': True, 'assigned': assigned})


@app.route('/areas/<int:area_id>/desasignar/requisicion', methods=['POST'])
def desasignar_requisicion_area(area_id):
    ids = request.form.getlist('requisicion_id') or []
    if not ids:
        single = request.form.get('requisicion_id')
        if single:
            ids = [single]
    clean_ids = [s for s in ids if s and str(s).lower() != 'none']
    if not clean_ids:
        return jsonify({'error': 'Falta requisicion_id'}), 400
    removed = 0
    for rid in clean_ids:
        try:
            if remove_requisicion_from_area(area_id, int(rid)):
                removed += 1
        except Exception:
            continue
    return jsonify({'success': True, 'removed': removed})

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

@app.route('/requisiciones/nueva', methods=['GET', 'POST'])
def crear_requisicion():
    """Crear nueva requisición"""
    if request.method == 'GET':
        areas = get_areas_safe()
        return render_template('requisiciones/crear.html', areas=areas)
    
    try:
        fecha_requisicion = request.form.get('fecha_requisicion')
        estado_requisicion = request.form.get('estado_requisicion', 'Pendiente')
        area_id = request.form.get('area_id')
        
        requisicion_id = insert_requisicion_safe(
            fecha_requisicion=fecha_requisicion,
            estado_requisicion=estado_requisicion,
            area_id=area_id if area_id else None
        )
        
        if requisicion_id:
            flash('Requisición creada exitosamente', 'success')
            return redirect(url_for('listar_requisiciones'))
        else:
            flash('Error al crear requisición', 'error')
            areas = get_areas_safe()
            return render_template('requisiciones/crear.html', areas=areas)
            
    except Exception as e:
        flash(f'Error al crear requisición: {str(e)}', 'error')
        areas = get_areas_safe()
        return render_template('requisiciones/crear.html', areas=areas)

@app.route('/requisiciones/<int:id>')
def ver_requisicion(id):
    """Ver detalle de una requisición"""
    try:
        requisicion = get_requisicion_by_id_safe(id)
        if not requisicion:
            flash('Requisición no encontrada', 'error')
            return redirect(url_for('listar_requisiciones'))
        return render_template('requisiciones/detalle.html', requisicion=requisicion)
    except Exception as e:
        flash(f'Error al cargar requisición: {str(e)}', 'error')
        return redirect(url_for('listar_requisiciones'))

@app.route('/requisiciones/<int:id>/editar', methods=['GET', 'POST'])
def editar_requisicion(id):
    """Editar una requisición existente"""
    if request.method == 'GET':
        try:
            requisicion = get_requisicion_by_id_safe(id)
            if not requisicion:
                flash('Requisición no encontrada', 'error')
                return redirect(url_for('listar_requisiciones'))
            areas = get_areas_safe()
            return render_template('requisiciones/editar.html', requisicion=requisicion, areas=areas)
        except Exception as e:
            flash(f'Error al cargar requisición: {str(e)}', 'error')
            return redirect(url_for('listar_requisiciones'))
    
    try:
        fecha_requisicion = request.form.get('fecha_requisicion')
        estado_requisicion = request.form.get('estado_requisicion', 'Pendiente')
        area_id = request.form.get('area_id')
        
        success = update_requisicion_safe(
            requisicion_id=id,
            fecha_requisicion=fecha_requisicion,
            estado_requisicion=estado_requisicion,
            area_id=area_id if area_id else None
        )
        
        if success:
            flash('Requisición actualizada exitosamente', 'success')
            return redirect(url_for('ver_requisicion', id=id))
        else:
            flash('Error al actualizar requisición', 'error')
            requisicion = get_requisicion_by_id_safe(id)
            areas = get_areas_safe()
            return render_template('requisiciones/editar.html', requisicion=requisicion, areas=areas)
            
    except Exception as e:
        flash(f'Error al actualizar requisición: {str(e)}', 'error')
        requisicion = get_requisicion_by_id_safe(id)
        areas = get_areas_safe()
        return render_template('requisiciones/editar.html', requisicion=requisicion, areas=areas)

@app.route('/requisiciones/<int:id>/eliminar', methods=['POST'])
def eliminar_requisicion(id):
    """Eliminar una requisición"""
    try:
        success = delete_requisicion_safe(id)
        if success:
            flash('Requisición eliminada exitosamente', 'success')
        else:
            flash('Error al eliminar requisición', 'error')
    except Exception as e:
        flash(f'Error al eliminar requisición: {str(e)}', 'error')
    return redirect(url_for('listar_requisiciones'))

# ===============================
# MOVIMIENTOS DE MATERIALES
# ===============================
# DUPLICADO ELIMINADO - Ya existe listar_movimientos_materiales() línea 1581

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

@app.route('/trabajos/<int:id>')
def ver_trabajo(id):
    """Ver detalle de un trabajo"""
    try:
        trabajo = get_trabajo_by_id_safe(id)
        if not trabajo:
            flash('Trabajo no encontrado', 'error')
            return redirect(url_for('listar_trabajos'))
        return render_template('trabajos/detalle.html', trabajo=trabajo)
    except Exception as e:
        flash(f'Error al cargar trabajo: {str(e)}', 'error')
        return redirect(url_for('listar_trabajos'))

@app.route('/trabajos/<int:id>/editar', methods=['GET', 'POST'])
def editar_trabajo(id):
    """Editar un trabajo existente"""
    if request.method == 'GET':
        try:
            trabajo = get_trabajo_by_id_safe(id)
            if not trabajo:
                flash('Trabajo no encontrado', 'error')
                return redirect(url_for('listar_trabajos'))
            return render_template('trabajos/editar.html', trabajo=trabajo)
        except Exception as e:
            flash(f'Error al cargar trabajo: {str(e)}', 'error')
            return redirect(url_for('listar_trabajos'))
    
    try:
        descripcion = request.form.get('descripcion', '').strip()
        precio_unitario = request.form.get('precio_unitario')
        unidad = request.form.get('unidad', '').strip()
        
        if not descripcion:
            flash('La descripción del trabajo es obligatoria', 'error')
            trabajo = get_trabajo_by_id_safe(id)
            return render_template('trabajos/editar.html', trabajo=trabajo)
        
        precio_numerico = None
        if precio_unitario:
            try:
                precio_numerico = float(precio_unitario)
            except ValueError:
                pass
        
        success = update_trabajo_safe(
            trabajo_id=id,
            descripcion=descripcion,
            precio_unitario=precio_numerico,
            unidad=unidad
        )
        
        if success:
            flash('Trabajo actualizado exitosamente', 'success')
            return redirect(url_for('ver_trabajo', id=id))
        else:
            flash('Error al actualizar trabajo', 'error')
            trabajo = get_trabajo_by_id_safe(id)
            return render_template('trabajos/editar.html', trabajo=trabajo)
            
    except Exception as e:
        flash(f'Error al actualizar trabajo: {str(e)}', 'error')
        trabajo = get_trabajo_by_id_safe(id)
        return render_template('trabajos/editar.html', trabajo=trabajo)

@app.route('/trabajos/<int:id>/eliminar', methods=['POST'])
def eliminar_trabajo(id):
    """Eliminar un trabajo"""
    try:
        success = delete_trabajo_safe(id)
        if success:
            flash('Trabajo eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar trabajo', 'error')
    except Exception as e:
        flash(f'Error al eliminar trabajo: {str(e)}', 'error')
    return redirect(url_for('listar_trabajos'))

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
# GESTIÓN DE INVENTARIOS
# ===============================
@app.route('/inventarios')
def inventarios():
    """Listar todos los inventarios con información de relaciones"""
    try:
        inventarios = get_inventarios_safe()
        return render_template('inventarios/listar.html', inventarios=inventarios)
    except Exception as e:
        flash(f'Error al cargar inventarios: {str(e)}', 'error')
        return render_template('inventarios/listar.html', inventarios=[])

@app.route('/inventarios/crear', methods=['GET', 'POST'])
def crear_inventario():
    """Crear nuevo inventario con asignación de bodegas y materiales"""
    if request.method == 'GET':
        try:
            bodegas = get_bodegas_safe()
            materiales = get_materiales_safe()
            return render_template('inventarios/crear.html', 
                                 bodegas=bodegas, 
                                 materiales=materiales)
        except Exception as e:
            flash(f'Error al cargar formulario: {str(e)}', 'error')
            return render_template('inventarios/crear.html', 
                                 bodegas=[], 
                                 materiales=[])
    
    # POST - Crear inventario
    try:
        cantidad = request.form.get('cantidad_inventario')
        bodegas_ids = request.form.getlist('bodegas')
        materiales_ids = request.form.getlist('materiales')
        
        # Validaciones básicas
        if cantidad and cantidad.strip():
            cantidad = float(cantidad)
        else:
            cantidad = None
        
        # Crear inventario básico
        inventario_id = insert_inventario_safe(cantidad_inventario=cantidad)
        
        if inventario_id:
            # Asignar bodegas si se seleccionaron
            if bodegas_ids:
                for bodega_id in bodegas_ids:
                    try:
                        asignar_bodegas_inventario_safe(inventario_id, [int(bodega_id)])
                    except:
                        pass  # Ignorar errores de asignación individual
            
            # Asignar materiales si se seleccionaron
            if materiales_ids:
                for material_id in materiales_ids:
                    try:
                        asignar_materiales_inventario_safe(inventario_id, [int(material_id)])
                    except:
                        pass  # Ignorar errores de asignación individual
            
            flash(f'Inventario #{inventario_id} creado exitosamente', 'success')
            return redirect(url_for('ver_inventario', id=inventario_id))
        else:
            flash('Error al crear inventario', 'error')
            bodegas = get_bodegas_safe()
            materiales = get_materiales_safe()
            return render_template('inventarios/crear.html', 
                                 bodegas=bodegas, 
                                 materiales=materiales)
            
    except Exception as e:
        flash(f'Error al crear inventario: {str(e)}', 'error')
        bodegas = get_bodegas_safe()
        materiales = get_materiales_safe()
        return render_template('inventarios/crear.html', 
                             bodegas=bodegas, 
                             materiales=materiales)

@app.route('/inventarios/<int:id>')
def ver_inventario(id):
    """Ver detalles de un inventario específico"""
    try:
        inventario = get_inventario_by_id_safe(id)
        if not inventario:
            flash('Inventario no encontrado', 'error')
            return redirect(url_for('inventarios'))
        
        # Obtener bodegas y materiales asignados
        bodegas_asignadas = []
        materiales_asignados = []
        valor_total = 0
        
        try:
            # Intentar obtener relaciones (puede fallar si no hay datos)
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                
                # Bodegas asignadas
                cursor.execute("""
                    SELECT b.id_bodega, b.responsable_bodega, b.ubicacion_bodega, b.capacidad_bodega
                    FROM BODEGAS b
                    JOIN BODEGA_INVENTARIO bi ON b.id_bodega = bi.id_bodega
                    WHERE bi.id_inventario = %s
                """, (id,))
                bodegas_asignadas = cursor.fetchall()
                
                # Materiales asignados con cálculo de valor
                cursor.execute("""
                    SELECT m.id_material, m.nombre_material, m.descripcion_material, m.precio_unitario
                    FROM MATERIALES m
                    JOIN INVENTARIO_MATERIAL im ON m.id_material = im.id_material
                    WHERE im.id_inventario = %s
                """, (id,))
                materiales_asignados = cursor.fetchall()
                
                # Calcular valor total estimado
                if materiales_asignados and inventario.get('cantidad_inventario'):
                    for material in materiales_asignados:
                        if material.get('precio_unitario'):
                            valor_total += float(material['precio_unitario']) * float(inventario['cantidad_inventario'])
                
                conn.close()
        except:
            pass  # Si falla la consulta, mostramos listas vacías
        
        return render_template('inventarios/detalle.html', 
                             inventario=inventario,
                             bodegas_asignadas=bodegas_asignadas,
                             materiales_asignados=materiales_asignados,
                             valor_total=valor_total)
        
    except Exception as e:
        flash(f'Error al cargar inventario: {str(e)}', 'error')
        return redirect(url_for('inventarios'))

@app.route('/inventarios/<int:id>/editar', methods=['GET', 'POST'])
def editar_inventario(id):
    """Editar inventario existente"""
    if request.method == 'GET':
        try:
            inventario = get_inventario_by_id_safe(id)
            if not inventario:
                flash('Inventario no encontrado', 'error')
                return redirect(url_for('inventarios'))
            
            bodegas = get_bodegas_safe()
            materiales = get_materiales_safe()
            
            # Obtener IDs de bodegas y materiales ya asignados
            bodegas_asignadas_ids = []
            materiales_asignados_ids = []
            
            try:
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    
                    # IDs de bodegas asignadas
                    cursor.execute("SELECT id_bodega FROM BODEGA_INVENTARIO WHERE id_inventario = %s", (id,))
                    bodegas_asignadas_ids = [row['id_bodega'] for row in cursor.fetchall()]
                    
                    # IDs de materiales asignados
                    cursor.execute("SELECT id_material FROM INVENTARIO_MATERIAL WHERE id_inventario = %s", (id,))
                    materiales_asignados_ids = [row['id_material'] for row in cursor.fetchall()]
                    
                    conn.close()
            except:
                pass
            
            return render_template('inventarios/editar.html', 
                                 inventario=inventario,
                                 bodegas=bodegas,
                                 materiales=materiales,
                                 bodegas_asignadas_ids=bodegas_asignadas_ids,
                                 materiales_asignados_ids=materiales_asignados_ids,
                                 bodegas_asignadas=bodegas_asignadas_ids,
                                 materiales_asignados=materiales_asignados_ids)
            
        except Exception as e:
            flash(f'Error al cargar inventario: {str(e)}', 'error')
            return redirect(url_for('inventarios'))
    
    # POST - Actualizar inventario
    try:
        cantidad = request.form.get('cantidad_inventario')
        bodegas_ids = request.form.getlist('bodegas')
        materiales_ids = request.form.getlist('materiales')
        
        # Validar cantidad
        if cantidad and cantidad.strip():
            cantidad = float(cantidad)
        else:
            cantidad = None
        
        # Actualizar información básica del inventario
        if update_inventario_safe(id, cantidad_inventario=cantidad):
            # Limpiar asignaciones existentes y crear nuevas
            conn = get_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    # Limpiar bodegas anteriores
                    cursor.execute("DELETE FROM BODEGA_INVENTARIO WHERE id_inventario = %s", (id,))
                    
                    # Asignar nuevas bodegas
                    for bodega_id in bodegas_ids:
                        cursor.execute("""
                            INSERT INTO BODEGA_INVENTARIO (id_bodega, id_inventario) 
                            VALUES (%s, %s)
                        """, (int(bodega_id), id))
                    
                    # Limpiar materiales anteriores
                    cursor.execute("DELETE FROM INVENTARIO_MATERIAL WHERE id_inventario = %s", (id,))
                    
                    # Asignar nuevos materiales
                    for material_id in materiales_ids:
                        cursor.execute("""
                            INSERT INTO INVENTARIO_MATERIAL (id_inventario, id_material) 
                            VALUES (%s, %s)
                        """, (id, int(material_id)))
                    
                    conn.commit()
                    conn.close()
                    
                    flash('Inventario actualizado exitosamente', 'success')
                    return redirect(url_for('ver_inventario', id=id))
                except Exception as e:
                    conn.rollback()
                    conn.close()
                    flash(f'Error al actualizar asignaciones: {str(e)}', 'error')
        else:
            flash('Error al actualizar inventario', 'error')
        
        return redirect(url_for('editar_inventario', id=id))
        
    except Exception as e:
        flash(f'Error al actualizar inventario: {str(e)}', 'error')
        return redirect(url_for('editar_inventario', id=id))

@app.route('/inventarios/<int:id>/eliminar', methods=['POST'])
def eliminar_inventario(id):
    """Eliminar inventario y sus relaciones"""
    try:
        if delete_inventario_safe(id):
            flash('Inventario eliminado exitosamente', 'success')
        else:
            flash('No se pudo eliminar el inventario', 'error')
    except Exception as e:
        flash(f'Error al eliminar inventario: {str(e)}', 'error')
    
    return redirect(url_for('inventarios'))

@app.route('/inventarios/<int:id>/materiales', methods=['GET', 'POST'])
def asignar_materiales_inventario(id):
    """Gestionar asignación de materiales a inventario"""
    try:
        inventario = get_inventario_by_id_safe(id)
        if not inventario:
            flash('Inventario no encontrado', 'error')
            return redirect(url_for('inventarios'))
        
        if request.method == 'GET':
            materiales = get_materiales_safe()
            # Obtener materiales ya asignados
            materiales_asignados = []
            try:
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_material FROM INVENTARIO_MATERIAL WHERE id_inventario = %s", (id,))
                    materiales_asignados = [row['id_material'] for row in cursor.fetchall()]
                    conn.close()
            except:
                pass
            
            return render_template('inventarios/asignar_materiales.html', 
                                 inventario=inventario,
                                 materiales=materiales,
                                 materiales_asignados=materiales_asignados)
        
        # POST - Actualizar asignación de materiales
        materiales_ids = request.form.getlist('materiales')
        
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Limpiar asignaciones actuales
                cursor.execute("DELETE FROM INVENTARIO_MATERIAL WHERE id_inventario = %s", (id,))
                
                # Agregar nuevas asignaciones
                for material_id in materiales_ids:
                    cursor.execute("""
                        INSERT INTO INVENTARIO_MATERIAL (id_inventario, id_material) 
                        VALUES (%s, %s)
                    """, (id, int(material_id)))
                
                conn.commit()
                conn.close()
                
                flash('Materiales asignados exitosamente', 'success')
                return redirect(url_for('ver_inventario', id=id))
            except Exception as e:
                conn.rollback()
                conn.close()
                flash(f'Error al asignar materiales: {str(e)}', 'error')
        else:
            flash('Error de conexión a base de datos', 'error')
        
        return redirect(url_for('asignar_materiales_inventario', id=id))
        
    except Exception as e:
        flash(f'Error en asignación de materiales: {str(e)}', 'error')
        return redirect(url_for('ver_inventario', id=id))

@app.route('/inventarios/<int:id>/bodegas', methods=['GET', 'POST'])
def asignar_bodegas_inventario(id):
    """Gestionar asignación de bodegas a inventario"""
    try:
        inventario = get_inventario_by_id_safe(id)
        if not inventario:
            flash('Inventario no encontrado', 'error')
            return redirect(url_for('inventarios'))
        
        if request.method == 'GET':
            bodegas = get_bodegas_safe()
            # Obtener bodegas ya asignadas
            bodegas_asignadas = []
            try:
                conn = get_connection()
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id_bodega FROM BODEGA_INVENTARIO WHERE id_inventario = %s", (id,))
                    bodegas_asignadas = [row['id_bodega'] for row in cursor.fetchall()]
                    conn.close()
            except:
                pass
            
            return render_template('inventarios/asignar_bodegas.html', 
                                 inventario=inventario,
                                 bodegas=bodegas,
                                 bodegas_asignadas=bodegas_asignadas)
        
        # POST - Actualizar asignación de bodegas
        bodegas_ids = request.form.getlist('bodegas')
        
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Limpiar asignaciones actuales
                cursor.execute("DELETE FROM BODEGA_INVENTARIO WHERE id_inventario = %s", (id,))
                
                # Agregar nuevas asignaciones
                for bodega_id in bodegas_ids:
                    cursor.execute("""
                        INSERT INTO BODEGA_INVENTARIO (id_bodega, id_inventario) 
                        VALUES (%s, %s)
                    """, (int(bodega_id), id))
                
                conn.commit()
                conn.close()
                
                flash('Bodegas asignadas exitosamente', 'success')
                return redirect(url_for('ver_inventario', id=id))
            except Exception as e:
                conn.rollback()
                conn.close()
                flash(f'Error al asignar bodegas: {str(e)}', 'error')
        else:
            flash('Error de conexión a base de datos', 'error')
        
        return redirect(url_for('asignar_bodegas_inventario', id=id))
        
    except Exception as e:
        flash(f'Error en asignación de bodegas: {str(e)}', 'error')
        return redirect(url_for('ver_inventario', id=id))

# ===============================
# GESTIÓN DE COMPRAS (ÓRDENES DE COMPRA)
# ===============================
@app.route('/compras')
def listar_compras():
    """Listar todas las órdenes de compra"""
    try:
        compras = get_compras_safe()
        return render_template('compras/listar.html', compras=compras)
    except Exception as e:
        flash(f'Error al cargar compras: {str(e)}', 'error')
        return render_template('compras/listar.html', compras=[])

@app.route('/compras/nueva', methods=['GET', 'POST'])
def crear_compra():
    """Crear nueva orden de compra"""
    if request.method == 'GET':
        proveedores = get_proveedores_safe()
        return render_template('compras/crear.html', proveedores=proveedores)
    
    try:
        numero_orden = request.form.get('numero_orden', '').strip()
        id_proveedor = request.form.get('id_proveedor')
        fecha_entrega_solicitada = request.form.get('fecha_entrega_solicitada')
        observaciones = request.form.get('observaciones', '').strip()
        
        if not numero_orden:
            flash('El número de orden es obligatorio', 'error')
            proveedores = get_proveedores_safe()
            return render_template('compras/crear.html', proveedores=proveedores)
        
        if not id_proveedor:
            flash('Debe seleccionar un proveedor', 'error')
            proveedores = get_proveedores_safe()
            return render_template('compras/crear.html', proveedores=proveedores)
        
        compra_id = insert_compra_safe(
            numero_orden=numero_orden,
            id_proveedor=int(id_proveedor),
            fecha_entrega_solicitada=fecha_entrega_solicitada if fecha_entrega_solicitada else None,
            observaciones=observaciones if observaciones else None
        )
        
        if compra_id:
            flash(f'Orden de compra "{numero_orden}" creada exitosamente', 'success')
            return redirect(url_for('listar_compras'))
        else:
            flash('Error al crear orden de compra', 'error')
            proveedores = get_proveedores_safe()
            return render_template('compras/crear.html', proveedores=proveedores)
            
    except Exception as e:
        flash(f'Error al crear compra: {str(e)}', 'error')
        proveedores = get_proveedores_safe()
        return render_template('compras/crear.html', proveedores=proveedores)

@app.route('/compras/<int:id>')
def ver_compra(id):
    """Ver detalle de una orden de compra"""
    try:
        compra = get_compra_by_id_safe(id)
        if not compra:
            flash('Orden de compra no encontrada', 'error')
            return redirect(url_for('listar_compras'))
        return render_template('compras/detalle.html', compra=compra)
    except Exception as e:
        flash(f'Error al cargar compra: {str(e)}', 'error')
        return redirect(url_for('listar_compras'))

@app.route('/compras/<int:id>/editar', methods=['GET', 'POST'])
def editar_compra(id):
    """Editar orden de compra"""
    if request.method == 'GET':
        try:
            compra = get_compra_by_id_safe(id)
            if not compra:
                flash('Orden de compra no encontrada', 'error')
                return redirect(url_for('listar_compras'))
            proveedores = get_proveedores_safe()
            return render_template('compras/editar.html', compra=compra, proveedores=proveedores)
        except Exception as e:
            flash(f'Error al cargar compra: {str(e)}', 'error')
            return redirect(url_for('listar_compras'))
    
    # POST - Actualizar
    try:
        numero_orden = request.form.get('numero_orden', '').strip()
        id_proveedor = request.form.get('id_proveedor')
        fecha_entrega_solicitada = request.form.get('fecha_entrega_solicitada')
        fecha_entrega_real = request.form.get('fecha_entrega_real')
        estado_orden = request.form.get('estado_orden', '').strip()
        observaciones = request.form.get('observaciones', '').strip()
        
        if not numero_orden:
            flash('El número de orden es obligatorio', 'error')
            compra = get_compra_by_id_safe(id)
            proveedores = get_proveedores_safe()
            return render_template('compras/editar.html', compra=compra, proveedores=proveedores)
        
        ok = update_compra_safe(
            id, 
            numero_orden=numero_orden,
            id_proveedor=int(id_proveedor) if id_proveedor else None,
            fecha_entrega_solicitada=fecha_entrega_solicitada if fecha_entrega_solicitada else None,
            fecha_entrega_real=fecha_entrega_real if fecha_entrega_real else None,
            estado_orden=estado_orden if estado_orden else None,
            observaciones=observaciones if observaciones else None
        )
        
        if ok:
            flash('Orden de compra actualizada exitosamente', 'success')
            return redirect(url_for('ver_compra', id=id))
        else:
            flash('Error al actualizar la orden de compra', 'error')
            compra = get_compra_by_id_safe(id)
            proveedores = get_proveedores_safe()
            return render_template('compras/editar.html', compra=compra, proveedores=proveedores)
            
    except Exception as e:
        flash(f'Error al actualizar compra: {str(e)}', 'error')
        compra = get_compra_by_id_safe(id)
        proveedores = get_proveedores_safe()
        return render_template('compras/editar.html', compra=compra, proveedores=proveedores)

@app.route('/compras/<int:id>/eliminar', methods=['POST'])
def eliminar_compra(id):
    """Eliminar orden de compra"""
    try:
        ok = delete_compra_safe(id)
        if ok:
            flash('Orden de compra eliminada exitosamente', 'success')
        else:
            flash('Error al eliminar la orden de compra', 'error')
    except Exception as e:
        flash(f'Error al eliminar compra: {str(e)}', 'error')
    return redirect(url_for('listar_compras'))

# ===============================
# GESTIÓN DE VENTAS (Alias de Facturas)
# ===============================
@app.route('/ventas')
def listar_ventas():
    """Listar todas las ventas (facturas)"""
    try:
        ventas = get_facturas_safe()
        return render_template('ventas/listar.html', ventas=ventas)
    except Exception as e:
        flash(f'Error al cargar ventas: {str(e)}', 'error')
        return render_template('ventas/listar.html', ventas=[])

@app.route('/ventas/nueva', methods=['GET', 'POST'])
def crear_venta():
    """Crear nueva venta (factura)"""
    if request.method == 'GET':
        contratos = get_contratos_facturables_safe()
        return render_template('ventas/crear.html', contratos=contratos)
    
    try:
        id_contrato = request.form.get('id_contrato')
        fecha_vencimiento = request.form.get('fecha_vencimiento')
        observaciones = request.form.get('observaciones', '').strip()
        metodo_pago = request.form.get('metodo_pago', 'Efectivo')
        
        if not id_contrato:
            flash('Debe seleccionar un contrato para facturar', 'error')
            contratos = get_contratos_facturables_safe()
            return render_template('ventas/crear.html', contratos=contratos)
        
        venta_id = insert_factura_safe(
            id_contrato=int(id_contrato),
            fecha_vencimiento=fecha_vencimiento,
            observaciones=observaciones,
            metodo_pago=metodo_pago
        )
        
        if venta_id:
            flash('Venta creada exitosamente', 'success')
            return redirect(url_for('listar_ventas'))
        else:
            flash('Error al crear venta', 'error')
            contratos = get_contratos_facturables_safe()
            return render_template('ventas/crear.html', contratos=contratos)
            
    except Exception as e:
        flash(f'Error al crear venta: {str(e)}', 'error')
        contratos = get_contratos_facturables_safe()
        return render_template('ventas/crear.html', contratos=contratos)

@app.route('/ventas/<int:id>')
def ver_venta(id):
    """Ver detalle de una venta"""
    try:
        venta = get_factura_by_id_safe(id)
        if not venta:
            flash('Venta no encontrada', 'error')
            return redirect(url_for('listar_ventas'))
        return render_template('ventas/detalle.html', venta=venta)
    except Exception as e:
        flash(f'Error al cargar venta: {str(e)}', 'error')
        return redirect(url_for('listar_ventas'))

@app.route('/ventas/<int:id>/editar', methods=['GET', 'POST'])
def editar_venta(id):
    """Editar venta"""
    if request.method == 'GET':
        try:
            venta = get_factura_by_id_safe(id)
            if not venta:
                flash('Venta no encontrada', 'error')
                return redirect(url_for('listar_ventas'))
            return render_template('ventas/editar.html', venta=venta)
        except Exception as e:
            flash(f'Error al cargar venta: {str(e)}', 'error')
            return redirect(url_for('listar_ventas'))
    
    # POST - Actualizar
    try:
        fecha_vencimiento = request.form.get('fecha_vencimiento')
        observaciones = request.form.get('observaciones', '').strip()
        metodo_pago = request.form.get('metodo_pago', '')
        estado = request.form.get('estado', '')
        
        ok = update_factura_safe(
            id,
            fecha_vencimiento=fecha_vencimiento if fecha_vencimiento else None,
            observaciones=observaciones if observaciones else None,
            metodo_pago=metodo_pago if metodo_pago else None,
            estado=estado if estado else None
        )
        
        if ok:
            flash('Venta actualizada exitosamente', 'success')
            return redirect(url_for('ver_venta', id=id))
        else:
            flash('Error al actualizar la venta', 'error')
            venta = get_factura_by_id_safe(id)
            return render_template('ventas/editar.html', venta=venta)
            
    except Exception as e:
        flash(f'Error al actualizar venta: {str(e)}', 'error')
        venta = get_factura_by_id_safe(id)
        return render_template('ventas/editar.html', venta=venta)

@app.route('/ventas/<int:id>/eliminar', methods=['POST'])
def eliminar_venta(id):
    """Eliminar venta"""
    try:
        ok = delete_factura_safe(id)
        if ok:
            flash('Venta eliminada exitosamente', 'success')
        else:
            flash('Error al eliminar la venta', 'error')
    except Exception as e:
        flash(f'Error al eliminar venta: {str(e)}', 'error')
    return redirect(url_for('listar_ventas'))

# ===============================
# GESTIÓN DE PAGOS
# ===============================
@app.route('/pagos')
def listar_pagos():
    """Listar todos los pagos"""
    try:
        pagos = get_pagos_safe()
        return render_template('pagos/listar.html', pagos=pagos)
    except Exception as e:
        flash(f'Error al cargar pagos: {str(e)}', 'error')
        return render_template('pagos/listar.html', pagos=[])

@app.route('/pagos/nuevo', methods=['GET', 'POST'])
def crear_pago():
    """Crear nuevo pago"""
    if request.method == 'GET':
        return render_template('pagos/crear.html')
    
    try:
        numero_recibo = request.form.get('numero_recibo', '').strip()
        monto_pago = request.form.get('monto_pago', '').strip()
        referencia_pago = request.form.get('referencia_pago', '').strip()
        observaciones_pago = request.form.get('observaciones_pago', '').strip()
        
        if not numero_recibo:
            flash('El número de recibo es obligatorio', 'error')
            return render_template('pagos/crear.html')
        
        if not monto_pago:
            flash('El monto del pago es obligatorio', 'error')
            return render_template('pagos/crear.html')
        
        try:
            monto_decimal = float(monto_pago)
            if monto_decimal <= 0:
                flash('El monto debe ser mayor a 0', 'error')
                return render_template('pagos/crear.html')
        except ValueError:
            flash('El monto debe ser un número válido', 'error')
            return render_template('pagos/crear.html')
        
        pago_id = insert_pago_safe(
            numero_recibo=numero_recibo,
            monto_pago=monto_decimal,
            referencia_pago=referencia_pago if referencia_pago else None,
            observaciones_pago=observaciones_pago if observaciones_pago else None
        )
        
        if pago_id:
            flash(f'Pago "{numero_recibo}" creado exitosamente', 'success')
            return redirect(url_for('listar_pagos'))
        else:
            flash('Error al crear pago', 'error')
            return render_template('pagos/crear.html')
            
    except Exception as e:
        flash(f'Error al crear pago: {str(e)}', 'error')
        return render_template('pagos/crear.html')

@app.route('/pagos/<int:id>')
def ver_pago(id):
    """Ver detalle de un pago"""
    try:
        pago = get_pago_by_id_safe(id)
        if not pago:
            flash('Pago no encontrado', 'error')
            return redirect(url_for('listar_pagos'))
        return render_template('pagos/detalle.html', pago=pago)
    except Exception as e:
        flash(f'Error al cargar pago: {str(e)}', 'error')
        return redirect(url_for('listar_pagos'))

@app.route('/pagos/<int:id>/editar', methods=['GET', 'POST'])
def editar_pago(id):
    """Editar pago"""
    if request.method == 'GET':
        try:
            pago = get_pago_by_id_safe(id)
            if not pago:
                flash('Pago no encontrado', 'error')
                return redirect(url_for('listar_pagos'))
            return render_template('pagos/editar.html', pago=pago)
        except Exception as e:
            flash(f'Error al cargar pago: {str(e)}', 'error')
            return redirect(url_for('listar_pagos'))
    
    # POST - Actualizar
    try:
        numero_recibo = request.form.get('numero_recibo', '').strip()
        monto_pago = request.form.get('monto_pago', '').strip()
        referencia_pago = request.form.get('referencia_pago', '').strip()
        observaciones_pago = request.form.get('observaciones_pago', '').strip()
        estado_pago = request.form.get('estado_pago', '').strip()
        
        if not numero_recibo:
            flash('El número de recibo es obligatorio', 'error')
            pago = get_pago_by_id_safe(id)
            return render_template('pagos/editar.html', pago=pago)
        
        monto_decimal = None
        if monto_pago:
            try:
                monto_decimal = float(monto_pago)
                if monto_decimal <= 0:
                    flash('El monto debe ser mayor a 0', 'error')
                    pago = get_pago_by_id_safe(id)
                    return render_template('pagos/editar.html', pago=pago)
            except ValueError:
                flash('El monto debe ser un número válido', 'error')
                pago = get_pago_by_id_safe(id)
                return render_template('pagos/editar.html', pago=pago)
        
        ok = update_pago_safe(
            id,
            numero_recibo=numero_recibo,
            monto_pago=monto_decimal,
            referencia_pago=referencia_pago if referencia_pago else None,
            observaciones_pago=observaciones_pago if observaciones_pago else None,
            estado_pago=estado_pago if estado_pago else None
        )
        
        if ok:
            flash('Pago actualizado exitosamente', 'success')
            return redirect(url_for('ver_pago', id=id))
        else:
            flash('Error al actualizar el pago', 'error')
            pago = get_pago_by_id_safe(id)
            return render_template('pagos/editar.html', pago=pago)
            
    except Exception as e:
        flash(f'Error al actualizar pago: {str(e)}', 'error')
        pago = get_pago_by_id_safe(id)
        return render_template('pagos/editar.html', pago=pago)

@app.route('/pagos/<int:id>/eliminar', methods=['POST'])
def eliminar_pago(id):
    """Eliminar pago"""
    try:
        ok = delete_pago_safe(id)
        if ok:
            flash('Pago eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar el pago', 'error')
    except Exception as e:
        flash(f'Error al eliminar pago: {str(e)}', 'error')
    return redirect(url_for('listar_pagos'))

# ===============================
# GESTIÓN DE NÓMINA
# ===============================
@app.route('/nomina')
def listar_nomina():
    """Listar todas las nóminas"""
    try:
        nominas = get_nominas_safe()
        return render_template('nomina/listar.html', nominas=nominas)
    except Exception as e:
        flash(f'Error al cargar nóminas: {str(e)}', 'error')
        return render_template('nomina/listar.html', nominas=[])

@app.route('/nomina/nueva', methods=['GET', 'POST'])
def crear_nomina():
    """Crear nueva nómina"""
    if request.method == 'GET':
        empleados = get_empleados_safe()
        return render_template('nomina/crear.html', empleados=empleados)
    
    try:
        id_empleado = request.form.get('id_empleado')
        periodo_mes = request.form.get('periodo_mes')
        periodo_ano = request.form.get('periodo_ano')
        horas_extras = request.form.get('horas_extras', '0').strip()
        bonificaciones = request.form.get('bonificaciones', '0').strip()
        deducciones = request.form.get('deducciones', '0').strip()
        
        if not id_empleado:
            flash('Debe seleccionar un empleado', 'error')
            empleados = get_empleados_safe()
            return render_template('nomina/crear.html', empleados=empleados)
        
        if not periodo_mes or not periodo_ano:
            flash('El periodo (mes y año) es obligatorio', 'error')
            empleados = get_empleados_safe()
            return render_template('nomina/crear.html', empleados=empleados)
        
        try:
            horas_extras_val = float(horas_extras) if horas_extras else 0
            bonificaciones_val = float(bonificaciones) if bonificaciones else 0
            deducciones_val = float(deducciones) if deducciones else 0
        except ValueError:
            flash('Los valores numéricos deben ser válidos', 'error')
            empleados = get_empleados_safe()
            return render_template('nomina/crear.html', empleados=empleados)
        
        nomina_id = calcular_nomina_safe(
            id_empleado=int(id_empleado),
            periodo_mes=int(periodo_mes),
            periodo_ano=int(periodo_ano),
            horas_extras=horas_extras_val,
            bonificaciones=bonificaciones_val,
            deducciones=deducciones_val
        )
        
        if nomina_id:
            flash('Nómina creada y calculada exitosamente', 'success')
            return redirect(url_for('listar_nomina'))
        else:
            flash('Error al crear nómina', 'error')
            empleados = get_empleados_safe()
            return render_template('nomina/crear.html', empleados=empleados)
            
    except Exception as e:
        flash(f'Error al crear nómina: {str(e)}', 'error')
        empleados = get_empleados_safe()
        return render_template('nomina/crear.html', empleados=empleados)

@app.route('/nomina/calcular', methods=['POST'])
def calcular_nomina():
    """Calcular nómina para empleado específico"""
    try:
        id_empleado = request.form.get('id_empleado')
        periodo_mes = request.form.get('periodo_mes')
        periodo_ano = request.form.get('periodo_ano')
        
        if not all([id_empleado, periodo_mes, periodo_ano]):
            flash('Faltan datos para calcular la nómina', 'error')
            return redirect(url_for('listar_nomina'))
        
        nomina_id = calcular_nomina_safe(
            id_empleado=int(id_empleado),
            periodo_mes=int(periodo_mes),
            periodo_ano=int(periodo_ano)
        )
        
        if nomina_id:
            flash('Nómina calculada exitosamente', 'success')
        else:
            flash('Error al calcular nómina', 'error')
            
    except Exception as e:
        flash(f'Error al calcular nómina: {str(e)}', 'error')
    
    return redirect(url_for('listar_nomina'))

@app.route('/nomina/<int:id>')
def ver_nomina(id):
    """Ver detalle de una nómina"""
    try:
        nomina = get_nomina_by_id_safe(id)
        if not nomina:
            flash('Nómina no encontrada', 'error')
            return redirect(url_for('listar_nomina'))
        return render_template('nomina/detalle.html', nomina=nomina)
    except Exception as e:
        flash(f'Error al cargar nómina: {str(e)}', 'error')
        return redirect(url_for('listar_nomina'))

@app.route('/nomina/<int:id>/editar', methods=['GET', 'POST'])
def editar_nomina(id):
    """Editar nómina"""
    if request.method == 'GET':
        try:
            nomina = get_nomina_by_id_safe(id)
            if not nomina:
                flash('Nómina no encontrada', 'error')
                return redirect(url_for('listar_nomina'))
            return render_template('nomina/editar.html', nomina=nomina)
        except Exception as e:
            flash(f'Error al cargar nómina: {str(e)}', 'error')
            return redirect(url_for('listar_nomina'))
    
    # POST - Actualizar
    try:
        horas_extras = request.form.get('horas_extras', '').strip()
        bonificaciones = request.form.get('bonificaciones', '').strip()
        deducciones = request.form.get('deducciones', '').strip()
        fecha_pago = request.form.get('fecha_pago')
        estado_nomina = request.form.get('estado_nomina', '').strip()
        observaciones_nomina = request.form.get('observaciones_nomina', '').strip()
        
        # Validar y convertir valores numéricos
        horas_extras_val = None
        bonificaciones_val = None
        deducciones_val = None
        
        try:
            if horas_extras:
                horas_extras_val = float(horas_extras)
            if bonificaciones:
                bonificaciones_val = float(bonificaciones)
            if deducciones:
                deducciones_val = float(deducciones)
        except ValueError:
            flash('Los valores numéricos deben ser válidos', 'error')
            nomina = get_nomina_by_id_safe(id)
            return render_template('nomina/editar.html', nomina=nomina)
        
        ok = update_nomina_safe(
            id,
            horas_extras=horas_extras_val,
            bonificaciones=bonificaciones_val,
            deducciones=deducciones_val,
            fecha_pago=fecha_pago if fecha_pago else None,
            estado_nomina=estado_nomina if estado_nomina else None,
            observaciones_nomina=observaciones_nomina if observaciones_nomina else None
        )
        
        if ok:
            flash('Nómina actualizada exitosamente', 'success')
            return redirect(url_for('ver_nomina', id=id))
        else:
            flash('Error al actualizar la nómina', 'error')
            nomina = get_nomina_by_id_safe(id)
            return render_template('nomina/editar.html', nomina=nomina)
            
    except Exception as e:
        flash(f'Error al actualizar nómina: {str(e)}', 'error')
        nomina = get_nomina_by_id_safe(id)
        return render_template('nomina/editar.html', nomina=nomina)

@app.route('/nomina/<int:id>/eliminar', methods=['POST'])
def eliminar_nomina(id):
    """Eliminar nómina"""
    try:
        ok = delete_nomina_safe(id)
        if ok:
            flash('Nómina eliminada exitosamente', 'success')
        else:
            flash('Error al eliminar la nómina', 'error')
    except Exception as e:
        flash(f'Error al eliminar nómina: {str(e)}', 'error')
    return redirect(url_for('listar_nomina'))

# ===============================
# ALIAS PARA COMPATIBILIDAD CON DIAGNÓSTICO
# ===============================

# Alias de inventario
def listar_inventario():
    """Alias de inventarios()"""
    return inventarios()

def crear_item_inventario():
    """Alias de crear_inventario()"""
    return crear_inventario()

def ver_item_inventario(id):
    """Alias de ver_inventario()"""
    return ver_inventario(id)

def editar_item_inventario(id):
    """Alias de editar_inventario()"""
    return editar_inventario(id)

def eliminar_item_inventario(id):
    """Alias de eliminar_inventario()"""
    return eliminar_inventario(id)

# ===============================
# API ENDPOINTS
# ===============================

@app.route('/api/tipo-obra/<int:id>')
def get_tipo_obra_api(id):
    """API endpoint para obtener detalles de un tipo de obra"""
    try:
        tipo = get_tipo_obra_by_id_safe(id)
        if tipo:
            return jsonify({
                'success': True,
                'tipo': {
                    'id': tipo[0],
                    'nombre': tipo[1],
                    'descripcion': tipo[2],
                    'unidad_medida': tipo[3],
                    'precio_base': float(tipo[8]) if tipo[8] else 0,
                    'precio_min': float(tipo[6]) if tipo[6] else 0,
                    'precio_max': float(tipo[7]) if tipo[7] else 0,
                    'rango_precio': tipo[4]
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Tipo de obra no encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===============================
# EJECUTAR APLICACIÓN
# ===============================

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
