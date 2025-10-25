#!/usr/bin/env python3
"""
Script para auditar todos los módulos del sistema y verificar CRUD completo
"""
import os
import re
from pathlib import Path

# Módulos según el usuario
MODULOS = [
    'obras', 'proyectos', 'actividades', 'areas', 'empleados', 
    'contratos', 'trabajos', 'materiales', 'proveedores', 'bodegas',
    'requisiciones', 'vehiculos', 'equipos', 'movimientos', 'bitacoras',
    'incidentes', 'avance', 'presupuesto', 'usuarios', 'auditorias',
    'facturas'
]

def buscar_rutas_modulo(app_path, modulo):
    """Busca todas las rutas CRUD de un módulo en app.py"""
    rutas = {
        'listar': False,
        'ver': False,
        'crear': False,
        'editar': False,
        'eliminar': False
    }
    
    with open(app_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
        
        # Patrones de búsqueda
        modulo_singular = modulo.rstrip('s')  # Simplificación
        
        # Listar
        if re.search(rf"@app\.route\('/{modulo}'\)", contenido):
            rutas['listar'] = True
            
        # Ver detalle (varias posibilidades)
        patrones_ver = [
            rf"@app\.route\('/{modulo}/<int:id>'\)",
            rf"@app\.route\('/{modulo}/<int:id_\w+>'\)",
            rf"def ver_{modulo_singular}\(",
        ]
        for patron in patrones_ver:
            if re.search(patron, contenido):
                rutas['ver'] = True
                break
                
        # Crear
        patrones_crear = [
            rf"@app\.route\('/{modulo}/nuevo'",
            rf"@app\.route\('/{modulo}/crear'",
            rf"def crear_{modulo_singular}\(",
        ]
        for patron in patrones_crear:
            if re.search(patron, contenido):
                rutas['crear'] = True
                break
                
        # Editar
        patrones_editar = [
            rf"@app\.route\('/{modulo}/<int:id>/editar'",
            rf"def editar_{modulo_singular}\(",
        ]
        for patron in patrones_editar:
            if re.search(patron, contenido):
                rutas['editar'] = True
                break
                
        # Eliminar
        patrones_eliminar = [
            rf"@app\.route\('/{modulo}/<int:id>/eliminar'",
            rf"def eliminar_{modulo_singular}\(",
        ]
        for patron in patrones_eliminar:
            if re.search(patron, contenido):
                rutas['eliminar'] = True
                break
    
    return rutas

def buscar_templates_modulo(templates_path, modulo):
    """Busca templates de un módulo"""
    templates = {
        'listar': False,
        'crear': False,
        'detalle': False,
        'editar': False
    }
    
    modulo_path = templates_path / modulo
    if not modulo_path.exists():
        return templates
    
    archivos = list(modulo_path.glob('*.html'))
    
    for archivo in archivos:
        nombre = archivo.stem
        if 'listar' in nombre:
            templates['listar'] = True
        if 'crear' in nombre:
            templates['crear'] = True
        if 'detalle' in nombre or 'ver' in nombre:
            templates['detalle'] = True
        if 'editar' in nombre:
            templates['editar'] = True
    
    return templates

def verificar_botones_template(templates_path, modulo):
    """Verifica si el template de listar tiene botones de acción"""
    botones = {
        'ver': False,
        'editar': False,
        'eliminar': False
    }
    
    modulo_path = templates_path / modulo
    if not modulo_path.exists():
        return botones
    
    # Buscar archivo listar
    listar_files = list(modulo_path.glob('listar*.html'))
    if not listar_files:
        return botones
    
    # Leer el primer archivo listar encontrado
    with open(listar_files[0], 'r', encoding='utf-8') as f:
        contenido = f.read()
        
        # Buscar botones
        if re.search(r'btn-view|Ver Detalle|ver_\w+', contenido, re.IGNORECASE):
            botones['ver'] = True
        if re.search(r'btn-edit|Editar|editar_\w+', contenido, re.IGNORECASE):
            botones['editar'] = True
        if re.search(r'btn-danger|Eliminar|eliminar_\w+', contenido, re.IGNORECASE):
            botones['eliminar'] = True
    
    return botones

def calcular_completitud(rutas, templates, botones):
    """Calcula el porcentaje de completitud de un módulo"""
    total = 0
    completo = 0
    
    # Rutas (peso: 50%)
    for ruta in rutas.values():
        total += 1
        if ruta:
            completo += 1
    
    # Templates (peso: 30%)
    for template in templates.values():
        total += 0.6
        if template:
            completo += 0.6
    
    # Botones (peso: 20%)
    for boton in botones.values():
        total += 0.4
        if boton:
            completo += 0.4
    
    return int((completo / total) * 100) if total > 0 else 0

def main():
    # Paths
    base_path = Path(__file__).parent
    app_path = base_path / 'app.py'
    templates_path = base_path / 'templates'
    
    print("=" * 80)
    print("AUDITORÍA COMPLETA DE MÓDULOS - SISTEMA ERP CONSTRUCTORA")
    print("=" * 80)
    print()
    
    resultados = []
    
    for modulo in MODULOS:
        print(f"Analizando: {modulo.upper()}...", end=" ")
        
        rutas = buscar_rutas_modulo(app_path, modulo)
        templates = buscar_templates_modulo(templates_path, modulo)
        botones = verificar_botones_template(templates_path, modulo)
        completitud = calcular_completitud(rutas, templates, botones)
        
        resultados.append({
            'modulo': modulo,
            'rutas': rutas,
            'templates': templates,
            'botones': botones,
            'completitud': completitud
        })
        
        print(f"{completitud}%")
    
    print()
    print("=" * 80)
    print("RESUMEN POR CATEGORÍA")
    print("=" * 80)
    print()
    
    # Ordenar por completitud
    resultados.sort(key=lambda x: x['completitud'], reverse=True)
    
    completos = [r for r in resultados if r['completitud'] >= 90]
    casi_completos = [r for r in resultados if 60 <= r['completitud'] < 90]
    incompletos = [r for r in resultados if 30 <= r['completitud'] < 60]
    minimos = [r for r in resultados if r['completitud'] < 30]
    
    print(f"🟢 COMPLETOS (≥90%): {len(completos)}")
    for r in completos:
        print(f"   ✅ {r['modulo'].capitalize()}: {r['completitud']}%")
    
    print()
    print(f"🟡 CASI COMPLETOS (60-89%): {len(casi_completos)}")
    for r in casi_completos:
        faltantes = []
        if not all(r['rutas'].values()):
            faltantes.append("rutas")
        if not all(r['templates'].values()):
            faltantes.append("templates")
        if not all(r['botones'].values()):
            faltantes.append("botones")
        print(f"   ⚠️  {r['modulo'].capitalize()}: {r['completitud']}% - Falta: {', '.join(faltantes)}")
    
    print()
    print(f"🟠 INCOMPLETOS (30-59%): {len(incompletos)}")
    for r in incompletos:
        print(f"   🔸 {r['modulo'].capitalize()}: {r['completitud']}%")
    
    print()
    print(f"🔴 MÍNIMOS (<30%): {len(minimos)}")
    for r in minimos:
        print(f"   ❌ {r['modulo'].capitalize()}: {r['completitud']}%")
    
    print()
    print("=" * 80)
    print("DETALLE POR MÓDULO")
    print("=" * 80)
    print()
    
    for r in resultados:
        if r['completitud'] < 90:  # Solo mostrar detalles de los incompletos
            print(f"\n📋 {r['modulo'].upper()} - {r['completitud']}%")
            print("-" * 40)
            
            print("  Rutas:")
            for ruta, estado in r['rutas'].items():
                icono = "✅" if estado else "❌"
                print(f"    {icono} {ruta}")
            
            print("  Templates:")
            for template, estado in r['templates'].items():
                icono = "✅" if estado else "❌"
                print(f"    {icono} {template}")
            
            print("  Botones en Listar:")
            for boton, estado in r['botones'].items():
                icono = "✅" if estado else "❌"
                print(f"    {icono} {boton}")
    
    print()
    print("=" * 80)
    print("PLAN DE ACCIÓN RECOMENDADO")
    print("=" * 80)
    print()
    
    if casi_completos:
        print("1️⃣ PRIORIDAD ALTA - Completar módulos casi listos:")
        for r in casi_completos[:5]:  # Top 5
            print(f"   • {r['modulo'].capitalize()}")
    
    if incompletos:
        print()
        print("2️⃣ PRIORIDAD MEDIA - Implementar módulos parciales:")
        for r in incompletos[:5]:  # Top 5
            print(f"   • {r['modulo'].capitalize()}")
    
    if minimos:
        print()
        print("3️⃣ PRIORIDAD BAJA - Construir desde cero:")
        for r in minimos[:5]:  # Top 5
            print(f"   • {r['modulo'].capitalize()}")
    
    print()
    print("=" * 80)

if __name__ == '__main__':
    main()
