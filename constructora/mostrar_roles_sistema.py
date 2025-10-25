#!/usr/bin/env python3
"""Script para mostrar todos los roles disponibles en el sistema"""

import sys
sys.path.append('.')

def mostrar_roles_completos():
    """Muestra todos los roles predeterminados del sistema"""
    
    roles_completos = [
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
    
    print("🎯 ROLES AGREGADOS AL SISTEMA DE USUARIOS")
    print("=" * 60)
    print(f"📊 Total de roles disponibles: {len(roles_completos)}")
    print()
    
    for i, rol in enumerate(roles_completos, 1):
        print(f"{i:2d}. 👤 {rol['nombre_rol']:22s} - {rol['descripcion_rol']}")
    
    print()
    print("✅ Estos roles ahora están disponibles en:")
    print("   • Formulario de crear usuario")
    print("   • Selector de rol en /usuarios/nuevo")
    print("   • Sistema de permisos y autenticación")
    print()
    print("🔧 Los roles se cargan automáticamente cuando:")
    print("   • No hay roles específicos en la base de datos")
    print("   • Se produce un error al consultar roles")
    print("   • Se inicializa el sistema por primera vez")

if __name__ == "__main__":
    mostrar_roles_completos()