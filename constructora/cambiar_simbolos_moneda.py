#!/usr/bin/env python3
"""
Script para cambiar todos los símbolos de moneda de $ a Q en los templates
"""
import os
import re
import glob

def reemplazar_simbolos_moneda():
    """Reemplaza símbolos $ por Q en templates y cambia iconos fa-dollar-sign"""
    
    # Directorio base de templates
    templates_dir = "templates"
    
    # Contador de cambios
    cambios = 0
    archivos_modificados = 0
    
    # Patrones a reemplazar
    patrones = [
        # Formato de dinero con ${{ }}
        (r'\$\{\{\s*"([^"]*)"\.format\(', r'Q{{ "\1".format('),
        # Formato simple ${{ variable }}
        (r'\$\{\{\s*([^}]+)\s*\}\}', r'Q{{ \1 }}'),
        # Alerta con $${variable}
        (r'Pago de \$\$\{([^}]+)\}', r'Pago de Q${\1}'),
        # Iconos fas fa-dollar-sign
        (r'fas fa-dollar-sign', r'fas fa-coins'),
        # Navegación con icono dollar
        (r'<i class="nav-icon fas fa-dollar-sign"></i>', r'<i class="nav-icon fas fa-coins"></i>'),
    ]
    
    # Buscar todos los archivos HTML en templates
    patron_archivos = os.path.join(templates_dir, "**", "*.html")
    archivos = glob.glob(patron_archivos, recursive=True)
    
    print(f"🔍 Encontrados {len(archivos)} archivos HTML en templates/")
    
    for archivo in archivos:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                contenido_original = contenido
            
            # Aplicar cada patrón
            for patron, reemplazo in patrones:
                contenido_nuevo = re.sub(patron, reemplazo, contenido)
                if contenido_nuevo != contenido:
                    matches = len(re.findall(patron, contenido))
                    print(f"  📝 {archivo}: {matches} reemplazos de '{patron}' → '{reemplazo}'")
                    cambios += matches
                    contenido = contenido_nuevo
            
            # Solo escribir si hubo cambios
            if contenido != contenido_original:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                archivos_modificados += 1
                print(f"  ✅ Actualizado: {archivo}")
                
        except Exception as e:
            print(f"  ❌ Error procesando {archivo}: {e}")
    
    print(f"\n🎉 Proceso completado:")
    print(f"  📊 Total cambios: {cambios}")
    print(f"  📁 Archivos modificados: {archivos_modificados}")
    
    # Casos específicos que necesitan revisión manual
    print(f"\n⚠️  REVISAR MANUALMENTE:")
    print(f"  • templates/facturas/listar_modern.html línea 211: alert con $ en pago")
    print(f"  • JavaScript con template literals que usan ${{}} para variables")
    print(f"  • Algunos archivos pueden tener $ en contexto no monetario")

if __name__ == "__main__":
    print("💱 Iniciando conversión de símbolos monetarios $ → Q")
    reemplazar_simbolos_moneda()