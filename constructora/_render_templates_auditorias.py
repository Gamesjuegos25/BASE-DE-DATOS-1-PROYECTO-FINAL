from flask import Flask, render_template
import os, sys

base = r"c:\\Users\\VICTUS\\Videos\\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\\BASE-DE-DATOS-1-PROYECTO-FINAL-master\\constructora"
sys.path.insert(0, base)
import app as app_module
app: Flask = app_module.app

sample_auditoria = {
    'id_auditoria': 1,
    'id': 1,
    'accion_auditoria': 'LOGIN_EXITOSO',
    'fecha_auditoria': '2025-01-20 10:30:45',
    'detalle_auditoria': 'Usuario admin accedió al sistema desde IP 192.168.1.100',
    'nombre_usuario': 'admin',
    'id_usuario': 5,
    'email_usuario': 'admin@constructora.com'
}

sample_auditorias = [
    sample_auditoria,
    {
        'id_auditoria': 2,
        'id': 2,
        'accion_auditoria': 'CREAR_OBRA',
        'fecha_auditoria': '2025-01-20 11:15:20',
        'detalle_auditoria': 'Creó obra: Construcción Plaza Central con valor $500000',
        'nombre_usuario': 'ingeniero1',
        'id_usuario': 8,
    },
    {
        'id_auditoria': 3,
        'id': 3,
        'accion_auditoria': 'ELIMINAR_MATERIAL',
        'fecha_auditoria': '2025-01-20 14:45:00',
        'detalle_auditoria': None,
        'nombre_usuario': None,
        'id_usuario': None,
    }
]

with app.app_context():
    with app.test_request_context('/'):
        pages = [
            ('auditorias/listar.html', {'auditorias': sample_auditorias}),
            ('auditorias/detalle.html', {'auditoria': sample_auditoria}),
        ]
        for tpl, kwargs in pages:
            html = render_template(tpl, **kwargs)
            print(tpl, 'OK', len(html))
