import os
import pytest
from database import (
    insert_area_safe, insert_obra_safe, insert_cliente_safe,
    assign_area_to_obra, get_obras_for_area, get_areas_safe
)

# Estos tests requieren una base de datos de desarrollo local y usan las mismas credenciales
# Ejecutar con: pytest -q


def test_area_assign_obra_flow():
    # Crear un cliente mínimo para la obra
    cliente_id = insert_cliente_safe('Cliente Test pytest')
    assert cliente_id is not None

    # Crear obra vinculada al cliente
    obra_id = insert_obra_safe(nombre='Obra Test pytest', descripcion='desc', ubicacion='loc', fecha_inicio=None, fecha_fin=None, valor=None, estado='Planeación', cliente_id=cliente_id)
    assert obra_id is not None

    # Crear área
    area_id = insert_area_safe('Área pytest')
    assert area_id is not None

    # Asignar área a obra
    ok = assign_area_to_obra(area_id, obra_id)
    assert ok is True

    # Verificar la relación
    obras = get_obras_for_area(area_id)
    assert any(o['id'] == obra_id for o in obras)

    # Listado general de áreas incluye la nueva área
    areas = get_areas_safe()
    assert any(a['id'] == area_id for a in areas)
