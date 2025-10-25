#!/usr/bin/env python3
"""
Sistema de Salarios Fijos por Cargo - Constructora
Implementa salarios estándar para todos los puestos de trabajo
"""

import sys
sys.path.append('.')
from database import get_connection

# Definición de salarios fijos por cargo (en Quetzales guatemaltecos)
SALARIOS_POR_CARGO = {
    'ARQUITECTO': 9500.00,           # Profesional especializado
    'INGENIERO': 8500.00,            # Profesional técnico
    'ADMINISTRADOR': 7200.00,        # Gestión administrativa
    'SUPERVISOR': 6200.00,           # Mandos medios
    'ADMINISTRATIVO': 4800.00,       # Personal de oficina
    'ALMACENISTA': 4200.00,          # Control de inventarios
    'CONDUCTOR': 3800.00,            # Operación de vehículos
    'OBRERO_ESPECIALIZADO': 3500.00, # Técnicos especializados
    'OPERARIO': 3200.00,             # Personal operativo calificado
    'OBRERO': 2800.00,               # Personal operativo básico
    'SEGURIDAD': 2600.00             # Personal de seguridad
}

def obtener_cargos_actuales():
    """Obtiene los cargos que ya existen en la base de datos"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT DISTINCT tipo_empleado, COUNT(*) as cantidad
            FROM empleados 
            WHERE tipo_empleado IS NOT NULL AND tipo_empleado != ''
            GROUP BY tipo_empleado
            ORDER BY tipo_empleado
        """)
        
        cargos_existentes = cur.fetchall()
        
        print("🔍 CARGOS ACTUALES EN LA BASE DE DATOS:")
        print("=" * 50)
        
        cargos_dict = {}
        for cargo, cantidad in cargos_existentes:
            cargos_dict[cargo] = cantidad
            print(f"📋 {cargo}: {cantidad} empleado(s)")
        
        cur.close()
        conn.close()
        
        return cargos_dict
        
    except Exception as e:
        print(f"❌ Error al consultar cargos: {e}")
        return {}

def actualizar_salarios_existentes():
    """Actualiza los salarios de empleados existentes según su cargo"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print("\n💰 ACTUALIZANDO SALARIOS EXISTENTES:")
        print("=" * 50)
        
        empleados_actualizados = 0
        
        for cargo, salario in SALARIOS_POR_CARGO.items():
            # Verificar si existen empleados con este cargo
            cur.execute("""
                SELECT COUNT(*) FROM empleados 
                WHERE tipo_empleado = %s
            """, (cargo,))
            
            cantidad = cur.fetchone()[0]
            
            if cantidad > 0:
                # Actualizar salarios para este cargo
                cur.execute("""
                    UPDATE empleados 
                    SET salario_fijo_empleado = %s 
                    WHERE tipo_empleado = %s
                """, (salario, cargo))
                
                empleados_actualizados += cantidad
                print(f"✅ {cargo}: {cantidad} empleado(s) → Q{salario:,.2f}/mes")
            else:
                print(f"⚪ {cargo}: No hay empleados con este cargo")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"\n📊 Total empleados actualizados: {empleados_actualizados}")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar salarios: {e}")
        return False

def crear_empleados_ejemplo():
    """Crea empleados de ejemplo para cargos que no existen"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Obtener cargos actuales
        cur.execute("""
            SELECT DISTINCT tipo_empleado 
            FROM empleados 
            WHERE tipo_empleado IS NOT NULL
        """)
        
        cargos_existentes = [row[0] for row in cur.fetchall()]
        
        print("\n👥 CREANDO EMPLEADOS DE EJEMPLO:")
        print("=" * 50)
        
        empleados_ejemplo = {
            'ARQUITECTO': 'María González',
            'ADMINISTRADOR': 'Carlos Rodríguez',
            'ALMACENISTA': 'Ana Torres',
            'CONDUCTOR': 'Miguel Herrera',
            'OPERARIO': 'José Morales',
            'SEGURIDAD': 'David Castillo'
        }
        
        empleados_creados = 0
        
        for cargo, nombre in empleados_ejemplo.items():
            if cargo not in cargos_existentes:
                salario = SALARIOS_POR_CARGO[cargo]
                
                cur.execute("""
                    INSERT INTO empleados (nombre_empleado, tipo_empleado, salario_fijo_empleado)
                    VALUES (%s, %s, %s)
                """, (nombre, cargo, salario))
                
                empleados_creados += 1
                print(f"✅ Creado: {nombre} - {cargo} - Q{salario:,.2f}/mes")
            else:
                print(f"⚪ {cargo}: Ya existe empleado con este cargo")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"\n📊 Empleados de ejemplo creados: {empleados_creados}")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear empleados de ejemplo: {e}")
        return False

def mostrar_reporte_salarios():
    """Muestra un reporte completo de salarios por cargo"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                tipo_empleado,
                COUNT(*) as cantidad,
                salario_fijo_empleado,
                COUNT(*) * salario_fijo_empleado as costo_total_mensual
            FROM empleados 
            WHERE tipo_empleado IS NOT NULL
            GROUP BY tipo_empleado, salario_fijo_empleado
            ORDER BY salario_fijo_empleado DESC
        """)
        
        resultados = cur.fetchall()
        
        print("\n📊 REPORTE DE SALARIOS POR CARGO:")
        print("=" * 70)
        print("CARGO".ljust(20) + "EMPLEADOS".ljust(12) + "SALARIO/MES".ljust(15) + "COSTO TOTAL/MES")
        print("-" * 70)
        
        total_empleados = 0
        costo_total_empresa = 0
        
        for cargo, cantidad, salario, costo_total in resultados:
            total_empleados += cantidad
            costo_total_empresa += costo_total
            
            print(f"{cargo:.20}".ljust(20) + 
                  f"{cantidad}".ljust(12) + 
                  f"Q{salario:,.2f}".ljust(15) + 
                  f"Q{costo_total:,.2f}")
        
        print("-" * 70)
        print(f"{'TOTAL'.ljust(20)}{total_empleados}".ljust(32) + 
              f"Q{costo_total_empresa:,.2f}")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error al generar reporte: {e}")
        return False

def main():
    """Función principal"""
    print("💼 SISTEMA DE SALARIOS FIJOS POR CARGO")
    print("🏗️  Constructora - Gestión de Recursos Humanos")
    print("=" * 60)
    
    # Mostrar estructura de salarios definida
    print("\n💰 ESCALA SALARIAL DEFINIDA:")
    print("=" * 40)
    
    for cargo, salario in sorted(SALARIOS_POR_CARGO.items(), key=lambda x: x[1], reverse=True):
        print(f"• {cargo:.25} Q{salario:,.2f}/mes")
    
    print(f"\nRango salarial: Q{min(SALARIOS_POR_CARGO.values()):,.2f} - Q{max(SALARIOS_POR_CARGO.values()):,.2f}")
    
    # Obtener estado actual
    cargos_actuales = obtener_cargos_actuales()
    
    # Actualizar salarios existentes
    if actualizar_salarios_existentes():
        print("✅ Salarios actualizados correctamente")
    
    # Crear empleados de ejemplo para cargos faltantes
    if crear_empleados_ejemplo():
        print("✅ Empleados de ejemplo creados")
    
    # Mostrar reporte final
    mostrar_reporte_salarios()
    
    print("\n🎯 RESULTADO:")
    print("✅ Sistema de salarios fijos implementado")
    print("✅ Todos los cargos tienen salarios estandarizados")
    print("✅ Empleados de ejemplo creados para nuevos cargos")

if __name__ == "__main__":
    main()