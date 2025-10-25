#!/usr/bin/env python3
"""
VERIFICADOR FINAL DE TEMPLATES
==============================
Verifica que todos los templates estén libres de errores
"""

import os
import re
from pathlib import Path

def verificar_template(archivo_path):
    """Verifica que un template esté libre de errores comunes"""
    errores = []
    
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # 1. Verificar múltiples extends
        extends_matches = re.findall(r'{%\s*extends', contenido)
        if len(extends_matches) > 1:
            errores.append(f"Múltiples declaraciones extends: {len(extends_matches)}")
        
        # 2. Verificar sintaxis de bloques
        bloques_mal_formados = re.findall(r'{%\w+', contenido)
        for bloque in bloques_mal_formados:
            if not re.match(r'{% \w+', bloque):
                errores.append(f"Bloque mal formado: {bloque}")
        
        # 3. Verificar que tenga extends
        if not re.search(r'{% extends', contenido):
            errores.append("Sin declaración extends")
        
        # 4. Verificar estructura básica
        if not re.search(r'{% block content %}', contenido):
            errores.append("Sin bloque content")
            
        if not re.search(r'{% endblock %}', contenido):
            errores.append("Sin cierre de bloque endblock")
        
        return errores
        
    except Exception as e:
        return [f"Error leyendo archivo: {str(e)}"]

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN FINAL DE TEMPLATES")
    print("=" * 40)
    
    templates_dir = Path('templates')
    archivos_html = list(templates_dir.rglob('*.html'))
    
    templates_ok = 0
    templates_con_errores = 0
    
    # Excluir archivos especiales
    archivos_excluir = ['base.html', 'dashboard.html', 'sistema_completo.html']
    
    for archivo in archivos_html:
        if archivo.name in archivos_excluir:
            continue
            
        errores = verificar_template(archivo)
        
        if errores:
            templates_con_errores += 1
            print(f"❌ {archivo.relative_to(templates_dir)}")
            for error in errores:
                print(f"   • {error}")
        else:
            templates_ok += 1
            print(f"✅ {archivo.relative_to(templates_dir)}")
    
    print(f"\n📊 RESUMEN FINAL:")
    print(f"   Templates correctos: {templates_ok}")
    print(f"   Templates con errores: {templates_con_errores}")
    print(f"   Total verificados: {templates_ok + templates_con_errores}")
    
    porcentaje_ok = (templates_ok / (templates_ok + templates_con_errores)) * 100 if (templates_ok + templates_con_errores) > 0 else 0
    print(f"   Porcentaje de éxito: {porcentaje_ok:.1f}%")
    
    if templates_con_errores == 0:
        print(f"\n🎉 ¡TODOS LOS TEMPLATES ESTÁN CORRECTOS!")
        print("✅ Sistema listo para uso")
    else:
        print(f"\n⚠️  Se encontraron {templates_con_errores} templates con errores")
        print("💡 Revisar y corregir antes de usar")

if __name__ == "__main__":
    main()