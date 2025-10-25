import sys
from database import get_connection

"""
Uso:
  py scripts/generar_factura_contrato.py <id_contrato>

Requisitos:
  - Haber ejecutado queries/contratos_facturacion.sql
  - Haber ejecutado queries/facturizar_contrato.sql
"""

def main():
    if len(sys.argv) < 2:
        print("Uso: py scripts/generar_factura_contrato.py <id_contrato>")
        sys.exit(1)
    contrato_id = int(sys.argv[1])

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT facturizar_contrato(%s)", (contrato_id,))
        factura_id = cur.fetchone()[0]
        conn.commit()
        print(f"Factura creada correctamente. ID factura: {factura_id}")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error generando factura: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
