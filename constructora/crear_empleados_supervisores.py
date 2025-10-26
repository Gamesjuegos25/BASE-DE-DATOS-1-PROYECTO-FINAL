#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import database as db

def crear_empleados_supervisores():
    """Crear empleados supervisores de ejemplo para el sistema"""
    empleados = [
        {
            'nombre': 'Juan Carlos',
            'apellido': 'Rodriguez Martinez',
            'tipo': 'Supervisor',
            'salario': 2500000,
            'telefono': '+57 301 234 5678',
            'email': 'juan.rodriguez@constructora.com'
        },
        {
            'nombre': 'Ana Maria',
            'apellido': 'Gonzalez Lopez',
            'tipo': 'Gerente',
            'salario': 3500000,
            'telefono': '+57 302 345 6789',
            'email': 'ana.gonzalez@constructora.com'
        },
        {
            'nombre': 'Carlos Eduardo',
            'apellido': 'Morales Silva',
            'tipo': 'Coordinador',
            'salario': 2800000,
            'telefono': '+57 303 456 7890',
            'email': 'carlos.morales@constructora.com'
        },
        {
            'nombre': 'Patricia Elena',
            'apellido': 'Hernandez Castro',
            'tipo': 'Jefe',
            'salario': 3200000,
            'telefono': '+57 304 567 8901',
            'email': 'patricia.hernandez@constructora.com'
        },
        {
            'nombre': 'Luis Fernando',
            'apellido': 'Ramirez Torres',
            'tipo': 'Encargado',
            'salario': 2300000,
            'telefono': '+57 305 678 9012',
            'email': 'luis.ramirez@constructora.com'
        }
    ]
    
    try:
        print("=== CREANDO EMPLEADOS SUPERVISORES ===")
        for emp in empleados:
            empleado_id = db.insert_empleado_safe(
                nombre=emp['nombre'],
                apellido=emp['apellido'],
                tipo=emp['tipo'],
                salario=emp['salario'],
                telefono=emp['telefono'],
                email=emp['email']
            )
            
            if empleado_id:
                print(f"✅ {emp['nombre']} {emp['apellido']} ({emp['tipo']}) - ID: {empleado_id}")
            else:
                print(f"❌ Error creando {emp['nombre']} {emp['apellido']}")
        
        # Verificar los empleados creados
        supervisores = db.get_empleados_supervisores_safe()
        print(f"\n=== EMPLEADOS SUPERVISORES DISPONIBLES ({len(supervisores)}) ===")
        for sup in supervisores:
            print(f"- ID: {sup['id_empleado']}, {sup['nombre_empleado']} {sup['apellido_empleado'] or ''} ({sup['tipo_empleado'] or 'Sin tipo'})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    crear_empleados_supervisores()