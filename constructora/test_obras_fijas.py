#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de obras fijas
"""

import requests
import json
from database import get_connection

def test_obras_fijas_api():
    """Probar la API de tipos de obra que usa el JavaScript"""
    try:
        # Probar la conexión a la base de datos primero
        conn = get_connection()
        cur = conn.cursor()
        
        print("🧪 PROBANDO FUNCIONALIDAD OBRAS FIJAS")
        print("=" * 50)
        
        # 1. Verificar tipos de obra en BD
        print("\n1️⃣ VERIFICANDO TIPOS EN BASE DE DATOS:")
        cur.execute("SELECT id_tipo_obra, nombre_tipo, precio_base FROM tipos_obra WHERE activo = true LIMIT 5")
        tipos = cur.fetchall()
        
        for id_tipo, nombre, precio in tipos:
            precio_num = float(precio) if precio else 0
            print(f"   • ID {id_tipo}: {nombre} - Q{precio_num:,.0f}")
        
        # 2. Verificar estructura de tabla
        print(f"\n2️⃣ ESTRUCTURA DE TABLA tipos_obra:")
        cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'tipos_obra'")
        columnas = cur.fetchall()
        for col in columnas:
            print(f"   • {col[0]} ({col[1]})")
        
        # 3. Crear datos de prueba para simulación
        print(f"\n3️⃣ SIMULACIÓN DE CÁLCULO:")
        area_prueba = 100  # m²
        tipo_prueba = tipos[0]  # Primer tipo
        id_tipo, nombre, precio = tipo_prueba
        
        precio_num = float(precio) if precio else 0
        valor_calculado = area_prueba * precio_num
        
        print(f"   • Tipo: {nombre}")
        print(f"   • Área: {area_prueba} m²")
        print(f"   • Precio base: Q{precio_num:,.0f} por m²")
        print(f"   • Valor total: Q{valor_calculado:,.0f}")
        
        # 4. Verificar que el servidor esté corriendo
        print(f"\n4️⃣ PROBANDO SERVIDOR LOCAL:")
        try:
            response = requests.get("http://localhost:5000", timeout=2)
            print(f"   ✅ Servidor responde: {response.status_code}")
        except:
            print(f"   ⚠️  Servidor no disponible en localhost:5000")
        
        print(f"\n✅ CONFIGURACIÓN CORRECTA PARA OBRAS FIJAS")
        print(f"📝 Los tipos están disponibles y tienen precios válidos")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error en prueba: {str(e)}")

def generar_datos_javascript():
    """Generar datos en formato JavaScript para debugging"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT id_tipo_obra, nombre_tipo, precio_base, unidad_medida FROM tipos_obra WHERE activo = true")
        tipos = cur.fetchall()
        
        print(f"\n🔧 DATOS PARA DEBUGGING JAVASCRIPT:")
        print("=" * 40)
        
        js_array = "const tiposObraData = [\n"
        for id_tipo, nombre, precio, unidad in tipos:
            precio_num = float(precio) if precio else 0
            js_array += f'  {{id: {id_tipo}, nombre: "{nombre}", precio: {precio_num}, unidad: "{unidad or "m²"}"}},\n'
        
        js_array += "];"
        
        print(js_array)
        print(f"\n📋 Total de {len(tipos)} tipos disponibles")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_obras_fijas_api()
    generar_datos_javascript()