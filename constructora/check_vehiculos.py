#!/usr/bin/env python3
from database import get_connection
import psycopg2.extras

conn = get_connection()
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

print("COLUMNAS DE LA TABLA VEHICULOS:")
cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'vehiculos'")
columnas = [row['column_name'] for row in cursor.fetchall()]
for col in columnas:
    print(f"  - {col}")

print("\nDATO MUESTRA:")
cursor.execute("SELECT * FROM vehiculos LIMIT 1")
sample = cursor.fetchone()
if sample:
    for k, v in sample.items():
        print(f"  {k}: {v}")

conn.close()