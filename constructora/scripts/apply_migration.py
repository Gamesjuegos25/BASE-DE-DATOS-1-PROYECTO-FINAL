from database import get_connection

migration_sql = [
    # Añadir columna id_material a INVENTARIOS si no existe
    "ALTER TABLE INVENTARIOS ADD COLUMN IF NOT EXISTS id_material INTEGER REFERENCES MATERIALES(id_material);",

    # Crear tabla plural MOVIMIENTOS_MATERIALES que usan las funciones del código
    "CREATE TABLE IF NOT EXISTS MOVIMIENTOS_MATERIALES (\n        id_movimiento_material SERIAL PRIMARY KEY,\n        id_material INTEGER REFERENCES MATERIALES(id_material),\n        tipo_movimiento VARCHAR(50) NOT NULL,\n        fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n        origen_movimiento VARCHAR(100),\n        destino_movimiento VARCHAR(100),\n        cantidad INTEGER\n    );"
]

if __name__ == '__main__':
    conn = get_connection()
    if conn is None:
        print('No se pudo obtener conexión. Revisa configuración de DB.')
        raise SystemExit(1)

    try:
        with conn:
            with conn.cursor() as cursor:
                for sql in migration_sql:
                    print('Ejecutando:', sql.splitlines()[0])
                    cursor.execute(sql)
            print('Migración aplicada correctamente.')
    except Exception as e:
        print('Error aplicando migración:', e)
        raise
    finally:
        try:
            conn.close()
        except Exception:
            pass
