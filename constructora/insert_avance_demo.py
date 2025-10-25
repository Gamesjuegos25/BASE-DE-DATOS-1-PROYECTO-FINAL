from database import get_obras_safe, insert_avance_safe, get_avance_by_id_safe
from datetime import date

print('== Insertando avance de prueba ==')
obras = get_obras_safe()
obra_id = None
if obras:
    # Tomar la primera obra disponible (intenta id_obra, luego id)
    o0 = obras[0]
    obra_id = o0.get('id_obra') or o0.get('id')
    print(f'Usando obra_id={obra_id}')
else:
    print('No hay obras disponibles; se insertará avance sin obra asociada')

avance_id = insert_avance_safe(
    porcentaje_fisico=12.5,
    porcentaje_financiero=9.0,
    fecha_avance=date.today().isoformat(),
    obra_id=obra_id
)
print('Nuevo id_avance =', avance_id)

if avance_id:
    a = get_avance_by_id_safe(avance_id)
    print('Detalle avance:', a)
else:
    print('No se pudo insertar el avance de prueba')
