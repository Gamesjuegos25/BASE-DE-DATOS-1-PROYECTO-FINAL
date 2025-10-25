#!/usr/bin/env python3
from database import get_clientes_safe, get_obras_safe

print("=== PRUEBA DE DATOS PARA CONTRATOS ===")

print("\n1. Obteniendo clientes...")
try:
    clientes_data = get_clientes_safe()
    print(f"   Encontrados {len(clientes_data)} clientes:")
    for i, cliente in enumerate(clientes_data[:3]):  # Mostrar solo los primeros 3
        print(f"   [{i+1}] ID: {cliente.get('id') or cliente.get('id_cliente')}, Nombre: {cliente.get('nombre', 'Sin nombre')}")
    if len(clientes_data) > 3:
        print(f"   ... y {len(clientes_data) - 3} más")
        
    # Convertir a formato de tuplas como esperan los templates
    clientes_tuplas = [(cliente.get('id') or cliente.get('id_cliente'), 
                       cliente.get('nombre', 'Sin nombre'))
                       for cliente in clientes_data]
    print(f"\n   Formato de tuplas (primeros 3):")
    for i, tupla in enumerate(clientes_tuplas[:3]):
        print(f"   [{i+1}] {tupla}")
        
except Exception as e:
    print(f"   ERROR: {e}")

print("\n2. Obteniendo obras...")
try:
    obras_data = get_obras_safe()
    print(f"   Encontradas {len(obras_data)} obras:")
    for i, obra in enumerate(obras_data[:3]):  # Mostrar solo las primeras 3
        print(f"   [{i+1}] ID: {obra.get('id_obra') or obra.get('id')}, Nombre: {obra.get('nombre', 'Sin nombre')}, Ubicación: {obra.get('ubicacion', 'Sin ubicación')}")
    if len(obras_data) > 3:
        print(f"   ... y {len(obras_data) - 3} más")
        
    # Convertir a formato de tuplas como esperan los templates
    obras_tuplas = [(obra.get('id_obra') or obra.get('id'), 
                    f"{obra.get('nombre', 'Sin nombre')} - {obra.get('ubicacion', 'Sin ubicación')}")
                    for obra in obras_data]
    print(f"\n   Formato de tuplas (primeras 3):")
    for i, tupla in enumerate(obras_tuplas[:3]):
        print(f"   [{i+1}] {tupla}")
        
except Exception as e:
    print(f"   ERROR: {e}")

print("\n=== FIN DE PRUEBA ===")