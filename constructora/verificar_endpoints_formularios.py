#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar y corregir todos los endpoints en los formularios de creación
"""
import os
import re
import glob

def extraer_endpoints_app():
    """Extrae todos los endpoints de crear del archivo app.py"""
    endpoints = {}
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar todas las funciones que manejan creación
        patron = r'@app\.route\([\'"]([^\'\"]*)[\'"].*methods.*POST.*\)\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        matches = re.findall(patron, contenido, re.MULTILINE | re.DOTALL)
        
        for ruta, funcion in matches:
            if 'nuevo' in ruta or 'crear' in funcion:
                modulo = ruta.split('/')[1] if '/' in ruta else ruta
                endpoints[modulo] = funcion
                
        print("📋 Endpoints de creación encontrados en app.py:")
        for modulo, funcion in sorted(endpoints.items()):
            print(f"   {modulo:20} -> {funcion}")
            
        return endpoints
        
    except Exception as e:
        print(f"❌ Error al leer app.py: {e}")
        return {}

def verificar_templates():
    """Verifica todos los templates de crear.html"""
    print("\n🔍 Verificando templates de creación...")
    print("=" * 60)
    
    crear_files = glob.glob("templates/*/crear.html")
    problemas = []
    
    for archivo in crear_files:
        modulo = archivo.replace("\\", "/").split("/")[-2]
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Buscar url_for específicamente en el action del formulario
            patron_form = r"<form[^>]*action\s*=\s*['\"]{{[^}]*url_for\s*\(\s*['\"]([^'\"]+)['\"]\s*\)[^}]*}}['\"]"
            matches = re.findall(patron_form, contenido, re.IGNORECASE)
            
            endpoint_usado = None
            if matches:
                endpoint_usado = matches[0]  # Tomar el primer (y probablemente único) endpoint del form
            
            if endpoint_usado:
                print(f"   {modulo:20} usa endpoint: {endpoint_usado}")
            else:
                print(f"⚠️  {modulo:20} - No se encontró endpoint de creación")
                problemas.append((modulo, archivo, "sin_endpoint"))
                
        except Exception as e:
            print(f"❌ {modulo:20} - Error: {e}")
            problemas.append((modulo, archivo, f"error: {e}"))
    
    return problemas

def corregir_endpoints():
    """Corrige los endpoints incorrectos basándose en los endpoints reales"""
    
    # Mapeo de correcciones conocidas
    correcciones = {
        'crear_requisicione': 'crear_requisicion',
        'crear_tipos_obra': 'tipos_obra_nuevo',
        'crear_actividade': 'crear_actividad'
    }
    
    print("\n🔧 Aplicando correcciones de endpoints...")
    print("=" * 60)
    
    crear_files = glob.glob("templates/*/crear.html")
    corregidos = 0
    
    for archivo in crear_files:
        modulo = archivo.replace("\\", "/").split("/")[-2]
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            contenido_original = contenido
            
            # Aplicar correcciones
            for incorrecto, correcto in correcciones.items():
                if incorrecto in contenido:
                    contenido = contenido.replace(f"url_for('{incorrecto}')", f"url_for('{correcto}')")
                    print(f"   ✅ {modulo}: {incorrecto} -> {correcto}")
                    corregidos += 1
            
            # Guardar si hubo cambios
            if contenido != contenido_original:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                    
        except Exception as e:
            print(f"   ❌ Error en {modulo}: {e}")
    
    print(f"\n📊 Total de correcciones aplicadas: {corregidos}")

def main():
    """Función principal"""
    print("🚀 Verificando y corrigiendo endpoints en formularios...")
    print("=" * 60)
    
    # Extraer endpoints reales
    endpoints_reales = extraer_endpoints_app()
    
    # Verificar templates
    problemas = verificar_templates()
    
    # Corregir endpoints conocidos
    corregir_endpoints()
    
    # Verificar nuevamente después de las correcciones
    print("\n🔍 Verificación final...")
    print("=" * 60)
    verificar_templates()
    
    print("\n✅ Verificación completada")

if __name__ == "__main__":
    main()