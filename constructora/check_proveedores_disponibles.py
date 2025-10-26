#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import database as db

def check_proveedores():
    try:
        proveedores = db.get_proveedores_safe()
        print(f"=== PROVEEDORES DISPONIBLES ({len(proveedores)}) ===")
        for p in proveedores:
            print(f"ID: {p.get('id_proveedor')}, Nombre: {p.get('nombre_proveedor')}")
        
        if len(proveedores) > 0:
            primer_proveedor = proveedores[0]
            print(f"\n✅ Primer proveedor disponible: ID {primer_proveedor.get('id_proveedor')}")
            return primer_proveedor.get('id_proveedor')
        else:
            print("\n❌ No hay proveedores disponibles")
            return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    check_proveedores()