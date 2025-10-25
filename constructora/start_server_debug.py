#!/usr/bin/env python3
"""
Script para verificar problemas de inicio del servidor
"""

import sys
sys.path.insert(0, '.')

try:
    print("Intentando importar app...")
    from app import app
    print("✓ App importada exitosamente")
    
    print("Verificando configuración...")
    print(f"  Debug mode: {app.config.get('DEBUG', False)}")
    print(f"  Secret key configurado: {'SECRET_KEY' in app.config}")
    
    print("Verificando rutas de materiales...")
    for rule in app.url_map.iter_rules():
        if 'material' in rule.rule.lower():
            print(f"  {rule.rule} -> {rule.endpoint}")
    
    print("\nIntentando iniciar servidor...")
    print("Nota: Presiona Ctrl+C para detener")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
    
except ImportError as e:
    print(f"✗ Error de importación: {e}")
    import traceback
    traceback.print_exc()
    
except Exception as e:
    print(f"✗ Error general: {e}")
    import traceback
    traceback.print_exc()