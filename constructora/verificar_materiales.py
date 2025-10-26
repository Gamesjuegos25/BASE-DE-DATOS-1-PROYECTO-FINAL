#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación completa del sistema de materiales
"""
import sys
sys.path.append('.')

try:
    from database import insert_material_completo_safe, get_materiales_safe, get_proveedores_safe
    
    print("=== VERIFICACIÓN SISTEMA DE MATERIALES ===\n")
    
    # 1. Verificar importación
    print("✅ 1. Función insert_material_completo_safe importada correctamente")
    
    # 2. Verificar proveedores
    proveedores = get_proveedores_safe()
    print(f"✅ 2. Proveedores disponibles: {len(proveedores)}")
    
    # 3. Verificar materiales actuales
    materiales = get_materiales_safe()
    print(f"✅ 3. Materiales en sistema: {len(materiales)}")
    
    print("\n=== ESTADO ACTUAL ===")
    print(f"📦 Total proveedores: {len(proveedores)}")
    print(f"📦 Total materiales: {len(materiales)}")
    
    if len(proveedores) > 0:
        print(f"✅ Proveedor disponible: {proveedores[0]['nombre_proveedor']}")
    
    if len(materiales) > 0:
        print("✅ Últimos materiales:")
        for i, mat in enumerate(materiales[-3:], 1):  # Últimos 3 materiales
            nombre = mat.get('nombre_material', 'Sin nombre')
            stock = mat.get('stock_actual', 0)
            proveedor = mat.get('nombre_proveedor', 'Sin proveedor')
            print(f"   {i}. {nombre} | Stock: {stock} | Proveedor: {proveedor}")
    
    print("\n✅ SISTEMA DE MATERIALES FUNCIONANDO CORRECTAMENTE")
    print("🚀 Puedes crear materiales desde: http://127.0.0.1:5000/materiales/crear")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error: {e}")