#!/usr/bin/env python3
from database import get_connection
import psycopg2.extras

conn = get_connection()
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

# Verificar cuántos registros hay en obras
cursor.execute('SELECT COUNT(*) as total FROM obras')
total = cursor.fetchone()['total']
print(f'Total obras: {total}')

if total > 0:
    # Mostrar primeros registros
    cursor.execute('SELECT id_obra, nombre_obra FROM obras LIMIT 5')
    print('Obras disponibles:')
    for row in cursor.fetchall():
        print(f'  ID: {row["id_obra"]} - {row["nombre_obra"]}')

conn.close()