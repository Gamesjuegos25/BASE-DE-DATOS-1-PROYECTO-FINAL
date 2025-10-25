from database import get_connection

try:
    conn = get_connection()
    cur = conn.cursor()
    
    # Verificar estructura de tipos_obra
    cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'tipos_obra' 
    ORDER BY ordinal_position
    """)
    columnas = cur.fetchall()
    print('Estructura tabla tipos_obra:')
    for col in columnas:
        print(f'  {col[0]}: {col[1]}')
    
    print()
    
    # Verificar datos
    cur.execute('SELECT * FROM tipos_obra LIMIT 5')
    tipos = cur.fetchall()
    print(f'Tipos de obra disponibles ({len(tipos)}):')
    for i, tipo in enumerate(tipos):
        print(f'  [{i+1}] {tipo}')
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f'Error: {str(e)}')