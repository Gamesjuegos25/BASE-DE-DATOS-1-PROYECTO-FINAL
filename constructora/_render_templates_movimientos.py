from flask import Flask, render_template
import os, sys

base = r"c:\\Users\\VICTUS\\Videos\\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\\BASE-DE-DATOS-1-PROYECTO-FINAL-master\\constructora"
sys.path.insert(0, base)
import app as app_module
app: Flask = app_module.app

sample_movimiento = {
    'id_movimiento_material': 1,
    'id': 1,
    'tipo_movimiento': 'Entrada',
    'cantidad': 50,
    'id_material': 5,
    'nombre_material': 'Cemento',
    'fecha_movimiento': '2025-01-15',
    'origen_movimiento': 'Proveedor XYZ',
    'destino_movimiento': 'Bodega Central'
}
sample_materiales = [
    {'id_material': 5, 'nombre': 'Cemento'},
    {'id_material': 6, 'nombre': 'Arena'}
]

with app.app_context():
    with app.test_request_context('/'):
        pages = [
            ('movimientos/listar.html', {'movimientos': [sample_movimiento]}),
            ('movimientos/crear.html', {'materiales': sample_materiales}),
            ('movimientos/detalle.html', {'movimiento': sample_movimiento}),
            ('movimientos/editar.html', {'movimiento': sample_movimiento, 'materiales': sample_materiales}),
        ]
        for tpl, kwargs in pages:
            html = render_template(tpl, **kwargs)
            print(tpl, 'OK', len(html))
