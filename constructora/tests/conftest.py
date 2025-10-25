import os
import sys

# Asegurar que la carpeta padre (constructora) esté en sys.path
HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import pytest
from database import get_connection


@pytest.fixture(autouse=True)
def db_transaction():
    """Inicia una transacción antes de cada test y hace rollback al finalizar.

    Esto ayuda a aislar los tests que modifican la base de datos.
    """
    conn = get_connection()
    if conn is None:
        pytest.skip('No hay conexión a la base de datos para tests')

    # Desactivar autocommit y abrir transacción
    original_autocommit = getattr(conn, 'autocommit', True)
    conn.autocommit = False

    try:
        yield
        # Al terminar el test, hacer rollback para dejar la BD limpia
        conn.rollback()
    finally:
        try:
            conn.autocommit = original_autocommit
            conn.close()
        except Exception:
            pass
