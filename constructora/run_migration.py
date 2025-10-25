#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    # Leer el archivo SQL
    with open('migrate_contratos.sql', 'r', encoding='utf-8') as f:
        migration_sql = f.read()
    
    # Ejecutar la migración
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(migration_sql)
            
            # Obtener los resultados de la verificación
            results = cursor.fetchall()
            print('Estructura actualizada de CONTRATOS:')
            for row in results:
                print(f'  {row[0]} ({row[1]}) - Nullable: {row[2]} - Default: {row[3]}')
                
    print('\nMigración completada exitosamente!')
    
except Exception as e:
    print(f'Error en la migración: {e}')