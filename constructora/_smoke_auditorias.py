import os, sys

base = r"c:\\Users\\VICTUS\\Videos\\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\\BASE-DE-DATOS-1-PROYECTO-FINAL-master\\constructora"
sys.path.insert(0, base)
import app as app_module
from flask import Flask

app: Flask = app_module.app
app.testing = True

print('=== PRUEBA DE AUDITORÍAS ===')

with app.test_client() as c:
    # Test listar
    r = c.get('/auditorias')
    print(f'/auditorias status: {r.status_code}')
    assert r.status_code == 200, 'Listar auditorías debe retornar 200'
    
    # Test detalle inexistente (debe redirigir)
    r2 = c.get('/auditorias/999999', follow_redirects=True)
    print(f'/auditorias/999999 (con redirect) status: {r2.status_code}')
    assert r2.status_code == 200

print('\n✅ SMOKE TEST OK - Módulo AUDITORÍAS')
