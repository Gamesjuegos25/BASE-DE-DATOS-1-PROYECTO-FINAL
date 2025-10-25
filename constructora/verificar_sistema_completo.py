from database import get_empleados_safe, obtener_roles_disponibles

print("🚀 Verificación completa del sistema de usuarios")
print("=" * 50)

# Verificar roles
print("\n📋 ROLES DISPONIBLES:")
roles = obtener_roles_disponibles()
print(f"Total de roles: {len(roles)}")
for rol in roles:
    print(f"  ✓ {rol['nombre_rol']} (ID: {rol['id_rol']})")

# Verificar empleados
print(f"\n👥 EMPLEADOS DISPONIBLES:")
empleados = get_empleados_safe()
print(f"Total de empleados: {len(empleados)}")
for emp in empleados:
    print(f"  ✓ {emp['nombre_empleado']} {emp['apellido_empleado']} - {emp['tipo_empleado']} (ID: {emp['id_empleado']})")

print(f"\n🎯 RESUMEN:")
print(f"  ✅ {len(roles)} roles configurados en la tabla 'roles'")
print(f"  ✅ {len(empleados)} empleados disponibles")
print(f"  ✅ Sistema listo para crear usuarios")
print(f"\n🌐 Accede a: http://localhost:5000/usuarios/nuevo")