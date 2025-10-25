#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            print("=== ESTRUCTURA EXACTA DE TABLAS DE INVENTARIO ===")
            
            # Estructura tabla inventarios
            print("\n1. TABLA INVENTARIOS:")
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'inventarios' 
                ORDER BY ordinal_position
            """)
            
            cols = cursor.fetchall()
            for col in cols:
                nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  {col[0]} ({col[1]}) - {nullable}{default}")
            
            # Ver datos de inventarios
            cursor.execute("SELECT * FROM inventarios LIMIT 5")
            inventarios = cursor.fetchall()
            print(f"\nDatos de inventarios ({len(inventarios)} registros):")
            for inv in inventarios:
                print(f"  {inv}")
            
            # Estructura tabla inventario_material
            print("\n2. TABLA INVENTARIO_MATERIAL:")
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
            
            # Ver datos de inventario_material
            cursor.execute("SELECT * FROM inventario_material LIMIT 5")
            inv_mat = cursor.fetchall()
            print(f"\nDatos inventario_material ({len(inv_mat)} registros):")
            for im in inv_mat:
                print(f"  {im}")
            
            # Query corregida para obtener datos reales
            print("\n3. DATOS COMPLETOS CON QUERY CORREGIDA:")
            cursor.execute("""
                SELECT 
                    m.id_material,
                    m.nombre_material,
                    m.unidad_material,
                    m.precio_unitario_material,
                    p.nombre_proveedor,
                    p.contacto_proveedor
                FROM materiales m
                LEFT JOIN proveedor_material pm ON m.id_material = pm.id_material
                LEFT JOIN proveedores p ON pm.id_proveedor = p.id_proveedor
                ORDER BY m.id_material
                LIMIT 5
            """)
            
            resultados = cursor.fetchall()
            for res in resultados:
                print(f"\nMaterial: {res[1]}")
                print(f"  Precio: Q{res[3] or 0}")
                print(f"  Proveedor: {res[4] or 'Sin proveedor'}")
                print(f"  Contacto: {res[5] or 'Sin contacto'}")
                
except Exception as e:
    print(f"Error: {e}")