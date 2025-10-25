#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de vista de detalle de proyecto con asignaciones
Autor: Sistema de Constructora
Fecha: 2024
"""

import requests
import webbrowser
from time import sleep

def probar_vista_detalle_proyecto():
    """Probar la nueva vista de detalle de proyecto con asignaciones"""
    print("🧪 PROBANDO VISTA DETALLE DE PROYECTO CON ASIGNACIONES")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # Verificar que el servidor esté corriendo
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor Flask está corriendo correctamente")
        else:
            print(f"⚠️ Servidor responde con código: {response.status_code}")
            
        # Probar vista de detalle de proyecto (ID 1 que tiene asignaciones)
        proyecto_id = 1
        detalle_url = f"{base_url}/proyectos/{proyecto_id}"
        
        print(f"\n📋 Probando detalle de proyecto ID: {proyecto_id}")
        print(f"🔗 URL: {detalle_url}")
        
        response = requests.get(detalle_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Vista de detalle de proyecto cargada correctamente")
            
            # Verificar que contenga las nuevas secciones
            content = response.text
            
            checks = [
                ("Equipo del Proyecto", "👥 Sección de equipo"),
                ("Arquitecto Principal", "🎨 Sección de arquitecto"), 
                ("Ingeniero Principal", "⚙️ Sección de ingeniero"),
                ("Obras Asignadas", "🏗️ Sección de obras"),
                ("Vehículos y Equipos", "🚚 Sección de vehículos"),
                ("Estadísticas", "📊 Sección de estadísticas"),
                ("María González", "👩‍🎨 Arquitecto asignado"),
                ("Jorge López", "👨‍⚙️ Ingeniero asignado"),
                ("Administracion", "🏢 Obra asignada"),
                ("ABC123", "🚗 Vehículo asignado"),
                ("DEF456", "🚛 Vehículo asignado")
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
            
        # Probar también listado de proyectos
        print(f"\n📋 Probando listado de proyectos...")
        response2 = requests.get(f"{base_url}/proyectos", timeout=10)
        
        if response2.status_code == 200:
            print("✅ Listado de proyectos cargado correctamente")
            print("🔗 Navegando desde listado a detalle...")
        else:
            print(f"❌ Error en listado: {response2.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor Flask")
        print("💡 Asegúrate de que esté ejecutando: python app.py")
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")

if __name__ == "__main__":
    # Esperar un momento para que el servidor esté listo
    print("⏳ Esperando que el servidor esté listo...")
    sleep(3)
    probar_vista_detalle_proyecto()