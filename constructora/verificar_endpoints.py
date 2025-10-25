"""
Script para verificar y corregir errores de endpoints en templates
Busca referencias incorrectas a endpoints Flask y las corrige automáticamente
"""

import os
import re
from pathlib import Path

def buscar_errores_endpoints():
    """Busca errores comunes de endpoints en los templates"""
    
    base_dir = Path("C:/Users/VICTUS/Videos/BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)/BASE-DE-DATOS-1-PROYECTO-FINAL-master/constructora")
    templates_dir = base_dir / "templates"
    
    errores_encontrados = []
    
    print("🔍 BUSCANDO ERRORES DE ENDPOINTS EN TEMPLATES")
    print("=" * 50)
    
    # Patrones de errores comunes
    errores_comunes = [
        (r"'crear_actividade'", "'crear_actividad'", "Endpoint incorrecto: crear_actividade"),
        (r'"crear_actividade"', '"crear_actividad"', "Endpoint incorrecto: crear_actividade"),
        (r"'editar_actividade'", "'editar_actividad'", "Endpoint incorrecto: editar_actividade"), 
        (r'"editar_actividade"', '"editar_actividad"', "Endpoint incorrecto: editar_actividade"),
        (r"'ver_actividade'", "'ver_actividad'", "Endpoint incorrecto: ver_actividade"),
        (r'"ver_actividade"', '"ver_actividad"', "Endpoint incorrecto: ver_actividade"),
        (r"'eliminar_actividade'", "'eliminar_actividad'", "Endpoint incorrecto: eliminar_actividade"),
        (r'"eliminar_actividade"', '"eliminar_actividad"', "Endpoint incorrecto: eliminar_actividade"),
    ]
    
    # Buscar en todos los archivos HTML
    for template_file in templates_dir.rglob("*.html"):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            contenido_original = contenido
            cambios_realizados = []
            
            # Verificar cada patrón de error
            for patron_error, correccion, descripcion in errores_comunes:
                if re.search(patron_error, contenido):
                    contenido = re.sub(patron_error, correccion, contenido)
                    cambios_realizados.append(descripcion)
            
            # Si se realizaron cambios, guardar el archivo
            if contenido != contenido_original:
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                ruta_relativa = template_file.relative_to(templates_dir)
                errores_encontrados.append({
                    'archivo': str(ruta_relativa),
                    'cambios': cambios_realizados
                })
                
                print(f"✅ Corregido: {ruta_relativa}")
                for cambio in cambios_realizados:
                    print(f"   • {cambio}")
                
        except Exception as e:
            print(f"❌ Error procesando {template_file}: {e}")
    
    return errores_encontrados

def verificar_endpoints_flask():
    """Verifica que todos los endpoints referenciados existan en app.py"""
    
    base_dir = Path("C:/Users/VICTUS/Videos/BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)/BASE-DE-DATOS-1-PROYECTO-FINAL-master/constructora")
    app_file = base_dir / "app.py"
    templates_dir = base_dir / "templates"
    
    print(f"\n🔎 VERIFICANDO CONSISTENCIA DE ENDPOINTS")
    print("-" * 40)
    
    # Leer app.py para obtener endpoints definidos
    try:
        with open(app_file, 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Extraer nombres de funciones (endpoints) del archivo app.py
        endpoints_definidos = set(re.findall(r'^def ([a-zA-Z_][a-zA-Z0-9_]*)\(', app_content, re.MULTILINE))
        
        print(f"📋 Endpoints encontrados en app.py: {len(endpoints_definidos)}")
        
    except Exception as e:
        print(f"❌ Error leyendo app.py: {e}")
        return []
    
    # Buscar referencias a url_for en templates
    endpoints_referenciados = set()
    problemas = []
    
    for template_file in templates_dir.rglob("*.html"):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Buscar url_for calls
            url_for_matches = re.findall(r"url_for\(['\"]([^'\"]+)['\"]", contenido)
            
            for endpoint in url_for_matches:
                endpoints_referenciados.add(endpoint)
                
                # Verificar si el endpoint existe
                if endpoint not in endpoints_definidos:
                    ruta_relativa = template_file.relative_to(templates_dir)
                    problemas.append({
                        'archivo': str(ruta_relativa),
                        'endpoint_faltante': endpoint,
                        'sugerencia': buscar_endpoint_similar(endpoint, endpoints_definidos)
                    })
        
        except Exception as e:
            print(f"❌ Error procesando {template_file}: {e}")
    
    print(f"📋 Referencias url_for encontradas: {len(endpoints_referenciados)}")
    
    if problemas:
        print(f"\n⚠️  PROBLEMAS ENCONTRADOS: {len(problemas)}")
        for problema in problemas:
            print(f"   📝 {problema['archivo']}")
            print(f"      ❌ Endpoint no encontrado: '{problema['endpoint_faltante']}'")
            if problema['sugerencia']:
                print(f"      💡 ¿Quizás quisiste decir: '{problema['sugerencia']}'?")
    else:
        print("✅ Todos los endpoints referenciados existen")
    
    return problemas

def buscar_endpoint_similar(endpoint_buscado, endpoints_disponibles):
    """Busca un endpoint similar usando distancia de edición simple"""
    from difflib import get_close_matches
    
    matches = get_close_matches(endpoint_buscado, endpoints_disponibles, n=1, cutoff=0.6)
    return matches[0] if matches else None

def main():
    """Función principal"""
    print("🚀 VERIFICADOR Y CORRECTOR DE ENDPOINTS")
    print("=" * 60)
    
    # Fase 1: Corregir errores conocidos
    errores_corregidos = buscar_errores_endpoints()
    
    # Fase 2: Verificar consistencia general
    problemas_restantes = verificar_endpoints_flask()
    
    # Reporte final
    print(f"\n📊 REPORTE FINAL")
    print("=" * 20)
    print(f"✅ Errores corregidos automáticamente: {len(errores_corregidos)}")
    print(f"⚠️  Problemas que requieren revisión manual: {len(problemas_restantes)}")
    
    if errores_corregidos:
        print(f"\n📋 ARCHIVOS CORREGIDOS:")
        for error in errores_corregidos:
            print(f"   • {error['archivo']}")
    
    if problemas_restantes:
        print(f"\n🔧 REQUIEREN REVISIÓN MANUAL:")
        for problema in problemas_restantes:
            print(f"   • {problema['archivo']}: {problema['endpoint_faltante']}")
    
    print(f"\n✅ VERIFICACIÓN COMPLETADA")
    
    if not problemas_restantes:
        print("🎉 ¡Todos los endpoints están correctos!")
    else:
        print("💡 Revisa manualmente los problemas indicados arriba")

if __name__ == "__main__":
    main()