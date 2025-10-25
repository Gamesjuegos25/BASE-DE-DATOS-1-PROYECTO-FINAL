#!/usr/bin/env python3
from database import insert_contrato_safe
import traceback

print("=== PRUEBA DE INSERCIÓN DE CONTRATO ===")

# Datos de prueba
test_data = {
    'numero_contrato': 'CON-2025-001',
    'cliente_id': 1,  # Constructora Nacional S.A.
    'obra_id': 16,    # Hospital del sur
    'fecha_inicio': '2025-10-25',
    'fecha_fin': '2025-12-31',
    'valor_total': 150000.00,
    'estado': 'activo',
    'tipo_pago': 'mensual'
}

print(f"Intentando crear contrato con datos:")
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
        print(f"\n✅ ¡ÉXITO! Contrato creado con ID: {contrato_id}")
    else:
        print(f"\n❌ ERROR: La función retornó None")
        
except Exception as e:
    print(f"\n💥 EXCEPCIÓN: {str(e)}")
    print(f"\nTraceback completo:")
    traceback.print_exc()

print("\n=== FIN DE PRUEBA ===")