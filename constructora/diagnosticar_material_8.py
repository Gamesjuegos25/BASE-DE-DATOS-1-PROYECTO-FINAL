#!/usr/bin/env python3
"""
Diagnóstico específico del material ID 8 (Cemento)
"""

import sys
sys.path.insert(0, '.')

from database import get_connection, get_material_by_id_safe

def diagnosticar_material_8():
    print("=== DIAGNÓSTICO MATERIAL ID 8 (CEMENTO) ===")
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Verificar datos del material
                print("\n1. DATOS DEL MATERIAL:")
                cursor.execute("SELECT * FROM materiales WHERE id_material = 8")
                material = cursor.fetchone()
                print(f"   Material: {material}")
                
                # Verificar relación con proveedor
                print("\n2. RELACIÓN PROVEEDOR:")
                cursor.execute("""
                    SELECT pm.*, p.nombre_proveedor, p.contacto_proveedor
                    FROM proveedor_material pm
                    LEFT JOIN proveedores p ON pm.id_proveedor = p.id_proveedor
                    WHERE pm.id_material = 8
                """)
                relacion = cursor.fetchone()
                if relacion:
                    print(f"   Relación: {relacion}")
                else:
                    print("   ❌ NO HAY RELACIÓN CON PROVEEDOR")
                
                # Verificar inventario
                print("\n3. INVENTARIO:")
                cursor.execute("""
                    SELECT im.*, i.cantidad_inventario
                    FROM inventario_material im
                    LEFT JOIN inventarios i ON im.id_inventario = i.id_inventario
                    WHERE im.id_material = 8
                """)
                inventario = cursor.fetchone()
                if inventario:
                    print(f"   Inventario: {inventario}")
                else:
                    print("   ❌ NO HAY REGISTRO DE INVENTARIO")
                
                # Verificar función get_material_by_id_safe
                print("\n4. FUNCIÓN get_material_by_id_safe:")
                material_func = get_material_by_id_safe(8)
                if material_func:
                    print(f"   Proveedor desde función: {material_func.get('proveedor_nombre', 'None')}")
                    print(f"   Stock desde función: {material_func.get('stock_actual', 'None')}")
                else:
                    print("   ❌ FUNCIÓN NO RETORNA DATOS")
                
                # Mostrar todos los proveedores disponibles
                print("\n5. PROVEEDORES DISPONIBLES:")
                cursor.execute("SELECT * FROM proveedores")
                proveedores = cursor.fetchall()
                for prov in proveedores:
                    print(f"   {prov}")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnosticar_material_8()