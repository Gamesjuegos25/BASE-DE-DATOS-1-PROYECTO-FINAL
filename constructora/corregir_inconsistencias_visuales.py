import os
import re
from pathlib import Path

def corregir_template_base(ruta_template):
    """Corrige un template para que extienda base.html"""
    try:
        with open(ruta_template, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Si ya extiende base.html, no hacer nada
        if 'extends "base.html"' in contenido:
            return False, "Ya extiende base.html"
        
        # Agregar extends al inicio si es necesario
        if not contenido.strip().startswith('{% extends'):
            # Buscar DOCTYPE o <html> y agregar extends antes
            if 'DOCTYPE html' in contenido:
                contenido = '{% extends "base.html" %}\n\n' + contenido
            elif '<html' in contenido:
                contenido = '{% extends "base.html" %}\n\n' + contenido
            else:
                # Si no encuentra estructura HTML, agregar al inicio
                contenido = '{% extends "base.html" %}\n\n' + contenido
        
        with open(ruta_template, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return True, "Extends agregado"
        
    except Exception as e:
        return False, f"Error: {e}"

def agregar_page_header(ruta_template):
    """Agrega page-header a un template de listado"""
    try:
        with open(ruta_template, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        if 'page-header' in contenido:
            return False, "Ya tiene page-header"
        
        # Extraer nombre del módulo del path
        modulo = Path(ruta_template).parent.name.title()
        
        # Template básico de page-header
        page_header = f'''<div class="page-header">
    <div class="header-content">
        <div class="header-left">
            <h1 class="page-title">
                <i class="fas fa-list"></i>
                Gestión de {modulo}
            </h1>
            <p class="page-subtitle">Control y administración de {modulo.lower()}</p>
        </div>
        <div class="header-actions">
            <a href="{{{{ url_for('crear_{modulo.lower()[:-1]}') }}}}" class="btn btn-primary">
                <i class="fas fa-plus"></i>
                Nuevo {modulo[:-1]}
            </a>
        </div>
    </div>
</div>

'''
        
        # Buscar donde insertar (después de {% block content %})
        if '{% block content %}' in contenido:
            contenido = contenido.replace('{% block content %}', f'{{% block content %}}\n{page_header}')
        
        with open(ruta_template, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return True, "Page-header agregado"
        
    except Exception as e:
        return False, f"Error: {e}"

def agregar_stats_grid(ruta_template):
    """Agrega stats-grid a un template de listado"""
    try:
        with open(ruta_template, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        if 'stats-grid' in contenido:
            return False, "Ya tiene stats-grid"
        
        # Template básico de stats-grid
        stats_grid = '''<!-- Estadísticas del Módulo -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-icon bg-blue">
            <i class="fas fa-list"></i>
        </div>
        <div class="stat-content">
            <div class="stat-number">{{ datos|length or 0 }}</div>
            <div class="stat-label">Total Registros</div>
        </div>
    </div>
    
    <div class="stat-card">
        <div class="stat-icon bg-green">
            <i class="fas fa-check-circle"></i>
        </div>
        <div class="stat-content">
            <div class="stat-number">{{ datos|length or 0 }}</div>
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
        
        # Buscar donde insertar (después de page-header o al inicio del contenido)
        if 'page-header' in contenido:
            # Insertar después del cierre de page-header
            contenido = re.sub(r'</div>\s*</div>\s*(\n\s*<!-- [^>]+ -->)?', 
                             f'</div>\n</div>\n\n{stats_grid}', contenido, count=1)
        elif '{% block content %}' in contenido:
            contenido = contenido.replace('{% block content %}', f'{{% block content %}}\n{stats_grid}')
        
        with open(ruta_template, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return True, "Stats-grid agregado"
        
    except Exception as e:
        return False, f"Error: {e}"

def corregir_formulario(ruta_template):
    """Corrige formularios para usar create-forms.css y create-form-container"""
    try:
        with open(ruta_template, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        cambios_realizados = []
        
        # Agregar create-forms.css si no está
        if 'create-forms.css' not in contenido:
            if '{% block content %}' in contenido:
                css_link = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/create-forms.css\') }}">\n\n'
                contenido = contenido.replace('{% block content %}', f'{{% block content %}}\n{css_link}')
                cambios_realizados.append("CSS agregado")
        
        # Agregar create-form-container si no está
        if 'create-form-container' not in contenido:
            # Buscar formularios y envolverlos
            if '<form' in contenido and 'create-form-container' not in contenido:
                # Patrón básico para envolver el formulario
                contenido = re.sub(
                    r'(<form[^>]*>)',
                    r'<div class="create-form-container">\n\1',
                    contenido
                )
                # Cerrar el contenedor antes del {% endblock %}
                contenido = re.sub(
                    r'(</form>\s*){% endblock %}',
                    r'\1</div>\n\n{% endblock %}',
                    contenido
                )
                cambios_realizados.append("Container agregado")
        
        if cambios_realizados:
            with open(ruta_template, 'w', encoding='utf-8') as f:
                f.write(contenido)
            return True, ", ".join(cambios_realizados)
        else:
            return False, "No necesita cambios"
        
    except Exception as e:
        return False, f"Error: {e}"

# Directorio base
base_dir = Path("C:/Users/VICTUS/Videos/BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)/BASE-DE-DATOS-1-PROYECTO-FINAL-master/constructora/templates")

# Lista de correcciones aplicadas
correcciones_aplicadas = []

# Módulos que necesitan más atención (según el análisis previo)
modulos_criticos = [
    'incidentes', 'avances', 'movimientos', 'areas', 'bodegas', 
    'auditorias', 'actividades', 'bitacoras'
]

print("🔧 CORRECCIÓN AUTOMÁTICA DE INCONSISTENCIAS VISUALES")
print("=" * 60)
print()

for modulo in modulos_criticos:
    modulo_dir = base_dir / modulo
    if not modulo_dir.exists():
        continue
    
    print(f"🛠️  Corrigiendo módulo: {modulo.upper()}")
    
    for archivo in ['listar.html', 'crear.html', 'editar.html', 'detalle.html']:
        ruta_archivo = modulo_dir / archivo
        if not ruta_archivo.exists():
            continue
        
        print(f"   📝 {archivo}:", end=" ")
        
        # Corregir extends base.html
        resultado, mensaje = corregir_template_base(ruta_archivo)
        if resultado:
            correcciones_aplicadas.append(f"{modulo}/{archivo}: {mensaje}")
            print("✅ Base", end=" ")
        
        # Para archivos de listado
        if archivo == 'listar.html':
            # Agregar page-header
            resultado, mensaje = agregar_page_header(ruta_archivo)
            if resultado:
                correcciones_aplicadas.append(f"{modulo}/{archivo}: {mensaje}")
                print("✅ Header", end=" ")
            
            # Agregar stats-grid
            resultado, mensaje = agregar_stats_grid(ruta_archivo)
            if resultado:
                correcciones_aplicadas.append(f"{modulo}/{archivo}: {mensaje}")
                print("✅ Stats", end=" ")
        
        # Para formularios
        if archivo in ['crear.html', 'editar.html']:
            resultado, mensaje = corregir_formulario(ruta_archivo)
            if resultado:
                correcciones_aplicadas.append(f"{modulo}/{archivo}: {mensaje}")
                print("✅ Forms", end=" ")
        
        print()
    
    print()

print("📊 RESUMEN DE CORRECCIONES")
print("=" * 30)
print(f"Total de correcciones aplicadas: {len(correcciones_aplicadas)}")
print()

if correcciones_aplicadas:
    print("📋 Detalles de correcciones:")
    for correccion in correcciones_aplicadas[:20]:  # Mostrar solo las primeras 20
        print(f"  • {correccion}")
    
    if len(correcciones_aplicadas) > 20:
        print(f"  ... y {len(correcciones_aplicadas) - 20} correcciones más")

print()
print("✅ CORRECCIÓN COMPLETADA")
print("💡 Recomendación: Ejecutar nuevamente el análisis para verificar mejoras")
print("🚀 Reinicia el servidor Flask para ver los cambios aplicados")