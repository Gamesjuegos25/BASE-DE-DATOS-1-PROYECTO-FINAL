#!/usr/bin/env python3
"""
Script para diagnosticar problemas con el módulo de actividades
"""

from database import get_connection
import psycopg2.extras

def diagnosticar_actividades():
    """Diagnosticar problemas con actividades"""
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        print("🔍 DIAGNÓSTICO DE ACTIVIDADES")
        print("=" * 50)
        
        # 1. Verificar estructura de tabla
        print("\n1️⃣ ESTRUCTURA DE TABLA:")
        cur.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'actividades' AND table_schema = 'public'
            ORDER BY ordinal_position
        """)
        columnas = cur.fetchall()
        
        if not columnas:
            print("   ❌ Tabla 'actividades' no existe")
            return
        
        for col in columnas:
            print(f"   • {col['column_name']} ({col['data_type']}) - {'NULL' if col['is_nullable'] == 'YES' else 'NOT NULL'}")
        
        # 2. Contar registros
        print(f"\n2️⃣ CONTENIDO DE TABLA:")
        cur.execute("SELECT COUNT(*) as total FROM actividades")
        total = cur.fetchone()['total']
        print(f"   • Total de registros: {total}")
        
        if total == 0:
            print("   ⚠️  La tabla está vacía - creando datos de ejemplo...")
            crear_actividades_ejemplo(cur)
            conn.commit()
            
            # Recontar después de insertar
            cur.execute("SELECT COUNT(*) as total FROM actividades")
            total = cur.fetchone()['total']
            print(f"   • Total después de insertar: {total}")
        
        # 3. Mostrar primeros 5 registros
        if total > 0:
            print(f"\n3️⃣ PRIMEROS 5 REGISTROS:")
            cur.execute("""
                SELECT 
                    id_actividad,
                    nombre_actividad,
                    descripcion_actividad,
                    fecha_programada_actividad
                FROM actividades 
                ORDER BY id_actividad
                LIMIT 5
            """)
            actividades = cur.fetchall()
            
            for act in actividades:
                print(f"   • ID {act['id_actividad']}: {act['nombre_actividad']}")
                print(f"     Descripción: {act['descripcion_actividad'] or 'Sin descripción'}")
                print(f"     Fecha: {act['fecha_programada_actividad'] or 'Sin fecha'}")
                print()
        
        # 4. Probar función get_actividades_safe
        print(f"\n4️⃣ PRUEBA DE FUNCIÓN get_actividades_safe():")
        from database import get_actividades_safe
        
        actividades_safe = get_actividades_safe()
        print(f"   • Registros devueltos: {len(actividades_safe)}")
        
        if actividades_safe:
            print("   • Estructura del primer registro:")
            primer_registro = actividades_safe[0]
            for key, value in primer_registro.items():
                print(f"     - {key}: {value}")
        else:
            print("   ❌ get_actividades_safe() no devuelve datos")
        
        cur.close()
        conn.close()
        
        print(f"\n✅ DIAGNÓSTICO COMPLETADO")
        
    except Exception as e:
        print(f"❌ Error en diagnóstico: {str(e)}")

def crear_actividades_ejemplo(cursor):
    """Crear actividades de ejemplo"""
    actividades_ejemplo = [
        ("Planificación del Proyecto", "Definir alcance, objetivos y cronograma inicial", "2024-12-01"),
        ("Preparación del Terreno", "Limpieza, nivelación y preparación del sitio", "2024-12-03"),
        ("Excavación", "Excavación para cimientos y fundaciones", "2024-12-05"),
        ("Fundaciones", "Construcción de cimientos y bases estructurales", "2024-12-10"),
        ("Estructura Principal", "Levantamiento de muros y estructura principal", "2024-12-15"),
    ]
    
    print("   📝 Insertando actividades de ejemplo...")
    for nombre, descripcion, fecha in actividades_ejemplo:
        try:
            cursor.execute("""
                INSERT INTO actividades (nombre_actividad, descripcion_actividad, fecha_programada_actividad)
                VALUES (%s, %s, %s)
            """, (nombre, descripcion, fecha))
            print(f"      ✓ {nombre}")
        except Exception as e:
            print(f"      ❌ Error insertando {nombre}: {str(e)}")

if __name__ == "__main__":
    diagnosticar_actividades()