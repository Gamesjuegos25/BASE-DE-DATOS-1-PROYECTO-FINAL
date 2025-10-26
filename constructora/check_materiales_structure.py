#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import database as db

def check_materiales_structure():
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        print("=== ESTRUCTURA TABLA MATERIALES ===")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'materiales' 
            ORDER BY ordinal_position;
        """)
        
        for row in cursor.fetchall():
            print(f"- {row[0]} ({row[1]}) - Nullable: {row[2]} - Default: {row[3]}")
        
        print("\n=== ESTRUCTURA TABLA INVENTARIOS ===")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'inventarios' 
            ORDER BY ordinal_position;
        """)
        
        for row in cursor.fetchall():
            print(f"- {row[0]} ({row[1]}) - Nullable: {row[2]} - Default: {row[3]}")
        
        print("\n=== ESTRUCTURA TABLA INVENTARIO_MATERIAL ===")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'inventario_material' 
            ORDER BY ordinal_position;
        """)
        
        for row in cursor.fetchall():
            print(f"- {row[0]} ({row[1]}) - Nullable: {row[2]} - Default: {row[3]}")
            
        # Verificar materiales existentes
        cursor.execute("SELECT COUNT(*) FROM MATERIALES")
        count_materiales = cursor.fetchone()[0]
        print(f"\nTotal materiales: {count_materiales}")
        
        # Mostrar ejemplos de materiales
        cursor.execute("SELECT * FROM MATERIALES LIMIT 3")
        materiales = cursor.fetchall()
        print("\nEjemplos materiales:")
        for m in materiales:
            print(f"- {m}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_materiales_structure()