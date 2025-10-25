"""
Smoke test de rutas de BODEGAS
"""
import sys
sys.path.insert(0, r'c:\Users\VICTUS\Videos\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\BASE-DE-DATOS-1-PROYECTO-FINAL-master\constructora')

from app import app

def test_bodegas_routes():
    """Probar rutas básicas de bodegas"""
    with app.test_client() as client:
        # Test 1: Listar bodegas
        response = client.get('/bodegas')
        print(f'/bodegas status: {response.status_code}')
        
        # Test 2: Crear bodega (GET)
        response = client.get('/bodegas/nueva')
        print(f'/bodegas/nueva status: {response.status_code}')
        
        # Test 3: Ver bodega inexistente (debe redirigir)
        response = client.get('/bodegas/999999', follow_redirects=True)
        print(f'/bodegas/999999 (con redirect) status: {response.status_code}')
        
        # Test 4: Editar bodega inexistente (debe redirigir)
        response = client.get('/bodegas/999999/editar', follow_redirects=True)
        print(f'/bodegas/999999/editar (con redirect) status: {response.status_code}')
        
        # Test 5: Asignar bodega inexistente (debe redirigir)
        response = client.get('/bodegas/999999/asignar', follow_redirects=True)
        print(f'/bodegas/999999/asignar (con redirect) status: {response.status_code}')
        
        print('\n✅ SMOKE TEST OK - Módulo BODEGAS')

if __name__ == '__main__':
    test_bodegas_routes()
