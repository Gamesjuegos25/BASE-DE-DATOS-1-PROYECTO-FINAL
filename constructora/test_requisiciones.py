"""
Script de prueba para el módulo de REQUISICIONES
"""
import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_requisiciones():
    """Prueba todas las rutas del módulo de requisiciones"""
    print("=" * 70)
    print("PROBANDO MÓDULO DE REQUISICIONES")
    print("=" * 70)
    
    # Test 1: Listar requisiciones
    print("\n1. Probando GET /requisiciones (listar)...")
    try:
        response = requests.get(f"{BASE_URL}/requisiciones", timeout=5)
        if response.status_code == 200:
            print(f"   ✓ Listar requisiciones: {response.status_code} OK")
            print(f"   - Tamaño de respuesta: {len(response.content)} bytes")
        else:
            print(f"   ✗ Error: {response.status_code}")
            print(f"   - Respuesta: {response.text[:200]}")
    except requests.exceptions.ConnectionError:
        print("   ✗ Error: No se puede conectar al servidor")
        print("   - Asegúrate de que el servidor esté corriendo (python app.py)")
        return False
    except Exception as e:
        print(f"   ✗ Error inesperado: {e}")
        return False
    
    # Test 2: Formulario de creación
    print("\n2. Probando GET /requisiciones/nueva (formulario crear)...")
    try:
        response = requests.get(f"{BASE_URL}/requisiciones/nueva", timeout=5)
        if response.status_code == 200:
            print(f"   ✓ Formulario crear: {response.status_code} OK")
            # Verificar que contenga elementos esperados
            if 'fecha_requisicion' in response.text and 'estado_requisicion' in response.text:
                print("   ✓ Formulario contiene campos esperados")
            else:
                print("   ⚠ Advertencia: Formulario puede estar incompleto")
        else:
            print(f"   ✗ Error: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    # Test 3: Verificar imports en app.py
    print("\n3. Verificando imports en app.py...")
    try:
        import app
        if hasattr(app, 'crear_requisicion'):
            print("   ✓ Ruta crear_requisicion existe")
        if hasattr(app, 'ver_requisicion'):
            print("   ✓ Ruta ver_requisicion existe")
        if hasattr(app, 'editar_requisicion'):
            print("   ✓ Ruta editar_requisicion existe")
        if hasattr(app, 'eliminar_requisicion'):
            print("   ✓ Ruta eliminar_requisicion existe")
    except Exception as e:
        print(f"   ✗ Error al importar app: {e}")
    
    # Test 4: Verificar funciones en database.py
    print("\n4. Verificando funciones en database.py...")
    try:
        from database import (
            get_requisiciones_safe,
            insert_requisicion_safe,
            get_requisicion_by_id_safe,
            update_requisicion_safe,
            delete_requisicion_safe
        )
        print("   ✓ get_requisiciones_safe importada")
        print("   ✓ insert_requisicion_safe importada")
        print("   ✓ get_requisicion_by_id_safe importada")
        print("   ✓ update_requisicion_safe importada")
        print("   ✓ delete_requisicion_safe importada")
    except ImportError as e:
        print(f"   ✗ Error al importar funciones: {e}")
    
    # Test 5: Verificar templates
    print("\n5. Verificando templates...")
    import os
    templates_dir = "templates/requisiciones"
    required_templates = ['listar.html', 'crear.html', 'detalle.html', 'editar.html']
    
    for template in required_templates:
        template_path = os.path.join(templates_dir, template)
        if os.path.exists(template_path):
            print(f"   ✓ {template} existe")
        else:
            print(f"   ✗ {template} NO existe")
    
    print("\n" + "=" * 70)
    print("PRUEBA COMPLETADA")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_requisiciones()
    sys.exit(0 if success else 1)
