#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación detallada de tablas de asignaciones
"""

from database import get_connection

def verificar_estructuras_asignacion():
    """Verificar estructura de tablas de asignación existentes"""
    conn = get_connection()
    cursor = conn.cursor()
    
    tablas_asignacion = [
        'area_empleado',
        'equipo_asignacion', 
        'obra_vehiculo',
        'asignaciones_equipo'
    ]
    
    try:
        for tabla in tablas_asignacion:
            print(f"\n=== ESTRUCTURA DE {tabla.upper()} ===")
            cursor.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = '{tabla}' 
            ORDER BY ordinal_position
            """)
            
            columns = cursor.fetchall()
            if columns:
                for col in columns:
                    nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                    print(f"  📌 {col[0]}: {col[1]} ({nullable})")
                    
                # Obtener algunos datos de ejemplo
                cursor.execute(f"SELECT * FROM {tabla} LIMIT 3")
                datos = cursor.fetchall()
                if datos:
                    print(f"\n📋 Datos de ejemplo en {tabla}:")
                    for i, row in enumerate(datos, 1):
                        print(f"    {i}: {row}")
                else:
                    print(f"    ⚠️ No hay datos en {tabla}")
            else:
                print(f"    ❌ No se encontraron columnas para {tabla}")
                
        # Verificar si hay relaciones directas en OBRAS
        print("\n=== CAMPOS DE EMPLEADOS EN OBRAS ===")
        cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'obras' 
        AND column_name ILIKE '%empleado%'
        OR column_name ILIKE '%arquitecto%'
        OR column_name ILIKE '%ingeniero%'
        ORDER BY column_name
        """)
        
        campos_empleados = cursor.fetchall()
        if campos_empleados:
            for col in campos_empleados:
                print(f"  🏗️ {col[0]}: {col[1]}")
        else:
            print("  ℹ️ No hay campos directos de empleados en OBRAS")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    verificar_estructuras_asignacion()