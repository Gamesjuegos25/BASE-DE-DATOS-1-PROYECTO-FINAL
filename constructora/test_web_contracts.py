#!/usr/bin/env python3
import requests
import json
from urllib.parse import urlencode

def test_web_contract_creation():
    """Probar la creación de contratos a través de la interfaz web"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("=== PRUEBA DE CREACIÓN WEB DE CONTRATOS ===")
    
    # 1. Probar acceso a la página de crear contrato
    try:
        print("1. Probando acceso a /contratos/nuevo...")
        response = requests.get(f"{base_url}/contratos/nuevo", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Página carga correctamente")
            
            # Verificar que contiene los elementos esperados
            content = response.text
            checks = [
                ('select id="cliente_id"', "Campo select de cliente"),
                ('select id="obra_id"', "Campo select de obra"),
                ('input id="numero_contrato"', "Campo número de contrato"),
                ('input id="valor_total"', "Campo valor total"),
                ('form method="POST"', "Formulario POST")
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"   ✅ {description}: Encontrado")
                else:
                    print(f"   ❌ {description}: NO encontrado")
        else:
            print(f"   ❌ Error al cargar página: {response.status_code}")
            print(f"   Contenido: {response.text[:500]}")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ No se puede conectar al servidor")
        print("   💡 Asegúrate de que el servidor esté corriendo en http://127.0.0.1:5000")
        return
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return
    
    # 2. Probar envío de formulario
    try:
        print("\n2. Probando envío de formulario...")
        
        form_data = {
            'numero_contrato': 'CON-WEB-TEST-001',
            'cliente_id': '1',
            'obra_id': '16', 
            'fecha_inicio': '2025-10-25',
            'fecha_fin': '2025-12-31',
            'valor_total': '175000.00',
            'estado': 'activo'
        }
        
        print("   Datos del formulario:")
        for key, value in form_data.items():
            print(f"     {key}: {value}")
        
        response = requests.post(
            f"{base_url}/contratos/nuevo", 
            data=form_data,
            timeout=10,
            allow_redirects=False
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Redirección (probable éxito)")
            redirect_location = response.headers.get('Location', 'No location header')
            print(f"   Redirecciona a: {redirect_location}")
        elif response.status_code == 200:
            print("   ⚠️  Retorna a la misma página (posible error)")
            # Buscar mensajes de error en la respuesta
            if "error" in response.text.lower() or "Error" in response.text:
                print("   ❌ Posible mensaje de error en la página")
            else:
                print("   ℹ️  Página recargada sin errores visibles")
        else:
            print(f"   ❌ Error inesperado: {response.status_code}")
            print(f"   Respuesta: {response.text[:500]}")
            
    except Exception as e:
        print(f"   ❌ Error en envío: {str(e)}")
    
    print("\n=== FIN DE PRUEBA WEB ===")

if __name__ == "__main__":
    test_web_contract_creation()