#!/usr/bin/env python3
"""
Test para verificar datos del formulario crear proyecto
"""

import os
import sys
from database import get_obras_safe, get_empleados_safe, get_vehiculos_safe

def test_datos_formulario():
    print("🔍 PROBANDO DATOS PARA FORMULARIO CREAR PROYECTO")
    print("=" * 60)
    
    # Test obras
    print("\n📍 OBRAS:")
    obras = get_obras_safe()
    print(f"Total obras: {len(obras)}")
    for i, obra in enumerate(obras[:3]):  # Solo primeros 3
        print(f"  {i+1}. ID: {obra.get('id_obra')} - Nombre: {obra.get('nombre', obra.get('nombre_obra', 'Sin nombre'))}")
        
    # Test empleados
    print("\n👥 EMPLEADOS:")
    empleados = get_empleados_safe()
    print(f"Total empleados: {len(empleados)}")
    
    arquitectos = [e for e in empleados if e.get('tipo_empleado') == 'ARQUITECTO']
    ingenieros = [e for e in empleados if e.get('tipo_empleado') == 'INGENIERO']
    
    print(f"\n🏗️ ARQUITECTOS ({len(arquitectos)}):")
    for i, emp in enumerate(arquitectos[:3]):
        print(f"  {i+1}. ID: {emp.get('id_empleado')} - {emp.get('nombre_empleado')} {emp.get('apellido_empleado')}")
        
    print(f"\n⚡ INGENIEROS ({len(ingenieros)}):")
    for i, emp in enumerate(ingenieros[:3]):
        print(f"  {i+1}. ID: {emp.get('id_empleado')} - {emp.get('nombre_empleado')} {emp.get('apellido_empleado')}")
    
    # Test vehiculos
    print("\n🚚 VEHÍCULOS:")
    vehiculos = get_vehiculos_safe()
    print(f"Total vehículos: {len(vehiculos)}")
    for i, vehiculo in enumerate(vehiculos[:3]):
        print(f"  {i+1}. ID: {vehiculo.get('id_vehiculo')} - {vehiculo.get('placa_vehiculo')} ({vehiculo.get('tipo_vehiculo')})")
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")

if __name__ == "__main__":
    test_datos_formulario()