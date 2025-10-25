#!/usr/bin/env python3
from database import insert_material_safe, get_materiales_safe
import traceback

def test_material_creation():
    """Probar la creación de materiales paso a paso"""
    
    print("=== DIAGNÓSTICO DE CREACIÓN DE MATERIALES ===")
    
    # 1. Verificar materiales existentes
    print("\n1. MATERIALES EXISTENTES:")
    try:
        materiales = get_materiales_safe()
        print(f"   Cantidad: {len(materiales)}")
        if materiales:
            for i, material in enumerate(materiales[:3]):
                print(f"   [{i+1}] ID: {material.get('id_material')}, Nombre: {material.get('nombre', 'Sin nombre')}")
    except Exception as e:
        print(f"   ❌ Error obteniendo materiales: {e}")
        return
    
    # 2. Intentar crear un material nuevo
    print("\n2. CREANDO NUEVO MATERIAL...")
    
    import random
    numero_aleatorio = random.randint(100, 999)
    
    test_data = {
        'nombre': f'Material Prueba {numero_aleatorio}',
        'unidad': 'unidad',
        'precio': 25.50
    }
    
    print(f"   Datos del material:")
    for key, value in test_data.items():
        print(f"     {key}: {value}")
    
    try:
        material_id = insert_material_safe(
            nombre=test_data['nombre'],
            unidad=test_data['unidad'],
            precio=test_data['precio']
        )
        
        if material_id:
            print(f"   ✅ ¡ÉXITO! Material creado con ID: {material_id}")
            
            # Verificar que se creó correctamente
            print("\n3. VERIFICANDO CREACIÓN...")
            materiales_actualizados = get_materiales_safe()
            material_encontrado = False
            
            for material in materiales_actualizados:
                if material.get('id_material') == material_id:
                    material_encontrado = True
                    print(f"   ✅ Material encontrado en la base:")
                    print(f"      ID: {material.get('id_material')}")
                    print(f"      Nombre: {material.get('nombre')}")
                    print(f"      Unidad: {material.get('unidad')}")
                    print(f"      Precio: {material.get('precio')}")
                    break
            
            if not material_encontrado:
                print(f"   ❌ Material no encontrado en listado (posible problema de caché)")
        else:
            print(f"   ❌ ERROR: La función insert_material_safe retornó None")
            
    except Exception as e:
        print(f"   💥 EXCEPCIÓN: {str(e)}")
        traceback.print_exc()
    
    print("\n=== FIN DE DIAGNÓSTICO ===")

if __name__ == "__main__":
    test_material_creation()