#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            print("=== VERIFICACIÓN DEL CONTRATO CREADO ===")
            
            # Obtener el último contrato creado
            cursor.execute("""
                SELECT 
                    c.id_contrato,
                    c.numero_contrato,
                    c.fecha_inicio_contrato,
                    c.fecha_fin_contrato,
                    c.valor_total,
                    c.estado,
                    c.tipo_pago_contrato,
                    c.id_cliente,
                    cl.nombre_cliente,
                    co.id_obra
                FROM contratos c
                LEFT JOIN clientes cl ON c.id_cliente = cl.id_cliente
                LEFT JOIN contrato_obra co ON c.id_contrato = co.id_contrato
                ORDER BY c.id_contrato DESC
                LIMIT 1
            """)
            
            contrato = cursor.fetchone()
            if contrato:
                print("Último contrato creado:")
                print(f"  ID Contrato: {contrato[0]}")
                print(f"  Número: {contrato[1]}")
                print(f"  Fecha Inicio: {contrato[2]}")
                print(f"  Fecha Fin: {contrato[3]}")
                print(f"  Valor Total: ${contrato[4]:,.2f}" if contrato[4] else "Sin valor")
                print(f"  Estado: {contrato[5]}")
                print(f"  Tipo Pago: {contrato[6]}")
                print(f"  Cliente ID: {contrato[7]}")
                print(f"  Nombre Cliente: {contrato[8]}")
                print(f"  Obra ID: {contrato[9]}" if contrato[9] else "Sin obra asignada")
                
                # Verificar si hay relación con obra
                if not contrato[9]:
                    print("\n🔍 Verificando tabla CONTRATO_OBRA...")
                    cursor.execute("SELECT * FROM contrato_obra WHERE id_contrato = %s", (contrato[0],))
                    obra_rel = cursor.fetchone()
                    if obra_rel:
                        print(f"  ✅ Relación encontrada: Contrato {obra_rel[0]} -> Obra {obra_rel[1]}")
                    else:
                        print(f"  ❌ No hay relación con obra")
            else:
                print("❌ No se encontró ningún contrato")
                
except Exception as e:
    print(f"Error: {e}")