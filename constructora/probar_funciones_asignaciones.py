#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de funciones de asignaciones de obras
Autor: Sistema de Constructora
Fecha: 2024
"""

from database import (
    get_empleados_asignados_obra_safe,
    get_materiales_asignados_obra_safe,
    get_vehiculos_asignados_obra_safe,
    get_resumen_asignaciones_obra_safe
)

def probar_funciones_asignaciones():
    """Probar todas las funciones de asignaciones"""
    print("🧪 PROBANDO FUNCIONES DE ASIGNACIONES DE OBRAS")
    print("=" * 60)
    
    # Usar la obra ID 9 que sabemos que existe
    id_obra = 9
    print(f"\n📋 Probando con obra ID: {id_obra}")
    
    # 1. Probar empleados asignados
    print(f"\n👥 EMPLEADOS ASIGNADOS:")
    empleados = get_empleados_asignados_obra_safe(id_obra)
    if empleados:
        for emp in empleados:
            print(f"   🧑‍💼 {emp['nombre_empleado']} {emp['apellido_empleado']}")
            print(f"      Rol: {emp['tipo_asignacion']}")
            print(f"      Tipo: {emp['tipo_empleado']}")
            print(f"      Fecha: {emp['fecha_asignacion']}")
            if emp['observaciones']:
                print(f"      📝 {emp['observaciones']}")
            print()
    else:
        print("   ⚠️ No hay empleados asignados")
    
    # 2. Probar materiales asignados
    print(f"\n🧱 MATERIALES ASIGNADOS:")
    materiales = get_materiales_asignados_obra_safe(id_obra)
    if materiales:
        for mat in materiales:
            print(f"   📦 {mat['nombre_material']}")
            print(f"      Cantidad: {mat['cantidad_asignada']} {mat['unidad_material']}")
            print(f"      Utilizado: {mat['cantidad_utilizada'] or 0} {mat['unidad_material']}")
            print(f"      Restante: {mat['cantidad_restante']} {mat['unidad_material']}")
            print(f"      Precio: ${mat['precio_final']:,.2f}")
            print(f"      Total: ${mat['valor_total']:,.2f}")
            if mat['observaciones']:
                print(f"      📝 {mat['observaciones']}")
            print()
    else:
        print("   ⚠️ No hay materiales asignados")
    
    # 3. Probar vehículos asignados
    print(f"\n🚚 VEHÍCULOS ASIGNADOS:")
    vehiculos = get_vehiculos_asignados_obra_safe(id_obra)
    if vehiculos:
        for veh in vehiculos:
            print(f"   🚗 {veh['placa_vehiculo']} ({veh['tipo_vehiculo']})")
            print(f"      Estado: {veh['estado_vehiculo']}")
            print()
    else:
        print("   ⚠️ No hay vehículos asignados")
    
    # 4. Probar resumen completo
    print(f"\n📊 RESUMEN COMPLETO:")
    resumen = get_resumen_asignaciones_obra_safe(id_obra)
    stats = resumen['estadisticas']
    
    print(f"   👥 Total empleados: {stats['total_empleados']}")
    print(f"   🧱 Total materiales: {stats['total_materiales']}")
    print(f"   🚚 Total vehículos: {stats['total_vehiculos']}")
    print(f"   💰 Valor materiales: ${stats['valor_total_materiales']:,.2f}")
    
    print(f"\n📋 Empleados por tipo:")
    for tipo, lista in stats['empleados_por_tipo'].items():
        print(f"   🏷️ {tipo}: {len(lista)} empleados")
    
    print(f"\n✅ Funciones probadas exitosamente!")

if __name__ == "__main__":
    probar_funciones_asignaciones()