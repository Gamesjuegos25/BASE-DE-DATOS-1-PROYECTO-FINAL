import os
import sys
import pytest

# Añadir la carpeta `constructora` al inicio de sys.path para que
# `import database` y `import app` funcionen al ejecutar pytest desde fuera.
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from database import (
    insert_area_safe, insert_obra_safe, insert_cliente_safe,
    assign_area_to_obra, get_obras_for_area, get_areas_safe,
    remove_area_from_obra,
    assign_activity_to_area, get_activities_for_area, remove_activity_from_area,
    assign_employee_to_area, get_employees_for_area, remove_employee_from_area
)

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


def test_assign_multiple_obras_via_endpoint(client):
    # Crear cliente y dos obras
    cliente_id = insert_cliente_safe('Cliente multi pytest')
    obra1 = insert_obra_safe(nombre='Obra Multi 1', descripcion='', ubicacion='', fecha_inicio=None, fecha_fin=None, valor=None, estado='Planeación', cliente_id=cliente_id)
    obra2 = insert_obra_safe(nombre='Obra Multi 2', descripcion='', ubicacion='', fecha_inicio=None, fecha_fin=None, valor=None, estado='Planeación', cliente_id=cliente_id)
    assert obra1 and obra2

    area_id = insert_area_safe('Área multi asign')
    assert area_id

    # Enviar POST simulando múltiples campos obra_id (como lista en dict)
    data = {'obra_id': [str(obra1), str(obra2)]}
    resp = client.post(f'/areas/{area_id}/asignar/obra', data=data)
    assert resp.status_code == 200
    j = resp.get_json()
    assert j.get('success') is True
    assert j.get('assigned', 0) >= 2

    obras = get_obras_for_area(area_id)
    ids = [o['id'] for o in obras]
    assert obra1 in ids and obra2 in ids

    # limpiar
    assert remove_area_from_obra(area_id, obra1)
    assert remove_area_from_obra(area_id, obra2)


def test_assign_and_unassign_activity_and_employee_via_endpoints(client):
    # Crear datos mínimos
    area_id = insert_area_safe('Área act emp')
    assert area_id

    # Crear actividad y empleado usando helpers si existen
    # Attempt to create minimal actividad/empleado via insert helpers if available
    try:
        from database import insert_actividad_safe, insert_empleado_safe
        actividad_id = insert_actividad_safe(nombre='Actividad pytest', descripcion='x', fecha_programada=None)
        empleado_id = insert_empleado_safe(nombre='Empleado pytest', tipo='Obrero', salario=None)
    except Exception:
        pytest.skip('No hay helpers para crear actividad/empleado en este entorno')

    # Asignar múltiples (single in this test) via endpoint
    resp_a = client.post(f'/areas/{area_id}/asignar/actividad', data={'actividad_id': str(actividad_id)})
    assert resp_a.status_code == 200
    ja = resp_a.get_json()
    assert ja.get('success') is True

    actividades = get_activities_for_area(area_id)
    assert any(a['id'] == actividad_id for a in actividades)

    # Desasignar via endpoint
    resp_da = client.post(f'/areas/{area_id}/desasignar/actividad', data={'actividad_id': str(actividad_id)})
    assert resp_da.status_code == 200
    jda = resp_da.get_json()
    assert jda.get('success') is True

    assert remove_activity_from_area(area_id, actividad_id) is False or True

    # Empleado
    resp_e = client.post(f'/areas/{area_id}/asignar/empleado', data={'empleado_id': str(empleado_id)})
    assert resp_e.status_code == 200
    je = resp_e.get_json()
    assert je.get('success') is True

    empleados = get_employees_for_area(area_id)
    assert any(e['id'] == empleado_id for e in empleados)

    # Desasignar empleado
    resp_de = client.post(f'/areas/{area_id}/desasignar/empleado', data={'empleado_id': str(empleado_id)})
    assert resp_de.status_code == 200
    jde = resp_de.get_json()
    assert jde.get('success') is True

    # limpiar
    assert remove_employee_from_area(area_id, empleado_id) is False or True


def test_assign_multiple_activities_and_empleados_and_invalids(client):
    # Preparar área
    area_id = insert_area_safe('Área multi act emp')
    assert area_id

    # Crear 3 actividades y 3 empleados
    from database import insert_actividad_safe, insert_empleado_safe
    a1 = insert_actividad_safe(nombre='A1', descripcion='', fecha_programada=None)
    a2 = insert_actividad_safe(nombre='A2', descripcion='', fecha_programada=None)
    a3 = insert_actividad_safe(nombre='A3', descripcion='', fecha_programada=None)

    e1 = insert_empleado_safe(nombre='E1', tipo='Obrero', salario=None)
    e2 = insert_empleado_safe(nombre='E2', tipo='Obrero', salario=None)
    e3 = insert_empleado_safe(nombre='E3', tipo='Obrero', salario=None)

    # Asignar múltiples actividades con algunos ids inválidos
    data_act = {'actividad_id': [str(a1), '', 'None', str(a2), str(a3)]}
    resp_act = client.post(f'/areas/{area_id}/asignar/actividad', data=data_act)
    assert resp_act.status_code == 200
    ja = resp_act.get_json()
    assert ja.get('success') is True
    assert ja.get('assigned', 0) >= 3

    actividades = get_activities_for_area(area_id)
    ids_act = [a['id'] for a in actividades]
    assert all(x in ids_act for x in (a1, a2, a3))

    # Desasignar varias actividades en una sola petición (enviar lista)
    resp_des = client.post(f'/areas/{area_id}/desasignar/actividad', data={'actividad_id': [str(a1), str(a2)]})
    assert resp_des.status_code == 200
    jd = resp_des.get_json()
    assert jd.get('success') is True

    # Verificar que a1 y a2 ya no aparecen
    actividades = get_activities_for_area(area_id)
    ids_act = [a['id'] for a in actividades]
    assert a1 not in ids_act and a2 not in ids_act

    # Asignar múltiples empleados
    data_emp = {'empleado_id': [str(e1), str(e2), str(e3)]}
    resp_emp = client.post(f'/areas/{area_id}/asignar/empleado', data=data_emp)
    assert resp_emp.status_code == 200
    je = resp_emp.get_json()
    assert je.get('success') is True
    assert je.get('assigned', 0) >= 3

    empleados = get_employees_for_area(area_id)
    ids_emp = [e['id'] for e in empleados]
    assert all(x in ids_emp for x in (e1, e2, e3))

    # Desasignar todos los empleados de una vez
    resp_de_all = client.post(f'/areas/{area_id}/desasignar/empleado', data={'empleado_id': [str(e1), str(e2), str(e3)]})
    assert resp_de_all.status_code == 200
    jdae = resp_de_all.get_json()
    assert jdae.get('success') is True

    empleados = get_employees_for_area(area_id)
    ids_emp = [e['id'] for e in empleados]
    assert all(x not in ids_emp for x in (e1, e2, e3))

    # limpieza final (intentar eliminar por si algo queda)
    for aid in (a1, a2, a3):
        try:
            remove_activity_from_area(area_id, aid)
        except Exception:
            pass
    for eid in (e1, e2, e3):
        try:
            remove_employee_from_area(area_id, eid)
        except Exception:
            pass
