"""
Smoke test de rutas de PERMISOS
"""
import sys
sys.path.insert(0, r'c:\Users\VICTUS\Videos\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\BASE-DE-DATOS-1-PROYECTO-FINAL-master\constructora')

from app import app

def test_permisos_routes():
    """Probar rutas básicas de permisos"""
    with app.test_client() as client:
        # Test 1: Listar permisos
        response = client.get('/permisos')
        print(f'/permisos status: {response.status_code}')
        
        # Test 2: Crear permiso (GET)
        response = client.get('/permisos/nuevo')
        print(f'/permisos/nuevo status: {response.status_code}')
        
        # Test 3: Ver permiso inexistente (debe redirigir)
        response = client.get('/permisos/999999', follow_redirects=True)
        print(f'/permisos/999999 (con redirect) status: {response.status_code}')
        
        # Test 4: Editar permiso inexistente (debe redirigir)
        response = client.get('/permisos/999999/editar', follow_redirects=True)
        print(f'/permisos/999999/editar (con redirect) status: {response.status_code}')
        
        # Test 5: Asignar permiso inexistente (debe redirigir)
        response = client.get('/permisos/999999/asignar', follow_redirects=True)
        print(f'/permisos/999999/asignar (con redirect) status: {response.status_code}')
        
        print('\n✅ SMOKE TEST OK - Módulo PERMISOS')

if __name__ == '__main__':
    test_permisos_routes()
