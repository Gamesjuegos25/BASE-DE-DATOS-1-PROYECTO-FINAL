#!/usr/bin/env python3
"""
Script para agregar campos de calendarización a la tabla actividades
"""

from database import get_connection

def extender_tabla_actividades():
    """Agregar campos de calendarización a actividades"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print("🔧 EXTENDIENDO TABLA ACTIVIDADES PARA CALENDARIZACIÓN")
        print("=" * 60)
        
        # Lista de campos a agregar
        campos_calendario = [
            ("hora_inicio", "TIME", "DEFAULT '08:00:00'"),
            ("hora_fin", "TIME", "DEFAULT '17:00:00'"),
            ("frecuencia", "VARCHAR(20)", "DEFAULT 'unica'"),
            ("notas_calendario", "TEXT", "DEFAULT NULL"),
            ("area_id", "INTEGER", "DEFAULT NULL"),
            ("duracion_estimada", "DECIMAL(4,2)", "DEFAULT NULL"),
            ("prioridad", "VARCHAR(20)", "DEFAULT 'media'"),
            ("estado", "VARCHAR(20)", "DEFAULT 'pendiente'"),
            ("fecha_creacion", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP"),
            ("fecha_actualizacion", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP")
        ]
        
        for campo, tipo, default in campos_calendario:
            try:
                # Verificar si el campo ya existe
                cur.execute("""
                    SELECT COUNT(*) FROM information_schema.columns 
                    WHERE table_name = 'actividades' 
                    AND column_name = %s
                    AND table_schema = 'public'
                """, (campo,))
                
                existe = cur.fetchone()[0] > 0
                
                if not existe:
                    sql = f"ALTER TABLE actividades ADD COLUMN {campo} {tipo} {default}"
                    cur.execute(sql)
                    print(f"   ✅ Campo '{campo}' agregado")
                else:
                    print(f"   ⚠️  Campo '{campo}' ya existe")
                    
            except Exception as e:
                print(f"   ❌ Error agregando '{campo}': {str(e)}")
        
        # Crear índices para mejor rendimiento
        indices = [
            ("idx_actividades_fecha_programada", "fecha_programada_actividad"),
            ("idx_actividades_area", "area_id"),
            ("idx_actividades_estado", "estado"),
            ("idx_actividades_prioridad", "prioridad")
        ]
        
        print(f"\n🔍 CREANDO ÍNDICES:")
        for nombre_indice, campo in indices:
            try:
                cur.execute(f"""
                    CREATE INDEX IF NOT EXISTS {nombre_indice} 
                    ON actividades({campo})
                """)
                print(f"   ✅ Índice '{nombre_indice}' creado")
            except Exception as e:
                print(f"   ❌ Error creando índice '{nombre_indice}': {str(e)}")
        
        # Agregar restricciones
        print(f"\n🛡️ AGREGANDO RESTRICCIONES:")
        restricciones = [
            ("chk_actividades_prioridad", "prioridad IN ('baja', 'media', 'alta', 'crítica')"),
            ("chk_actividades_estado", "estado IN ('pendiente', 'en_progreso', 'completada', 'cancelada')"),
            ("chk_actividades_frecuencia", "frecuencia IN ('unica', 'diaria', 'semanal', 'mensual')")
        ]
        
        for nombre_restriccion, condicion in restricciones:
            try:
                cur.execute(f"""
                    ALTER TABLE actividades 
                    ADD CONSTRAINT {nombre_restriccion} 
                    CHECK ({condicion})
                """)
                print(f"   ✅ Restricción '{nombre_restriccion}' agregada")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"   ⚠️  Restricción '{nombre_restriccion}' ya existe")
                else:
                    print(f"   ❌ Error agregando restricción '{nombre_restriccion}': {str(e)}")
        
        conn.commit()
        
        # Mostrar estructura final
        print(f"\n📋 ESTRUCTURA FINAL DE TABLA:")
        cur.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'actividades' AND table_schema = 'public'
            ORDER BY ordinal_position
        """)
        
        columnas = cur.fetchall()
        for col in columnas:
            default = col[3][:30] + "..." if col[3] and len(str(col[3])) > 30 else (col[3] or "No default")
            nullable = "SI" if col[2] == "YES" else "NO"
            print(f"   • {col[0]:25} {col[1]:15} NULL:{nullable:3} Default: {default}")
        
        cur.close()
        conn.close()
        
        print(f"\n✅ CALENDARIZACIÓN AGREGADA EXITOSAMENTE")
        
    except Exception as e:
        print(f"❌ Error extendiendo tabla: {str(e)}")

if __name__ == "__main__":
    extender_tabla_actividades()