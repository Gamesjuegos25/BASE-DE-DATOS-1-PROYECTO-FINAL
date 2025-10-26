#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import database as db

def test_crear_proveedor():
    try:
        # Test de creación de proveedor
        nombre = "PRUEBA PROVEEDOR TEST"
        contacto = "Tel: 123-456-789 | Email: test@test.com"
        
        print(f"Intentando crear proveedor: {nombre}")
        proveedor_id = db.insert_proveedor_safe(nombre=nombre, contacto=contacto)
        
        if proveedor_id:
            print(f"✅ Proveedor creado exitosamente con ID: {proveedor_id}")
            
            # Verificar que se creó correctamente
            proveedor = db.get_proveedor_by_id_safe(proveedor_id)
            print(f"✅ Datos del proveedor: {proveedor}")
            
            return True
        else:
            print("❌ Error al crear proveedor")
            return False
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_listar_proveedores():
    try:
        proveedores = db.get_proveedores_safe()
        print(f"\n=== LISTADO PROVEEDORES ({len(proveedores)}) ===")
        for p in proveedores:
            print(f"ID: {p.get('id_proveedor')}, Nombre: {p.get('nombre_proveedor')}")
        return True
    except Exception as e:
        print(f"❌ Error listando proveedores: {e}")
        return False

if __name__ == "__main__":
    print("=== TEST PROVEEDORES ===")
    test_crear_proveedor()
    test_listar_proveedores()