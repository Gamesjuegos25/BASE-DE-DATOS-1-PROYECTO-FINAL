import os, sys

base = r"c:\\Users\\VICTUS\\Videos\\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\\BASE-DE-DATOS-1-PROYECTO-FINAL-master\\constructora"
sys.path.insert(0, base)
import app as app_module
from flask import Flask

app: Flask = app_module.app
app.testing = True

print('=== PRUEBA DE MOVIMIENTOS DE MATERIALES ===')

with app.test_client() as c:
    # Test listar
    r = c.get('/movimientos')
    print(f'/movimientos status: {r.status_code}')
    assert r.status_code == 200, 'Listar movimientos debe retornar 200'
    
    # Test crear GET
    r2 = c.get('/movimientos/nuevo')
    print(f'/movimientos/nuevo GET status: {r2.status_code}')
    assert r2.status_code == 200, 'Formulario crear debe retornar 200'
    
    # Test detalle inexistente (debe redirigir)
    r3 = c.get('/movimientos/999999', follow_redirects=True)
    print(f'/movimientos/999999 (con redirect) status: {r3.status_code}')
    assert r3.status_code == 200

print('\n✅ SMOKE TEST OK - Módulo MOVIMIENTOS DE MATERIALES')
