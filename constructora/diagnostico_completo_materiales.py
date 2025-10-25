#!/usr/bin/env python3
"""
Script de diagnóstico completo para el módulo de materiales
"""

import sys
sys.path.insert(0, '.')

from database import get_materiales_safe, get_material_by_id_safe

def analizar_datos_materiales():
    print("=" * 60)
    print("DIAGNÓSTICO COMPLETO - MÓDULO MATERIALES")
    print("=" * 60)
    
    # Obtener materiales
    materiales = get_materiales_safe()
    
    print(f"\nTotal de materiales encontrados: {len(materiales)}")
    
    # Análisis de campos disponibles
    if materiales:
        print(f"\nCampos disponibles en el primer material:")
        primer_material = materiales[0]
        for campo in sorted(primer_material.keys()):
            valor = primer_material.get(campo)
            print(f"  {campo}: {valor} ({type(valor).__name__})")
    
    print(f"\n" + "=" * 60)
    print("ANÁLISIS DETALLADO POR MATERIAL")
    print("=" * 60)
    
    for i, material in enumerate(materiales, 1):
        print(f"\n{i}. {material.get('nombre', 'SIN NOMBRE')}")
        print(f"   ID: {material.get('id_material')}")
        print(f"   ├─ Información Básica:")
        print(f"   │  ├─ Unidad: {material.get('unidad', 'No especificada')}")
        print(f"   │  ├─ Precio: Q{material.get('precio_unitario', 0):,.2f}")
        print(f"   │  └─ Descripción: {material.get('descripcion', 'Sin descripción')}")
        
        print(f"   ├─ Stock/Inventario:")
        print(f"   │  ├─ Stock Actual: {material.get('stock_actual', 'N/D')}")
        print(f"   │  └─ Stock Mínimo: {material.get('stock_minimo', 'N/D')}")
        
        print(f"   ├─ Proveedor:")
        print(f"   │  ├─ Nombre: {material.get('proveedor_nombre', 'Sin proveedor')}")
        print(f"   │  └─ Contacto: {material.get('proveedor_contacto', 'Sin contacto')}")
        
        print(f"   └─ Clasificación:")
        print(f"      ├─ Categoría: {material.get('categoria', 'Sin categoría')}")
        print(f"      └─ Estado: {material.get('estado', 'Sin estado')}")
    
    print(f"\n" + "=" * 60)
    print("RESUMEN DE PROBLEMAS IDENTIFICADOS")
    print("=" * 60)
    
    problemas = []
    
    # Contadores para análisis
    sin_proveedor = 0
    sin_stock = 0
    sin_descripcion = 0
    
    for material in materiales:
        if not material.get('proveedor_nombre'):
            sin_proveedor += 1
        if material.get('stock_actual', 0) == 0:
            sin_stock += 1
        if material.get('descripcion') == 'Sin descripción':
            sin_descripcion += 1
    
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   • Materiales sin proveedor: {sin_proveedor}/{len(materiales)} ({sin_proveedor/len(materiales)*100:.1f}%)")
    print(f"   • Materiales sin stock: {sin_stock}/{len(materiales)} ({sin_stock/len(materiales)*100:.1f}%)")
    print(f"   • Materiales sin descripción: {sin_descripcion}/{len(materiales)} ({sin_descripcion/len(materiales)*100:.1f}%)")
    
    print(f"\n🔧 RECOMENDACIONES:")
    if sin_proveedor > 0:
        print(f"   1. Asignar proveedores a {sin_proveedor} materiales")
    if sin_descripcion == len(materiales):
        print(f"   2. Agregar descripciones detalladas a los materiales")
    if sin_stock > 0:
        print(f"   3. Actualizar información de stock para {sin_stock} materiales")
    
    # Verificar datos de un material específico
    print(f"\n" + "=" * 60)
    print("PRUEBA DE DETALLE INDIVIDUAL")
    print("=" * 60)
    
    if materiales:
        material_id = materiales[0]['id_material']
        detalle = get_material_by_id_safe(material_id)
        
        print(f"\nDetalle del material ID {material_id}:")
        if detalle:
            for campo, valor in detalle.items():
                print(f"   {campo}: {valor}")
        else:
            print("   ERROR: No se pudo obtener el detalle")

if __name__ == "__main__":
    try:
        analizar_datos_materiales()
    except Exception as e:
        print(f"ERROR en el análisis: {e}")
        import traceback
        traceback.print_exc()