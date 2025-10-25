#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación de tablas de asignaciones para obras
Autor: Sistema de Constructora
Fecha: 2024
"""

from database import get_connection
import psycopg2.extras

def verificar_tablas_asignaciones():
    """Verificar qué tablas de asignaciones existen"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Buscar tablas relacionadas con asignaciones
        cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND (table_name ILIKE '%asign%' OR 
             table_name ILIKE '%empleado%' OR
             table_name ILIKE '%obra%' OR
             table_name ILIKE '%material%' OR
             table_name ILIKE '%vehiculo%' OR
             table_name ILIKE '%equipo%')
        ORDER BY table_name
        """)
        
        print("=== TABLAS RELACIONADAS CON ASIGNACIONES ===")
        tablas = cursor.fetchall()
        for row in tablas:
            print(f"  📋 {row[0]}")
        
        print("\n=== ESTRUCTURA DE TABLAS CLAVE ===")
        
        # Verificar estructura de obras
        cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'obras' 
        ORDER BY ordinal_position
        """)
        
        print("\n📊 OBRAS:")
        for col in cursor.fetchall():
            print(f"    {col[0]}: {col[1]}")
            
        # Verificar empleados
        cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'empleados' 
        ORDER BY ordinal_position
        """)
        
        print("\n👥 EMPLEADOS:")
        for col in cursor.fetchall():
            print(f"    {col[0]}: {col[1]}")
            
        # Verificar si hay tablas de asignación específicas
        posibles_tablas = ['obras_empleados', 'asignaciones_obras', 'empleados_obras', 'obra_empleados']
        
        print("\n=== VERIFICANDO TABLAS DE ASIGNACIÓN ===")
        for tabla in posibles_tablas:
            cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            )
            """, (tabla,))
            
            existe = cursor.fetchone()[0]
            if existe:
                print(f"✅ {tabla} - EXISTE")
                cursor.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{tabla}' 
                ORDER BY ordinal_position
                """)
                for col in cursor.fetchall():
                    print(f"    {col[0]}: {col[1]}")
            else:
                print(f"❌ {tabla} - NO EXISTE")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verificar_tablas_asignaciones()