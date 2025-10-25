#!/usr/bin/env python3
"""
Iniciador simple de la aplicación Flask
"""

import os
import sys
import subprocess

def iniciar_aplicacion():
    """Inicia la aplicación Flask"""
    try:
        # Cambiar al directorio correcto
        directorio = r"C:\Users\VICTUS\Videos\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\BASE-DE-DATOS-1-PROYECTO-FINAL-master\constructora"
        
        print(f"Cambiando al directorio: {directorio}")
        os.chdir(directorio)
        
        print("Directorio actual:", os.getcwd())
        print("Archivos en directorio:")
        for archivo in os.listdir("."):
            if archivo.endswith(('.py', '.html')):
                print(f"  - {archivo}")
        
        # Verificar que app.py existe
        if not os.path.exists("app.py"):
            print("ERROR: app.py no encontrado")
            return False
        
        print("\n¡app.py encontrado! Iniciando aplicación...")
        print("=" * 50)
        
        # Iniciar la aplicación
        resultado = subprocess.run([sys.executable, "app.py"], 
                                 capture_output=False, 
                                 text=True,
                                 cwd=directorio)
        
        return True
        
    except Exception as e:
        print(f"Error al iniciar aplicación: {e}")
        return False

if __name__ == "__main__":
    iniciar_aplicacion()