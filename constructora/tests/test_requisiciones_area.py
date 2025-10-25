import os
import sys
import pytest

# Permitir imports de la carpeta constructora al ejecutar pytest
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from database import (
    insert_area_safe, get_requisiciones_for_area, remove_requisicion_from_area, get_connection
)

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


def test_assign_and_unassign_single_requisicion_via_endpoints(client):
    area_id = insert_area_safe('Área req single')
    assert area_id

    # Crear requisición mínima: si no existe helper, insertar por SQL usando get_connection
    try:
        # Intentar usar una función pública si existe
        from database import insert_requisicion_safe as _ins_req
        req_id = _ins_req(fecha=None, estado='Pendiente')
    except Exception:
        # Insertar directamente vía SQL
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO REQUISICIONES (fecha_requisicion, estado_requisicion) VALUES (CURRENT_DATE, %s) RETURNING id_requisicion", ('Pendiente',))
                    req_id = cursor.fetchone()[0]
                    conn.commit()
        except Exception:
            pytest.skip('No se pudo crear requisicion en la BD')

    # asignar vía endpoint
    resp = client.post(f'/areas/{area_id}/asignar/requisicion', data={'requisicion_id': str(req_id)})
    assert resp.status_code == 200
    j = resp.get_json()
    assert j.get('success') is True

    reqs = get_requisiciones_for_area(area_id)
    assert any(r['id'] == req_id for r in reqs)

    # desasignar
    resp2 = client.post(f'/areas/{area_id}/desasignar/requisicion', data={'requisicion_id': str(req_id)})
    assert resp2.status_code == 200
    j2 = resp2.get_json()
    assert j2.get('success') is True

    # limpiar
    try:
        remove_requisicion_from_area(area_id, req_id)
    except Exception:
        pass


def test_assign_multiple_requisiciones_and_handle_invalids(client):
    area_id = insert_area_safe('Área req multi')
    assert area_id

    # Crear tres requisiciones (usar helper si existe, si no insertar por SQL)
    rlist = []
    try:
        from database import insert_requisicion_safe as _ins_req
        rlist = [_ins_req(fecha=None, estado='Pendiente') for _ in range(3)]
    except Exception:
        try:
            with get_connection() as conn:
                with conn.cursor() as cursor:
                    for _ in range(3):
                        cursor.execute("INSERT INTO REQUISICIONES (fecha_requisicion, estado_requisicion) VALUES (CURRENT_DATE, %s) RETURNING id_requisicion", ('Pendiente',))
                        rlist.append(cursor.fetchone()[0])
                    conn.commit()
        except Exception:
            pytest.skip('No se pudieron crear requisiciones en la BD')
    r1, r2, r3 = rlist

    data = {'requisicion_id': [str(r1), '', 'None', str(r2), str(r3)]}
    resp = client.post(f'/areas/{area_id}/asignar/requisicion', data=data)
    assert resp.status_code == 200
    j = resp.get_json()
    assert j.get('success') is True
    assert j.get('assigned', 0) >= 3

    reqs = get_requisiciones_for_area(area_id)
    ids = [r['id'] for r in reqs]
    assert all(x in ids for x in (r1, r2, r3))

    # Desasignar varios en una sola petición
    resp2 = client.post(f'/areas/{area_id}/desasignar/requisicion', data={'requisicion_id': [str(r1), str(r2)]})
    assert resp2.status_code == 200
    j2 = resp2.get_json()
    assert j2.get('success') is True

    reqs_after = get_requisiciones_for_area(area_id)
    ids_after = [r['id'] for r in reqs_after]
    assert r1 not in ids_after and r2 not in ids_after

    # limpiar
    try:
        remove_requisicion_from_area(area_id, r3)
    except Exception:
        pass
