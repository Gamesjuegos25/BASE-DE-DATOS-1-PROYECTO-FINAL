#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import database as db

def test_crear_bodega():
    try:
        # Test de creación de bodega con empleado supervisor
        print("=== TEST CREAR BODEGA ===")
        
        # Datos de prueba
        responsable_id = "3"  # Juan Carlos (Supervisor)
        ubicacion = "Zona Industrial Norte - Sector A"
        capacidad = "1500 m³ - Materiales pesados" 
        telefono = "+57 1 234-5678"
        estado = "Activa"
        observaciones = "Bodega principal para materiales de construcción"
        
        print(f"Creando bodega con responsable ID: {responsable_id}")
        
        bodega_id = db.insert_bodega_safe(
            responsable_bodega=responsable_id,
            ubicacion_bodega=ubicacion,
            capacidad_bodega=capacidad,
            telefono_bodega=telefono,
            estado_bodega=estado,
            observaciones_bodega=observaciones
        )
        
        if bodega_id:
            print(f"✅ Bodega creada exitosamente con ID: {bodega_id}")
            
            # Verificar que se creó correctamente
            bodega = db.get_bodega_by_id_safe(bodega_id)
            if bodega:
                print(f"✅ Verificación exitosa: {bodega}")
            
            return True
        else:
            print("❌ Error al crear bodega")
            return False
            
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_listar_bodegas():
    try:
        bodegas = db.get_bodegas_safe()
        print(f"\n=== LISTADO BODEGAS ({len(bodegas)}) ===")
        for b in bodegas:
            print(f"ID: {b.get('id_bodega')}, Responsable: {b.get('responsable_bodega')}, Ubicación: {b.get('ubicacion_bodega')}")
        return True
    except Exception as e:
        print(f"❌ Error listando bodegas: {e}")
        return False

if __name__ == "__main__":
    test_crear_bodega()
    test_listar_bodegas()