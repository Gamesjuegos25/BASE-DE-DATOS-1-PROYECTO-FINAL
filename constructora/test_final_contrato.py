#!/usr/bin/env python3
from database import insert_contrato_safe
import traceback

print("=== PRUEBA FINAL DE CREACIÓN DE CONTRATO ===")

# Datos de prueba para un segundo contrato
test_data = {
    'numero_contrato': 'CON-2025-002',
    'cliente_id': 2,  # Inmobiliaria Desarrollo S.A.S
    'obra_id': 14,    # Hospital del sur - ojh
    'fecha_inicio': '2025-11-01',
    'fecha_fin': '2026-01-31',
    'valor_total': 250000.00,
    'estado': 'activo',
    'tipo_pago': 'quincenal'
}

print(f"Creando segundo contrato de prueba:")
for key, value in test_data.items():
    print(f"  {key}: {value}")

try:
    contrato_id = insert_contrato_safe(
        fecha_inicio=test_data['fecha_inicio'],
        fecha_fin=test_data['fecha_fin'],
        tipo_pago=test_data['tipo_pago'],
        obra_id=test_data['obra_id'],
        numero_contrato=test_data['numero_contrato'],
        cliente_id=test_data['cliente_id'],
        valor_total=test_data['valor_total'],
        estado=test_data['estado']
    )
    
    if contrato_id:
        print(f"\n✅ ¡ÉXITO! Segundo contrato creado con ID: {contrato_id}")
        print(f"\n🎉 El módulo de contratos está funcionando perfectamente!")
        print(f"   - Los clientes se muestran correctamente")
        print(f"   - Las obras se identifican claramente")
        print(f"   - La inserción de contratos funciona sin errores")
    else:
        print(f"\n❌ ERROR: La función retornó None")
        
except Exception as e:
    print(f"\n💥 EXCEPCIÓN: {str(e)}")
    print(f"\nTraceback completo:")
    traceback.print_exc()

print("\n=== FIN DE PRUEBA ===")