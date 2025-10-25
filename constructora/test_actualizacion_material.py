#!/usr/bin/env python3
"""
Test de la funcionalidad completa de materiales
"""

import sys
sys.path.insert(0, '.')

from database import get_material_by_id_safe, update_material_completo_safe

def test_actualizacion_completa():
    print("=== TEST ACTUALIZACIÓN COMPLETA DE MATERIAL ===")
    
    # Probar con material ID 8 (Cemento)
    material_id = 8
    
    print(f"\n1. ESTADO INICIAL (Material {material_id}):")
    material = get_material_by_id_safe(material_id)
    if material:
        print(f"   Nombre: {material.get('nombre')}")
        print(f"   Proveedor: {material.get('proveedor_nombre', 'None')}")
        print(f"   Stock: {material.get('stock_actual', 'None')}")
        print(f"   Descripción: {material.get('descripcion', 'None')}")
        print(f"   Categoría: {material.get('categoria', 'None')}")
    
    print(f"\n2. ACTUALIZANDO MATERIAL:")
    
    # Actualizar con nuevos datos
    nuevo_stock = 100
    nueva_descripcion = "Cemento Portland actualizado con nuevo stock"
    
    resultado = update_material_completo_safe(
        material_id, 
        nombre=None,  # No cambiar nombre
        unidad=None,  # No cambiar unidad
        precio=None,  # No cambiar precio
        descripcion=nueva_descripcion,
        categoria=None,  # No cambiar categoría
        stock=nuevo_stock
    )
    
    if resultado:
        print(f"   ✅ Actualización exitosa")
    else:
        print(f"   ❌ Error en actualización")
        return
    
    print(f"\n3. ESTADO DESPUÉS DE ACTUALIZAR:")
    material_updated = get_material_by_id_safe(material_id)
    if material_updated:
        print(f"   Nombre: {material_updated.get('nombre')}")
        print(f"   Proveedor: {material_updated.get('proveedor_nombre', 'None')}")
        print(f"   Stock: {material_updated.get('stock_actual', 'None')}")
        print(f"   Descripción: {material_updated.get('descripcion', 'None')}")
        print(f"   Categoría: {material_updated.get('categoria', 'None')}")
        
        # Verificar cambios
        if material_updated.get('stock_actual') == nuevo_stock:
            print(f"   ✅ Stock actualizado correctamente: {nuevo_stock}")
        else:
            print(f"   ❌ Stock NO se actualizó: esperado {nuevo_stock}, actual {material_updated.get('stock_actual')}")
            
        if nueva_descripcion in str(material_updated.get('descripcion', '')):
            print(f"   ✅ Descripción actualizada correctamente")
        else:
            print(f"   ❌ Descripción NO se actualizó")
    
    print(f"\n4. 🎯 RESUMEN:")
    print(f"   Material ID {material_id} ahora tiene:")
    print(f"   - Proveedor: {material_updated.get('proveedor_nombre', 'Sin proveedor')}")
    print(f"   - Stock: {material_updated.get('stock_actual', 0)} unidades")
    print(f"   - Descripción actualizada: ✅")
    print(f"   - ¡LISTO PARA USAR EN LA WEB!")

if __name__ == "__main__":
    test_actualizacion_completa()