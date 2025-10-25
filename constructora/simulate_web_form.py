#!/usr/bin/env python3
"""
Simulador de creación de contrato web - Debugger avanzado
"""
from database import get_clientes_safe, get_obras_safe, insert_contrato_safe
from flask import Flask
import traceback

def simulate_web_form_submission():
    """Simular exactamente lo que hace el formulario web"""
    
    print("=== SIMULACIÓN COMPLETA DEL FORMULARIO WEB ===")
    
    # 1. Simular carga de datos para los selects (GET request)
    print("\n1. CARGANDO DATOS PARA LOS SELECTS...")
    try:
        # Obtener datos tal como lo hace la función crear_contrato()
        obras_data = get_obras_safe()
        clientes_data = get_clientes_safe()
        
        # Convertir a formato de tuplas como en la función real
        obras = [(obra.get('id_obra') or obra.get('id'), 
                 f"{obra.get('nombre', 'Sin nombre')} - {obra.get('ubicacion', 'Sin ubicación')}")
                 for obra in obras_data]
        
        clientes = [(cliente.get('id') or cliente.get('id_cliente'), 
                    cliente.get('nombre', 'Sin nombre'))
                    for cliente in clientes_data]
        
        print(f"   ✅ Clientes cargados: {len(clientes)}")
        if clientes:
            print(f"      Primer cliente: {clientes[0]}")
            
        print(f"   ✅ Obras cargadas: {len(obras)}")
        if obras:
            print(f"      Primera obra: {obras[0]}")
            
    except Exception as e:
        print(f"   ❌ ERROR cargando datos: {str(e)}")
        traceback.print_exc()
        return
    
    # 2. Simular envío del formulario (POST request) 
    print("\n2. SIMULANDO ENVÍO DEL FORMULARIO...")
    
    # Datos que típicamente enviaría el formulario
    import random
    numero_unico = f'CON-SIM-{random.randint(100, 999)}'
    
    form_data = {
        'numero_contrato': numero_unico,
        'cliente_id': str(clientes[0][0]) if clientes else '1',
        'obra_id': str(obras[0][0]) if obras else '16',
        'fecha_inicio': '2025-10-25',
        'fecha_fin': '2025-12-31', 
        'valor_total': '180000.00',
        'estado': 'activo',
        'tipo_pago': 'quincenal'
    }
    
    print("   Datos del formulario:")
    for key, value in form_data.items():
        print(f"     {key}: {value}")
    
    # 3. Validaciones (como en la función crear_contrato)
    print("\n3. EJECUTANDO VALIDACIONES...")
    
    fecha_inicio = form_data.get('fecha_inicio')
    obra_id = form_data.get('obra_id')
    
    if not fecha_inicio:
        print("   ❌ ERROR: Fecha de inicio faltante")
        return
    elif not obra_id:
        print("   ❌ ERROR: Obra ID faltante")
        return
    else:
        print("   ✅ Validaciones básicas pasaron")
    
    # 4. Intentar inserción (como en la función crear_contrato)
    print("\n4. INSERTANDO CONTRATO...")
    
    try:
        contrato_id = insert_contrato_safe(
            fecha_inicio=form_data['fecha_inicio'],
            fecha_fin=form_data['fecha_fin'],
            tipo_pago=form_data['tipo_pago'],
            obra_id=int(form_data['obra_id']),
            numero_contrato=form_data['numero_contrato'],
            cliente_id=int(form_data['cliente_id']),
            valor_total=float(form_data['valor_total']),
            estado=form_data['estado']
        )
        
        if contrato_id:
            print(f"   ✅ ¡ÉXITO! Contrato creado con ID: {contrato_id}")
            print("   🎉 El formulario web debería funcionar correctamente")
        else:
            print("   ❌ ERROR: La función insert_contrato_safe retornó None")
            
    except Exception as e:
        print(f"   ❌ EXCEPCIÓN durante inserción: {str(e)}")
        traceback.print_exc()
    
    print("\n=== FIN DE SIMULACIÓN ===")

if __name__ == "__main__":
    simulate_web_form_submission()