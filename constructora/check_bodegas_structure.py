#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import database as db

def check_bodegas_structure():
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Verificar estructura de la tabla
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default 
            FROM information_schema.columns 
            WHERE table_name = 'bodegas' 
            ORDER BY ordinal_position;
        """)
        
        print("=== ESTRUCTURA TABLA BODEGAS ===")
        for row in cursor.fetchall():
            print(f"- {row[0]} ({row[1]}) - Nullable: {row[2]} - Default: {row[3]}")
        
        # Verificar datos existentes
        cursor.execute("SELECT COUNT(*) FROM BODEGAS")
        count = cursor.fetchone()[0]
        print(f"\nTotal bodegas: {count}")
        
        # Verificar empleados disponibles para el dropdown
        cursor.execute("""
            SELECT id_empleado, nombre_empleado, apellido_empleado, tipo_empleado 
            FROM EMPLEADOS 
            WHERE tipo_empleado IN ('Supervisor', 'Gerente', 'Coordinador', 'Jefe')
            ORDER BY nombre_empleado 
            LIMIT 10
        """)
        empleados = cursor.fetchall()
        print(f"\n=== EMPLEADOS SUPERVISORES DISPONIBLES ({len(empleados)}) ===")
        for emp in empleados:
            print(f"- ID: {emp[0]}, Nombre: {emp[1]} {emp[2] or ''}, Tipo: {emp[3]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_bodegas_structure()