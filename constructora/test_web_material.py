#!/usr/bin/env python3
"""
Test directo de las rutas de materiales
"""

import sys
sys.path.insert(0, '.')

def test_material_route():
    try:
        print("=== TEST DIRECTO DE RUTA MATERIALES ===")
        
        from app import app
        from database import get_material_by_id_safe
        
        print("✓ App y database importados correctamente")
        
        # Simular una request
        with app.test_client() as client:
            print("\n1. Probando lista de materiales...")
            response = client.get('/materiales')
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print("  ✓ Lista de materiales carga correctamente")
            else:
                print(f"  ✗ Error: {response.status_code}")
                print(f"  Data: {response.get_data(as_text=True)[:200]}")
            
            print("\n2. Probando detalle de material ID 1...")
            response = client.get('/materiales/1')
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                html_content = response.get_data(as_text=True)
                print("  ✓ Detalle de material carga correctamente")
                
                # Buscar datos específicos en el HTML
                if 'Cementos Nacionales' in html_content:
                    print("  ✓ Proveedor encontrado en HTML")
                else:
                    print("  ✗ Proveedor NO encontrado en HTML")
                
                if '500' in html_content and 'Stock' in html_content:
                    print("  ✓ Stock encontrado en HTML")
                else:
                    print("  ✗ Stock NO encontrado en HTML")
                    
                # Mostrar fragmento del HTML para debug
                print(f"\n  Fragmento del HTML:")
                lines = html_content.split('\n')
                for i, line in enumerate(lines):
                    if 'proveedor' in line.lower() or 'stock' in line.lower():
                        print(f"    Línea {i}: {line.strip()}")
                        
            else:
                print(f"  ✗ Error: {response.status_code}")
                print(f"  Data: {response.get_data(as_text=True)[:500]}")
        
        print("\n3. Verificando datos directos...")
        material = get_material_by_id_safe(1)
        if material:
            print(f"  ✓ Material cargado: {material.get('nombre')}")
            print(f"  ✓ Proveedor: {material.get('proveedor_nombre', 'None')}")
            print(f"  ✓ Stock: {material.get('stock_actual', 'None')}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_material_route()