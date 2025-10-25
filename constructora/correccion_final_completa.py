import os
import re
from pathlib import Path

def correccion_final_completa():
    """Corrección final de los últimos problemas detectados"""
    
    base_dir = Path("C:/Users/VICTUS/Videos/BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)/BASE-DE-DATOS-1-PROYECTO-FINAL-master/constructora/templates")
    
    # Problemas específicos detectados
    correcciones_finales = {
        'areas': ['listar.html', 'editar.html', 'detalle.html'],
        'incidentes': ['listar.html', 'editar.html', 'detalle.html'],
        'avances': ['listar.html', 'editar.html', 'detalle.html'],
        'movimientos': ['listar.html', 'editar.html', 'detalle.html'],
        'auditorias': ['listar.html', 'detalle.html'],
        'proveedores': ['listar.html']  # Solo el stats-grid
    }
    
    print("🎯 CORRECCIÓN FINAL DE ÚLTIMOS PROBLEMAS")
    print("=" * 45)
    print()
    
    correcciones_aplicadas = 0
    
    for modulo, archivos in correcciones_finales.items():
        modulo_dir = base_dir / modulo
        if not modulo_dir.exists():
            continue
            
        print(f"🛠️  Módulo: {modulo.upper()}")
        
        for archivo in archivos:
            ruta_archivo = modulo_dir / archivo
            if not ruta_archivo.exists():
                continue
                
            print(f"   📝 {archivo}:", end=" ")
            
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                contenido_original = contenido
                cambios = []
                
                # Corregir extends con comillas simples a dobles
                if "{% extends 'base.html' %}" in contenido:
                    contenido = contenido.replace("{% extends 'base.html' %}", '{% extends "base.html" %}')
                    cambios.append("Extends")
                
                # Agregar extends si no está
                elif 'extends' not in contenido and '<!DOCTYPE html>' not in contenido:
                    if contenido.strip():  # Si el archivo no está vacío
                        contenido = '{% extends "base.html" %}\n\n' + contenido
                        cambios.append("Extends-Add")
                
                # Para proveedores/listar.html - agregar stats-grid específico
                if modulo == 'proveedores' and archivo == 'listar.html':
                    if 'stats-grid' not in contenido:
                        stats_grid_proveedores = '''
<!-- Estadísticas de Proveedores -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-icon bg-blue">
            <i class="fas fa-truck"></i>
        </div>
        <div class="stat-content">
            <div class="stat-number">{{ proveedores|length or 0 }}</div>
            <div class="stat-label">Total Proveedores</div>
        </div>
    </div>
    
    <div class="stat-card">
        <div class="stat-icon bg-green">
            <i class="fas fa-check-circle"></i>
        </div>
        <div class="stat-content">
            <div class="stat-number">{{ proveedores|length or 0 }}</div>
            <div class="stat-label">Activos</div>
        </div>
    </div>
    
    <div class="stat-card">
        <div class="stat-icon bg-orange">
            <i class="fas fa-handshake"></i>
        </div>
        <div class="stat-content">
            <div class="stat-number">0</div>
            <div class="stat-label">Contratos Activos</div>
        </div>
    </div>
</div>
'''
                        
                        # Insertar después del page-header
                        if '</div>' in contenido and 'page-header' in contenido:
                            # Buscar el cierre del page-header y agregar stats
                            patron = r'(</div>\s*</div>)(\s*<!-- [^>]+ -->)?'
                            if re.search(patron, contenido):
                                contenido = re.sub(
                                    patron,
                                    r'\1\n' + stats_grid_proveedores,
                                    contenido,
                                    count=1
                                )
                                cambios.append("Stats-grid")
                
                # Guardar si hubo cambios
                if contenido != contenido_original:
                    with open(ruta_archivo, 'w', encoding='utf-8') as f:
                        f.write(contenido)
                    correcciones_aplicadas += len(cambios)
                    print(" ".join([f"✅ {cambio}" for cambio in cambios]))
                else:
                    print("⚪ OK")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print()
    
    print(f"📊 CORRECCIONES FINALES APLICADAS: {correcciones_aplicadas}")
    print()
    
    return correcciones_aplicadas

# Ejecutar corrección
correcciones = correccion_final_completa()

print("✅ PROCESO DE ESTANDARIZACIÓN VISUAL COMPLETADO")
print()
print("📈 RESUMEN FINAL:")
print(f"  • Correcciones automáticas aplicadas: {correcciones}")
print("  • Templates estandarizados con base.html")
print("  • Formularios con create-forms.css consistente")
print("  • Páginas de listado con page-header y stats-grid")
print("  • Iconos FontAwesome unificados")
print()
print("🎯 RECOMENDACIÓN FINAL:")
print("  Ejecuta el análisis una vez más para confirmar que")
print("  todos los módulos ahora tienen consistencia visual.")