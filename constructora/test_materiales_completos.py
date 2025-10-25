#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from database import get_materiales_safe, get_material_by_id_safe

print("=== PRUEBA DE FUNCIONES ACTUALIZADAS ===")

# Probar lista de materiales
print("\n1. LISTA DE MATERIALES CON INFORMACIÓN COMPLETA:")
materiales = get_materiales_safe()

for mat in materiales[:3]:  # Solo primeros 3 para no saturar
    print(f"\nMaterial: {mat.get('nombre', 'N/D')}")
    print(f"  ID: {mat.get('id_material', 'N/D')}")
    print(f"  Precio: Q{mat.get('precio_unitario', 0)}")
    print(f"  Stock actual: {mat.get('stock_actual', 'N/D')}")
    print(f"  Stock mínimo: {mat.get('stock_minimo', 'N/D')}")
    print(f"  Proveedor: {mat.get('proveedor_nombre', 'Sin proveedor')}")
    print(f"  Contacto: {mat.get('proveedor_contacto', 'Sin contacto')}")
    print(f"  Descripción: {mat.get('descripcion', 'Sin descripción')}")
    print(f"  Categoría: {mat.get('categoria', 'Sin categoría')}")
    print(f"  Estado: {mat.get('estado', 'Sin estado')}")

# Probar detalle individual
print(f"\n2. DETALLE INDIVIDUAL (Material ID: 1):")
material = get_material_by_id_safe(1)

if material:
    print(f"Material: {material.get('nombre', 'N/D')}")
    print(f"  Precio: Q{material.get('precio_unitario', 0)}")
    print(f"  Stock actual: {material.get('stock_actual', 'N/D')}")
    print(f"  Stock mínimo: {material.get('stock_minimo', 'N/D')}")
    print(f"  Proveedor: {material.get('proveedor_nombre', 'Sin proveedor')}")
    print(f"  Contacto: {material.get('proveedor_contacto', 'Sin contacto')}")
else:
    print("Material no encontrado")

print(f"\nTotal materiales disponibles: {len(materiales)}")