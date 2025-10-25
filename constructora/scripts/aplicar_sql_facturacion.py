import os
import sys
from pathlib import Path

# Permitir importar database desde este script
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database import get_connection

QUERIES_DIR = ROOT_DIR / 'queries'
FILES = [
    QUERIES_DIR / 'contratos_facturacion.sql',
    QUERIES_DIR / 'facturizar_contrato.sql',
]

def aplicar_sql():
    for f in FILES:
        if not f.exists():
            print(f"Archivo no encontrado: {f}")
            return 1
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for f in FILES:
                    sql = f.read_text(encoding='utf-8')
                    print(f"Aplicando: {f.name} ...")
                    cur.execute(sql)
            conn.commit()
            print("Listo: SQL de facturación aplicado correctamente.")
            return 0
    except Exception as e:
        print(f"Error aplicando SQL: {e}")
        return 2

if __name__ == '__main__':
    sys.exit(aplicar_sql())
