#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            print('Buscando todas las tablas con "contrato" en el nombre:')
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name LIKE '%contrato%'
                ORDER BY table_name
            """)
            tables = cursor.fetchall()
            for table in tables:
                print(f'  - {table[0]}')
                
            print('\nEstructura de CONTRATO_OBRA:')
            cursor.execute("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'contrato_obra' 
                AND table_schema = 'public'
                ORDER BY ordinal_position
            """)
            cols = cursor.fetchall()
            for col in cols:
                print(f'  {col[0]} ({col[1]}) - Nullable: {col[2]}')
                
except Exception as e:
    print(f'Error: {e}')