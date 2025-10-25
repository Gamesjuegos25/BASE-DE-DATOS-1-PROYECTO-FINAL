"""
Script para probar que el fix de bitácora funciona
"""
import requests

BASE_URL = "http://127.0.0.1:5000"

print("=" * 70)
print("PROBANDO FIX DE BITÁCORAS")
print("=" * 70)

# Probar formulario de crear bitácora
print("\nProbando GET /bitacoras/nueva...")
try:
    response = requests.get(f"{BASE_URL}/bitacoras/nueva", timeout=5)
    if response.status_code == 200:
        print(f"✓ Formulario carga correctamente: {response.status_code} OK")
        
        # Verificar que no contenga 'moment()'
        if 'moment()' in response.text:
            print("✗ ERROR: Todavía contiene moment()")
        else:
            print("✓ No contiene moment()")
        
        # Verificar que contenga el campo fecha
        if 'fecha_bitacora' in response.text:
            print("✓ Contiene campo fecha_bitacora")
        else:
            print("✗ ERROR: No contiene campo fecha_bitacora")
            
        print(f"✓ Tamaño de respuesta: {len(response.content)} bytes")
    else:
        print(f"✗ Error: {response.status_code}")
        print(f"Respuesta: {response.text[:500]}")
except requests.exceptions.ConnectionError:
    print("✗ Error: No se puede conectar al servidor")
    print("  Asegúrate de que el servidor esté corriendo (python app.py)")
except Exception as e:
    print(f"✗ Error inesperado: {e}")

print("\n" + "=" * 70)
print("PRUEBA COMPLETADA")
print("=" * 70)
