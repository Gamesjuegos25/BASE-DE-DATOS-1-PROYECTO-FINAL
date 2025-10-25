#!/usr/bin/env python3
"""
Crear empleados de ejemplo para cargos faltantes
Corrige el problema de secuencia y agrega empleados para todos los cargos
"""

import sys
sys.path.append('.')
from database import get_connection

def corregir_secuencia_empleados():
    """Corrige la secuencia de IDs de empleados"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Obtener el máximo ID actual
        cur.execute("SELECT MAX(id_empleado) FROM empleados")
        max_id = cur.fetchone()[0] or 0
        
        # Establecer la secuencia al siguiente valor disponible
        nuevo_valor = max_id + 1
        cur.execute(f"SELECT setval('empleados_id_empleado_seq', {nuevo_valor}, false)")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Secuencia corregida. Próximo ID: {nuevo_valor}")
        return True
        
    except Exception as e:
        print(f"❌ Error al corregir secuencia: {e}")
        return False

def crear_empleados_faltantes():
    """Crea empleados para los cargos que no existen"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Obtener cargos existentes
        cur.execute("""
            SELECT DISTINCT tipo_empleado 
            FROM empleados 
            WHERE tipo_empleado IS NOT NULL
        """)
        
        cargos_existentes = [row[0] for row in cur.fetchall()]
        
        # Definir empleados de ejemplo para cargos faltantes
        empleados_nuevos = {
            'ARQUITECTO': ('María González', 9500.00),
            'ADMINISTRADOR': ('Carlos Rodríguez', 7200.00),
            'ALMACENISTA': ('Ana Torres', 4200.00),
            'CONDUCTOR': ('Miguel Herrera', 3800.00),
            'OPERARIO': ('José Morales', 3200.00),
            'SEGURIDAD': ('David Castillo', 2600.00)
        }
        
        print("👥 CREANDO EMPLEADOS PARA CARGOS FALTANTES:")
        print("=" * 50)
        
        empleados_creados = 0
        
        for cargo, (nombre, salario) in empleados_nuevos.items():
            if cargo not in cargos_existentes:
                cur.execute("""
                    INSERT INTO empleados (nombre_empleado, tipo_empleado, salario_fijo_empleado)
                    VALUES (%s, %s, %s)
                """, (nombre, cargo, salario))
                
                empleados_creados += 1
                print(f"✅ {nombre} - {cargo} - Q{salario:,.2f}/mes")
            else:
                print(f"⚪ {cargo}: Ya existe")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"\n📊 Empleados creados: {empleados_creados}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def mostrar_empleados_completos():
    """Muestra todos los empleados con sus salarios actualizados"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                id_empleado,
                nombre_empleado,
                tipo_empleado,
                salario_fijo_empleado
            FROM empleados 
            ORDER BY salario_fijo_empleado DESC, nombre_empleado
        """)
        
        empleados = cur.fetchall()
        
        print("\n👥 TODOS LOS EMPLEADOS CON SALARIOS ACTUALIZADOS:")
        print("=" * 70)
        print("ID".ljust(5) + "NOMBRE".ljust(20) + "CARGO".ljust(25) + "SALARIO/MES")
        print("-" * 70)
        
        for emp_id, nombre, cargo, salario in empleados:
            print(f"{emp_id}".ljust(5) + 
                  f"{nombre:.19}".ljust(20) + 
                  f"{cargo:.24}".ljust(25) + 
                  f"Q{salario:,.2f}")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 COMPLETANDO SISTEMA DE EMPLEADOS")
    print("=" * 50)
    
    # Corregir secuencia
    if corregir_secuencia_empleados():
        # Crear empleados faltantes
        if crear_empleados_faltantes():
            # Mostrar resultado final
            mostrar_empleados_completos()
            
            print("\n🎯 COMPLETADO:")
            print("✅ Secuencia de IDs corregida")
            print("✅ Empleados de ejemplo creados para todos los cargos")
            print("✅ Sistema de salarios fijos 100% implementado")

if __name__ == "__main__":
    main()