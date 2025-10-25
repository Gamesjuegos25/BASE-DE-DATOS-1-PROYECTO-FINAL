#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de vista de detalle de obra con asignaciones
Autor: Sistema de Constructora
Fecha: 2024
"""

import requests
import webbrowser
from time import sleep

def probar_vista_detalle_obra():
    """Probar la nueva vista de detalle de obra con asignaciones"""
    print("🧪 PROBANDO VISTA DETALLE DE OBRA CON ASIGNACIONES")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # Verificar que el servidor esté corriendo
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor Flask está corriendo correctamente")
        else:
            print(f"⚠️ Servidor responde con código: {response.status_code}")
            
        # Probar vista de detalle de obra (ID 9 que tiene asignaciones)
        obra_id = 9
        detalle_url = f"{base_url}/obras/{obra_id}"
        
        print(f"\n🏗️ Probando detalle de obra ID: {obra_id}")
        print(f"🔗 URL: {detalle_url}")
        
        response = requests.get(detalle_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Vista de detalle de obra cargada correctamente")
            
            # Verificar que contenga las nuevas secciones
            content = response.text
            
            checks = [
                ("Recursos Asignados", "🔍 Sección de recursos asignados"),
                ("Equipo de Trabajo", "👥 Sección de empleados"), 
                ("Materiales Asignados", "🧱 Sección de materiales"),
                ("Vehículos y Equipos", "🚚 Sección de vehículos"),
                ("Información del Cliente", "👤 Sección de cliente"),
                ("Pedro Sánchez", "📋 Datos de empleado asignado"),
                ("Cemento Gris", "📦 Material asignado"),
                ("ABC123", "🚗 Vehículo asignado")
            ]
            
            for texto, descripcion in checks:
                if texto in content:
                    print(f"   ✅ {descripcion}")
                else:
                    print(f"   ❌ {descripcion} - No encontrado")
            
            # Abrir en navegador para inspección visual
            print(f"\n🌐 Abriendo vista en navegador...")
            webbrowser.open(detalle_url)
            
        else:
            print(f"❌ Error al cargar detalle: {response.status_code}")
            print(f"Response: {response.text[:500]}")
            
        # Probar también con obra que podría no tener asignaciones (ID 10)
        print(f"\n🏗️ Probando obra sin muchas asignaciones (ID 10)...")
        response2 = requests.get(f"{base_url}/obras/10", timeout=10)
        
        if response2.status_code == 200:
            print("✅ Vista alternativa cargada correctamente")
        else:
            print(f"❌ Error en vista alternativa: {response2.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor Flask")
        print("💡 Asegúrate de que esté ejecutando: python app.py")
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")

if __name__ == "__main__":
    # Esperar un momento para que el servidor esté listo
    print("⏳ Esperando que el servidor esté listo...")
    sleep(3)
    probar_vista_detalle_obra()