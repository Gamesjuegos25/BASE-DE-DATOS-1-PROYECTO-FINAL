import psycopg2
import os

def test_area():
    try:
        # Configurar codificación
        os.environ['PGCLIENTENCODING'] = 'LATIN1'
        
        # Conectar a la base de datos
        conn = psycopg2.connect(
            dbname='cosntructora',
            user='postgres',
            password='123654',
            host='localhost',
            port='5432',
            options="-c client_encoding=LATIN1"
        )
        
        # Crear un cursor
        cursor = conn.cursor()
        
        # Probar una inserción simple
        cursor.execute("INSERT INTO AREAS (nombre_area) VALUES (%s) RETURNING id_area", ('Area Test',))
        area_id = cursor.fetchone()[0]
        print(f"Área insertada con ID: {area_id}")
        
        # Consultar las áreas existentes
        cursor.execute("SELECT id_area, nombre_area FROM AREAS")
        areas = cursor.fetchall()
        print("\nÁreas existentes:")
        for area in areas:
            print(f"ID: {area[0]}, Nombre: {area[1]}")
        
        # Confirmar cambios
        conn.commit()
        print("\nPrueba completada exitosamente")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    test_area()