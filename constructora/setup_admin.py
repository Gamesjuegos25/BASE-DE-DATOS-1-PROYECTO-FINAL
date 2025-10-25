#!/usr/bin/env python3
"""
Script de configuración inicial del sistema
Crea el usuario administrador por defecto y configura permisos básicos
"""

import sys
import os
from datetime import datetime
import bcrypt

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db_connection

def crear_usuario_admin():
    """Crea el usuario administrador por defecto del sistema"""
    
    print("🔧 Configuración inicial del Sistema ERP Constructora")
    print("=" * 60)
    
    # Verificar si ya existe un usuario administrador
    conn = get_db_connection()
    if not conn:
        print("❌ Error: No se pudo conectar a la base de datos")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar si ya hay usuarios en el sistema
        cursor.execute("SELECT COUNT(*) FROM USUARIOS_SISTEMA WHERE activo = true")
        usuarios_activos = cursor.fetchone()[0]
        
        if usuarios_activos > 0:
            print(f"ℹ️ Ya existen {usuarios_activos} usuarios activos en el sistema")
            respuesta = input("¿Desea crear un nuevo usuario administrador? (s/n): ").lower()
            if respuesta != 's':
                print("✅ Configuración cancelada por el usuario")
                return True
        
        print("\n📝 Creando usuario administrador...")
        
        # Solicitar datos del administrador
        nombre_usuario = input("Nombre de usuario (admin): ").strip() or "admin"
        nombre_completo = input("Nombre completo (Administrador Sistema): ").strip() or "Administrador Sistema"
        email = input("Email (admin@constructora.com): ").strip() or "admin@constructora.com"
        
        # Solicitar contraseña
        while True:
            password = input("Contraseña (mínimo 6 caracteres): ").strip()
            if len(password) >= 6:
                break
            print("❌ La contraseña debe tener al menos 6 caracteres")
        
        # Para producción, usar bcrypt para hash de contraseña
        # password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # Por ahora usaremos texto plano para desarrollo
        password_hash = password
        
        # Insertar el usuario administrador
        cursor.execute("""
            INSERT INTO USUARIOS_SISTEMA (
                nombre_usuario, password_hash, nombre_completo, email, 
                rol, activo, fecha_creacion, creado_por,
                intentos_fallidos, fecha_ultimo_acceso
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            nombre_usuario, password_hash, nombre_completo, email,
            'ADMINISTRADOR', True, datetime.now(), 'SISTEMA',
            0, datetime.now()
        ))
        
        # Obtener ID del usuario creado
        cursor.execute("SELECT id FROM USUARIOS_SISTEMA WHERE nombre_usuario = %s", (nombre_usuario,))
        usuario_id = cursor.fetchone()[0]
        
        # Crear permisos básicos si no existen
        permisos_basicos = [
            ('ADMIN_USUARIOS', 'Administración de usuarios del sistema'),
            ('VER_REPORTES', 'Visualizar reportes y estadísticas'),
            ('CREAR_OBRAS', 'Crear nuevas obras y proyectos'),
            ('EDITAR_OBRAS', 'Modificar obras existentes'),
            ('ELIMINAR_OBRAS', 'Eliminar obras del sistema'),
            ('GESTIONAR_EMPLEADOS', 'Administrar empleados y personal'),
            ('GESTIONAR_MATERIALES', 'Administrar materiales e inventario'),
            ('GESTIONAR_PROVEEDORES', 'Administrar proveedores y contratistas'),
            ('GESTIONAR_VEHICULOS', 'Administrar vehículos y equipos'),
            ('VER_AUDITORIA', 'Visualizar logs de auditoría del sistema'),
        ]
        
        for codigo, descripcion in permisos_basicos:
            cursor.execute("""
                INSERT INTO PERMISOS_SISTEMA (codigo, nombre, descripcion, activo)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (codigo) DO NOTHING
            """, (codigo, codigo.replace('_', ' ').title(), descripcion, True))
        
        # Asignar todos los permisos al administrador
        cursor.execute("SELECT id, codigo FROM PERMISOS_SISTEMA WHERE activo = true")
        permisos = cursor.fetchall()
        
        for permiso_id, codigo in permisos:
            cursor.execute("""
                INSERT INTO USUARIOS_PERMISOS (usuario_id, permiso_id, fecha_asignacion, asignado_por)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (usuario_id, permiso_id) DO NOTHING
            """, (usuario_id, permiso_id, datetime.now(), 'SISTEMA'))
        
        # Registrar auditoría
        cursor.execute("""
            INSERT INTO AUDITORIA_ACCESOS (
                usuario_id, accion, detalles, fecha_accion, ip_address
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            usuario_id, 'USUARIO_CREADO', 
            f'Usuario administrador {nombre_usuario} creado por setup inicial',
            datetime.now(), '127.0.0.1'
        ))
        
        conn.commit()
        
        print("\n✅ Usuario administrador creado exitosamente!")
        print(f"   👤 Usuario: {nombre_usuario}")
        print(f"   📧 Email: {email}")
        print(f"   🔑 Contraseña: {password}")
        print(f"   👥 Rol: ADMINISTRADOR")
        print(f"   🛡️ Permisos asignados: {len(permisos)}")
        
        print("\n🚀 El sistema está listo para usar!")
        print("   Inicie la aplicación con: python app.py")
        print("   Acceda con las credenciales creadas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al crear el usuario administrador: {e}")
        if conn:
            conn.rollback()
        return False
    
    finally:
        if conn:
            conn.close()

def verificar_tablas():
    """Verifica que las tablas necesarias existan en la base de datos"""
    
    conn = get_db_connection()
    if not conn:
        print("❌ Error: No se pudo conectar a la base de datos")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar tablas principales
        tablas_requeridas = [
            'USUARIOS_SISTEMA',
            'PERMISOS_SISTEMA', 
            'USUARIOS_PERMISOS',
            'AUDITORIA_ACCESOS'
        ]
        
        print("🔍 Verificando estructura de base de datos...")
        
        for tabla in tablas_requeridas:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                )
            """, (tabla.lower(),))
            
            existe = cursor.fetchone()[0]
            if existe:
                print(f"   ✅ Tabla {tabla} encontrada")
            else:
                print(f"   ❌ Tabla {tabla} NO encontrada")
                print(f"      Ejecute primero: python migrar_db.py")
                return False
        
        print("✅ Todas las tablas necesarias están disponibles\n")
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar tablas: {e}")
        return False
    
    finally:
        if conn:
            conn.close()

def main():
    """Función principal del setup"""
    
    print("🏗️ Sistema ERP Constructora - Configuración Inicial")
    print("=" * 60)
    
    # Verificar estructura de BD
    if not verificar_tablas():
        return
    
    # Crear usuario administrador
    if crear_usuario_admin():
        print("\n" + "=" * 60)
        print("🎉 Configuración completada exitosamente!")
        print("   El sistema está listo para funcionar")
    else:
        print("\n" + "=" * 60)
        print("❌ La configuración no se pudo completar")
        print("   Revise los errores y vuelva a intentar")

if __name__ == "__main__":
    main()