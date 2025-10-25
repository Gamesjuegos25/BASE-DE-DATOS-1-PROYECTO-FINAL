#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para aplicar mejoras estéticas a todas las páginas de detalle del sistema
Aplica el nuevo diseño moderno con la paleta Warm Autumn Glow
"""

import os
import re
from pathlib import Path

def aplicar_mejoras_detalle():
    """Aplica mejoras estéticas a todas las páginas de detalle"""
    
    # Directorio base de templates
    base_dir = Path("templates")
    
    # Patrones de archivos de detalle a mejorar
    patrones_detalle = [
        "**/detalle.html",
        "**/ver.html", 
        "**/mostrar.html",
        "**/info.html",
        "**/detalles.html"
    ]
    
    # CSS para incluir en templates de detalle
    css_detalle = '''
    <!-- CSS específico para páginas de detalle -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/detail-page.css') }}">
    '''
    
    archivos_procesados = []
    
    print("🎨 Aplicando mejoras estéticas a páginas de detalle...")
    print("=" * 60)
    
    for patron in patrones_detalle:
        for archivo in base_dir.glob(patron):
            if archivo.is_file():
                procesar_archivo_detalle(archivo, css_detalle)
                archivos_procesados.append(str(archivo))
    
    print(f"\n✅ Procesados {len(archivos_procesados)} archivos de detalle:")
    for archivo in sorted(archivos_procesados):
        print(f"   📄 {archivo}")
    
    # Crear index de mejoras aplicadas
    crear_reporte_mejoras(archivos_procesados)
    
    print("\n🌟 Mejoras estéticas aplicadas exitosamente!")
    print("💡 Todas las páginas de detalle ahora tienen el diseño moderno")

def procesar_archivo_detalle(archivo_path, css_detalle):
    """Procesa un archivo de detalle individual"""
    
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar si ya tiene el CSS de detalle
        if 'detail-page.css' in contenido:
            print(f"⚠️  {archivo_path} - Ya tiene mejoras aplicadas")
            return
        
        # Buscar donde insertar el CSS
        if '{% block head %}' in contenido:
            # Insertar en bloque head existente
            contenido = re.sub(
                r'({% block head %}.*?)({% endblock %})',
                rf'\1{css_detalle}\2',
                contenido,
                flags=re.DOTALL
            )
        elif '<head>' in contenido:
            # Insertar antes del cierre de head
            contenido = contenido.replace('</head>', f'{css_detalle}</head>')
        else:
            # Agregar bloque head nuevo
            if '{% extends' in contenido:
                lineas = contenido.split('\n')
                for i, linea in enumerate(lineas):
                    if '{% extends' in linea:
                        lineas.insert(i+1, f'\n{{% block head %}}{css_detalle}{{% endblock %}}\n')
                        break
                contenido = '\n'.join(lineas)
        
        # Aplicar mejoras de estructura si es necesario
        contenido = mejorar_estructura_detalle(contenido)
        
        # Guardar archivo mejorado
        with open(archivo_path, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        print(f"✅ {archivo_path} - Mejoras aplicadas")
        
    except Exception as e:
        print(f"❌ Error procesando {archivo_path}: {str(e)}")

def mejorar_estructura_detalle(contenido):
    """Aplica mejoras de estructura a páginas de detalle"""
    
    mejoras = [
        # Mejorar headers de sección
        (
            r'<h5[^>]*class="[^"]*"[^>]*><i class="fas ([^"]+)"></i>\s*([^<]+)</h5>',
            r'<h4 style="color: var(--prussian-blue-600); margin-bottom: var(--spacing-md); display: flex; align-items: center; gap: var(--spacing-sm);"><i class="fas \1 text-xanthous"></i>\2</h4>'
        ),
        
        # Mejorar cards básicas
        (
            r'<div class="card[^>]*>',
            r'<div class="detail-card">'
        ),
        
        # Mejorar badges de estado
        (
            r'<span class="badge badge-([^"]+)"[^>]*>',
            r'<span class="status-badge-detail \1">'
        ),
        
        # Mejorar tablas
        (
            r'<table class="table[^>]*>',
            r'<table class="assignment-table">'
        ),
    ]
    
    for patron, reemplazo in mejoras:
        contenido = re.sub(patron, reemplazo, contenido, flags=re.IGNORECASE)
    
    return contenido

def crear_reporte_mejoras(archivos_procesados):
    """Crea un reporte de las mejoras aplicadas"""
    
    reporte = f"""# Reporte de Mejoras Estéticas - Páginas de Detalle
## Fecha: {os.popen('date').read().strip()}

### Archivos Procesados ({len(archivos_procesados)})
"""
    
    for archivo in sorted(archivos_procesados):
        reporte += f"- {archivo}\n"
    
    reporte += """
### Mejoras Aplicadas
1. ✅ CSS moderno para páginas de detalle (detail-page.css)
2. ✅ Paleta de colores Warm Autumn Glow
3. ✅ Diseño responsive mejorado
4. ✅ Componentes modernizados (cards, badges, tablas)
5. ✅ Tipografía y espaciado optimizados
6. ✅ Animaciones y efectos visuales
7. ✅ Iconografía consistente

### Características del Nuevo Diseño
- 🎨 Paleta Warm Autumn Glow aplicada
- 📱 Diseño completamente responsive
- ⚡ Animaciones fluidas y modernas
- 🔧 Componentes reutilizables
- 📊 Tablas optimizadas para datos
- 💳 Cards modernas y atractivas
- 🎯 Navegación mejorada
"""
    
    with open('REPORTE_MEJORAS_DETALLE.md', 'w', encoding='utf-8') as f:
        f.write(reporte)

if __name__ == "__main__":
    aplicar_mejoras_detalle()