#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import database as db

def test_crear_material_completo():
    try:
        # Test de creación de material completo
        print("=== TEST CREAR MATERIAL COMPLETO ===")
        
        # Datos de prueba
        nombre = "Cemento Portland Tipo I"
        unidad = "Saco 50kg"
        precio = 25000.0
        descripcion = "Cemento para uso general en construcción"
        categoria = "Cemento"
        stock = 100
        proveedor_id = 4  # Usar proveedor disponible ID 4
        
        print(f"Creando material: {nombre}")
        print(f"Stock inicial: {stock}")
        print(f"Proveedor ID: {proveedor_id}")
        
        material_id = db.insert_material_completo_safe(
            nombre=nombre,
            unidad=unidad,
            precio=precio,
            descripcion=descripcion,
            categoria=categoria,
            stock=stock,
            proveedor_id=proveedor_id
        )
        
        if material_id:
            print(f"✅ Material creado exitosamente con ID: {material_id}")
            
            # Verificar que se creó correctamente
            materiales = db.get_materiales_safe()
            material_creado = None
            for m in materiales:
                if m.get('id_material') == material_id:
                    material_creado = m
                    break
            
            if material_creado:
                print(f"✅ Verificación exitosa:")
                print(f"  - Nombre: {material_creado.get('nombre')}")
                print(f"  - Stock: {material_creado.get('stock')}")
                print(f"  - Categoría: {material_creado.get('categoria')}")
                print(f"  - Proveedor: {material_creado.get('proveedor_nombre')}")
            
            return True
        else:
            print("❌ Error al crear material")
            return False
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_listar_materiales():
    try:
        materiales = db.get_materiales_safe()
        print(f"\n=== LISTADO MATERIALES ({len(materiales)}) ===")
        for m in materiales:
            print(f"ID: {m.get('id_material')}, Nombre: {m.get('nombre')}, Stock: {m.get('stock')}, Proveedor: {m.get('proveedor_nombre', 'Sin proveedor')}")
        return True
    except Exception as e:
        print(f"❌ Error listando materiales: {e}")
        return False

if __name__ == "__main__":
    test_crear_material_completo()
    test_listar_materiales()