import os
import re
from pathlib import Path

# Función para analizar un template
def analizar_template(ruta_template):
    """Analiza un template y extrae información sobre su estructura"""
    try:
        with open(ruta_template, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        resultado = {
            'archivo': ruta_template,
            'extends_base': 'extends "base.html"' in contenido,
            'tiene_page_header': 'page-header' in contenido,
            'tiene_breadcrumb': 'breadcrumb' in contenido,
            'tiene_page_title': 'page-title' in contenido,
            'tiene_stats_grid': 'stats-grid' in contenido,
            'tiene_create_form_container': 'create-form-container' in contenido,
            'usa_create_forms_css': 'create-forms.css' in contenido,
            'usa_table_styles_css': 'table-styles.css' in contenido,
            'tiene_form_card': 'form-card' in contenido or 'create-form-card' in contenido,
            'tiene_btn_primary': 'btn btn-primary' in contenido,
            'tiene_iconos_fa': 'fas fa-' in contenido,
            'estructura_tabla': 'data-table' in contenido or 'table' in contenido,
        }
        
        return resultado
        
    except Exception as e:
        print(f"Error analizando {ruta_template}: {e}")
        return None

# Directorio base de templates
base_dir = Path("C:/Users/VICTUS/Videos/BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)/BASE-DE-DATOS-1-PROYECTO-FINAL-master/constructora/templates")

# Módulos a analizar
modulos = [
    'obras', 'proyectos', 'empleados', 'materiales', 'proveedores',
    'vehiculos', 'equipos', 'contratos', 'trabajos', 'actividades',
    'areas', 'bitacoras', 'incidentes', 'avances', 'presupuestos',
    'usuarios', 'auditorias', 'bodegas', 'movimientos', 'requisiciones'
]

# Tipos de páginas a verificar
tipos_paginas = ['listar.html', 'crear.html', 'editar.html', 'detalle.html']

print("🔍 ANÁLISIS DE CONSISTENCIA VISUAL DE MÓDULOS")
print("=" * 80)
print()

resultados = {}
problemas_encontrados = []

for modulo in modulos:
    modulo_dir = base_dir / modulo
    if not modulo_dir.exists():
        print(f"⚠️  Módulo {modulo} no existe")
        continue
    
    print(f"📁 Analizando módulo: {modulo.upper()}")
    resultados[modulo] = {}
    
    for tipo_pagina in tipos_paginas:
        archivo_template = modulo_dir / tipo_pagina
        if archivo_template.exists():
            resultado = analizar_template(archivo_template)
            if resultado:
                resultados[modulo][tipo_pagina] = resultado
                
                # Verificar consistencia
                if not resultado['extends_base']:
                    problemas_encontrados.append(f"{modulo}/{tipo_pagina}: No extiende base.html")
                
                if tipo_pagina == 'listar.html':
                    if not resultado['tiene_page_header']:
                        problemas_encontrados.append(f"{modulo}/{tipo_pagina}: Falta page-header")
                    if not resultado['tiene_stats_grid']:
                        problemas_encontrados.append(f"{modulo}/{tipo_pagina}: Falta stats-grid")
                
                if tipo_pagina in ['crear.html', 'editar.html']:
                    if not resultado['usa_create_forms_css']:
                        problemas_encontrados.append(f"{modulo}/{tipo_pagina}: No usa create-forms.css")
                    if not resultado['tiene_create_form_container']:
                        problemas_encontrados.append(f"{modulo}/{tipo_pagina}: Falta create-form-container")
                
                print(f"  ✅ {tipo_pagina}")
            else:
                print(f"  ❌ Error analizando {tipo_pagina}")
        else:
            print(f"  ⚠️  {tipo_pagina} no existe")
    
    print()

# Generar reporte de consistencia
print("📊 REPORTE DE CONSISTENCIA")
print("=" * 50)

if not problemas_encontrados:
    print("🎉 ¡PERFECTO! Todos los módulos siguen el mismo patrón visual")
else:
    print(f"⚠️  Se encontraron {len(problemas_encontrados)} inconsistencias:")
    print()
    
    for problema in problemas_encontrados:
        print(f"  • {problema}")

print()
print("📈 ESTADÍSTICAS GENERALES")
print("-" * 30)

total_templates = sum(len(modulos_data) for modulos_data in resultados.values())
templates_con_base = sum(1 for modulo_data in resultados.values() 
                        for template_data in modulo_data.values() 
                        if template_data.get('extends_base', False))

templates_con_iconos = sum(1 for modulo_data in resultados.values() 
                          for template_data in modulo_data.values() 
                          if template_data.get('tiene_iconos_fa', False))

print(f"Total de templates analizados: {total_templates}")
print(f"Templates que extienden base.html: {templates_con_base}/{total_templates}")
print(f"Templates con iconos FontAwesome: {templates_con_iconos}/{total_templates}")

# Verificar módulos específicos que podrían necesitar actualización
print()
print("🎯 MÓDULOS QUE NECESITAN REVISIÓN")
print("-" * 35)

modulos_necesitan_revision = []
for modulo, templates in resultados.items():
    problemas_modulo = [p for p in problemas_encontrados if p.startswith(modulo)]
    if problemas_modulo:
        modulos_necesitan_revision.append((modulo, len(problemas_modulo)))

if modulos_necesitan_revision:
    modulos_necesitan_revision.sort(key=lambda x: x[1], reverse=True)
    for modulo, num_problemas in modulos_necesitan_revision:
        print(f"  📝 {modulo}: {num_problemas} problemas")
else:
    print("  ✅ Ningún módulo necesita revisión mayor")

print()
print("💡 RECOMENDACIONES:")
print("-" * 20)
print("  1. Todos los templates deben extender 'base.html'")
print("  2. Páginas de listado deben tener 'page-header' y 'stats-grid'")
print("  3. Formularios deben usar 'create-forms.css' y 'create-form-container'")
print("  4. Mantener consistencia en iconos FontAwesome")
print("  5. Usar clases CSS estándar: 'btn btn-primary', 'form-control', etc.")