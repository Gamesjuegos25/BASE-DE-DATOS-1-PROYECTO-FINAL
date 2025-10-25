#!/usr/bin/env python3
"""
Servidor simplificado para probar materiales
"""

import sys
sys.path.insert(0, '.')

from flask import Flask, render_template
from database import get_materiales_safe, get_material_by_id_safe

# Crear app Flask simple
simple_app = Flask(__name__)
simple_app.secret_key = 'test_key_123'

@simple_app.route('/')
def home():
    return '<h1>Servidor de Test - Materiales</h1><a href="/materiales">Ver Materiales</a>'

@simple_app.route('/materiales')
def listar_materiales():
    materiales = get_materiales_safe()
    return render_template('materiales/listar_modern.html', materiales=materiales)

@simple_app.route('/materiales/<int:id>')
def ver_material(id):
    material = get_material_by_id_safe(id)
    if material:
        return render_template('materiales/detalle.html', material=material)
    else:
        return f'Material {id} no encontrado'

if __name__ == '__main__':
    print("=== SERVIDOR SIMPLIFICADO DE MATERIALES ===")
    print("🚀 Iniciando en http://127.0.0.1:5000")
    print("📋 Rutas disponibles:")
    print("   / - Inicio")
    print("   /materiales - Lista de materiales")
    print("   /materiales/1 - Detalle material ID 1")
    print("   /materiales/2 - Detalle material ID 2")
    print("   etc...")
    print("\nPresiona Ctrl+C para detener")
    
    simple_app.run(debug=True, host='127.0.0.1', port=5000)