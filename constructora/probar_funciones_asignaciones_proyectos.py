#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de funciones de asignaciones de proyectos
Autor: Sistema de Constructora
Fecha: 2024
"""

from database import (
    get_obras_asignadas_proyecto_safe,
    get_empleados_asignados_proyecto_safe,
    get_vehiculos_asignados_proyecto_safe,
    get_resumen_asignaciones_proyecto_safe
)

def probar_funciones_asignaciones_proyectos():
    """Probar todas las funciones de asignaciones de proyectos"""
    print("🧪 PROBANDO FUNCIONES DE ASIGNACIONES DE PROYECTOS")
    print("=" * 60)
    
    # Usar el proyecto ID 1 que sabemos que tiene asignaciones
    id_proyecto = 1
    print(f"\n📋 Probando con proyecto ID: {id_proyecto}")
    
    # 1. Probar obras asignadas
    print(f"\n🏗️ OBRAS ASIGNADAS AL PROYECTO:")
    obras = get_obras_asignadas_proyecto_safe(id_proyecto)
    if obras:
        for obra in obras:
            print(f"   🏢 {obra['nombre_obra']}")
            print(f"      Tipo: {obra['tipo_obra']}")
            print(f"      Estado: {obra['estado_obra']}")
            print(f"      Ubicación: {obra['ubicacion_obra'] or 'N/D'}")
            print(f"      Valor: Q{obra['valor_obra']:,.2f}" if obra['valor_obra'] else "      Valor: N/D")
            print(f"      Fecha asignación: {obra['fecha_asignacion']}")
            if obra['observaciones_asignacion']:
                print(f"      📝 {obra['observaciones_asignacion']}")
            print()
    else:
        print("   ⚠️ No hay obras asignadas")
    
    # 2. Probar empleados asignados
    print(f"\n👥 EMPLEADOS ASIGNADOS AL PROYECTO:")
    empleados = get_empleados_asignados_proyecto_safe(id_proyecto)
    if empleados:
        for emp in empleados:
            print(f"   🧑‍💼 {emp['nombre_empleado']} {emp['apellido_empleado']}")
            print(f"      Rol en proyecto: {emp['tipo_asignacion']}")
            print(f"      Especialidad: {emp['tipo_empleado']}")
            print(f"      Fecha asignación: {emp['fecha_asignacion']}")
            if emp['responsabilidad']:
                print(f"      🎯 Responsabilidad: {emp['responsabilidad']}")
            if emp['telefono']:
                print(f"      📞 {emp['telefono']}")
            if emp['email']:
                print(f"      📧 {emp['email']}")
            if emp['observaciones']:
                print(f"      📝 {emp['observaciones']}")
            print()
    else:
        print("   ⚠️ No hay empleados asignados")
    
    # 3. Probar vehículos asignados
    print(f"\n🚚 VEHÍCULOS ASIGNADOS AL PROYECTO:")
    vehiculos = get_vehiculos_asignados_proyecto_safe(id_proyecto)
    if vehiculos:
        for veh in vehiculos:
            print(f"   🚗 {veh['placa_vehiculo']} ({veh['tipo_vehiculo']})")
            print(f"      Estado: {veh['estado_vehiculo']}")
            print(f"      Fecha asignación: {veh['fecha_asignacion']}")
            if veh['proposito']:
                print(f"      🎯 Propósito: {veh['proposito']}")
            if veh['observaciones']:
                print(f"      📝 {veh['observaciones']}")
            print()
    else:
        print("   ⚠️ No hay vehículos asignados")
    
    # 4. Probar resumen completo
    print(f"\n📊 RESUMEN COMPLETO DEL PROYECTO:")
    resumen = get_resumen_asignaciones_proyecto_safe(id_proyecto)
    stats = resumen['estadisticas']
    
    print(f"   🏗️ Total obras asignadas: {stats['total_obras']}")
    print(f"   👥 Total empleados: {stats['total_empleados']}")
    print(f"   🏗️ Arquitectos: {stats['total_arquitectos']}")
    print(f"   ⚙️ Ingenieros: {stats['total_ingenieros']}")
    print(f"   🚚 Total vehículos: {stats['total_vehiculos']}")
    print(f"   💰 Valor total obras: Q{stats['valor_total_obras']:,.2f}")
    
    print(f"\n📋 Empleados por rol en proyecto:")
    for tipo, lista in stats['empleados_por_tipo'].items():
        print(f"   🏷️ {tipo}: {len(lista)} empleado(s)")
        for emp in lista:
            print(f"      - {emp['nombre_empleado']} {emp['apellido_empleado']}")
    
    print(f"\n📋 Arquitectos específicos:")
    for arq in resumen['arquitectos']:
        print(f"   🎨 {arq['nombre_empleado']} {arq['apellido_empleado']}")
        if arq['responsabilidad']:
            print(f"      Responsabilidad: {arq['responsabilidad']}")
    
    print(f"\n📋 Ingenieros específicos:")
    for ing in resumen['ingenieros']:
        print(f"   ⚙️ {ing['nombre_empleado']} {ing['apellido_empleado']}")
        if ing['responsabilidad']:
            print(f"      Responsabilidad: {ing['responsabilidad']}")
    
    print(f"\n✅ Funciones de asignaciones de proyectos probadas exitosamente!")

if __name__ == "__main__":
    probar_funciones_asignaciones_proyectos()