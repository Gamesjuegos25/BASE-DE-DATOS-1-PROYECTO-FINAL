"""
Test de renderizado de templates de PERMISOS
"""
import sys
sys.path.insert(0, r'c:\Users\VICTUS\Videos\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\BASE-DE-DATOS-1-PROYECTO-FINAL-master\constructora')

from app import app
from flask import render_template

def test_render_permisos():
    """Probar renderizado de templates de permisos"""
    with app.app_context():
        with app.test_request_context('/'):
            # Datos de prueba
            permisos = [
                {
                    'id_permiso': 1,
                    'modulo_permiso': 'Obras',
                    'nivel_acceso_permiso': 'Lectura',
                    'usuarios_asignados': 3
                },
                {
                    'id_permiso': 2,
                    'modulo_permiso': 'Facturas',
                    'nivel_acceso_permiso': 'Admin',
                    'usuarios_asignados': 1
                },
                {
                    'id_permiso': 3,
                    'modulo_permiso': 'Reportes',
                    'nivel_acceso_permiso': None,
                    'usuarios_asignados': 0
                }
            ]
            
            permiso = {
                'id_permiso': 1,
                'modulo_permiso': 'Obras',
                'nivel_acceso_permiso': 'Lectura',
                'usuarios_asignados': 3
            }
            
            usuarios_asignados = [
                {
                    'id_usuario': 1,
                    'nombre_usuario': 'admin',
                    'correo_usuario': 'admin@constructora.com',
                    'rol_usuario': 'Administrador',
                    'fecha_asignacion_usuario_permiso': None
                },
                {
                    'id_usuario': 2,
                    'nombre_usuario': 'jperez',
                    'correo_usuario': 'jperez@constructora.com',
                    'rol_usuario': 'Usuario',
                    'fecha_asignacion_usuario_permiso': None
                }
            ]
            
            usuarios_sin_permiso = [
                {
                    'id_usuario': 3,
                    'nombre_usuario': 'mgarcia',
                    'correo_usuario': 'mgarcia@constructora.com',
                    'rol_usuario': 'Usuario'
                }
            ]
            
            # Test 1: listar
            try:
                html = render_template('permisos/listar.html', permisos=permisos)
                print(f'✅ permisos/listar.html OK {len(html)}')
            except Exception as e:
                print(f'❌ permisos/listar.html ERROR: {e}')
            
            # Test 2: crear
            try:
                html = render_template('permisos/crear.html')
                print(f'✅ permisos/crear.html OK {len(html)}')
            except Exception as e:
                print(f'❌ permisos/crear.html ERROR: {e}')
            
            # Test 3: detalle
            try:
                html = render_template('permisos/detalle.html', 
                                     permiso=permiso, 
                                     usuarios_asignados=usuarios_asignados)
                print(f'✅ permisos/detalle.html OK {len(html)}')
            except Exception as e:
                print(f'❌ permisos/detalle.html ERROR: {e}')
            
            # Test 4: editar
            try:
                html = render_template('permisos/editar.html', permiso=permiso)
                print(f'✅ permisos/editar.html OK {len(html)}')
            except Exception as e:
                print(f'❌ permisos/editar.html ERROR: {e}')
            
            # Test 5: asignar
            try:
                html = render_template('permisos/asignar.html',
                                     permiso=permiso,
                                     usuarios_con_permiso=usuarios_asignados,
                                     usuarios_sin_permiso=usuarios_sin_permiso)
                print(f'✅ permisos/asignar.html OK {len(html)}')
            except Exception as e:
                print(f'❌ permisos/asignar.html ERROR: {e}')

if __name__ == '__main__':
    test_render_permisos()
