#!/usr/bin/env python3
"""
Test específico para verificar carga de proveedores y stock
"""

import sys
sys.path.insert(0, '.')

from database import get_material_by_id_safe, get_connection

def test_material_details():
    print("=== TEST DETALLADO DE CARGA DE MATERIAL ===")
    
    # Probar con material que sabemos que tiene proveedor y stock (ID: 1)
    print("\n1. PROBANDO MATERIAL ID: 1 (Cemento Gris 50kg)")
    material = get_material_by_id_safe(1)
    
    if material:
        print(f"✓ Material encontrado: {material.get('nombre')}")
        print(f"  Proveedor: '{material.get('proveedor_nombre', 'None')}'")
        print(f"  Contacto: '{material.get('proveedor_contacto', 'None')}'")
        print(f"  Stock actual: {material.get('stock_actual', 'None')}")
        print(f"  Stock mínimo: {material.get('stock_minimo', 'None')}")
        print(f"  Descripción: '{material.get('descripcion', 'None')}'")
        print(f"  Categoría: '{material.get('categoria', 'None')}'")
        
        # Mostrar todos los campos disponibles
        print(f"\n  Todos los campos:")
        for key, value in material.items():
            print(f"    {key}: {value}")
    else:
        print("✗ Material no encontrado")
    
    print("\n" + "="*50)
    print("2. VERIFICACIÓN DIRECTA EN BASE DE DATOS")
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Query directa para verificar datos
                cursor.execute("""
                    SELECT 
                        m.id_material,
                        m.nombre_material,
                        p.nombre_proveedor,
                        p.contacto_proveedor,
                        i.cantidad_inventario,
                        m.descripcion_material,
                        m.categoria_material
                    FROM materiales m
                    LEFT JOIN proveedor_material pm ON m.id_material = pm.id_material
                    LEFT JOIN proveedores p ON pm.id_proveedor = p.id_proveedor
                    LEFT JOIN inventario_material im ON m.id_material = im.id_material
                    LEFT JOIN inventarios i ON im.id_inventario = i.id_inventario
                    WHERE m.id_material = %s
                """, (1,))
                
                result = cursor.fetchone()
                if result:
                    print(f"✓ Query directa exitosa:")
                    print(f"  ID: {result[0]}")
                    print(f"  Nombre: {result[1]}")
                    print(f"  Proveedor: {result[2]}")
                    print(f"  Contacto: {result[3]}")
                    print(f"  Stock: {result[4]}")
                    print(f"  Descripción: {result[5]}")
                    print(f"  Categoría: {result[6]}")
                else:
                    print("✗ No se encontraron datos en query directa")
                    
    except Exception as e:
        print(f"Error en query directa: {e}")

if __name__ == "__main__":
    test_material_details()