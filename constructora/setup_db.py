import psycopg2
import os

def setup_database():
    # Configuración de la conexión
    DB_CONFIG = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': '123654',
        'database': 'cosntructora',
        'options': "-c client_encoding=LATIN1"
    }
    
    try:
        # Establecer LATIN1 como codificación
        os.environ['PGCLIENTENCODING'] = 'LATIN1'
        
        # Conectar a la base de datos
        print("Conectando a la base de datos...")
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_client_encoding('LATIN1')
        cursor = conn.cursor()

        # Leer y ejecutar el script SQL
        print("Ejecutando script CREAR_TABLAS_OBLIGATORIO.sql...")
        with open('CREAR_TABLAS_OBLIGATORIO.sql', 'r', encoding='latin1') as file:
            sql_script = file.read()
            cursor.execute(sql_script)
        
        # Leer y ejecutar el script de datos
        print("Ejecutando script DATOS_COMPLETOS_SISTEMA.sql...")
        with open('DATOS_COMPLETOS_SISTEMA.sql', 'r', encoding='latin1') as file:
            sql_script = file.read()
            cursor.execute(sql_script)
        
        # Confirmar los cambios
        conn.commit()
        print("✅ Base de datos configurada exitosamente")
        
        # Probar inserción de área
        print("\nProbando inserción de área...")
        cursor.execute("INSERT INTO AREAS (nombre_area) VALUES ('Área de Prueba') RETURNING id_area")
        area_id = cursor.fetchone()[0]
        print(f"✅ Área insertada con ID: {area_id}")
        
        # Listar áreas
        print("\nÁreas existentes:")
        cursor.execute("SELECT id_area, nombre_area FROM AREAS")
        areas = cursor.fetchall()
        for area in areas:
            print(f"ID: {area[0]}, Nombre: {area[1]}")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    setup_database()