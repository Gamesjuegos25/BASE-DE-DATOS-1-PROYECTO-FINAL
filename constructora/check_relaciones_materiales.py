#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            print("=== ESTRUCTURA DE TABLAS RELACIONADAS ===")
            
            # Estructura tabla PROVEEDORES
            print("\n1. TABLA PROVEEDORES:")
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'proveedores' 
                ORDER BY ordinal_position
            """)
            
            cols = cursor.fetchall()
            for col in cols:
                nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                print(f"  {col[0]} ({col[1]}) - {nullable}")
                
            # Datos de proveedores
            cursor.execute("SELECT COUNT(*) FROM proveedores")
            count = cursor.fetchone()[0]
            print(f"  Total proveedores: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM proveedores LIMIT 3")
                proveedores = cursor.fetchall()
                print("  Proveedores de ejemplo:")
                for prov in proveedores:
                    print(f"    {prov}")
            
            # Tabla PROVEEDOR_MATERIAL (relación)
            print("\n2. TABLA PROVEEDOR_MATERIAL:")
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'proveedor_material' 
                ORDER BY ordinal_position
            """)
            
            cols = cursor.fetchall()
            for col in cols:
                nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                print(f"  {col[0]} ({col[1]}) - {nullable}")
                
            cursor.execute("SELECT COUNT(*) FROM proveedor_material")
            count = cursor.fetchone()[0]
            print(f"  Total relaciones: {count}")
            
            # Tabla INVENTARIO_MATERIAL (stock)
            print("\n3. TABLA INVENTARIO_MATERIAL:")
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'inventario_material' 
                ORDER BY ordinal_position
            """)
            
            cols = cursor.fetchall()
            for col in cols:
                nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                print(f"  {col[0]} ({col[1]}) - {nullable}")
                
            cursor.execute("SELECT COUNT(*) FROM inventario_material")
            count = cursor.fetchone()[0]
            print(f"  Total registros de inventario: {count}")
            
            # Verificar si hay datos de stock para materiales existentes
            print("\n4. VERIFICACIÓN DE DATOS REALES:")
            cursor.execute("""
                SELECT m.id_material, m.nombre_material,
                       COUNT(pm.id_proveedor) as num_proveedores,
                       COUNT(im.id_inventario) as tiene_inventario
                FROM materiales m
                LEFT JOIN proveedor_material pm ON m.id_material = pm.id_material
                LEFT JOIN inventario_material im ON m.id_material = im.id_material
                GROUP BY m.id_material, m.nombre_material
                ORDER BY m.id_material
                LIMIT 5
            """)
            
            resultados = cursor.fetchall()
            print("Material -> Proveedores -> Stock:")
            for res in resultados:
                print(f"  {res[1]} -> {res[2]} proveedores -> {'SÍ' if res[3] > 0 else 'NO'} tiene stock")
                
except Exception as e:
    print(f"Error: {e}")