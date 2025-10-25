from flask import Flask, render_template
import os, sys

base = r"c:\\Users\\VICTUS\\Videos\\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\\BASE-DE-DATOS-1-PROYECTO-FINAL-master\\constructora"

# Usar la app real con rutas registradas
sys.path.insert(0, base)
import app as app_module  # importa constructora/app.py
app: Flask = app_module.app

sample_incidente = {
    'id_incidente': 1,
    'id': 1,
    'fecha_incidente': '2025-01-01',
    'estado_incidente': 'Reportado',
    'descripcion_incidente': 'Fuga menor de agua en tubería',
    'id_obra': 10,
    'nombre_obra': 'Obra Demo'
}
sample_obras = [
    {'id_obra': 10, 'nombre_obra': 'Obra Demo'},
    {'id_obra': 11, 'nombre_obra': 'Obra B'}
]

with app.app_context():
    with app.test_request_context('/'):
        pages = [
            ('incidentes/listar.html', {'incidentes': []}),
            ('incidentes/crear.html', {'obras': sample_obras}),
            ('incidentes/detalle.html', {'incidente': sample_incidente}),
            ('incidentes/editar.html', {'incidente': sample_incidente, 'obras': sample_obras}),
        ]
        for tpl, kwargs in pages:
            html = render_template(tpl, **kwargs)
            print(tpl, 'OK', len(html))
