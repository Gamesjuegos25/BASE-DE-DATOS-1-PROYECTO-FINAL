#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creador de tablas de asignación para obras
Autor: Sistema de Constructora
Fecha: 2024
"""

from database import get_connection
import psycopg2

def crear_tablas_asignacion():
    """Crear las tablas de asignación obra_empleado y obra_material"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        print("🔨 Creando tablas de asignación para obras...")
        
        # Leer el script SQL
        with open('crear_tablas_asignacion.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Ejecutar el script
        cursor.execute(sql_script)
        conn.commit()
        
        print("✅ Tablas creadas exitosamente!")
        
        # Verificar que se crearon correctamente
        print("\n📋 Verificando tablas creadas:")
        
        tablas_verificar = ['obra_empleado', 'obra_material']
        
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
        
        # Insertar algunos datos de prueba
        print("\n🧪 Insertando datos de prueba...")
        
        # Datos de prueba para obra_empleado
        cursor.execute("""
        INSERT INTO obra_empleado (id_obra, id_empleado, tipo_asignacion, observaciones) 
        VALUES 
            (1, 1, 'ARQUITECTO', 'Arquitecto principal del proyecto'),
            (1, 2, 'INGENIERO', 'Ingeniero estructural'),
            (1, 3, 'OBRERO', 'Obrero especializado en construcción'),
            (2, 1, 'ARQUITECTO', 'Supervisión arquitectónica'),
            (2, 4, 'OBRERO', 'Trabajo de albañilería')
        ON CONFLICT (id_obra, id_empleado, tipo_asignacion) DO NOTHING
        """)
        
        # Datos de prueba para obra_material
        cursor.execute("""
        INSERT INTO obra_material (id_obra, id_material, cantidad_asignada, precio_unitario_obra, observaciones)
        VALUES 
            (1, 1, 100.0, 25000.00, 'Cemento para estructura principal'),
            (1, 2, 500.0, 1200.00, 'Ladrillos para muros'),
            (2, 1, 50.0, 25000.00, 'Cemento para acabados'),
            (2, 3, 200.0, 850.00, 'Arena para mezcla')
        ON CONFLICT (id_obra, id_material) DO NOTHING
        """)
        
        conn.commit()
        print("✅ Datos de prueba insertados!")
        
        # Mostrar resumen de datos
        cursor.execute("SELECT COUNT(*) FROM obra_empleado")
        count_emp = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM obra_material") 
        count_mat = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM obra_vehiculo")
        count_veh = cursor.fetchone()[0]
        
        print(f"\n📊 RESUMEN DE ASIGNACIONES:")
        print(f"   👥 Empleados asignados: {count_emp}")
        print(f"   🧱 Materiales asignados: {count_mat}")
        print(f"   🚚 Vehículos asignados: {count_veh}")
        
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    crear_tablas_asignacion()