#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            print("=== REPARANDO SECUENCIA CONTRATOS ===")
            
            # Ver el MAX ID en la tabla
            cursor.execute("SELECT COALESCE(MAX(id_contrato), 0) FROM contratos")
            max_id = cursor.fetchone()[0]
            print(f"MAX ID en tabla CONTRATOS: {max_id}")
            
            # Ver el valor actual de la secuencia usando last_value
            cursor.execute("SELECT last_value, is_called FROM contratos_id_contrato_seq")
            seq_info = cursor.fetchone()
            last_value = seq_info[0]
            is_called = seq_info[1]
            
            print(f"Secuencia last_value: {last_value}, is_called: {is_called}")
            
            # Calcular el próximo valor que debería usar la secuencia
            next_seq_value = max_id + 1
            print(f"Próximo valor correcto para secuencia: {next_seq_value}")
            
            # Actualizar la secuencia
            cursor.execute(f"SELECT setval('contratos_id_contrato_seq', {next_seq_value}, false)")
            print(f"✅ Secuencia actualizada a {next_seq_value}")
            
            # Verificar
            cursor.execute("SELECT nextval('contratos_id_contrato_seq')")
            next_val = cursor.fetchone()[0]
            print(f"✅ Próximo ID disponible: {next_val}")
            
            # Resetear para que el próximo nextval() funcione correctamente
            cursor.execute(f"SELECT setval('contratos_id_contrato_seq', {next_seq_value}, false)")
            
            conn.commit()
            print("\n🎉 Secuencia reparada exitosamente!")
            
except Exception as e:
    print(f"Error: {e}")