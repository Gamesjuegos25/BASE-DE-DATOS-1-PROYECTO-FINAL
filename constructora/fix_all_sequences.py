#!/usr/bin/env python3
import psycopg2
from database import get_connection

def fix_all_sequences():
    """Reparar todas las secuencias de la base de datos"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                print("=== REPARACIÓN MASIVA DE SECUENCIAS ===")
                
                # Obtener todas las tablas con secuencias
                cursor.execute("""
                    SELECT 
                        t.table_name,
                        c.column_name,
                        pg_get_serial_sequence(t.table_name, c.column_name) as sequence_name
                    FROM information_schema.tables t
                    JOIN information_schema.columns c ON c.table_name = t.table_name
                    WHERE t.table_schema = 'public'
                    AND c.column_default LIKE 'nextval%'
                    AND pg_get_serial_sequence(t.table_name, c.column_name) IS NOT NULL
                    ORDER BY t.table_name
                """)
                
                sequences = cursor.fetchall()
                print(f"Encontradas {len(sequences)} secuencias para revisar:\n")
                
                fixed_count = 0
                
                for table_name, column_name, sequence_name in sequences:
                    try:
                        # Obtener el MAX ID de la tabla
                        cursor.execute(f"SELECT COALESCE(MAX({column_name}), 0) FROM {table_name}")
                        max_id = cursor.fetchone()[0]
                        
                        # Obtener el valor actual de la secuencia
                        cursor.execute(f"SELECT last_value, is_called FROM {sequence_name}")
                        seq_info = cursor.fetchone()
                        last_value = seq_info[0]
                        is_called = seq_info[1]
                        
                        # Calcular el próximo valor correcto
                        next_val = max_id + 1
                        
                        print(f"📊 {table_name}.{column_name}:")
                        print(f"   MAX ID: {max_id}")
                        print(f"   Secuencia: {last_value} (called: {is_called})")
                        
                        # Solo reparar si es necesario
                        if last_value < max_id or (last_value == max_id and is_called):
                            cursor.execute(f"SELECT setval('{sequence_name}', {next_val}, false)")
                            print(f"   🔧 REPARADA: {last_value} → {next_val}")
                            fixed_count += 1
                        else:
                            print(f"   ✅ OK: No necesita reparación")
                            
                        print()
                        
                    except Exception as e:
                        print(f"   ❌ ERROR en {table_name}: {str(e)}")
                        print()
                
                conn.commit()
                print(f"🎉 COMPLETADO: {fixed_count} secuencias reparadas de {len(sequences)} revisadas")
                
    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    fix_all_sequences()