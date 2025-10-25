#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # 1. Ver el estado actual de la tabla CONTRATOS
            print("=== DIAGNÓSTICO DE TABLA CONTRATOS ===")
            
            # Revisar contenido actual
            cursor.execute("SELECT id_contrato, numero_contrato, fecha_inicio_contrato FROM contratos ORDER BY id_contrato")
            contratos = cursor.fetchall()
            print(f"\nContratos existentes ({len(contratos)}):")
            for contrato in contratos:
                print(f"  ID: {contrato[0]}, Número: {contrato[1]}, Fecha: {contrato[2]}")
            
            # Ver el valor actual de la secuencia
            cursor.execute("SELECT currval('contratos_id_contrato_seq')")
            seq_value = cursor.fetchone()[0]
            print(f"\nValor actual de secuencia: {seq_value}")
            
            # Ver el MAX ID en la tabla
            cursor.execute("SELECT COALESCE(MAX(id_contrato), 0) FROM contratos")
            max_id = cursor.fetchone()[0]
            print(f"MAX ID en tabla: {max_id}")
            
            if seq_value <= max_id:
                print(f"\n🚨 PROBLEMA: Secuencia ({seq_value}) <= MAX ID ({max_id})")
                new_seq_value = max_id + 1
                print(f"🔧 Corrigiendo secuencia a: {new_seq_value}")
                
                cursor.execute(f"SELECT setval('contratos_id_contrato_seq', {new_seq_value})")
                cursor.execute("SELECT currval('contratos_id_contrato_seq')")
                updated_seq = cursor.fetchone()[0]
                print(f"✅ Secuencia actualizada a: {updated_seq}")
            else:
                print(f"\n✅ Secuencia OK: {seq_value} > {max_id}")
                
except Exception as e:
    print(f"Error: {e}")