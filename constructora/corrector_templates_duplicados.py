#!/usr/bin/env python3
"""
CORRECTOR DE TEMPLATES DUPLICADOS
==================================
Corrige templates con declaraciones {% extends %} duplicadas
"""

import os
import re
from pathlib import Path

def corregir_template_duplicado(archivo_path):
    """Corrige un template con extends duplicados"""
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar patrones de extends duplicados
        patron_problema = r'({% extends "base\.html" %}.*?{% block head %}.*?{% endblock %})\s*\n\s*\n\s*({%extends "base\.html"%})'
        
        if re.search(patron_problema, contenido, re.DOTALL):
            print(f"🔧 Corrigiendo: {archivo_path}")
            
            # Reemplazar el patrón problemático
            contenido_corregido = re.sub(
                patron_problema,
                r'\1',  # Solo mantener la primera parte
                contenido,
                flags=re.DOTALL
            )
            
            # También corregir bloques de título duplicados
            contenido_corregido = re.sub(
                r'({%block title%}.*?{%endblock%})',
                lambda m: m.group(1).replace('{%block title%}', '{% block title %}').replace('{%endblock%}', '{% endblock %}'),
                contenido_corregido
            )
            
            # Corregir bloques de contenido duplicados
            contenido_corregido = re.sub(
                r'({%block content%})',
                '{% block content %}',
                contenido_corregido
            )
            
            # Corregir bloques de cierre
            contenido_corregido = re.sub(
                r'({%endblock%})',
                '{% endblock %}',
                contenido_corregido
            )
            
            # Hacer backup
            backup_path = f"{archivo_path}.backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            # Guardar archivo corregido
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(contenido_corregido)
            
            print(f"✅ Corregido: {os.path.basename(archivo_path)}")
            return True
        else:
            print(f"ℹ️  No necesita corrección: {os.path.basename(archivo_path)}")
            return False
            
    except Exception as e:
        print(f"❌ Error corrigiendo {archivo_path}: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🔧 CORRECTOR DE TEMPLATES CON EXTENDS DUPLICADOS")
    print("=" * 50)
    
    # Archivos identificados con problemas
    archivos_problematicos = [
        'templates/bitacoras/crear.html',
        'templates/contratos/crear.html', 
        'templates/requisiciones/crear.html',
        'templates/trabajos/crear.html',
        'templates/usuarios/crear.html'
    ]
    
    corregidos = 0
    
    for archivo_rel in archivos_problematicos:
        archivo_path = Path(archivo_rel)
        if archivo_path.exists():
            if corregir_template_duplicado(archivo_path):
                corregidos += 1
        else:
            print(f"⚠️  Archivo no encontrado: {archivo_rel}")
    
    print(f"\n📊 RESUMEN:")
    print(f"   Templates corregidos: {corregidos}")
    print(f"   Total procesados: {len(archivos_problematicos)}")
    
    if corregidos > 0:
        print(f"\n✅ ¡Corrección completada!")
        print("💡 Reinicia el servidor Flask para aplicar los cambios")
    else:
        print(f"\nℹ️  No se encontraron templates que necesiten corrección")

if __name__ == "__main__":
    main()