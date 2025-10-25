#!/usr/bin/env python3
"""
Script para arreglar la secuencia SERIAL de presupuestos_obra
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from database import get_connection

def arreglar_secuencia_presupuestos():
    """Arregla la secuencia SERIAL de la tabla PRESUPUESTOS_OBRA"""
    print("🔧 ARREGLANDO SECUENCIA DE PRESUPUESTOS_OBRA")
    print("="*60)
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # 1. Ver el estado actual
                print("\n1. Estado actual de la secuencia:")
                cursor.execute("""
                    SELECT last_value, is_called 
                    FROM presupuestos_obra_id_presupuesto_seq;
                """)
                seq_info = cursor.fetchone()
                print(f"   Último valor: {seq_info[0]}, Is called: {seq_info[1]}")
                
                # 2. Ver el máximo ID actual en la tabla
                cursor.execute("SELECT MAX(id_presupuesto) FROM presupuestos_obra;")
                max_id = cursor.fetchone()[0]
                print(f"   Máximo ID en tabla: {max_id}")
                
                # 3. Corregir la secuencia
                if max_id is not None:
                    next_val = max_id + 1
                    print(f"\n2. Estableciendo secuencia al siguiente valor: {next_val}")
                    cursor.execute(f"""
                        SELECT setval('presupuestos_obra_id_presupuesto_seq', {next_val}, false);
                    """)
                else:
                    print(f"\n2. Tabla vacía, reiniciando secuencia a 1")
                    cursor.execute("""
                        SELECT setval('presupuestos_obra_id_presupuesto_seq', 1, false);
                    """)
                
                # 4. Verificar que se corrigió
                cursor.execute("""
                    SELECT last_value, is_called 
                    FROM presupuestos_obra_id_presupuesto_seq;
                """)
                seq_info_new = cursor.fetchone()
                print(f"✅ Nueva secuencia: último valor: {seq_info_new[0]}, Is called: {seq_info_new[1]}")
                
                # 5. Probar inserción
                print("\n3. Probando inserción de prueba...")
                cursor.execute("""
                    INSERT INTO presupuestos_obra (monto_estimado_presupuesto, fecha_presupuesto)
                    VALUES (999.99, CURRENT_DATE) RETURNING id_presupuesto;
                """)
                new_id = cursor.fetchone()[0]
                print(f"✅ Presupuesto de prueba creado con ID: {new_id}")
                
                # 6. Limpiar datos de prueba
                cursor.execute("DELETE FROM presupuestos_obra WHERE id_presupuesto = %s", (new_id,))
                print(f"🧹 Datos de prueba eliminados")
                
    except Exception as e:
        print(f"❌ Error arreglando secuencia: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("🎯 SECUENCIA ARREGLADA - ¡Presupuestos deberían funcionar ahora!")

if __name__ == "__main__":
    arreglar_secuencia_presupuestos()