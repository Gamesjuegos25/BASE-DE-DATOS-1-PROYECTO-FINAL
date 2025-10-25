#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            print("=== ESTRUCTURA DE LA TABLA MATERIALES ===")
            
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'materiales' 
                AND table_schema = 'public'
                ORDER BY ordinal_position
            """)
            
            cols = cursor.fetchall()
            print(f"Columnas encontradas: {len(cols)}")
            
            for col in cols:
                nullable = "NULL" if col[2] == 'YES' else "NOT NULL"
                default = f" DEFAULT {col[3]}" if col[3] else ""
                print(f"  {col[0]} ({col[1]}) - {nullable}{default}")
                
except Exception as e:
    print(f"Error: {e}")