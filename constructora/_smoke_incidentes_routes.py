import os, sys
from flask import Flask

base = r"c:\\Users\\VICTUS\\Videos\\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\\BASE-DE-DATOS-1-PROYECTO-FINAL-master\\constructora"
sys.path.insert(0, base)
import app as app_module
app: Flask = app_module.app
app.testing = True

with app.test_client() as c:
    r = c.get('/incidentes')
    print('/incidentes status:', r.status_code)
    assert r.status_code == 200, 'Listar incidentes debe devolver 200'

    # Detalle inexistente debe redirigir a /incidentes
    r2 = c.get('/incidentes/999999', follow_redirects=True)
    print('/incidentes/999999 follow_redirects status:', r2.status_code)
    assert r2.status_code == 200

print('SMOKE OK')
