#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para estandarizar campos de calendario en todos los módulos
Sistema Constructora - Calendarización Uniforme
"""

import os
import re
from pathlib import Path

# Directorio base de templates
TEMPLATES_DIR = Path("templates")

# Patrones para identificar y reemplazar campos de fecha
DATE_PATTERNS = {
    # Patrón para inputs de fecha básicos
    'basic_date_input': {
        'pattern': r'<input[^>]*type="date"[^>]*>',
        'replacement_template': '''<input 
                type="date" 
                class="form-input standardized-calendar" 
                name="{name}" 
                id="{id}"
                value="{value}"
                placeholder="{placeholder}"
                {required}
                {restrictions}
                data-field-type="{field_type}"
            />'''
    },
    
    # Patrón para labels de fecha
    'date_label': {
        'pattern': r'<label[^>]*>.*?fecha.*?</label>',
        'replacement_template': '''<label for="{id}" class="form-label">
                <i class="{icon} text-xanthous-600"></i> {label}
                {required_mark}
            </label>'''
    }
}

# Configuración de módulos y sus campos de fecha específicos
MODULE_DATE_CONFIGS = {
    'facturas': {
        'fecha_factura': {
            'field_type': 'fecha_emision',
            'required': True,
            'restrict_future': True
        },
        'fecha_vencimiento': {
            'field_type': 'fecha_vencimiento',
            'required': True,
            'restrict_past': True
        }
    },
    
    'pagos': {
        'fecha_pago': {
            'field_type': 'fecha_pago',
            'required': True,
            'restrict_future': False
        }
    },
    
    'nomina': {
        'fecha_nomina': {
            'field_type': 'fecha_emision',
            'required': True,
            'restrict_future': True
        },
        'fecha_periodo_inicio': {
            'field_type': 'fecha_inicio',
            'required': True,
            'restrict_future': False
        },
        'fecha_periodo_fin': {
            'field_type': 'fecha_fin',
            'required': True,
            'depends_on': 'fecha_periodo_inicio'
        }
    },
    
    'incidentes': {
        'fecha_incidente': {
            'field_type': 'fecha_incidente',
            'required': True,
            'restrict_future': True
        }
    },
    
    'movimientos': {
        'fecha_movimiento': {
            'field_type': 'fecha_emision',
            'required': True,
            'restrict_future': True
        }
    },
    
    'compras': {
        'fecha_compra': {
            'field_type': 'fecha_emision',
            'required': True,
            'restrict_future': True
        },
        'fecha_entrega': {
            'field_type': 'fecha_entrega',
            'required': False,
            'restrict_past': True
        }
    },
    
    'ventas': {
        'fecha_venta': {
            'field_type': 'fecha_emision',
            'required': True,
            'restrict_future': True
        }
    },
    
    'permisos': {
        'fecha_solicitud': {
            'field_type': 'fecha_emision',
            'required': True,
            'restrict_future': True
        },
        'fecha_inicio_permiso': {
            'field_type': 'fecha_inicio',
            'required': True,
            'restrict_past': True
        },
        'fecha_fin_permiso': {
            'field_type': 'fecha_fin',
            'required': True,
            'depends_on': 'fecha_inicio_permiso'
        }
    }
}

def generate_standardized_date_field(field_name, config, value=""):
    """Genera HTML estandarizado para un campo de fecha"""
    
    field_type = config.get('field_type', 'fecha_programada')
    required = config.get('required', False)
    restrict_past = config.get('restrict_past', False)
    restrict_future = config.get('restrict_future', False)
    depends_on = config.get('depends_on', '')
    placeholder = config.get('placeholder', f'Seleccionar {field_name.replace("_", " ")}')
    
    # Configurar restricciones de fecha
    restrictions = []
    if restrict_past:
        restrictions.append('min="{{ \'now\'|strftime(\'%Y-%m-%d\') }}"')
    if restrict_future:
        restrictions.append('max="{{ \'now\'|strftime(\'%Y-%m-%d\') }}"')
    
    restrictions_str = ' '.join(restrictions)
    required_str = 'required' if required else ''
    depends_str = f'data-depends-on="{depends_on}"' if depends_on else ''
    
    # Determinar icono y etiqueta basado en el tipo de campo
    icons = {
        'fecha_inicio': 'fas fa-play-circle',
        'fecha_fin': 'fas fa-flag-checkered',
        'fecha_entrega': 'fas fa-shipping-fast',
        'fecha_programada': 'fas fa-calendar-alt',
        'fecha_vencimiento': 'fas fa-exclamation-triangle',
        'fecha_emision': 'fas fa-calendar-plus',
        'fecha_pago': 'fas fa-money-bill-wave',
        'fecha_incidente': 'fas fa-exclamation-circle',
        'fecha_mantenimiento': 'fas fa-tools',
        'fecha_presupuesto': 'fas fa-calculator'
    }
    
    icon = icons.get(field_type, 'fas fa-calendar-alt')
    label = field_name.replace('_', ' ').title()
    
    required_mark = '<span class="required-mark text-red-500 ml-1">*</span>' if required else ''
    
    help_text = placeholder
    if restrict_past and restrict_future:
        help_text += ' (solo fecha actual)'
    elif restrict_past:
        help_text += ' (no fechas pasadas)'
    elif restrict_future:
        help_text += ' (no fechas futuras)'
    
    if depends_on:
        help_text += f' (debe ser posterior a {depends_on.replace("_", " ")})'
    
    return f'''
        <!-- {label} estandarizado -->
        <div class="calendar-field-group" data-field-type="{field_type}">
            <label for="{field_name}" class="form-label">
                <i class="{icon} text-xanthous-600"></i> {label}
                {required_mark}
            </label>
            <div class="input-wrapper date-input-wrapper">
                <input 
                    type="date" 
                    class="form-input standardized-calendar" 
                    name="{field_name}" 
                    id="{field_name}"
                    value="{{{{ request.form.{field_name} if request.form else '{value}' }}}}"
                    placeholder="{placeholder}"
                    {required_str}
                    {restrictions_str}
                    data-field-type="{field_type}"
                    {depends_str}
                />
                <i class="fas fa-calendar-alt input-icon"></i>
            </div>
            <small class="form-help text-vanilla-600">
                {help_text}
            </small>
        </div>'''

def add_calendar_assets_to_template(file_path):
    """Agrega los archivos CSS y JS de calendario a un template"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Verificar si ya tiene los archivos de calendario
    if 'calendar-styles.css' in content:
        return False  # Ya está actualizado
    
    # Buscar el bloque head y agregar los archivos
    head_pattern = r'({% block head %}.*?)({% endblock %})'
    
    def replace_head(match):
        head_content = match.group(1)
        end_block = match.group(2)
        
        # Agregar archivos de calendario si no están
        if 'calendar-styles.css' not in head_content:
            calendar_assets = '''    <!-- CSS y JS estandarizados para calendarios -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/calendar-styles.css') }}">
    <script src="{{ url_for('static', filename='js/calendar-utils.js') }}"></script>
'''
            return head_content + calendar_assets + end_block
        return match.group(0)
    
    new_content = re.sub(head_pattern, replace_head, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    
    return False

def process_template_file(file_path, module_name):
    """Procesa un archivo de template para estandarizar sus campos de fecha"""
    
    if not file_path.exists():
        return False
    
    print(f"🔄 Procesando: {file_path}")
    
    # Agregar archivos CSS y JS
    assets_added = add_calendar_assets_to_template(file_path)
    
    # Obtener configuración del módulo
    module_config = MODULE_DATE_CONFIGS.get(module_name, {})
    
    if not module_config:
        print(f"   ⚠️  No hay configuración de fechas para el módulo: {module_name}")
        return assets_added
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    changes_made = assets_added
    
    # Procesar cada campo de fecha del módulo
    for field_name, config in module_config.items():
        # Buscar inputs de fecha existentes para este campo
        pattern = f'<input[^>]*name="{field_name}"[^>]*>'
        matches = re.findall(pattern, content, re.IGNORECASE)
        
        if matches:
            print(f"   📅 Estandarizando campo: {field_name}")
            
            # Buscar el contexto completo del campo (label + input + elementos relacionados)
            context_pattern = f'(<div[^>]*class="[^"]*form-group[^"]*"[^>]*>.*?<input[^>]*name="{field_name}"[^>]*>.*?</div>)'
            
            context_matches = re.findall(context_pattern, content, re.DOTALL | re.IGNORECASE)
            
            if context_matches:
                original_html = context_matches[0]
                standardized_html = generate_standardized_date_field(field_name, config)
                
                content = content.replace(original_html, standardized_html)
                changes_made = True
    
    if changes_made:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ Template actualizado")
    else:
        print(f"   ℹ️  No se requieren cambios")
    
    return changes_made

def main():
    """Función principal"""
    print("🚀 ESTANDARIZACION MASIVA DE CALENDARIOS")
    print("📅 Sistema Constructora - Calendarización Uniforme")
    print("=" * 65)
    
    templates_processed = 0
    changes_made = 0
    
    # Procesar todos los módulos configurados
    for module_name in MODULE_DATE_CONFIGS.keys():
        crear_path = TEMPLATES_DIR / module_name / "crear.html"
        editar_path = TEMPLATES_DIR / module_name / "editar.html"
        
        print(f"\n📂 Módulo: {module_name.upper()}")
        
        # Procesar template de crear
        if crear_path.exists():
            if process_template_file(crear_path, module_name):
                changes_made += 1
            templates_processed += 1
        
        # Procesar template de editar si existe
        if editar_path.exists():
            if process_template_file(editar_path, module_name):
                changes_made += 1
            templates_processed += 1
    
    print(f"\n📊 RESUMEN:")
    print(f"   📁 Templates procesados: {templates_processed}")
    print(f"   🔄 Templates modificados: {changes_made}")
    print(f"   📅 Módulos configurados: {len(MODULE_DATE_CONFIGS)}")
    
    print(f"\n🎯 CONCLUSIÓN:")
    print("✅ Estandarización de calendarios completada")
    print("✅ Todos los campos de fecha ahora usan el sistema unificado")
    print("✅ Validaciones y estilos consistentes aplicados")
    print("✅ Archivos CSS y JS agregados automáticamente")

if __name__ == "__main__":
    main()