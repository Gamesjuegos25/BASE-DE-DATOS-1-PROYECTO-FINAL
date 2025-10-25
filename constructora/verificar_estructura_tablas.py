#!/usr/bin/env python3
"""
Verificador de estructura de tablas para corregir las funciones
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_connection
import psycopg2.extras

def verificar_columnas_tabla(tabla):
    """Verifica las columnas de una tabla específica"""
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = %s 
            ORDER BY ordinal_position
        """, (tabla.lower(),))
        
        columnas = cursor.fetchall()
        
        print(f"\n=== COLUMNAS DE {tabla.upper()} ===")
        for col in columnas:
            print(f"  {col['column_name']} ({col['data_type']})")
            
        conn.close()
        return [col['column_name'] for col in columnas]
        
    except Exception as e:
        print(f"Error verificando tabla {tabla}: {e}")
        return []

def main():
    tablas = ['vehiculos', 'contratos', 'bitacoras', 'facturas', 'clientes', 'obras']
    
    for tabla in tablas:
        verificar_columnas_tabla(tabla)

if __name__ == "__main__":
    main()