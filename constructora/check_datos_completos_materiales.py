#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            print("=== DATOS COMPLETOS DE MATERIALES CON PROVEEDORES Y STOCK ===")
            
            # Query completa con todas las relaciones
            cursor.execute("""
                SELECT 
                    m.id_material,
                    m.nombre_material,
                    m.unidad_material,
                    m.precio_unitario_material,
                    p.nombre_proveedor,
                    p.contacto_proveedor,
                    i.cantidad_actual,
                    i.cantidad_minima,
                    i.ubicacion_bodega
                FROM materiales m
                LEFT JOIN proveedor_material pm ON m.id_material = pm.id_material
                LEFT JOIN proveedores p ON pm.id_proveedor = p.id_proveedor
                LEFT JOIN inventario_material im ON m.id_material = im.id_material
                LEFT JOIN inventarios i ON im.id_inventario = i.id_inventario
                ORDER BY m.id_material
            """)
            
            resultados = cursor.fetchall()
            print(f"\nResultados encontrados: {len(resultados)}")
            
            for res in resultados:
                print(f"\nMaterial ID: {res[0]}")
                print(f"  Nombre: {res[1]}")
                print(f"  Unidad: {res[2]}")
                print(f"  Precio: {res[3]}")
                print(f"  Proveedor: {res[4] or 'Sin proveedor'}")
                print(f"  Contacto: {res[5] or 'Sin contacto'}")
                print(f"  Stock actual: {res[6] or 'Sin stock'}")
                print(f"  Stock mínimo: {res[7] or 'Sin mínimo'}")
                print(f"  Ubicación: {res[8] or 'Sin ubicación'}")
            
            # Verificar estructura de tabla inventarios
            print("\n=== ESTRUCTURA TABLA INVENTARIOS ===")
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'inventarios' 
                ORDER BY ordinal_position
            """)
            
            cols = cursor.fetchall()
            for col in cols:
                nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                print(f"  {col[0]} ({col[1]}) - {nullable}")
                
            # Ver datos directos de inventarios
            print("\n=== DATOS DIRECTOS DE INVENTARIOS ===")
            cursor.execute("SELECT * FROM inventarios ORDER BY id_inventario")
            inventarios = cursor.fetchall()
            
            for inv in inventarios:
                print(f"  Inventario: {inv}")
                
except Exception as e:
    print(f"Error: {e}")