import requests
from database import get_avances_safe

BASE='http://127.0.0.1:5000'
print('GET /avances ->', requests.get(f'{BASE}/avances', timeout=5).status_code)

avs = get_avances_safe()
if avs:
    aid = avs[0]['id_avance']
    print('GET detalle ->', requests.get(f'{BASE}/avances/{aid}', timeout=5).status_code)
    print('GET editar ->', requests.get(f'{BASE}/avances/{aid}/editar', timeout=5).status_code)
else:
    print('No hay avances para probar detalle/editar')
