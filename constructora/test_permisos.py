from database import verificar_permiso_usuario, obtener_permisos_usuario

# ID del usuario con rol ADMINISTRADOR
id_usuario = 1

print("\n===== VERIFICANDO PERMISOS DEL USUARIO 1 (ADMINISTRADOR) =====")

# Obtener todos los permisos
permisos = obtener_permisos_usuario(id_usuario)
print(f"\nPermisos del usuario: {len(permisos)} permisos")
for permiso in permisos:
    print(f"  - {permiso.get('codigo_permiso')}: {permiso.get('nombre_permiso')}")

# Verificar permisos específicos
print("\n===== VERIFICANDO PERMISOS ESPECÍFICOS =====")
permisos_a_verificar = ['ADMIN_USUARIOS', 'ADMIN_SISTEMA', 'VER_REPORTES', 'GESTIONAR_OBRAS']

for codigo_permiso in permisos_a_verificar:
    tiene_permiso = verificar_permiso_usuario(id_usuario, codigo_permiso)
    print(f"  {codigo_permiso}: {'✅ SÍ' if tiene_permiso else '❌ NO'}")
