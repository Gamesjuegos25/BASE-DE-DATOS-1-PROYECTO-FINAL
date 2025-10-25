#!/usr/bin/env python3
import psycopg2
from database import get_connection

try:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            print("=== VERIFICACIÓN DE CONTRATOS CON MÉTODO DE PAGO ===")
            
            # Obtener los últimos contratos creados
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
                    co.id_obra,
                    o.nombre_obra
                FROM contratos c
                LEFT JOIN clientes cl ON c.id_cliente = cl.id_cliente
                LEFT JOIN contrato_obra co ON c.id_contrato = co.id_contrato
                LEFT JOIN obras o ON co.id_obra = o.id_obra
                WHERE c.numero_contrato LIKE 'CON-%'
                ORDER BY c.id_contrato DESC
                LIMIT 5
            """)
            
            contratos = cursor.fetchall()
            print(f"Últimos {len(contratos)} contratos creados:\n")
            
            for contrato in contratos:
                print(f"📋 CONTRATO #{contrato[0]}")
                print(f"   Número: {contrato[1]}")
                print(f"   Fecha Inicio: {contrato[2]}")
                print(f"   Fecha Fin: {contrato[3]}")
                print(f"   Valor: ${contrato[4]:,.2f}" if contrato[4] else "Sin valor")
                print(f"   Estado: {contrato[5]}")
                print(f"   💳 Método de Pago: {contrato[6] or 'Sin método'}")
                print(f"   Cliente: {contrato[8]} (ID: {contrato[7]})")
                print(f"   Obra: {contrato[10]} (ID: {contrato[9]})")
                print()
                
            # Estadísticas de métodos de pago
            print("📊 ESTADÍSTICAS DE MÉTODOS DE PAGO:")
            cursor.execute("""
                SELECT 
                    tipo_pago_contrato,
                    COUNT(*) as cantidad
                FROM contratos 
                WHERE tipo_pago_contrato IS NOT NULL
                GROUP BY tipo_pago_contrato
                ORDER BY cantidad DESC
            """)
            
            metodos = cursor.fetchall()
            for metodo in metodos:
                print(f"   {metodo[0]}: {metodo[1]} contratos")
                
except Exception as e:
    print(f"Error: {e}")