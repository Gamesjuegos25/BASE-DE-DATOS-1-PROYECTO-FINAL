#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'contratos' 
                AND table_schema = 'public'
                ORDER BY ordinal_position
            """)
            cols = cursor.fetchall()
            print('Estructura de la tabla CONTRATOS:')
            for col in cols:
                print(f'  {col[0]} ({col[1]}) - Nullable: {col[2]}')
                
            print('\nVerificando si la tabla existe:')
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'contratos'
                )
            """)
            exists = cursor.fetchone()[0]
            print(f'Tabla CONTRATOS existe: {exists}')
            
            if not exists:
                print('\nBuscando tablas similares:')
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name LIKE '%contrato%'
                """)
                similar = cursor.fetchall()
                for table in similar:
                    print(f'  - {table[0]}')
                    
except Exception as e:
    print(f'Error: {e}')