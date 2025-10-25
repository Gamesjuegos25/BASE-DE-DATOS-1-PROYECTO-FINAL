from database import get_connection

try:
    conn = get_connection()
    cur = conn.cursor()
    
    # Primero ver qué columnas tiene la tabla
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'usuarios_sistema'
        ORDER BY ordinal_position
    """)
    
    print("\n===== COLUMNAS DE USUARIOS_SISTEMA =====")
    columnas = [row[0] for row in cur.fetchall()]
    print(", ".join(columnas))
    
    # Ahora consultar los usuarios
    cur.execute("""
        SELECT * 
        FROM USUARIOS_SISTEMA 
        ORDER BY id_usuario DESC 
        LIMIT 3
    """)
    
    print("\n===== USUARIOS REGISTRADOS =====")
    usuarios = cur.fetchall()
    if usuarios:
        for usuario in usuarios:
            print(f"Usuario completo: {usuario}")
    else:
        print("No hay usuarios registrados")
    
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
