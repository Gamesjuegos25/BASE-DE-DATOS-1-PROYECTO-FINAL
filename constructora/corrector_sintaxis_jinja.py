#!/usr/bin/env python3
"""
CORRECTOR DE SINTAXIS JINJA2
============================
Corrige la sintaxis escapada en templates Jinja2
"""

import os
import re
from pathlib import Path

def corregir_sintaxis_jinja(archivo_path):
    """Corrige sintaxis Jinja2 escapada"""
    try:
        with open(archivo_path, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Contar problemas de sintaxis
        problemas = 0
        
        # Corregir dobles % en bloques Jinja
        patron_doble_porcentaje = r'{%%\s*(.*?)\s*%%}'
        matches = re.findall(patron_doble_porcentaje, contenido)
        if matches:
            problemas += len(matches)
            contenido = re.sub(patron_doble_porcentaje, r'{% \1 %}', contenido)
        
        if problemas > 0:
            print(f"🔧 Corrigiendo: {archivo_path.name} ({problemas} problemas)")
            
            # Hacer backup
            backup_path = f"{archivo_path}.backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(open(archivo_path, 'r', encoding='utf-8').read())
            
            # Guardar archivo corregido
            with open(archivo_path, 'w', encoding='utf-8') as f:
                f.write(contenido)
            
            return True
        else:
            return False
            
    except Exception as e:
        print(f"❌ Error corrigiendo {archivo_path}: {str(e)}")
        return False

def main():
    """Función principal"""
    print("🔧 CORRECTOR DE SINTAXIS JINJA2")
    print("=" * 35)
    
    # Módulos que fueron creados automáticamente
    modulos_generados = [
        'clientes', 'herramientas', 'compras', 
        'ventas', 'pagos', 'nomina', 'auditorias', 'usuarios'
    ]
    
    templates_dir = Path('templates')
    corregidos = 0
    total_procesados = 0
    
    for modulo in modulos_generados:
        modulo_dir = templates_dir / modulo
        if modulo_dir.exists():
            archivos_html = list(modulo_dir.glob('*.html'))
            for archivo in archivos_html:
                total_procesados += 1
                if corregir_sintaxis_jinja(archivo):
                    corregidos += 1
        else:
            print(f"⚠️  Directorio no encontrado: {modulo}")
    
    print(f"\n📊 RESUMEN:")
    print(f"   Templates corregidos: {corregidos}")
    print(f"   Total procesados: {total_procesados}")
    
    if corregidos > 0:
        print(f"\n✅ ¡Corrección de sintaxis completada!")
        print("💡 Los templates ahora tienen sintaxis Jinja2 válida")
    else:
        print(f"\nℹ️  No se encontraron problemas de sintaxis")

if __name__ == "__main__":
    main()