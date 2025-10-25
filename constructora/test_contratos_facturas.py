import requests
import time

# Esperar a que el servidor esté listo
time.sleep(2)

BASE_URL = "http://127.0.0.1:5000"

def test_contratos():
    """Probar módulo CONTRATOS"""
    print("\n🔍 PROBANDO MÓDULO CONTRATOS")
    print("=" * 50)
    
    try:
        # Test 1: Listar contratos
        print("\n1. GET /contratos")
        response = requests.get(f"{BASE_URL}/contratos", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Página de contratos carga correctamente")
            # Buscar si hay datos
            if "Sin obra asignada" in response.text or "nombre_obra" in response.text.lower():
                print("   📊 Datos de obras encontrados en la respuesta")
            else:
                print("   ⚠️  No se encontraron datos de obras")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def test_facturas():
    """Probar módulo FACTURAS"""
    print("\n🔍 PROBANDO MÓDULO FACTURAS")
    print("=" * 50)
    
    try:
        # Test 1: Listar facturas
        print("\n1. GET /facturas")
        response = requests.get(f"{BASE_URL}/facturas", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Página de facturas carga correctamente")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

def test_dashboard():
    """Probar dashboard"""
    print("\n🔍 PROBANDO DASHBOARD")
    print("=" * 50)
    
    try:
        print("\n1. GET / (dashboard)")
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Dashboard carga correctamente")
            # Buscar módulos
            if "Facturación & Contratos" in response.text:
                print("   ✅ Módulo 'Facturación & Contratos' visible")
            else:
                print("   ⚠️  Módulo 'Facturación & Contratos' no encontrado")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

if __name__ == "__main__":
    print("\n🚀 INICIANDO PRUEBAS DEL SISTEMA")
    print("=" * 50)
    
    test_dashboard()
    test_contratos()
    test_facturas()
    
    print("\n\n✅ PRUEBAS COMPLETADAS")
    print("=" * 50)
