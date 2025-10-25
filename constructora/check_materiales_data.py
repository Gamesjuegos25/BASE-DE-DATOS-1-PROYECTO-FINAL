#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            print("=== DATOS ACTUALES EN LA TABLA MATERIALES ===")
            
            cursor.execute("SELECT COUNT(*) FROM materiales")
            count = cursor.fetchone()[0]
            print(f"Total de materiales: {count}")
            
            if count > 0:
                cursor.execute("""
                    SELECT id_material, nombre_material, unidad_material, precio_unitario_material
                    FROM materiales 
                    ORDER BY id_material
                """)
                
                materiales = cursor.fetchall()
                print("\nMateriales existentes:")
                for mat in materiales:
                    print(f"  ID: {mat[0]} | Nombre: {mat[1]} | Unidad: {mat[2]} | Precio: {mat[3]}")
            else:
                print("No hay materiales en la tabla")
                
except Exception as e:
    print(f"Error: {e}")