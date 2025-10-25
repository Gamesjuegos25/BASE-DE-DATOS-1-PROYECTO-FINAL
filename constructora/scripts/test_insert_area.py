from database import insert_area_safe, get_areas_safe
import json

print('Insertando área de prueba...')
area_id = insert_area_safe('Área de prueba desde script con acentos áéíóú ñ')
print('ID insertado:', area_id)

areas = get_areas_safe()
print('Primeras áreas (max 10):')
print(json.dumps(areas[:10], ensure_ascii=False, indent=2))
