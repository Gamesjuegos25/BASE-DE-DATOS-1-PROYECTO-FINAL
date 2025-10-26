#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import database as db

def check_proveedores_structure():
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Verificar estructura de la tabla
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'proveedores' 
            ORDER BY ordinal_position;
        """)
        
        print("=== ESTRUCTURA TABLA PROVEEDORES ===")
        for row in cursor.fetchall():
            print(f"- {row[0]} ({row[1]}) - Nullable: {row[2]} - Default: {row[3]}")
        
        # Verificar datos existentes
        cursor.execute("SELECT COUNT(*) FROM PROVEEDORES")
        count = cursor.fetchone()[0]
        print(f"\nTotal proveedores: {count}")
        
        # Mostrar algunos ejemplos
        cursor.execute("SELECT * FROM PROVEEDORES LIMIT 3")
        proveedores = cursor.fetchall()
        print("\nEjemplos:")
        for p in proveedores:
            print(f"- {p}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_proveedores_structure()