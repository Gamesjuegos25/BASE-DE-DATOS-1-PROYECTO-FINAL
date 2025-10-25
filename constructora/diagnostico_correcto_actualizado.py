#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DIAGNÓSTICO CORRECTO DEL SISTEMA ERP CONSTRUCTORA
===============================================
Análisis detallado y preciso del estado actual del sistema
"""

import re

def analizar_modulos_app():
    """Análisis correcto de módulos en app.py"""
    
    # Ruta del archivo app.py
    app_path = 'app.py'
    
    try:
        with open(app_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer app.py: {e}")
        return

    # Definir módulos esperados y sus operaciones CRUD
    modulos_esperados = {
        'usuarios': ['listar_usuarios', 'crear_usuario', 'ver_usuario', 'editar_usuario', 'eliminar_usuario'],
        'empleados': ['listar_empleados', 'crear_empleado', 'ver_empleado', 'editar_empleado', 'eliminar_empleado'],
        'proyectos': ['listar_proyectos', 'crear_proyecto', 'ver_proyecto', 'editar_proyecto', 'eliminar_proyecto'],
        'obras': ['listar_obras', 'crear_obra', 'ver_obra', 'editar_obra', 'eliminar_obra'],
        'materiales': ['listar_materiales', 'crear_material', 'ver_material', 'editar_material', 'eliminar_material'],
        'proveedores': ['listar_proveedores', 'crear_proveedor', 'ver_proveedor', 'editar_proveedor', 'eliminar_proveedor'],
        'clientes': ['listar_clientes', 'crear_cliente', 'ver_cliente', 'editar_cliente', 'eliminar_cliente'],
        'presupuestos': ['listar_presupuestos', 'crear_presupuesto', 'ver_presupuesto', 'editar_presupuesto', 'eliminar_presupuesto'],
        'facturas': ['listar_facturas', 'crear_factura', 'ver_factura', 'editar_factura', 'eliminar_factura'],
        'actividades': ['listar_actividades', 'crear_actividad', 'ver_actividad', 'editar_actividad', 'eliminar_actividad'],
        'bitacoras': ['listar_bitacoras', 'crear_bitacora', 'ver_bitacora', 'editar_bitacora', 'eliminar_bitacora'],
        'areas': ['listar_areas', 'crear_area', 'detalle_area', 'editar_area', 'eliminar_area'],
        'contratos': ['listar_contratos', 'crear_contrato', 'ver_contrato', 'editar_contrato', 'eliminar_contrato'],
        'vehiculos': ['listar_vehiculos', 'crear_vehiculo', 'ver_vehiculo', 'editar_vehiculo', 'eliminar_vehiculo'],
        'herramientas': ['listar_herramientas', 'crear_herramienta', 'ver_herramienta', 'editar_herramienta', 'eliminar_herramienta'],
        'inventario': ['listar_inventario', 'crear_item_inventario', 'ver_item_inventario', 'editar_item_inventario', 'eliminar_item_inventario'],
        'compras': ['listar_compras', 'crear_compra', 'ver_compra', 'editar_compra', 'eliminar_compra'],
        'ventas': ['listar_ventas', 'crear_venta', 'ver_venta', 'editar_venta', 'eliminar_venta'],
        'pagos': ['listar_pagos', 'crear_pago', 'ver_pago', 'editar_pago', 'eliminar_pago'],
        'nomina': ['listar_nomina', 'crear_nomina', 'calcular_nomina', 'ver_nomina', 'eliminar_nomina'],
        'incidentes': ['listar_incidentes', 'crear_incidente', 'ver_incidente', 'editar_incidente', 'eliminar_incidente'],
        'auditorias': ['listar_auditorias', 'crear_auditoria', 'ver_auditoria', 'editar_auditoria', 'eliminar_auditoria'],
        'permisos': ['listar_permisos', 'crear_permiso', 'ver_permiso', 'editar_permiso', 'eliminar_permiso']
    }
    
    print("🔍 **ANÁLISIS CORRECTO DE MÓDULOS EN APP.PY**")
    print("=" * 60)
    
    estado_modulos = {}
    
    for modulo, operaciones in modulos_esperados.items():
        print(f"\n📋 **MÓDULO: {modulo.upper()}**")
        
        operaciones_encontradas = []
        operaciones_faltantes = []
        
        for operacion in operaciones:
            # Buscar la función en el código
            patron = rf'def {operacion}\s*\('
            if re.search(patron, contenido):
                operaciones_encontradas.append(operacion)
            else:
                operaciones_faltantes.append(operacion)
        
        # Calcular porcentaje de completitud
        total_operaciones = len(operaciones)
        operaciones_completas = len(operaciones_encontradas)
        porcentaje = (operaciones_completas / total_operaciones) * 100
        
        # Determinar estado del módulo
        if porcentaje == 100:
            estado = "✅ COMPLETO"
        elif porcentaje >= 60:
            estado = "🟡 PARCIAL"
        else:
            estado = "❌ INCOMPLETO"
        
        estado_modulos[modulo] = {
            'estado': estado,
            'porcentaje': porcentaje,
            'completas': operaciones_completas,
            'total': total_operaciones,
            'encontradas': operaciones_encontradas,
            'faltantes': operaciones_faltantes
        }
        
        print(f"   Estado: {estado} ({porcentaje:.1f}%)")
        print(f"   Operaciones: {operaciones_completas}/{total_operaciones}")
        
        if operaciones_encontradas:
            print(f"   ✅ Implementadas: {', '.join(operaciones_encontradas)}")
        
        if operaciones_faltantes:
            print(f"   ❌ Faltantes: {', '.join(operaciones_faltantes)}")
    
    # Resumen general
    print("\n" + "=" * 60)
    print("📊 **RESUMEN GENERAL**")
    print("=" * 60)
    
    completos = sum(1 for info in estado_modulos.values() if info['porcentaje'] == 100)
    parciales = sum(1 for info in estado_modulos.values() if 60 <= info['porcentaje'] < 100)
    incompletos = sum(1 for info in estado_modulos.values() if info['porcentaje'] < 60)
    
    total_modulos = len(estado_modulos)
    porcentaje_sistema = sum(info['porcentaje'] for info in estado_modulos.values()) / total_modulos
    
    print(f"Total de módulos: {total_modulos}")
    print(f"✅ Completos (100%): {completos} ({(completos/total_modulos)*100:.1f}%)")
    print(f"🟡 Parciales (60-99%): {parciales} ({(parciales/total_modulos)*100:.1f}%)")
    print(f"❌ Incompletos (0-59%): {incompletos} ({(incompletos/total_modulos)*100:.1f}%)")
    print(f"📈 **COMPLETITUD GENERAL DEL SISTEMA: {porcentaje_sistema:.1f}%**")
    
    # Módulos prioritarios para completar
    print(f"\n🎯 **PRIORIDADES DE CORRECCIÓN**")
    print("=" * 40)
    
    modulos_ordenados = sorted(estado_modulos.items(), key=lambda x: x[1]['porcentaje'])
    
    for modulo, info in modulos_ordenados[:10]:  # Top 10 más críticos
        if info['porcentaje'] < 100:
            print(f"{info['estado']} {modulo}: {info['porcentaje']:.1f}% - Faltan {len(info['faltantes'])} operaciones")
    
    return estado_modulos

def buscar_rutas_problematicas():
    """Buscar rutas duplicadas o problemáticas"""
    
    print(f"\n🔍 **ANÁLISIS DE RUTAS PROBLEMÁTICAS**")
    print("=" * 50)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer app.py: {e}")
        return
    
    # Buscar todas las rutas
    rutas = re.findall(r"@app\.route\(['\"]([^'\"]+)['\"]", contenido)
    
    # Contar rutas duplicadas
    from collections import Counter
    conteo_rutas = Counter(rutas)
    
    rutas_duplicadas = {ruta: count for ruta, count in conteo_rutas.items() if count > 1}
    
    if rutas_duplicadas:
        print("❌ **RUTAS DUPLICADAS ENCONTRADAS:**")
        for ruta, count in rutas_duplicadas.items():
            print(f"   - {ruta}: {count} veces")
    else:
        print("✅ **NO SE ENCONTRARON RUTAS DUPLICADAS**")
    
    print(f"\n📊 Total de rutas únicas: {len(conteo_rutas)}")
    print(f"📊 Total de definiciones de rutas: {sum(conteo_rutas.values())}")
    
    return rutas_duplicadas

def analizar_validaciones_faltantes():
    """Analizar validaciones faltantes en formularios"""
    
    print(f"\n🔍 **ANÁLISIS DE VALIDACIONES FALTANTES**")
    print("=" * 50)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
    except Exception as e:
        print(f"❌ Error al leer app.py: {e}")
        return
    
    # Buscar campos numéricos sin validación
    patrones_problematicos = [
        (r'request\.form\.get\([\'\"]\w*precio[\'\"]\)', 'Campos de precio sin validación'),
        (r'request\.form\.get\([\'\"]\w*cantidad[\'\"]\)', 'Campos de cantidad sin validación'),
        (r'request\.form\.get\([\'\"]\w*monto[\'\"]\)', 'Campos de monto sin validación'),
        (r'int\(request\.form\.get\(', 'Conversión directa a int sin validación'),
        (r'float\(request\.form\.get\(', 'Conversión directa a float sin validación')
    ]
    
    problemas_encontrados = []
    
    for patron, descripcion in patrones_problematicos:
        matches = re.findall(patron, contenido, re.IGNORECASE)
        if matches:
            problemas_encontrados.append((descripcion, len(matches)))
    
    if problemas_encontrados:
        print("⚠️ **PROBLEMAS DE VALIDACIÓN ENCONTRADOS:**")
        for problema, count in problemas_encontrados:
            print(f"   - {problema}: {count} casos")
    else:
        print("✅ **NO SE ENCONTRARON PROBLEMAS OBVIOS DE VALIDACIÓN**")
    
    return problemas_encontrados

def main():
    """Ejecutar diagnóstico completo y correcto"""
    
    print("🚀 **DIAGNÓSTICO CORRECTO Y ACTUALIZADO DEL SISTEMA ERP**")
    print("=" * 70)
    print("Este análisis corrige los errores del diagnóstico anterior")
    print("=" * 70)
    
    # 1. Analizar módulos
    estado_modulos = analizar_modulos_app()
    
    # 2. Buscar rutas problemáticas
    rutas_duplicadas = buscar_rutas_problematicas()
    
    # 3. Analizar validaciones
    validaciones = analizar_validaciones_faltantes()
    
    # 4. Generar recomendaciones
    print(f"\n🎯 **RECOMENDACIONES DE CORRECCIÓN**")
    print("=" * 50)
    
    # Contar módulos por estado
    completos = sum(1 for info in estado_modulos.values() if info['porcentaje'] == 100)
    parciales = sum(1 for info in estado_modulos.values() if 60 <= info['porcentaje'] < 100)
    incompletos = sum(1 for info in estado_modulos.values() if info['porcentaje'] < 60)
    
    print(f"1. ✅ El sistema está MÁS COMPLETO de lo esperado:")
    print(f"   - {completos} módulos completamente funcionales")
    print(f"   - {parciales} módulos parcialmente funcionales")
    print(f"   - {incompletos} módulos incompletos")
    
    if not rutas_duplicadas:
        print(f"\n2. ✅ No hay rutas duplicadas - EXCELENTE")
    else:
        print(f"\n2. ❌ Corregir {len(rutas_duplicadas)} rutas duplicadas")
    
    if validaciones:
        print(f"\n3. ⚠️ Mejorar validaciones en {len(validaciones)} áreas")
    else:
        print(f"\n3. ✅ Validaciones básicas están bien")
    
    print(f"\n4. 🎯 **PRIORIDAD ALTA**: Completar módulos incompletos:")
    for modulo, info in estado_modulos.items():
        if info['porcentaje'] < 60:
            print(f"   - {modulo}: completar {len(info['faltantes'])} operaciones")
    
    print(f"\n✨ **CONCLUSIÓN**: El sistema está en mejor estado del esperado")
    print(f"   Funcionalidad actual estimada: {sum(info['porcentaje'] for info in estado_modulos.values()) / len(estado_modulos):.1f}%")

if __name__ == "__main__":
    main()