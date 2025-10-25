import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

# Conectar directamente a la base de datos
conn_params = {
    'dbname': os.getenv('DB_NAME', 'constructora_db'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

print(f"\n📊 CONECTANDO A BASE DE DATOS: {conn_params['dbname']}")
print("=" * 60)

try:
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Consulta 1: Ver estructura de OBRAS
    print("\n1. ESTRUCTURA DE TABLA OBRAS:")
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'obras'
        ORDER BY ordinal_position
    """)
    columnas = cursor.fetchall()
    for col in columnas:
        print(f"   - {col['column_name']}: {col['data_type']}")
    
    # Consulta 2: Contar registros
    print("\n2. CONTEO DE REGISTROS:")
    cursor.execute("SELECT COUNT(*) as total FROM OBRAS")
    print(f"   Obras: {cursor.fetchone()['total']}")
    
    cursor.execute("SELECT COUNT(*) as total FROM CONTRATOS")
    print(f"   Contratos: {cursor.fetchone()['total']}")
    
    cursor.execute("SELECT COUNT(*) as total FROM CONTRATO_OBRA")
    print(f"   CONTRATO_OBRA (relaciones): {cursor.fetchone()['total']}")
    
    cursor.execute("SELECT COUNT(*) as total FROM FACTURAS")
    print(f"   Facturas: {cursor.fetchone()['total']}")
    
    # Consulta 3: Ver primeras obras
    print("\n3. PRIMERAS 3 OBRAS (DATOS REALES):")
    cursor.execute("SELECT * FROM OBRAS LIMIT 3")
    obras = cursor.fetchall()
    for i, obra in enumerate(obras, 1):
        print(f"\n   Obra {i}:")
        for key, value in obra.items():
            print(f"      {key}: {value}")
    
    # Consulta 4: Ver relaciones CONTRATO_OBRA
    print("\n4. RELACIONES CONTRATO_OBRA:")
    cursor.execute("SELECT * FROM CONTRATO_OBRA")
    relaciones = cursor.fetchall()
    print(f"   Total relaciones: {len(relaciones)}")
    for rel in relaciones:
        print(f"   - Contrato {rel.get('id_contrato')} → Obra {rel.get('id_obra')}")
    
    cursor.close()
    conn.close()
    print("\n✅ CONSULTA COMPLETADA")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("=" * 60 + "\n")
