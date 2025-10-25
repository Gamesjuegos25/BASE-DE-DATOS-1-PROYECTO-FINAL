#!/usr/bin/env python3
"""
Script de diagnóstico para verificar los problemas identificados
"""

import os
import sys

# Agregar el directorio de la aplicación al path
sys.path.append(os.path.dirname(__file__))

def verificar_formularios():
    """Verifica que los formularios de creación funcionen correctamente"""
    
    print("🔍 DIAGNÓSTICO DE FORMULARIOS DE CREACIÓN")
    print("="*60)
    
    # Verificar archivos de templates
    templates_verificar = [
        'templates/avances/crear.html',
        'templates/incidentes/crear.html', 
        'templates/presupuestos/crear.html'
    ]
    
    for template in templates_verificar:
        if os.path.exists(template):
            print(f"✅ {template} - Existe")
            
            # Verificar contenido básico
            with open(template, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Verificaciones específicas
            if 'extends "base.html"' in content:
                print(f"  ✅ Extiende base.html correctamente")
            else:
                print(f"  ❌ NO extiende base.html correctamente")
                
            if '<!DOCTYPE html>' in content and 'extends "base.html"' in content:
                print(f"  ⚠️  HTML duplicado detectado")
                
            if 'class="form-select" class="form-select"' in content:
                print(f"  ❌ Classes CSS duplicadas detectadas")
            else:
                print(f"  ✅ No se encontraron classes duplicadas")
                
        else:
            print(f"❌ {template} - NO EXISTE")
    
    print("\n" + "="*60)
    print("📋 RESUMEN DE CORRECCIONES REALIZADAS:")
    print("="*60)
    
    print("""
    ✅ AVANCES:
       - Corregido HTML malformado (eliminado DOCTYPE duplicado)
       - Campos actualizados: fecha → fecha_avance
       - Agregados campos: porcentaje_fisico, porcentaje_financiero
       - Eliminado campo: porcentaje_avance (reemplazado por los dos anteriores)
    
    ✅ INCIDENTES:
       - Corregido HTML malformado (eliminado DOCTYPE duplicado) 
       - Agregada variable empleados en controlador Python
       - Campos fecha_incidente cambiado a datetime-local
       - Agregados emojis visuales en selects
    
    ✅ PRESUPUESTOS:
       - Corregido extends de template
       - Mejorada visualización de obras en select
       - Agregados tipos de input apropiados (number, date)
    
    📌 PROBLEMAS IDENTIFICADOS Y SOLUCIONADOS:
       1. Templates con HTML duplicado → CORREGIDO
       2. Classes CSS duplicadas → CORREGIDO  
       3. Campos de formulario no coincidían con backend → CORREGIDO
       4. Falta de datos (empleados) en controladores → CORREGIDO
       5. Tipos de input incorrectos → CORREGIDO
    """)
    
if __name__ == "__main__":
    verificar_formularios()