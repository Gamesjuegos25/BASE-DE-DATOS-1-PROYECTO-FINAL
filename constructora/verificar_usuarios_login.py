from database import obtener_usuarios_sistema

print("🔐 Verificando usuarios en el sistema...")
usuarios = obtener_usuarios_sistema()

print(f"Total de usuarios: {len(usuarios)}")
print("\n👤 Primeros 5 usuarios:")
for i, usuario in enumerate(usuarios[:5], 1):
    print(f"{i}. Usuario: {usuario['nombre_usuario']}")
    print(f"   Rol: {usuario['nombre_rol']}")
    print(f"   Email: {usuario['email']}")
    print(f"   Nombre completo: {usuario['nombre_completo']}")
    print()

if len(usuarios) == 0:
    print("❌ No hay usuarios en el sistema")
    print("💡 El sistema necesita un usuario administrador para acceder")
else:
    print("✅ Hay usuarios en el sistema")
    print("🌐 Puedes intentar hacer login en: http://127.0.0.1:5000/login")