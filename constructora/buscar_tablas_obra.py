#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buscar todas las tablas de asignaciones relacionadas con obras
"""

from database import get_connection

def buscar_tablas_obra():
    """Buscar todas las tablas que contengan 'obra' en el nombre"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name ILIKE '%obra%'
        ORDER BY table_name
        """)
        
        print("=== TODAS LAS TABLAS CON 'OBRA' ===")
        tablas_obra = cursor.fetchall()
        for row in tablas_obra:
            print(f"  📋 {row[0]}")
            
        # Verificar estructura de las que parecen de asignación
        tablas_asignacion = ['obra_vehiculo', 'obra_area', 'obra_cliente']
        
        for tabla in tablas_asignacion:
            print(f"\n=== {tabla.upper()} ===")
            cursor.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = '{tabla}' 
            ORDER BY ordinal_position
            """)
            
            columns = cursor.fetchall()
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                print(f"  📌 {col[0]}: {col[1]} ({nullable})")
                
        # Verificar si necesitamos crear tablas de asignación
        print("\n=== VERIFICANDO NECESIDAD DE CREAR TABLAS ===")
        
        tablas_necesarias = [
            ('obra_empleado', 'Para asignar empleados (arquitectos, ingenieros, obreros) a obras'),
            ('obra_material', 'Para asignar materiales específicos a obras'),
        ]
        
        for tabla, descripcion in tablas_necesarias:
            cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            )
            """, (tabla,))
            
            existe = cursor.fetchone()[0]
            if existe:
                print(f"✅ {tabla} - YA EXISTE")
            else:
                print(f"❌ {tabla} - NECESITA CREARSE ({descripcion})")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    buscar_tablas_obra()