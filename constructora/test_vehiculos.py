#!/usr/bin/env python3
"""
Script para probar funciones de vehiculos
"""

import sys
sys.path.append('.')
from database import get_vehiculos_safe, get_vehiculo_by_id_safe

def main():
    print('=== PRUEBA get_vehiculos_safe() ===')
    vehiculos = get_vehiculos_safe()
    print(f'Total vehículos obtenidos: {len(vehiculos)}')
    
    if vehiculos:
        print('\nPrimeros 3 vehículos:')
        for i, vehiculo in enumerate(vehiculos[:3], 1):
            print(f'{i}. {vehiculo}')
            
        # Probar get_vehiculo_by_id_safe
        primer_id = vehiculos[0].get('id_vehiculo') or vehiculos[0].get('id')
        if primer_id:
            print(f'\n=== PRUEBA get_vehiculo_by_id_safe({primer_id}) ===')
            vehiculo_detalle = get_vehiculo_by_id_safe(primer_id)
            print(f'Detalle: {vehiculo_detalle}')
    else:
        print('❌ No se encontraron vehículos')

if __name__ == '__main__':
    main()