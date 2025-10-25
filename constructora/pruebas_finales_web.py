#!/usr/bin/env python3
"""
🌐 PRUEBAS FINALES DEL SISTEMA WEB
Verifica que la aplicación Flask esté funcionando correctamente
"""

import sys
import os
import requests
import time
from datetime import datetime

def verificar_servidor(url="http://127.0.0.1:5000"):
    """Verifica si el servidor Flask está corriendo"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"✅ Servidor Flask funcionando en {url}")
            return True
        else:
            print(f"❌ Servidor respondió con código {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ No se puede conectar al servidor en {url}")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Timeout conectando a {url}")
        return False
    except Exception as e:
        print(f"❌ Error verificando servidor: {e}")
        return False

def verificar_rutas_principales(base_url="http://127.0.0.1:5000"):
    """Verifica las rutas principales del sistema"""
    rutas_importantes = [
        "/",
        "/empleados",
        "/materiales",
        "/obras",
        "/proveedores",
        "/equipos",
        "/vehiculos",
        "/contratos",
        "/bitacoras"
    ]
    
    resultados = []
    
    print("\n🔍 Verificando rutas principales...")
    for ruta in rutas_importantes:
        url = base_url + ruta
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {ruta} - OK")
                resultados.append((ruta, True))
            else:
                print(f"   ❌ {ruta} - Error {response.status_code}")
                resultados.append((ruta, False))
        except Exception as e:
            print(f"   ❌ {ruta} - Error: {str(e)[:50]}...")
            resultados.append((ruta, False))
        
        time.sleep(0.5)  # Pausa entre requests
    
    return resultados

def verificar_funcionalidad_bd(base_url="http://127.0.0.1:5000"):
    """Verifica que las páginas principales carguen datos correctamente"""
    rutas_con_datos = [
        "/empleados",
        "/materiales", 
        "/obras",
        "/proveedores",
        "/equipos",
        "/vehiculos",
        "/contratos",
        "/bitacoras"
    ]
    
    resultados = []
    
    print("\n🔍 Verificando carga de datos...")
    for ruta in rutas_con_datos:
        url = base_url + ruta
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                contenido = response.text
                # Verificar que no sea una página vacía
                if len(contenido) > 1000:  # Página con contenido
                    # Verificar que tenga estructura de tabla o cards
                    if any(word in contenido.lower() for word in ['table', 'card', 'list-group', 'datos']):
                        print(f"   ✅ {ruta} - Datos cargados correctamente")
                        resultados.append((ruta, True))
                    else:
                        print(f"   ⚠️  {ruta} - Página carga pero sin estructura de datos")
                        resultados.append((ruta, False))
                else:
                    print(f"   ⚠️  {ruta} - Página muy pequeña, posible error")
                    resultados.append((ruta, False))
            else:
                print(f"   ❌ {ruta} - Error {response.status_code}")
                resultados.append((ruta, False))
        except Exception as e:
            print(f"   ❌ {ruta} - Error: {str(e)[:50]}...")
            resultados.append((ruta, False))
        
        time.sleep(0.5)
    
    return resultados

def main():
    print("=" * 60)
    print("🌐 PRUEBAS FINALES DEL SISTEMA WEB")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    base_url = "http://127.0.0.1:5000"
    
    # 1. Verificar que el servidor esté corriendo
    print("\n1️⃣  Verificando servidor Flask...")
    if not verificar_servidor(base_url):
        print("\n❌ FALLO: El servidor Flask no está corriendo.")
        print("💡 Asegúrate de ejecutar 'python app.py' antes de estas pruebas")
        return False
    
    # 2. Verificar rutas principales
    print("\n2️⃣  Verificando rutas principales...")
    resultados_rutas = verificar_rutas_principales(base_url)
    
    # 3. Verificar funcionalidad de base de datos
    print("\n3️⃣  Verificando carga de datos...")
    resultados_detalle = verificar_funcionalidad_bd(base_url)
    
    # 4. Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS WEB")
    print("=" * 60)
    
    # Contar éxitos
    rutas_ok = sum(1 for _, ok in resultados_rutas if ok)
    total_rutas = len(resultados_rutas)
    
    detalle_ok = sum(1 for _, ok in resultados_detalle if ok)
    total_detalle = len(resultados_detalle)
    
    print(f"🔗 Rutas principales: {rutas_ok}/{total_rutas} funcionando")
    print(f"� Carga de datos: {detalle_ok}/{total_detalle} funcionando")
    
    total_ok = rutas_ok + detalle_ok
    total_pruebas = total_rutas + total_detalle
    porcentaje = (total_ok / total_pruebas) * 100
    
    print(f"\n🎯 RESULTADO FINAL: {total_ok}/{total_pruebas} pruebas exitosas ({porcentaje:.1f}%)")
    
    if porcentaje >= 90:
        print("🎉 ¡SISTEMA FUNCIONANDO EXCELENTEMENTE!")
        return True
    elif porcentaje >= 70:
        print("✅ Sistema funcionando bien con algunos ajustes menores")
        return True
    else:
        print("⚠️  Sistema necesita ajustes importantes")
        return False

if __name__ == "__main__":
    exito = main()
    print(f"\n{'🎊 PRUEBAS COMPLETADAS EXITOSAMENTE' if exito else '🔧 SE NECESITAN AJUSTES'}")
    sys.exit(0 if exito else 1)