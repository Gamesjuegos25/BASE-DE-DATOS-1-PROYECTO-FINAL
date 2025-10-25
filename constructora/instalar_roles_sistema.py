#!/usr/bin/env python3
"""
Script para insertar roles en el sistema de constructora
Ejecuta los INSERT statements para crear la estructura de roles
"""

import sys
sys.path.append('.')

from database import get_connection
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def crear_tabla_roles():
    """Crear tabla roles si no existe"""
    sql_crear_tabla = """
    CREATE TABLE IF NOT EXISTS roles (
        id_rol SERIAL PRIMARY KEY,
        nombre_rol VARCHAR(50) NOT NULL UNIQUE,
        descripcion_rol VARCHAR(200),
        permisos TEXT[],
        activo BOOLEAN DEFAULT true,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    return sql_crear_tabla

def insertar_roles():
    """Insertar todos los roles del sistema"""
    sql_insertar_roles = """
    INSERT INTO roles (nombre_rol, descripcion_rol, permisos, activo) VALUES
    ('ADMINISTRADOR', 'Administrador del sistema con acceso completo', 
     ARRAY['ADMIN_USUARIOS', 'ADMIN_SISTEMA', 'VER_REPORTES', 'GESTIONAR_OBRAS', 'GESTIONAR_EMPLEADOS', 'GESTIONAR_FINANZAS'], true),
    
    ('Ingeniero Civil', 'Ingeniero Civil especializado en construcción', 
     ARRAY['GESTIONAR_OBRAS', 'VER_REPORTES', 'CREAR_PROYECTOS', 'SUPERVISAR_CONSTRUCCION'], true),
    
    ('Arquitecto', 'Arquitecto responsable del diseño y planificación', 
     ARRAY['GESTIONAR_OBRAS', 'CREAR_PROYECTOS', 'VER_REPORTES', 'DISEÑO_ARQUITECTONICO'], true),
    
    ('Supervisor de Obra', 'Supervisor encargado del control y seguimiento de obras', 
     ARRAY['SUPERVISAR_CONSTRUCCION', 'GESTIONAR_EMPLEADOS', 'VER_REPORTES', 'CONTROL_CALIDAD'], true),
    
    ('Jefe de Proyecto', 'Jefe responsable de la gestión integral de proyectos', 
     ARRAY['GESTIONAR_PROYECTOS', 'GESTIONAR_EMPLEADOS', 'VER_REPORTES', 'PLANIFICACION'], true),
    
    ('Contador', 'Contador responsable de la gestión financiera', 
     ARRAY['GESTIONAR_FINANZAS', 'VER_REPORTES', 'CONTABILIDAD', 'FACTURACION'], true),
    
    ('Operador de Equipo', 'Operador especializado en manejo de maquinaria', 
     ARRAY['OPERAR_EQUIPOS', 'VER_REPORTES', 'MANTENIMIENTO_EQUIPOS'], true),
    
    ('Almacenista', 'Encargado del control de inventarios y almacén', 
     ARRAY['GESTIONAR_INVENTARIO', 'GESTIONAR_MATERIALES', 'VER_REPORTES'], true),
    
    ('Asistente', 'Asistente administrativo con funciones de apoyo', 
     ARRAY['VER_REPORTES', 'ASISTENCIA_ADMINISTRATIVA'], true),
    
    ('Otro', 'Rol genérico para otros cargos no especificados', 
     ARRAY['VER_REPORTES'], true)
    
    ON CONFLICT (nombre_rol) DO UPDATE SET
        descripcion_rol = EXCLUDED.descripcion_rol,
        permisos = EXCLUDED.permisos,
        fecha_modificacion = CURRENT_TIMESTAMP;
    """
    return sql_insertar_roles

def crear_indices():
    """Crear índices para optimizar consultas"""
    indices = [
        "CREATE INDEX IF NOT EXISTS idx_usuarios_sistema_rol ON usuarios_sistema(rol_usuario);",
        "CREATE INDEX IF NOT EXISTS idx_roles_nombre ON roles(nombre_rol);",
        "CREATE INDEX IF NOT EXISTS idx_roles_activo ON roles(activo);"
    ]
    return indices

def insertar_usuarios_prueba():
    """Insertar usuarios de prueba para cada rol"""
    sql_usuarios = """
    INSERT INTO usuarios_sistema (nombre_usuario, rol_usuario, correo_usuario, contrasena_usuario) VALUES
    ('ing_civil_01', 'Ingeniero Civil', 'ingeniero@constructora.com', 'password123'),
    ('arquitecto_01', 'Arquitecto', 'arquitecto@constructora.com', 'password123'),
    ('supervisor_01', 'Supervisor de Obra', 'supervisor@constructora.com', 'password123'),
    ('jefe_proy_01', 'Jefe de Proyecto', 'jefe@constructora.com', 'password123'),
    ('contador_01', 'Contador', 'contador@constructora.com', 'password123'),
    ('operador_01', 'Operador de Equipo', 'operador@constructora.com', 'password123'),
    ('almacenista_01', 'Almacenista', 'almacenista@constructora.com', 'password123'),
    ('asistente_01', 'Asistente', 'asistente@constructora.com', 'password123')
    
    ON CONFLICT (nombre_usuario) DO NOTHING;
    """
    return sql_usuarios

def verificar_instalacion():
    """Verificar que los roles se instalaron correctamente"""
    verificaciones = [
        ("Roles creados:", "SELECT COUNT(*) as total_roles FROM roles WHERE activo = true;"),
        ("Usuarios con rol:", "SELECT COUNT(*) as usuarios_con_rol FROM usuarios_sistema WHERE rol_usuario IS NOT NULL;"),
        ("Detalle roles:", """
            SELECT r.id_rol, r.nombre_rol, r.descripcion_rol, 
                   COUNT(u.id_usuario) as usuarios_asignados
            FROM roles r 
            LEFT JOIN usuarios_sistema u ON u.rol_usuario = r.nombre_rol
            WHERE r.activo = true
            GROUP BY r.id_rol, r.nombre_rol, r.descripcion_rol
            ORDER BY r.id_rol;
        """)
    ]
    return verificaciones

def ejecutar_instalacion_roles():
    """Función principal para instalar todos los roles"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        logger.info("🚀 Iniciando instalación de roles del sistema...")
        
        # 1. Crear tabla roles
        logger.info("📋 Creando tabla roles...")
        cursor.execute(crear_tabla_roles())
        conn.commit()
        logger.info("✅ Tabla roles creada/verificada")
        
        # 2. Insertar roles
        logger.info("🎭 Insertando roles del sistema...")
        cursor.execute(insertar_roles())
        conn.commit()
        logger.info("✅ Roles insertados correctamente")
        
        # 3. Crear índices
        logger.info("🔍 Creando índices de optimización...")
        for indice in crear_indices():
            cursor.execute(indice)
        conn.commit()
        logger.info("✅ Índices creados")
        
        # 4. Insertar usuarios de prueba (opcional)
        respuesta = input("¿Desea insertar usuarios de prueba para cada rol? (s/n): ")
        if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            logger.info("👥 Insertando usuarios de prueba...")
            cursor.execute(insertar_usuarios_prueba())
            conn.commit()
            logger.info("✅ Usuarios de prueba insertados")
        
        # 5. Verificar instalación
        logger.info("🔎 Verificando instalación...")
        verificaciones = verificar_instalacion()
        
        for titulo, consulta in verificaciones:
            logger.info(f"\n{titulo}")
            cursor.execute(consulta)
            resultados = cursor.fetchall()
            
            if "Detalle roles" in titulo:
                logger.info("ID | Rol                    | Descripción                          | Usuarios")
                logger.info("-" * 80)
                for fila in resultados:
                    logger.info(f"{fila[0]:2d} | {fila[1]:22s} | {fila[2]:36s} | {fila[3]:2d}")
            else:
                for fila in resultados:
                    logger.info(f"   {fila[0]}")
        
        cursor.close()
        conn.close()
        
        logger.info("\n🎉 ¡Instalación de roles completada exitosamente!")
        logger.info("📝 Los roles están ahora disponibles en:")
        logger.info("   • Formulario de crear usuario (/usuarios/nuevo)")
        logger.info("   • Sistema de autenticación y permisos")
        logger.info("   • Gestión de usuarios (/usuarios)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error durante la instalación: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🏗️  INSTALADOR DE ROLES - SISTEMA CONSTRUCTORA")
    print("=" * 60)
    print()
    
    exito = ejecutar_instalacion_roles()
    
    if exito:
        print("\n✨ Proceso completado con éxito!")
    else:
        print("\n💥 Proceso completado con errores. Revisar logs.")
    
    print("\n" + "=" * 60)