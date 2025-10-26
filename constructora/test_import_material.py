#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de importación de la función insert_material_completo_safe
"""
import sys
sys.path.append('.')

try:
    from database import insert_material_completo_safe, get_materiales_safe, get_proveedores_safe
    print("✅ Función insert_material_completo_safe importada exitosamente")
    
    # Verificar si hay proveedores disponibles
    proveedores = get_proveedores_safe()
    print(f"📦 Proveedores disponibles: {len(proveedores)}")
    
    if len(proveedores) > 0:
        print("Primer proveedor:", proveedores[0])
        
        # Test del material
        material_id = insert_material_completo_safe(
            nombre="Material de Prueba",
            unidad="Metro",
            precio=25.50,
            descripcion="Material de prueba para verificar función",
            categoria="Construcción", 
            stock=50,
            proveedor_id=proveedores[0]['id_proveedor']
        )
        
        if material_id:
            print(f"✅ Material creado exitosamente con ID: {material_id}")
            
            # Verificar que aparece en la lista
            materiales = get_materiales_safe()
            material_encontrado = None
            for mat in materiales:
                if mat.get('id_material') == material_id:
                    material_encontrado = mat
                    break
            
            if material_encontrado:
                print(f"✅ Material encontrado en lista:")
                print(f"   - Nombre: {material_encontrado.get('nombre_material')}")
                print(f"   - Stock: {material_encontrado.get('stock_actual')}")
                print(f"   - Proveedor: {material_encontrado.get('nombre_proveedor', 'N/A')}")
            else:
                print("❌ Material no encontrado en lista")
        else:
            print("❌ Error al crear material")
    else:
        print("❌ No hay proveedores disponibles")
        
except ImportError as e:
    print(f"❌ Error al importar función: {e}")
except Exception as e:
    print(f"❌ Error general: {e}")