#!/usr/bin/env python3
"""
Test del formulario web de materiales - POST request simulado
"""
import requests
import random

def test_material_web_form():
    """Probar el formulario web de materiales con POST request"""
    
    print("=== PRUEBA REAL DEL FORMULARIO WEB DE MATERIALES ===")
    
    base_url = "http://127.0.0.1:5000"
    
    # 1. Primero, obtener la página del formulario (GET)
    try:
        print("1. OBTENIENDO PÁGINA DEL FORMULARIO...")
        response = requests.get(f"{base_url}/materiales/nuevo", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Error al cargar formulario: {response.text[:300]}")
            return
        else:
            print("   ✅ Formulario carga correctamente")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ No se puede conectar al servidor")
        print("   💡 Asegúrate de que el servidor esté corriendo en http://127.0.0.1:5000")
        return
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return
    
    # 2. Enviar datos del formulario (POST)
    try:
        print("\n2. ENVIANDO FORMULARIO...")
        
        numero_aleatorio = random.randint(100, 999)
        
        form_data = {
            'nombre': f'Material Web Test {numero_aleatorio}',
            'categoria': 'Concreto y Cemento',
            'unidad_medida': 'Kilogramo',
            'precio_unitario': '35.50',
            'stock_minimo': '5'
        }
        
        print("   Datos enviados:")
        for key, value in form_data.items():
            print(f"     {key}: {value}")
        
        response = requests.post(
            f"{base_url}/materiales/nuevo", 
            data=form_data,
            timeout=10,
            allow_redirects=False
        )
        
        print(f"   Status de respuesta: {response.status_code}")
        
        if response.status_code == 302:
            print("   ✅ Redirección (probable éxito)")
            redirect_location = response.headers.get('Location', 'No location header')
            print(f"   Redirecciona a: {redirect_location}")
            
            # Verificar si se redirige a la lista de materiales
            if 'materiales' in redirect_location.lower():
                print("   ✅ Redirige a lista de materiales - ¡ÉXITO!")
            else:
                print(f"   ⚠️  Redirige a ubicación inesperada")
                
        elif response.status_code == 200:
            print("   ⚠️  Retorna a la misma página (posible error)")
            # Buscar mensajes de error o éxito en la respuesta
            content = response.text.lower()
            if "error" in content:
                print("   ❌ Posible mensaje de error en la página")
            elif "éxito" in content or "success" in content:
                print("   ✅ Posible mensaje de éxito")
            else:
                print("   ℹ️  Sin mensajes evidentes")
        else:
            print(f"   ❌ Error inesperado: {response.status_code}")
            print(f"   Respuesta: {response.text[:500]}")
            
    except Exception as e:
        print(f"   ❌ Error en envío: {str(e)}")
    
    print("\n=== FIN DE PRUEBA WEB ===")

if __name__ == "__main__":
    test_material_web_form()