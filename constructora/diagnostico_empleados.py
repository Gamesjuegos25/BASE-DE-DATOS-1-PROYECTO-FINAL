#!/usr/bin/env python3
"""
Verificar qué datos está devolviendo la función get_empleados_safe()
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database import get_connection
except ImportError:
    print("Error: No se pudo importar database.py")
    sys.exit(1)

def verificar_estructura_empleados():
    """Verifica qué campos están siendo devueltos por las consultas de empleados"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print("🔍 VERIFICANDO ESTRUCTURA DE DATOS DE EMPLEADOS")
        print("=" * 55)
        
        # Ver estructura de la tabla
        print("\n1️⃣ ESTRUCTURA DE LA TABLA:")
        print("-" * 30)
        cur.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'empleados'
            ORDER BY ordinal_position
        """)
        
        columnas = cur.fetchall()
        for col in columnas:
            nombre, tipo, nullable = col
            print(f"• {nombre} ({tipo}) - {'NULL' if nullable == 'YES' else 'NOT NULL'}")
        
        # Ver datos reales
        print(f"\n2️⃣ DATOS REALES (Primeros 3 empleados):")
        print("-" * 45)
        cur.execute("""
            SELECT 
                id_empleado,
                nombre_empleado,
                apellido_empleado,
                tipo_empleado,
                salario_fijo_empleado,
                telefono,
                email,
                fecha_ingreso
            FROM empleados 
            ORDER BY id_empleado
            LIMIT 3
        """)
        
        empleados = cur.fetchall()
        
        campos = ['id_empleado', 'nombre_empleado', 'apellido_empleado', 'tipo_empleado', 
                 'salario_fijo_empleado', 'telefono', 'email', 'fecha_ingreso']
        
        for i, emp in enumerate(empleados, 1):
            print(f"\nEmpleado {i}:")
            for j, campo in enumerate(campos):
                valor = emp[j] if j < len(emp) else 'N/A'
                print(f"  {campo}: {valor}")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def simular_get_empleados_safe():
    """Simula lo que debería hacer get_empleados_safe()"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print(f"\n3️⃣ SIMULANDO get_empleados_safe():")
        print("-" * 40)
        
        # Esta debería ser la consulta que usa get_empleados_safe
        cur.execute("""
            SELECT 
                id_empleado,
                nombre_empleado,
                apellido_empleado,
                tipo_empleado,
                salario_fijo_empleado,
                telefono,
                email,
                fecha_ingreso
            FROM empleados 
            ORDER BY id_empleado
        """)
        
        empleados = cur.fetchall()
        
        print(f"Total empleados encontrados: {len(empleados)}")
        
        # Convertir a diccionarios como lo haría la función real
        empleados_dict = []
        for emp in empleados:
            empleado_dict = {
                'id_empleado': emp[0],
                'nombre_empleado': emp[1],
                'apellido_empleado': emp[2],
                'tipo_empleado': emp[3],
                'salario_fijo_empleado': emp[4],
                'telefono': emp[5],
                'email': emp[6],
                'fecha_ingreso': emp[7]
            }
            empleados_dict.append(empleado_dict)
        
        # Mostrar ejemplo
        if empleados_dict:
            print(f"\nEjemplo de estructura de diccionario:")
            print(f"Empleado 1: {empleados_dict[0]}")
        
        cur.close()
        conn.close()
        
        return empleados_dict
        
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    """Función principal"""
    print("🔧 DIAGNÓSTICO DE EMPLEADOS")
    print("=" * 30)
    
    # 1. Verificar estructura
    if verificar_estructura_empleados():
        print("✅ Estructura verificada")
    
    # 2. Simular función
    empleados = simular_get_empleados_safe()
    if empleados:
        print("✅ Simulación exitosa")
        print(f"\n📊 RESUMEN:")
        print(f"• Total empleados: {len(empleados)}")
        print(f"• Con apellido: {sum(1 for emp in empleados if emp.get('apellido_empleado'))}")
        print(f"• Con teléfono: {sum(1 for emp in empleados if emp.get('telefono'))}")
        print(f"• Con email: {sum(1 for emp in empleados if emp.get('email'))}")
        print(f"• Con fecha: {sum(1 for emp in empleados if emp.get('fecha_ingreso'))}")
        
        print(f"\n💡 RECOMENDACIÓN:")
        print("Si los campos aparecen aquí pero no en la web, el problema está en:")
        print("1. La función get_empleados_safe() en database.py")
        print("2. El template que se está usando (debe ser listar.html)")
        print("3. La consulta SQL no incluye todos los campos")

if __name__ == "__main__":
    main()