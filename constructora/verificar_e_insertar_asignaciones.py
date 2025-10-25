#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar datos existentes e insertar asignaciones válidas
"""

from database import get_connection

def verificar_e_insertar_datos():
    """Verificar datos existentes e insertar asignaciones válidas"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        print("🔍 Verificando datos existentes...")
        
        # Verificar obras existentes
        cursor.execute("SELECT id_obra, nombre_obra FROM obras ORDER BY id_obra LIMIT 5")
        obras = cursor.fetchall()
        print(f"\n📋 OBRAS DISPONIBLES:")
        for obra in obras:
            print(f"   🏗️ ID: {obra[0]} - {obra[1]}")
        
        # Verificar empleados existentes
        cursor.execute("SELECT id_empleado, nombre_empleado, tipo_empleado FROM empleados ORDER BY id_empleado LIMIT 5")
        empleados = cursor.fetchall()
        print(f"\n👥 EMPLEADOS DISPONIBLES:")
        for emp in empleados:
            print(f"   👤 ID: {emp[0]} - {emp[1]} ({emp[2]})")
            
        # Verificar materiales existentes
        cursor.execute("SELECT id_material, nombre_material FROM materiales ORDER BY id_material LIMIT 5")
        materiales = cursor.fetchall()
        print(f"\n🧱 MATERIALES DISPONIBLES:")
        for mat in materiales:
            print(f"   📦 ID: {mat[0]} - {mat[1]}")
            
        # Verificar vehículos existentes
        cursor.execute("SELECT id_vehiculo, placa_vehiculo, tipo_vehiculo FROM vehiculos ORDER BY id_vehiculo LIMIT 5")
        vehiculos = cursor.fetchall()
        print(f"\n🚚 VEHÍCULOS DISPONIBLES:")
        for veh in vehiculos:
            print(f"   🚗 ID: {veh[0]} - {veh[1]} ({veh[2]})")
        
        if obras and empleados and materiales:
            print(f"\n🧪 Insertando datos de prueba con IDs válidos...")
            
            # Usar los primeros IDs disponibles
            id_obra1 = obras[0][0]
            id_obra2 = obras[1][0] if len(obras) > 1 else obras[0][0]
            id_emp1 = empleados[0][0]
            id_emp2 = empleados[1][0] if len(empleados) > 1 else empleados[0][0]
            id_mat1 = materiales[0][0]
            id_mat2 = materiales[1][0] if len(materiales) > 1 else materiales[0][0]
            
            # Insertar asignaciones de empleados
            cursor.execute("""
            INSERT INTO obra_empleado (id_obra, id_empleado, tipo_asignacion, observaciones) 
            VALUES 
                (%s, %s, 'ARQUITECTO', 'Arquitecto principal del proyecto'),
                (%s, %s, 'INGENIERO', 'Ingeniero estructural')
            ON CONFLICT (id_obra, id_empleado, tipo_asignacion) DO NOTHING
            """, (id_obra1, id_emp1, id_obra1, id_emp2))
            
            # Insertar asignaciones de materiales
            cursor.execute("""
            INSERT INTO obra_material (id_obra, id_material, cantidad_asignada, precio_unitario_obra, observaciones)
            VALUES 
                (%s, %s, 100.0, 25000.00, 'Material principal del proyecto'),
                (%s, %s, 500.0, 1200.00, 'Material secundario')
            ON CONFLICT (id_obra, id_material) DO NOTHING
            """, (id_obra1, id_mat1, id_obra2, id_mat2))
            
            # Insertar asignación de vehículo si hay disponible
            if vehiculos:
                id_veh1 = vehiculos[0][0]
                cursor.execute("""
                INSERT INTO obra_vehiculo (id_obra, id_vehiculo) 
                VALUES (%s, %s)
                ON CONFLICT (id_obra, id_vehiculo) DO NOTHING
                """, (id_obra1, id_veh1))
            
            conn.commit()
            print("✅ Datos de prueba insertados correctamente!")
            
            # Mostrar resumen final
            cursor.execute("SELECT COUNT(*) FROM obra_empleado")
            count_emp = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM obra_material") 
            count_mat = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM obra_vehiculo")
            count_veh = cursor.fetchone()[0]
            
            print(f"\n📊 RESUMEN FINAL DE ASIGNACIONES:")
            print(f"   👥 Empleados asignados: {count_emp}")
            print(f"   🧱 Materiales asignados: {count_mat}")
            print(f"   🚚 Vehículos asignados: {count_veh}")
            
        else:
            print("⚠️ No hay suficientes datos base para crear asignaciones")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    verificar_e_insertar_datos()