#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def verificar_botones_modulos():
    """Verificar los botones de ver, editar y eliminar en todos los módulos"""
    
    templates_dir = Path("templates")
    modulos_reporte = {}
    
    # Lista de módulos esperados
    modulos = [
        "obras", "empleados", "proveedores", "materiales", "vehiculos", 
        "equipos", "bodegas", "actividades", "areas", "contratos", 
        "facturas", "proyectos", "usuarios", "requisiciones", "tipos_obra",
        "trabajos", "auditorias", "bitacoras", "incidentes", "movimientos", 
        "presupuestos", "avances", "permisos"
    ]
    
    for modulo in modulos:
        modulo_dir = templates_dir / modulo
        listar_file = modulo_dir / "listar.html"
        
        if not modulo_dir.exists():
            modulos_reporte[modulo] = {
                'existe_directorio': False,
                'tiene_listar': False,
                'botones': {'ver': False, 'editar': False, 'eliminar': False}
            }
            continue
            
        if not listar_file.exists():
            modulos_reporte[modulo] = {
                'existe_directorio': True,
                'tiene_listar': False,
                'botones': {'ver': False, 'editar': False, 'eliminar': False}
            }
            continue
            
        # Leer el archivo y verificar botones
        try:
            with open(listar_file, 'r', encoding='utf-8') as f:
                contenido = f.read()
                
            botones = {
                'ver': bool(re.search(r'btn-view|fa-eye|bi-eye|Ver detalles?', contenido, re.IGNORECASE)),
                'editar': bool(re.search(r'btn-edit|fa-edit|bi-edit|fa-pencil|bi-pencil|Editar', contenido, re.IGNORECASE)),
                'eliminar': bool(re.search(r'btn-danger|btn-delete|fa-trash|bi-trash|Eliminar', contenido, re.IGNORECASE))
            }
            
            modulos_reporte[modulo] = {
                'existe_directorio': True,
                'tiene_listar': True,
                'botones': botones
            }
            
        except Exception as e:
            modulos_reporte[modulo] = {
                'existe_directorio': True,
                'tiene_listar': True,
                'error': str(e),
                'botones': {'ver': False, 'editar': False, 'eliminar': False}
            }
    
    return modulos_reporte

def generar_reporte(modulos_reporte):
    """Generar reporte detallado de los módulos"""
    print("=" * 80)
    print("🔍 REPORTE DE VERIFICACIÓN DE BOTONES EN MÓDULOS")
    print("=" * 80)
    
    # Estadísticas generales
    total_modulos = len(modulos_reporte)
    modulos_con_directorio = sum(1 for m in modulos_reporte.values() if m['existe_directorio'])
    modulos_con_listar = sum(1 for m in modulos_reporte.values() if m['tiene_listar'])
    
    print(f"\n📊 ESTADÍSTICAS GENERALES:")
    print(f"   • Total módulos verificados: {total_modulos}")
    print(f"   • Módulos con directorio: {modulos_con_directorio}/{total_modulos}")
    print(f"   • Módulos con listar.html: {modulos_con_listar}/{total_modulos}")
    
    # Análisis por estado
    completos = []
    incompletos = []
    sin_implementar = []
    
    for modulo, info in modulos_reporte.items():
        if not info['existe_directorio'] or not info['tiene_listar']:
            sin_implementar.append(modulo)
        elif all(info['botones'].values()):
            completos.append(modulo)
        else:
            incompletos.append(modulo)
    
    print(f"\n✅ MÓDULOS COMPLETOS ({len(completos)}):")
    for modulo in completos:
        print(f"   • {modulo.upper()}: ✓ Ver, ✓ Editar, ✓ Eliminar")
    
    print(f"\n⚠️  MÓDULOS INCOMPLETOS ({len(incompletos)}):")
    for modulo in incompletos:
        info = modulos_reporte[modulo]
        botones_str = []
        if info['botones']['ver']:
            botones_str.append("✓ Ver")
        else:
            botones_str.append("✗ Ver")
            
        if info['botones']['editar']:
            botones_str.append("✓ Editar")
        else:
            botones_str.append("✗ Editar")
            
        if info['botones']['eliminar']:
            botones_str.append("✓ Eliminar")
        else:
            botones_str.append("✗ Eliminar")
            
        print(f"   • {modulo.upper()}: {', '.join(botones_str)}")
    
    print(f"\n❌ MÓDULOS SIN IMPLEMENTAR ({len(sin_implementar)}):")
    for modulo in sin_implementar:
        info = modulos_reporte[modulo]
        if not info['existe_directorio']:
            print(f"   • {modulo.upper()}: Sin directorio")
        elif not info['tiene_listar']:
            print(f"   • {modulo.upper()}: Sin archivo listar.html")
    
    # Resumen de acciones requeridas
    print(f"\n🔧 ACCIONES REQUERIDAS:")
    
    if sin_implementar:
        print(f"   1. Crear {len(sin_implementar)} módulos faltantes")
        
    if incompletos:
        print(f"   2. Completar botones en {len(incompletos)} módulos")
        for modulo in incompletos:
            info = modulos_reporte[modulo]
            botones_faltantes = []
            if not info['botones']['ver']:
                botones_faltantes.append('Ver')
            if not info['botones']['editar']:
                botones_faltantes.append('Editar')
            if not info['botones']['eliminar']:
                botones_faltantes.append('Eliminar')
            
            print(f"      • {modulo}: Agregar {', '.join(botones_faltantes)}")
    
    # Porcentaje de completitud
    if modulos_con_listar > 0:
        porcentaje_completos = (len(completos) / modulos_con_listar) * 100
        print(f"\n📈 COMPLETITUD DEL SISTEMA: {porcentaje_completos:.1f}%")
        
    print("\n" + "=" * 80)

if __name__ == '__main__':
    modulos_reporte = verificar_botones_modulos()
    generar_reporte(modulos_reporte)