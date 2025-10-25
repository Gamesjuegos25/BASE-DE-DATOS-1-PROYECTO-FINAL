#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creador de tablas de asignación para proyectos
Autor: Sistema de Constructora
Fecha: 2024
"""

from database import get_connection
import psycopg2

def crear_tablas_asignacion_proyectos():
    """Crear las tablas de asignación para proyectos"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        print("🔨 Creando tablas de asignación para proyectos...")
        
        # Leer el script SQL
        with open('crear_tablas_asignacion_proyectos.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Ejecutar el script
        cursor.execute(sql_script)
        conn.commit()
        
        print("✅ Tablas creadas exitosamente!")
        
        # Verificar que se crearon correctamente
        print("\n📋 Verificando tablas creadas:")
        
        tablas_verificar = ['proyecto_obra', 'proyecto_empleado', 'proyecto_vehiculo']
        
        for tabla in tablas_verificar:
            cursor.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = '{tabla}' 
            ORDER BY ordinal_position
            """)
            
            print(f"\n✨ {tabla.upper()}:")
            columns = cursor.fetchall()
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                print(f"   📌 {col[0]}: {col[1]} ({nullable})")
        
        # Obtener datos base para insertar pruebas
        cursor.execute("SELECT id_proyecto, nombre_proyecto FROM proyectos ORDER BY id_proyecto LIMIT 3")
        proyectos = cursor.fetchall()
        
        cursor.execute("SELECT id_obra, nombre_obra FROM obras ORDER BY id_obra LIMIT 3")
        obras = cursor.fetchall()
        
        cursor.execute("SELECT id_empleado, nombre_empleado, tipo_empleado FROM empleados WHERE tipo_empleado IN ('ARQUITECTO', 'INGENIERO') ORDER BY id_empleado LIMIT 5")
        empleados = cursor.fetchall()
        
        cursor.execute("SELECT id_vehiculo, placa_vehiculo, tipo_vehiculo FROM vehiculos ORDER BY id_vehiculo LIMIT 3")
        vehiculos = cursor.fetchall()
        
        print(f"\n🔍 Datos disponibles:")
        print(f"   📋 Proyectos: {len(proyectos)}")
        print(f"   🏗️ Obras: {len(obras)}")
        print(f"   👥 Arquitectos/Ingenieros: {len(empleados)}")
        print(f"   🚚 Vehículos: {len(vehiculos)}")
        
        if proyectos and obras and empleados and vehiculos:
            print(f"\n🧪 Insertando datos de prueba...")
            
            # Asignar proyecto 1 a obra
            if len(obras) >= 1:
                cursor.execute("""
                INSERT INTO proyecto_obra (id_proyecto, id_obra, observaciones)
                VALUES (%s, %s, %s)
                ON CONFLICT (id_proyecto, id_obra) DO NOTHING
                """, (proyectos[0][0], obras[0][0], f"Proyecto {proyectos[0][1]} asignado a obra {obras[0][1]}"))
            
            # Asignar empleados al proyecto
            for i, emp in enumerate(empleados[:2]):  # Solo los primeros 2
                tipo_rol = 'ARQUITECTO' if emp[2] == 'ARQUITECTO' else 'INGENIERO'
                responsabilidad = f"Responsable técnico como {tipo_rol} del proyecto"
                
                cursor.execute("""
                INSERT INTO proyecto_empleado (id_proyecto, id_empleado, tipo_asignacion, responsabilidad, observaciones)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id_proyecto, id_empleado, tipo_asignacion) DO NOTHING
                """, (proyectos[0][0], emp[0], tipo_rol, responsabilidad, f"{emp[1]} asignado como {tipo_rol}"))
            
            # Asignar vehículos al proyecto
            for i, veh in enumerate(vehiculos[:2]):  # Solo los primeros 2
                proposito = f"Vehículo {veh[2]} para transporte y logística del proyecto"
                
                cursor.execute("""
                INSERT INTO proyecto_vehiculo (id_proyecto, id_vehiculo, proposito, observaciones)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (id_proyecto, id_vehiculo) DO NOTHING
                """, (proyectos[0][0], veh[0], proposito, f"Vehículo {veh[1]} asignado al proyecto"))
            
            conn.commit()
            print("✅ Datos de prueba insertados!")
            
        else:
            print("⚠️ No hay suficientes datos base para crear asignaciones de prueba")
            
        # Mostrar resumen de asignaciones
        cursor.execute("SELECT COUNT(*) FROM proyecto_obra")
        count_obras = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM proyecto_empleado") 
        count_emp = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM proyecto_vehiculo")
        count_veh = cursor.fetchone()[0]
        
        print(f"\n📊 RESUMEN DE ASIGNACIONES DE PROYECTOS:")
        print(f"   🏗️ Obras asignadas: {count_obras}")
        print(f"   👥 Empleados asignados: {count_emp}")
        print(f"   🚚 Vehículos asignados: {count_veh}")
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    crear_tablas_asignacion_proyectos()