#!/usr/bin/env python3
from database import get_connection
import psycopg2.extras

conn = get_connection()
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# Verificar todas las tablas que contengan 'fact'
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name ILIKE '%fact%' ORDER BY table_name")
print('=== TABLAS CON "FACT" ===')
for row in cursor.fetchall():
    print(f'  📄 {row["table_name"]}')

# Verificar todas las tablas disponibles
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
print('\n=== TODAS LAS TABLAS ===')
for row in cursor.fetchall():
    print(f'  {row["table_name"]}')

conn.close()