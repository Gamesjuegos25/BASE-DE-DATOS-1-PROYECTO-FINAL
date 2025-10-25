#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            print("=== VERIFICACIÓN DE TABLAS RELACIONADAS CON MATERIALES ===")
            
            # Verificar si existe tabla de proveedores
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE '%proveedores%'
                ORDER BY table_name
            """)
            
            tablas_proveedores = cursor.fetchall()
            print(f"\nTablas de proveedores encontradas: {len(tablas_proveedores)}")
            for tabla in tablas_proveedores:
                print(f"  - {tabla[0]}")
                
            # Verificar si existe tabla de stock/inventario
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND (table_name LIKE '%stock%' OR table_name LIKE '%inventario%')
                ORDER BY table_name
            """)
            
            tablas_stock = cursor.fetchall()
            print(f"\nTablas de stock/inventario encontradas: {len(tablas_stock)}")
            for tabla in tablas_stock:
                print(f"  - {tabla[0]}")
                
            # Verificar todas las tablas disponibles
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """)
            
            todas_tablas = cursor.fetchall()
            print(f"\nTodas las tablas disponibles ({len(todas_tablas)}):")
            for tabla in todas_tablas:
                print(f"  - {tabla[0]}")
                
except Exception as e:
    print(f"Error: {e}")