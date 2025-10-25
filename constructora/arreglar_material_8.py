#!/usr/bin/env python3
"""
Agregar proveedor y stock al material ID 8 (Cemento)
"""

import sys
sys.path.insert(0, '.')

from database import get_connection

def arreglar_material_8():
    print("=== ARREGLANDO MATERIAL ID 8 (CEMENTO) ===")
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # 1. Asignar proveedor (usaremos Cementos Nacionales)
                print("\n1. Asignando proveedor...")
                cursor.execute("""
                    INSERT INTO proveedor_material (id_proveedor, id_material)
                    VALUES (1, 8)
                    ON CONFLICT (id_proveedor, id_material) DO NOTHING
                """)
                if cursor.rowcount > 0:
                    print("   ✓ Proveedor asignado: Cementos Nacionales S.A.")
                else:
                    print("   ℹ️ Relación ya existía")
                
                # 2. Crear registro de inventario
                print("\n2. Creando registro de inventario...")
                
                # Primero crear el inventario
                cursor.execute("""
                    INSERT INTO inventarios (cantidad_inventario)
                    VALUES (75)
                    RETURNING id_inventario
                """)
                inventario_id = cursor.fetchone()[0]
                print(f"   ✓ Inventario creado con ID: {inventario_id}, cantidad: 75")
                
                # Luego asociar con el material
                cursor.execute("""
                    INSERT INTO inventario_material (id_inventario, id_material)
                    VALUES (%s, 8)
                    ON CONFLICT (id_inventario, id_material) DO NOTHING
                """, (inventario_id,))
                
                if cursor.rowcount > 0:
                    print("   ✓ Material asociado al inventario")
                else:
                    print("   ℹ️ Asociación ya existía")
                
                conn.commit()
                print("\n3. ✅ CAMBIOS GUARDADOS EN BASE DE DATOS")
                
                # 3. Verificar resultado
                print("\n4. VERIFICACIÓN:")
                cursor.execute("""
                    SELECT 
                        m.nombre_material,
                        p.nombre_proveedor,
                        p.contacto_proveedor,
                        i.cantidad_inventario
                    FROM materiales m
                    LEFT JOIN proveedor_material pm ON m.id_material = pm.id_material
                    LEFT JOIN proveedores p ON pm.id_proveedor = p.id_proveedor
                    LEFT JOIN inventario_material im ON m.id_material = im.id_material
                    LEFT JOIN inventarios i ON im.id_inventario = i.id_inventario
                    WHERE m.id_material = 8
                """)
                
                resultado = cursor.fetchone()
                if resultado:
                    print(f"   Material: {resultado[0]}")
                    print(f"   Proveedor: {resultado[1]}")
                    print(f"   Contacto: {resultado[2]}")
                    print(f"   Stock: {resultado[3]}")
                else:
                    print("   ❌ No se pudo verificar")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    arreglar_material_8()