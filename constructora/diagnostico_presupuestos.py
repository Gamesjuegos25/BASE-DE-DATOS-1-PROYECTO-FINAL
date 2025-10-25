#!/usr/bin/env python3
"""
Script de diagnóstico para presupuestos
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from database import (
    get_connection, 
    insert_presupuesto_safe, 
    get_obras_safe,
    test_database_connection
)

def diagnosticar_presupuestos():
    print("🔍 DIAGNÓSTICO DE PRESUPUESTOS")
    print("="*60)
    
    # 1. Verificar conexión a la base de datos
    print("\n1. Verificando conexión a base de datos...")
    if test_database_connection():
        print("✅ Conexión exitosa")
    else:
        print("❌ Fallo en conexión")
        return
    
    # 2. Verificar que existan las tablas
    print("\n2. Verificando tablas necesarias...")
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Verificar PRESUPUESTOS_OBRA
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_name = 'presupuestos_obra'
                """)
                if cursor.fetchone():
                    print("✅ Tabla PRESUPUESTOS_OBRA existe")
                else:
                    print("❌ Tabla PRESUPUESTOS_OBRA NO existe")
                
                # Verificar OBRA_PRESUPUESTO
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_name = 'obra_presupuesto'
                """)
                if cursor.fetchone():
                    print("✅ Tabla OBRA_PRESUPUESTO existe")
                else:
                    print("❌ Tabla OBRA_PRESUPUESTO NO existe")
                
    except Exception as e:
        print(f"❌ Error verificando tablas: {e}")
        return
    
    # 3. Verificar estructura de tablas
    print("\n3. Verificando estructura de PRESUPUESTOS_OBRA...")
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'presupuestos_obra'
                """)
                columns = cursor.fetchall()
                print("Columnas encontradas:")
                for col in columns:
                    print(f"  - {col[0]}: {col[1]}")
                
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return
    
    # 4. Verificar que get_obras_safe funcione
    print("\n4. Verificando get_obras_safe...")
    try:
        obras = get_obras_safe()
        if obras:
            print(f"✅ get_obras_safe funciona - {len(obras)} obras encontradas")
            print(f"Primera obra: {obras[0] if obras else 'Ninguna'}")
        else:
            print("⚠️  get_obras_safe no devolvió obras")
    except Exception as e:
        print(f"❌ Error en get_obras_safe: {e}")
    
    # 5. Probar insert_presupuesto_safe
    print("\n5. Probando insert_presupuesto_safe...")
    try:
        # Prueba básica sin obra
        presupuesto_id = insert_presupuesto_safe(
            monto_estimado=1000.50,
            fecha_presupuesto=None,
            obra_id=None
        )
        
        if presupuesto_id:
            print(f"✅ Presupuesto de prueba creado con ID: {presupuesto_id}")
            
            # Verificar que se creó correctamente
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        SELECT id_presupuesto, monto_estimado_presupuesto, fecha_presupuesto 
                        FROM presupuestos_obra WHERE id_presupuesto = %s
                    """, (presupuesto_id,))
                    result = cursor.fetchone()
                    if result:
                        print(f"✅ Datos verificados: ID={result[0]}, Monto={result[1]}, Fecha={result[2]}")
                    
                    # Limpiar datos de prueba
                    cursor.execute("DELETE FROM presupuestos_obra WHERE id_presupuesto = %s", (presupuesto_id,))
                    print("🧹 Datos de prueba eliminados")
        else:
            print("❌ Fallo al crear presupuesto de prueba")
            
    except Exception as e:
        print(f"❌ Error en prueba de inserción: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("📋 DIAGNÓSTICO COMPLETADO")

if __name__ == "__main__":
    diagnosticar_presupuestos()