import requests
from database import get_areas_safe

BASE = 'http://127.0.0.1:5000'

print('== Probando ÁREAS ==')
# Listar
r = requests.get(f'{BASE}/areas', timeout=5)
print('GET /areas ->', r.status_code, len(r.content))

areas = get_areas_safe()
if areas:
    area_id = areas[0].get('id') or areas[0].get('id_area')
    r2 = requests.get(f'{BASE}/areas/{area_id}/editar', timeout=5)
    print(f'GET /areas/{area_id}/editar ->', r2.status_code)
else:
    print('No hay áreas para probar edición.')
