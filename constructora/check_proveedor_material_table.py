#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import database as db

def check_proveedor_material_table():
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Verificar si existe la tabla proveedor_material
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'proveedor_material'
            )
        """)
        
        existe = cursor.fetchone()[0]
        print(f"Tabla proveedor_material existe: {existe}")
        
        if existe:
            print("\n=== ESTRUCTURA TABLA PROVEEDOR_MATERIAL ===")
            cursor.execute("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'proveedor_material' 
                ORDER BY ordinal_position;
            """)
            
            for row in cursor.fetchall():
                print(f"- {row[0]} ({row[1]}) - Nullable: {row[2]}")
        
        else:
            print("❌ La tabla proveedor_material NO existe")
            print("✅ Necesitamos crearla para relacionar materiales con proveedores")
        
        conn.close()
        return existe
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_proveedor_material_table()