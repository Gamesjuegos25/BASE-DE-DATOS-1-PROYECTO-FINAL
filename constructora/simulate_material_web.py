#!/usr/bin/env python3
"""
Simulación del formulario web de materiales para identificar problemas
"""
from database import insert_material_safe, get_materiales_safe
import traceback

def simulate_material_web_form():
    """Simular exactamente lo que hace el formulario web de materiales"""
    
    print("=== SIMULACIÓN FORMULARIO WEB DE MATERIALES ===")
    
    # Datos que enviaría el formulario HTML
    form_data = {
        'nombre': 'Cemento Portland Tipo I Web Test',
        'categoria': 'Concreto y Cemento',
        'unidad_medida': 'Saco',
        'precio_unitario': '45.75',
        'stock_minimo': '10'
    }
    
    print("1. DATOS DEL FORMULARIO:")
    for key, value in form_data.items():
        print(f"   {key}: {value}")
    
    # Simular el procesamiento como en app.py
    print("\n2. PROCESAMIENTO COMO EN APP.PY:")
    
    try:
        # Extraer datos como lo hace crear_material()
        nombre = form_data.get('nombre', '').strip()
        unidad = form_data.get('unidad_medida', '').strip()
        precio = form_data.get('precio_unitario')
        categoria = form_data.get('categoria', '').strip()
        
        print(f"   nombre: '{nombre}'")
        print(f"   unidad: '{unidad}'")
        print(f"   precio: '{precio}'")
        print(f"   categoria: '{categoria}' (NO SE USA)")
        
        # Validación como en app.py
        if not nombre:
            print("   ❌ ERROR: Nombre vacío")
            return
        else:
            print("   ✅ Validación de nombre: OK")
        
        # Conversión de precio como en app.py
        precio_numerico = None
        if precio:
            try:
                precio_numerico = float(precio)
                print(f"   ✅ Conversión de precio: {precio_numerico}")
            except ValueError:
                print(f"   ❌ ERROR: Precio inválido: {precio}")
                return
        
        # Llamar a insert_material_safe como en app.py
        print(f"\n3. INSERTANDO MATERIAL...")
        print(f"   Llamando: insert_material_safe(nombre='{nombre}', unidad='{unidad}', precio={precio_numerico})")
        
        material_id = insert_material_safe(nombre=nombre, unidad=unidad, precio=precio_numerico)
        
        if material_id:
            print(f"   ✅ ¡ÉXITO! Material creado con ID: {material_id}")
            
            # Verificar que aparece en la lista
            print(f"\n4. VERIFICANDO EN LISTADO...")
            materiales = get_materiales_safe()
            encontrado = False
            for material in materiales:
                if material.get('id_material') == material_id:
                    encontrado = True
                    print(f"   ✅ Material encontrado:")
                    print(f"      Nombre: {material.get('nombre')}")
                    print(f"      Unidad: {material.get('unidad')}")
                    print(f"      Precio: {material.get('precio')}")
                    break
            
            if not encontrado:
                print(f"   ❌ Material NO encontrado en listado")
        else:
            print(f"   ❌ ERROR: insert_material_safe retornó None")
            
    except Exception as e:
        print(f"   💥 EXCEPCIÓN: {str(e)}")
        traceback.print_exc()
    
    print("\n=== FIN DE SIMULACIÓN ===")

if __name__ == "__main__":
    simulate_material_web_form()