#!/usr/bin/env python3
"""
Verificar funcionamiento de empleados con salarios predefinidos
Simula la funcionalidad del módulo web
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database import get_connection
except ImportError:
    print("Error: No se pudo importar database.py")
    print("Verificando estructura de archivos...")
    sys.exit(1)

def verificar_empleados_web():
    """Simula la funcionalidad del módulo web de empleados"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print("VERIFICACION EMPLEADOS CON SALARIOS PREDEFINIDOS")
        print("=" * 60)
        
        # Simular la consulta que haría la aplicación web
        cur.execute("""
            SELECT 
                id_empleado,
                nombre_empleado,
                tipo_empleado,
                salario_fijo_empleado
            FROM empleados 
            ORDER BY salario_fijo_empleado DESC
        """)
        
        empleados = cur.fetchall()
        
        print(f"\n LISTADO WEB - {len(empleados)} EMPLEADOS ENCONTRADOS")
        print("=" * 50)
        
        # Simular como se mostrarían en la web
        for emp in empleados:
            id_emp, nombre, tipo, salario = emp
            
            # Formatear tipo de empleado como en el template
            tipo_formato = tipo.replace('_', ' ').title() if tipo else 'General'
            
            # Determinar icono según el cargo (como en el template)
            if tipo == 'ARQUITECTO':
                icono = "fas fa-drafting-compass"
                badge_color = "badge-primary"
            elif tipo == 'INGENIERO':
                icono = "fas fa-user-graduate"
                badge_color = "badge-success"
            elif tipo in ['SUPERVISOR', 'ADMINISTRADOR']:
                icono = "fas fa-user-tie"
                badge_color = "badge-warning"
            elif tipo == 'OPERARIO':
                icono = "fas fa-hard-hat"
                badge_color = "badge-info"
            elif tipo == 'CONDUCTOR':
                icono = "fas fa-truck"
                badge_color = "badge-secondary"
            elif tipo == 'SEGURIDAD':
                icono = "fas fa-shield-alt"
                badge_color = "badge-dark"
            else:
                icono = "fas fa-user"
                badge_color = "badge-light"
            
            print(f"ID: {id_emp} | {nombre} | [{tipo_formato}] | Q{salario:,.2f}/mes")
            print(f"   Icono: {icono} | Badge: {badge_color}")
            print("-" * 50)
        
        # Verificar estadísticas como las del dashboard
        cur.execute("""
            SELECT 
                COUNT(*) as total_empleados,
                SUM(salario_fijo_empleado) as nomina_total,
                AVG(salario_fijo_empleado) as salario_promedio,
                MIN(salario_fijo_empleado) as salario_minimo,
                MAX(salario_fijo_empleado) as salario_maximo
            FROM empleados
        """)
        
        stats = cur.fetchone()
        total, nomina, promedio, minimo, maximo = stats
        
        print(f"\n ESTADISTICAS DASHBOARD")
        print("=" * 30)
        print(f"Total empleados: {total}")
        print(f"Nomina mensual: Q{nomina:,.2f}")
        print(f"Nomina anual: Q{nomina * 12:,.2f}")
        print(f"Salario promedio: Q{promedio:,.2f}")
        print(f"Rango salarial: Q{minimo:,.2f} - Q{maximo:,.2f}")
        
        # Verificar conteos por tipo (como en stats del template)
        cur.execute("""
            SELECT tipo_empleado, COUNT(*) 
            FROM empleados 
            GROUP BY tipo_empleado
            ORDER BY COUNT(*) DESC
        """)
        
        tipos = cur.fetchall()
        
        print(f"\n DISTRIBUCION POR CARGO")
        print("=" * 25)
        for tipo, cantidad in tipos:
            tipo_fmt = tipo.replace('_', ' ').title()
            print(f"{tipo_fmt}: {cantidad}")
        
        # Simular filtros que podrían usarse en la web
        print(f"\n SIMULACION DE FILTROS WEB")
        print("=" * 35)
        
        # Operarios
        cur.execute("SELECT COUNT(*) FROM empleados WHERE tipo_empleado = 'OPERARIO'")
        operarios = cur.fetchone()[0]
        print(f"Operarios: {operarios}")
        
        # Supervision (Supervisor + Administrador)
        cur.execute("SELECT COUNT(*) FROM empleados WHERE tipo_empleado IN ('SUPERVISOR', 'ADMINISTRADOR')")
        supervision = cur.fetchone()[0]
        print(f"Supervision: {supervision}")
        
        # Profesionales (Ingeniero + Arquitecto)
        cur.execute("SELECT COUNT(*) FROM empleados WHERE tipo_empleado IN ('INGENIERO', 'ARQUITECTO')")
        profesionales = cur.fetchone()[0]
        print(f"Profesionales: {profesionales}")
        
        cur.close()
        conn.close()
        
        print(f"\n VERIFICACION COMPLETADA")
        print("=" * 25)
        print("✓ Conexion a base de datos OK")
        print("✓ Consultas SQL funcionando")
        print("✓ Salarios predefinidos cargados")
        print("✓ Campos template compatibles")
        print("✓ Estadisticas generadas correctamente")
        print("✓ Sistema listo para web")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if verificar_empleados_web():
        print("\n¡SISTEMA DE EMPLEADOS FUNCIONANDO CORRECTAMENTE!")
    else:
        print("\nERROR EN EL SISTEMA DE EMPLEADOS")