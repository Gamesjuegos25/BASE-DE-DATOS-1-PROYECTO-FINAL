#!/usr/bin/env python3
"""
CORRECTOR DE NOMBRES DE RUTAS
=============================
Ajusta nombres de rutas en templates para que coincidan con app.py
"""

import os
import re
from pathlib import Path

def corregir_nombres_rutas():
    """Corrige nombres de rutas en templates de módulos nuevos"""
    
    # Mapeo de rutas incorrectas a correctas
    mapeo_rutas = {
        'crear_clientes': 'crear_cliente',
        'listar_clientes': 'listar_clientes',  # Este está bien
        'editar_clientes': 'editar_cliente', 
        'ver_clientes': 'ver_cliente',
        'eliminar_clientes': 'eliminar_cliente'
    }
    
    print("🔧 CORRECTOR DE NOMBRES DE RUTAS")
    print("=" * 35)
    
    # Módulos que necesitan corrección
    modulos = ['clientes']  # Solo clientes por ahora
    templates_dir = Path('templates')
    
    for modulo in modulos:
        modulo_dir = templates_dir / modulo
        if modulo_dir.exists():
            archivos_html = list(modulo_dir.glob('*.html'))
            
            for archivo in archivos_html:
                print(f"🔍 Revisando: {archivo.name}")
                
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                    
                    contenido_original = contenido
                    
                    # Aplicar correcciones
                    for ruta_incorrecta, ruta_correcta in mapeo_rutas.items():
                        # Buscar y reemplazar en url_for()
                        patron = rf"url_for\(['\"]({ruta_incorrecta})['\"]"
                        contenido = re.sub(patron, f"url_for('{ruta_correcta}'", contenido)
                    
                    # Si hubo cambios, guardar
                    if contenido != contenido_original:
                        with open(archivo, 'w', encoding='utf-8') as f:
                            f.write(contenido)
                        print(f"✅ Corregido: {archivo.name}")
                    else:
                        print(f"ℹ️  Sin cambios: {archivo.name}")
                        
                except Exception as e:
                    print(f"❌ Error con {archivo.name}: {str(e)}")

def crear_templates_basicos_otros_modulos():
    """Crea templates básicos para otros módulos que no existen en app.py"""
    
    print("\n🏗️  CREANDO RUTAS BÁSICAS PARA OTROS MÓDULOS")
    print("=" * 45)
    
    # Módulos que necesitan rutas básicas
    modulos_sin_rutas = ['herramientas', 'compras', 'ventas', 'pagos', 'nomina']
    
    rutas_basicas = ""
    
    for modulo in modulos_sin_rutas:
        rutas_basicas += f"""
# =================== RUTAS {modulo.upper()} ===================

@app.route('/{modulo}')
def listar_{modulo}():
    \"\"\"Listar {modulo}\"\"\"
    return render_template('{modulo}/listar.html', {modulo}=[])

@app.route('/{modulo}/crear', methods=['GET', 'POST'])
def crear_{modulo}():
    \"\"\"Crear {modulo[:-1]}\"\"\"
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_{modulo}'))
    return render_template('{modulo}/crear.html')

@app.route('/{modulo}/<int:id>')
def ver_{modulo}(id):
    \"\"\"Ver {modulo[:-1]}\"\"\"
    return render_template('{modulo}/detalle.html')

@app.route('/{modulo}/<int:id>/editar', methods=['GET', 'POST'])  
def editar_{modulo}(id):
    \"\"\"Editar {modulo[:-1]}\"\"\"
    if request.method == 'POST':
        flash('Funcionalidad en desarrollo', 'info')
        return redirect(url_for('listar_{modulo}'))
    return render_template('{modulo}/editar.html')

"""
    
    # Guardar archivo con rutas básicas
    with open('rutas_basicas_modulos_nuevos.py', 'w', encoding='utf-8') as f:
        f.write(f"""# RUTAS BÁSICAS PARA MÓDULOS NUEVOS
# ==================================
# Agregar al final de app.py antes de if __name__ == '__main__'

{rutas_basicas}""")
    
    print("📄 Archivo creado: rutas_basicas_modulos_nuevos.py")
    print("💡 Copiar contenido e insertar en app.py")

def main():
    """Función principal"""
    # 1. Corregir nombres de rutas
    corregir_nombres_rutas()
    
    # 2. Crear rutas básicas para otros módulos
    crear_templates_basicos_otros_modulos()
    
    print(f"\n🎯 CORRECCIÓN COMPLETADA")
    print("=" * 25)
    print("✅ Nombres de rutas ajustados")
    print("✅ Rutas básicas generadas") 
    print("💡 Agregar rutas básicas a app.py para completar funcionalidad")

if __name__ == "__main__":
    main()