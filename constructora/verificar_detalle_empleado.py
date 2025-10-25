#!/usr/bin/env python3
"""
Verificación de datos de empleados para la vista de detalles
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from database import get_empleado_by_id_safe

def verificar_empleado_detalle():
    print("🔍 Verificando función get_empleado_by_id_safe...")
    
    # Intentar obtener el empleado con ID 1
    empleado = get_empleado_by_id_safe(1)
    
    if empleado:
        print("✅ Empleado encontrado!")
        print(f"📊 Campos disponibles:")
        for campo, valor in empleado.items():
            print(f"  • {campo}: {valor}")
        
        print(f"\n🎯 Verificación de campos específicos:")
        print(f"  • Nombre completo: {empleado.get('nombre_empleado', 'N/D')} {empleado.get('apellido_empleado', '')}")
        print(f"  • Tipo/Cargo: {empleado.get('tipo_empleado', 'N/D')}")
        print(f"  • Salario: Q{empleado.get('salario_fijo_empleado', 0):,.2f}" if empleado.get('salario_fijo_empleado') is not None else "  • Salario: N/D")
        print(f"  • Teléfono: {empleado.get('telefono', 'N/D')}")
        print(f"  • Email: {empleado.get('email', 'N/D')}")
        print(f"  • Fecha ingreso: {empleado.get('fecha_ingreso', 'N/D')}")
    else:
        print("❌ No se encontró el empleado con ID 1")
        print("   Esto puede ser normal si no hay empleados en la base de datos")

if __name__ == "__main__":
    verificar_empleado_detalle()