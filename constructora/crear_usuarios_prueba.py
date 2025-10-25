#!/usr/bin/env python3
"""
Script para crear un usuario de prueba en el sistema
"""

import sys
import os
from datetime import datetime

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_connection

def crear_usuario_prueba():
    """Crear un usuario de prueba en el sistema"""
    
    print("🔧 Creando usuario de prueba...")
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                
                # Verificar si ya existe el usuario de prueba
                cursor.execute("SELECT id_usuario FROM USUARIOS_SISTEMA WHERE nombre_usuario = %s", ('admin',))
                if cursor.fetchone():
                    print("❌ El usuario 'admin' ya existe")
                    return False
                
                # Insertar usuario de prueba
                cursor.execute("""
                    INSERT INTO USUARIOS_SISTEMA (
                        nombre_usuario, 
                        rol_usuario, 
                        correo_usuario, 
                        contrasena_usuario
                    ) VALUES (%s, %s, %s, %s)
                    RETURNING id_usuario
                """, (
                    'admin',           # nombre_usuario
                    'ADMINISTRADOR',   # rol_usuario
                    'admin@constructora.com',  # correo_usuario
                    'admin123'         # contrasena_usuario (texto plano para prueba)
                ))
                
                usuario_id = cursor.fetchone()[0]
                
                # Registrar auditoría
                cursor.execute("""
                    INSERT INTO AUDITORIAS (
                        accion_auditoria, 
                        fecha_auditoria
                    ) VALUES (%s, CURRENT_TIMESTAMP)
                """, ('USUARIO_PRUEBA: Usuario admin creado para pruebas',))
                
                conn.commit()
                
                print("✅ Usuario de prueba creado exitosamente!")
                print(f"   👤 Usuario: admin")
                print(f"   🔑 Contraseña: admin123")
                print(f"   📧 Email: admin@constructora.com")
                print(f"   👥 Rol: ADMINISTRADOR")
                print(f"   🆔 ID: {usuario_id}")
                
                return True
                
    except Exception as e:
        print(f"❌ Error al crear usuario de prueba: {e}")
        return False

def crear_usuario_operador():
    """Crear un usuario operador de prueba"""
    
    print("🔧 Creando usuario operador de prueba...")
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                
                # Verificar si ya existe
                cursor.execute("SELECT id_usuario FROM USUARIOS_SISTEMA WHERE nombre_usuario = %s", ('operador',))
                if cursor.fetchone():
                    print("❌ El usuario 'operador' ya existe")
                    return False
                
                # Insertar usuario operador
                cursor.execute("""
                    INSERT INTO USUARIOS_SISTEMA (
                        nombre_usuario, 
                        rol_usuario, 
                        correo_usuario, 
                        contrasena_usuario
                    ) VALUES (%s, %s, %s, %s)
                    RETURNING id_usuario
                """, (
                    'operador',        # nombre_usuario
                    'OPERADOR',        # rol_usuario
                    'operador@constructora.com',  # correo_usuario
                    'op123'           # contrasena_usuario
                ))
                
                usuario_id = cursor.fetchone()[0]
                
                # Registrar auditoría
                cursor.execute("""
                    INSERT INTO AUDITORIAS (
                        accion_auditoria, 
                        fecha_auditoria
                    ) VALUES (%s, CURRENT_TIMESTAMP)
                """, ('USUARIO_PRUEBA: Usuario operador creado para pruebas',))
                
                conn.commit()
                
                print("✅ Usuario operador creado exitosamente!")
                print(f"   👤 Usuario: operador")
                print(f"   🔑 Contraseña: op123")
                print(f"   📧 Email: operador@constructora.com")
                print(f"   👥 Rol: OPERADOR")
                print(f"   🆔 ID: {usuario_id}")
                
                return True
                
    except Exception as e:
        print(f"❌ Error al crear usuario operador: {e}")
        return False

def listar_usuarios():
    """Listar todos los usuarios del sistema"""
    
    print("📋 Usuarios en el sistema:")
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        id_usuario,
                        nombre_usuario,
                        rol_usuario,
                        correo_usuario
                    FROM USUARIOS_SISTEMA
                    ORDER BY id_usuario
                """)
                
                usuarios = cursor.fetchall()
                
                if usuarios:
                    print(f"{'ID':<5} {'Usuario':<15} {'Rol':<15} {'Email':<30}")
                    print("-" * 70)
                    for usuario in usuarios:
                        print(f"{usuario[0]:<5} {usuario[1]:<15} {usuario[2]:<15} {usuario[3]:<30}")
                else:
                    print("No hay usuarios en el sistema")
                
                return usuarios
                
    except Exception as e:
        print(f"❌ Error al listar usuarios: {e}")
        return []

def main():
    """Función principal"""
    
    print("🏗️ Sistema ERP Constructora - Creador de Usuarios de Prueba")
    print("=" * 60)
    
    # Listar usuarios existentes
    usuarios_existentes = listar_usuarios()
    print()
    
    # Crear usuarios de prueba
    if not any(u[1] == 'admin' for u in usuarios_existentes):
        crear_usuario_prueba()
    else:
        print("ℹ️ Usuario admin ya existe")
    
    print()
    
    if not any(u[1] == 'operador' for u in usuarios_existentes):
        crear_usuario_operador()
    else:
        print("ℹ️ Usuario operador ya existe")
    
    print()
    print("🎉 Usuarios de prueba listos!")
    print("   Puedes iniciar sesión en: http://127.0.0.1:5000/login")
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()