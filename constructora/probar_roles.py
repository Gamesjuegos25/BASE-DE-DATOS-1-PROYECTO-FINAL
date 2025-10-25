from database import obtener_roles_disponibles

print("🔍 Probando obtener_roles_disponibles...")
roles = obtener_roles_disponibles()

print(f"\n✅ Se encontraron {len(roles)} roles:")
for rol in roles:
    print(f"  - {rol['nombre_rol']} (ID: {rol['id_rol']})")
    if 'descripcion_rol' in rol:
        print(f"    Descripción: {rol['descripcion_rol']}")

print("\n🎯 Los roles ahora se obtienen desde la tabla 'roles' correctamente!")