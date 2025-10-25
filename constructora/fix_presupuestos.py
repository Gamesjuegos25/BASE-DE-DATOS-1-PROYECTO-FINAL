#!/usr/bin/env python3
"""
Script simple para arreglar la secuencia de presupuestos
"""

import sys
import os

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from database import get_connection
    
    print("🔧 ARREGLANDO PRESUPUESTOS...")
    
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Ver contenido actual
            cursor.execute("SELECT id_presupuesto, monto_estimado_presupuesto FROM presupuestos_obra ORDER BY id_presupuesto;")
            existing = cursor.fetchall()
            print(f"Registros existentes: {len(existing)}")
            for reg in existing:
                print(f"  ID: {reg[0]}, Monto: {reg[1]}")
            
            # Obtener máximo ID
            cursor.execute("SELECT MAX(id_presupuesto) FROM presupuestos_obra;")
            max_id = cursor.fetchone()[0] or 0
            print(f"Máximo ID actual: {max_id}")
            
            # Arreglar secuencia
            next_val = max_id + 1
            cursor.execute(f"SELECT setval('presupuestos_obra_id_presupuesto_seq', {next_val}, false);")
            print(f"✅ Secuencia establecida en: {next_val}")
            
            # Verificar
            cursor.execute("SELECT currval('presupuestos_obra_id_presupuesto_seq');")
            current = cursor.fetchone()[0]
            print(f"✅ Valor actual de secuencia: {current}")
            
    print("🎯 ¡ARREGLADO! Ahora intenta crear un presupuesto.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()