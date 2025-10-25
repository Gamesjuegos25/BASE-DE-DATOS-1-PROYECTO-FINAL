#!/usr/bin/env python3
"""
Script para aplicar diseño responsivo a las tablas de los módulos principales
Aplica clases CSS responsivas Bootstrap a las columnas de las tablas
"""

import os
import re
from pathlib import Path

def aplicar_responsive_materiales():
    """Aplica diseño responsivo al módulo de materiales"""
    archivo = "templates/materiales/listar.html"
    
    if not os.path.exists(archivo):
        print(f"❌ No se encontró {archivo}")
        return
    
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Aplicar clases responsivas a headers
    contenido = re.sub(
        r'<th>ID</th>',
        '<th class="d-none d-md-table-cell">ID</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Descripción</th>',
        '<th class="d-none d-lg-table-cell">Descripción</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Categoría</th>',
        '<th class="d-none d-sm-table-cell">Categoría</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Precio Unitario</th>',
        '<th class="d-none d-md-table-cell">Precio Unitario</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Stock</th>',
        '<th class="d-none d-sm-table-cell">Stock</th>',
        contenido
    )
    
    # Aplicar clases responsivas a celdas
    contenido = re.sub(
        r'<td>{{ material\.id }}</td>',
        '<td class="d-none d-md-table-cell">{{ material.id }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ material\.descripcion }}</td>',
        '<td class="d-none d-lg-table-cell">{{ material.descripcion }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ material\.categoria }}</td>',
        '<td class="d-none d-sm-table-cell">{{ material.categoria }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>Q{{ "{:,.2f}".format\(material\.precio_unitario\) }}</td>',
        '<td class="d-none d-md-table-cell font-weight-bold text-success">Q{{ "{:,.2f}".format(material.precio_unitario) }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ material\.stock }}</td>',
        '<td class="d-none d-sm-table-cell">{{ material.stock }}</td>',
        contenido
    )
    
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✅ Aplicado diseño responsivo a {archivo}")

def aplicar_responsive_proveedores():
    """Aplica diseño responsivo al módulo de proveedores"""
    archivo = "templates/proveedores/listar.html"
    
    if not os.path.exists(archivo):
        print(f"❌ No se encontró {archivo}")
        return
    
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Aplicar clases responsivas a headers
    contenido = re.sub(
        r'<th>ID</th>',
        '<th class="d-none d-md-table-cell">ID</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Dirección</th>',
        '<th class="d-none d-lg-table-cell">Dirección</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Teléfono</th>',
        '<th class="d-none d-sm-table-cell">Teléfono</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Email</th>',
        '<th class="d-none d-md-table-cell">Email</th>',
        contenido
    )
    
    # Aplicar clases responsivas a celdas
    contenido = re.sub(
        r'<td>{{ proveedor\.id }}</td>',
        '<td class="d-none d-md-table-cell">{{ proveedor.id }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ proveedor\.direccion }}</td>',
        '<td class="d-none d-lg-table-cell">{{ proveedor.direccion }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ proveedor\.telefono }}</td>',
        '<td class="d-none d-sm-table-cell">{{ proveedor.telefono }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ proveedor\.email }}</td>',
        '<td class="d-none d-md-table-cell">{{ proveedor.email }}</td>',
        contenido
    )
    
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✅ Aplicado diseño responsivo a {archivo}")

def aplicar_responsive_contratos():
    """Aplica diseño responsivo al módulo de contratos"""
    archivo = "templates/contratos/listar.html"
    
    if not os.path.exists(archivo):
        print(f"❌ No se encontró {archivo}")
        return
    
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Aplicar clases responsivas a headers
    contenido = re.sub(
        r'<th>ID</th>',
        '<th class="d-none d-lg-table-cell">ID</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Descripción</th>',
        '<th class="d-none d-md-table-cell">Descripción</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Fecha Inicio</th>',
        '<th class="d-none d-sm-table-cell">Fecha Inicio</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Fecha Fin</th>',
        '<th class="d-none d-sm-table-cell">Fecha Fin</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Monto</th>',
        '<th class="d-none d-md-table-cell">Monto</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Estado</th>',
        '<th class="d-none d-lg-table-cell">Estado</th>',
        contenido
    )
    
    # Aplicar clases responsivas a celdas
    contenido = re.sub(
        r'<td>{{ contrato\.id }}</td>',
        '<td class="d-none d-lg-table-cell">{{ contrato.id }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ contrato\.descripcion }}</td>',
        '<td class="d-none d-md-table-cell">{{ contrato.descripcion }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ contrato\.fecha_inicio }}</td>',
        '<td class="d-none d-sm-table-cell">{{ contrato.fecha_inicio }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ contrato\.fecha_fin }}</td>',
        '<td class="d-none d-sm-table-cell">{{ contrato.fecha_fin }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>Q{{ "{:,.2f}".format\(contrato\.monto\) }}</td>',
        '<td class="d-none d-md-table-cell font-weight-bold text-primary">Q{{ "{:,.2f}".format(contrato.monto) }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ contrato\.estado }}</td>',
        '<td class="d-none d-lg-table-cell">{{ contrato.estado }}</td>',
        contenido
    )
    
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✅ Aplicado diseño responsivo a {archivo}")

def aplicar_responsive_facturas():
    """Aplica diseño responsivo al módulo de facturas"""
    archivo = "templates/facturas/listar.html"
    
    if not os.path.exists(archivo):
        print(f"❌ No se encontró {archivo}")
        return
    
    with open(archivo, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Aplicar clases responsivas a headers
    contenido = re.sub(
        r'<th>ID</th>',
        '<th class="d-none d-md-table-cell">ID</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Cliente</th>',
        '<th class="d-table-cell">Cliente</th>',  # Siempre visible
        contenido
    )
    
    contenido = re.sub(
        r'<th>Fecha</th>',
        '<th class="d-none d-sm-table-cell">Fecha</th>',
        contenido
    )
    
    contenido = re.sub(
        r'<th>Monto Total</th>',
        '<th class="d-table-cell font-weight-bold">Monto Total</th>',  # Siempre visible
        contenido
    )
    
    contenido = re.sub(
        r'<th>Estado</th>',
        '<th class="d-none d-lg-table-cell">Estado</th>',
        contenido
    )
    
    # Aplicar clases responsivas a celdas
    contenido = re.sub(
        r'<td>{{ factura\.id }}</td>',
        '<td class="d-none d-md-table-cell">{{ factura.id }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ factura\.fecha }}</td>',
        '<td class="d-none d-sm-table-cell">{{ factura.fecha }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>Q{{ "{:,.2f}".format\(factura\.monto_total\) }}</td>',
        '<td class="font-weight-bold text-success">Q{{ "{:,.2f}".format(factura.monto_total) }}</td>',
        contenido
    )
    
    contenido = re.sub(
        r'<td>{{ factura\.estado }}</td>',
        '<td class="d-none d-lg-table-cell">{{ factura.estado }}</td>',
        contenido
    )
    
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(contenido)
    
    print(f"✅ Aplicado diseño responsivo a {archivo}")

def main():
    """Función principal"""
    print("🎨 Aplicando diseño responsivo a tablas principales...")
    print("=" * 60)
    
    # Cambiar al directorio del proyecto
    os.chdir(os.path.dirname(__file__))
    
    # Aplicar responsive a módulos principales
    aplicar_responsive_materiales()
    aplicar_responsive_proveedores()
    aplicar_responsive_contratos()
    aplicar_responsive_facturas()
    
    print("=" * 60)
    print("✅ ¡Diseño responsivo aplicado exitosamente!")
    print("\n📱 Las tablas ahora son responsivas:")
    print("   - Móvil: Solo columnas esenciales")
    print("   - Tablet: Columnas principales")
    print("   - Desktop: Todas las columnas")

if __name__ == "__main__":
    main()