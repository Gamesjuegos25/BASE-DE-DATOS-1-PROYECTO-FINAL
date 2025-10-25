import os
import re
from pathlib import Path

def corregir_modulos_restantes():
    """Corrige los módulos que aún tienen inconsistencias"""
    
    base_dir = Path("C:/Users/VICTUS/Videos/BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)/BASE-DE-DATOS-1-PROYECTO-FINAL-master/constructora/templates")
    
    # Módulos que necesitan corrección adicional según el último análisis
    correcciones_pendientes = {
        'obras': ['listar.html', 'editar.html'],
        'proyectos': ['editar.html'],
        'empleados': ['editar.html'],
        'materiales': ['editar.html'],
        'proveedores': ['listar.html', 'editar.html'],
        'vehiculos': ['editar.html'],
        'equipos': ['editar.html'],
        'contratos': ['listar.html', 'editar.html'],
        'trabajos': ['listar.html', 'editar.html'],
        'presupuestos': ['listar.html', 'editar.html'],
        'usuarios': ['listar.html', 'editar.html'],
        'requisiciones': ['listar.html', 'editar.html'],
    }
    
    print("🔧 CORRECCIÓN FINAL DE INCONSISTENCIAS RESTANTES")
    print("=" * 55)
    print()
    
    correcciones_aplicadas = 0
    
    for modulo, archivos in correcciones_pendientes.items():
        modulo_dir = base_dir / modulo
        if not modulo_dir.exists():
            continue
            
        print(f"🛠️  Corrigiendo módulo: {modulo.upper()}")
        
        for archivo in archivos:
            ruta_archivo = modulo_dir / archivo
            if not ruta_archivo.exists():
                continue
                
            print(f"   📝 {archivo}:", end=" ")
            
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                contenido_modificado = contenido
                cambios = []
                
                # Para archivos de listado que necesitan stats-grid
                if archivo == 'listar.html' and 'stats-grid' not in contenido:
                    modulo_singular = modulo[:-1] if modulo.endswith('s') else modulo
                    
                    stats_grid = f'''
<!-- Estadísticas del Módulo -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-icon bg-blue">
            <i class="fas fa-list"></i>
        </div>
        <div class="stat-content">
            <div class="stat-number">{{{{ {modulo}|length or 0 }}}}</div>
            <div class="stat-label">Total {modulo.title()}</div>
        </div>
    </div>
    
    <div class="stat-card">
        <div class="stat-icon bg-green">
            <i class="fas fa-check-circle"></i>
        </div>
        <div class="stat-content">
            <div class="stat-number">{{{{ {modulo}|length or 0 }}}}</div>
            <div class="stat-label">Activos</div>
        </div>
    </div>
    
    <div class="stat-card">
        <div class="stat-icon bg-orange">
            <i class="fas fa-clock"></i>
        </div>
        <div class="stat-content">
            <div class="stat-number">0</div>
            <div class="stat-label">Pendientes</div>
        </div>
    </div>
</div>
'''
                    
                    # Insertar stats-grid después de page-header o al inicio
                    if 'page-header' in contenido_modificado:
                        # Buscar el cierre del page-header
                        patron = r'(<div class="page-header">.*?</div>\s*</div>)'
                        if re.search(patron, contenido_modificado, re.DOTALL):
                            contenido_modificado = re.sub(
                                patron, 
                                r'\1\n' + stats_grid,
                                contenido_modificado, 
                                flags=re.DOTALL
                            )
                            cambios.append("Stats-grid")
                
                # Para archivos de edición que necesitan create-forms.css y container
                if archivo == 'editar.html':
                    # Agregar CSS si no está
                    if 'create-forms.css' not in contenido_modificado:
                        if '{% block content %}' in contenido_modificado:
                            css_link = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/create-forms.css\') }}">\n\n'
                            contenido_modificado = contenido_modificado.replace(
                                '{% block content %}', 
                                f'{{% block content %}}\n{css_link}'
                            )
                            cambios.append("CSS")
                    
                    # Agregar container si no está
                    if 'create-form-container' not in contenido_modificado and '<form' in contenido_modificado:
                        # Buscar el formulario y envolverlo
                        patron_form = r'(<form[^>]*>)'
                        if re.search(patron_form, contenido_modificado):
                            contenido_modificado = re.sub(
                                patron_form,
                                r'<div class="create-form-container">\n\1',
                                contenido_modificado
                            )
                            # Cerrar container antes del endblock
                            contenido_modificado = re.sub(
                                r'(</form>\s*){% endblock %}',
                                r'\1</div>\n\n{% endblock %}',
                                contenido_modificado
                            )
                            cambios.append("Container")
                
                # Para proveedores que necesita page-header específicamente
                if modulo == 'proveedores' and archivo == 'listar.html' and 'page-header' not in contenido:
                    page_header = '''<div class="page-header">
    <div class="header-content">
        <div class="header-left">
            <h1 class="page-title">
                <i class="fas fa-truck"></i>
                Gestión de Proveedores
            </h1>
            <p class="page-subtitle">Control y administración de proveedores</p>
        </div>
        <div class="header-actions">
            <a href="{{ url_for('crear_proveedor') }}" class="btn btn-primary">
                <i class="fas fa-plus"></i>
                Nuevo Proveedor
            </a>
        </div>
    </div>
</div>

'''
                    
                    if '{% block content %}' in contenido_modificado:
                        contenido_modificado = contenido_modificado.replace(
                            '{% block content %}', 
                            f'{{% block content %}}\n{page_header}'
                        )
                        cambios.append("Page-header")
                
                # Guardar si hubo cambios
                if contenido_modificado != contenido:
                    with open(ruta_archivo, 'w', encoding='utf-8') as f:
                        f.write(contenido_modificado)
                    correcciones_aplicadas += len(cambios)
                    print(" ".join([f"✅ {cambio}" for cambio in cambios]))
                else:
                    print("⚪ Sin cambios")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print()
    
    print(f"📊 TOTAL DE CORRECCIONES APLICADAS: {correcciones_aplicadas}")
    print()
    print("✅ PROCESO COMPLETADO")
    print("💡 Ejecuta el análisis nuevamente para verificar las mejoras")
    
corregir_modulos_restantes()