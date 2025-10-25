import os
import sys
import pytest

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from database import (
    insert_area_safe, get_requisiciones_safe, get_requisiciones_for_area,
    get_connection, insert_material_safe, actualizar_stock_material_safe,
    get_movimientos_materiales_recientes_safe
)

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client


def test_detalles_requisicion_and_count(client):
    # Crear área y requisición + detalles
    area_id = insert_area_safe('Área detalles req')
    assert area_id

    # Crear requisición por SQL
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO REQUISICIONES (fecha_requisicion, estado_requisicion) VALUES (CURRENT_DATE, %s) RETURNING id_requisicion", ('Pendiente',))
            req_id = cursor.fetchone()[0]
            # Crear dos detalles
            cursor.execute("INSERT INTO DETALLES_REQUISICION (cantidad_requisicion) VALUES (%s) RETURNING id_detalle_requisicion", (10,))
            det1 = cursor.fetchone()[0]
            cursor.execute("INSERT INTO DETALLES_REQUISICION (cantidad_requisicion) VALUES (%s) RETURNING id_detalle_requisicion", (5,))
            det2 = cursor.fetchone()[0]
            # Asociar detalles a la requisicion
            cursor.execute("INSERT INTO REQUISICION_DETALLE (id_requisicion, id_detalle_requisicion) VALUES (%s, %s)", (req_id, det1))
            cursor.execute("INSERT INTO REQUISICION_DETALLE (id_requisicion, id_detalle_requisicion) VALUES (%s, %s)", (req_id, det2))
            # Asociar requisicion al area
            cursor.execute("INSERT INTO AREA_REQUISICION (id_area, id_requisicion) VALUES (%s, %s)", (area_id, req_id))
            conn.commit()

    # Consultar requisiciones y verificar items_solicitados >= 2
    reqs = get_requisiciones_safe()
    found = next((r for r in reqs if r.get('id_requisicion') == req_id or r.get('id') == req_id), None)
    assert found is not None
    # items_solicitados may venir en clave items_solicitados
    items = found.get('items_solicitados') or found.get('items') or 0
    assert int(items) >= 2

    # Verificar get_requisiciones_for_area muestra la requisición
    reqs_area = get_requisiciones_for_area(area_id)
    assert any(r['id'] == req_id for r in reqs_area)


def test_movimientos_materiales_and_stock_update(client):
    # Crear material
    mat_id = insert_material_safe('Material pytest', unidad='kg', precio=10.0)
    assert mat_id

    # Actualizar stock usando la función refactorizada (inserta en INVENTARIOS y MOVIMIENTOS_MATERIAL)
    ok = actualizar_stock_material_safe(mat_id, 50, tipo_movimiento='Entrada prueba')
    assert ok is True

    # Verificar que el movimiento fue registrado
    movimientos = get_movimientos_materiales_recientes_safe(limite=10)
    # Debe existir al menos un movimiento para mat_id
    found = any(m.get('id_material') == mat_id for m in movimientos)
    assert found, f"No se encontró movimiento para material {mat_id}"

    # Verificar que el inventario tiene la cantidad correcta
    with get_connection() as conn:
        with conn.cursor(cursor_factory=__import__('psycopg2').extras.RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM INVENTARIOS WHERE id_material = %s", (mat_id,))
            inv = cursor.fetchone()
    assert inv is not None
    assert inv.get('cantidad_inventario') == 50
