"""
Test de renderizado de templates de BODEGAS
"""
import sys
sys.path.insert(0, r'c:\Users\VICTUS\Videos\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\BASE-DE-DATOS-1-PROYECTO-FINAL-master\constructora')

from app import app
from flask import render_template

def test_render_bodegas():
    """Probar renderizado de templates de bodegas"""
    with app.app_context():
        with app.test_request_context('/'):
            # Datos de prueba
            bodegas = [
                {
                    'id_bodega': 1,
                    'responsable_bodega': 'Juan Pérez',
                    'obras_asignadas': 3,
                    'inventarios_asignados': 15
                },
                {
                    'id_bodega': 2,
                    'responsable_bodega': 'María García',
                    'obras_asignadas': 1,
                    'inventarios_asignados': 8
                }
            ]
            
            bodega = {
                'id_bodega': 1,
                'responsable_bodega': 'Juan Pérez',
                'obras_asignadas': 3,
                'inventarios_asignados': 15
            }
            
            obras_asignadas = [
                {
                    'id_obra': 1,
                    'nombre_obra': 'Edificio Central',
                    'ubicacion_obra': 'Centro',
                    'fecha_inicio_obra': None
                }
            ]
            
            obras_sin_bodega = [
                {
                    'id_obra': 2,
                    'nombre_obra': 'Plaza Norte',
                    'ubicacion_obra': 'Norte'
                }
            ]
            
            # Test 1: listar
            try:
                html = render_template('bodegas/listar.html', bodegas=bodegas)
                print(f'✅ bodegas/listar.html OK {len(html)}')
            except Exception as e:
                print(f'❌ bodegas/listar.html ERROR: {e}')
            
            # Test 2: crear
            try:
                html = render_template('bodegas/crear.html')
                print(f'✅ bodegas/crear.html OK {len(html)}')
            except Exception as e:
                print(f'❌ bodegas/crear.html ERROR: {e}')
            
            # Test 3: detalle
            try:
                html = render_template('bodegas/detalle.html', 
                                     bodega=bodega, 
                                     obras_asignadas=obras_asignadas)
                print(f'✅ bodegas/detalle.html OK {len(html)}')
            except Exception as e:
                print(f'❌ bodegas/detalle.html ERROR: {e}')
            
            # Test 4: editar
            try:
                html = render_template('bodegas/editar.html', bodega=bodega)
                print(f'✅ bodegas/editar.html OK {len(html)}')
            except Exception as e:
                print(f'❌ bodegas/editar.html ERROR: {e}')
            
            # Test 5: asignar
            try:
                html = render_template('bodegas/asignar.html',
                                     bodega=bodega,
                                     obras_con_bodega=obras_asignadas,
                                     obras_sin_bodega=obras_sin_bodega)
                print(f'✅ bodegas/asignar.html OK {len(html)}')
            except Exception as e:
                print(f'❌ bodegas/asignar.html ERROR: {e}')

if __name__ == '__main__':
    test_render_bodegas()
