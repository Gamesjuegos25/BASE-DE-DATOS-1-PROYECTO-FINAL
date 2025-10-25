#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar todos los formularios al estilo de obras, empleados y proyectos
Aplica el estilo visual consistente que extiende base.html con tarjetas organizadas
"""
import os
import glob

def generar_template_estilo_moderno(modulo, campos_especificos=None):
    """Genera un template con el estilo moderno de obras/empleados/proyectos"""
    
    # Campos por módulo (igual que antes pero con mejor estructura)
    campos_por_modulo = {
        'contratos': [
            {'name': 'numero_contrato', 'type': 'text', 'label': 'Número de Contrato', 'required': True, 'icon': 'fas fa-file-contract'},
            {'name': 'cliente_id', 'type': 'select', 'label': 'Cliente', 'required': True, 'options': 'clientes', 'icon': 'fas fa-user-tie'},
            {'name': 'obra_id', 'type': 'select', 'label': 'Obra', 'required': True, 'options': 'obras', 'icon': 'fas fa-building'},
            {'name': 'fecha_inicio', 'type': 'date', 'label': 'Fecha de Inicio', 'required': True, 'icon': 'fas fa-calendar-plus'},
            {'name': 'fecha_fin', 'type': 'date', 'label': 'Fecha de Fin', 'required': True, 'icon': 'fas fa-calendar-check'},
            {'name': 'valor_total', 'type': 'number', 'label': 'Valor Total', 'required': True, 'step': '0.01', 'icon': 'fas fa-dollar-sign'},
            {'name': 'estado', 'type': 'select', 'label': 'Estado', 'required': True, 'manual_options': ['activo', 'inactivo', 'completado'], 'icon': 'fas fa-flag'},
        ],
        'bitacoras': [
            {'name': 'obra_id', 'type': 'select', 'label': 'Obra', 'required': True, 'options': 'obras', 'icon': 'fas fa-building'},
            {'name': 'empleado_id', 'type': 'select', 'label': 'Empleado', 'required': True, 'options': 'empleados', 'icon': 'fas fa-user'},
            {'name': 'fecha', 'type': 'date', 'label': 'Fecha', 'required': True, 'icon': 'fas fa-calendar'},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción', 'required': True, 'rows': '4', 'icon': 'fas fa-align-left'},
            {'name': 'horas_trabajadas', 'type': 'number', 'label': 'Horas Trabajadas', 'required': True, 'step': '0.5', 'icon': 'fas fa-clock'},
            {'name': 'actividad', 'type': 'text', 'label': 'Actividad', 'required': True, 'icon': 'fas fa-tasks'},
        ],
        'bodegas': [
            {'name': 'nombre', 'type': 'text', 'label': 'Nombre de la Bodega', 'required': True, 'icon': 'fas fa-warehouse'},
            {'name': 'ubicacion', 'type': 'text', 'label': 'Ubicación', 'required': True, 'icon': 'fas fa-map-marker-alt'},
            {'name': 'capacidad_maxima', 'type': 'number', 'label': 'Capacidad Máxima', 'required': True, 'icon': 'fas fa-weight'},
            {'name': 'encargado', 'type': 'text', 'label': 'Encargado', 'required': False, 'icon': 'fas fa-user-tie'},
            {'name': 'telefono', 'type': 'tel', 'label': 'Teléfono', 'required': False, 'icon': 'fas fa-phone'},
            {'name': 'estado', 'type': 'select', 'label': 'Estado', 'required': True, 'manual_options': ['activa', 'inactiva', 'mantenimiento'], 'icon': 'fas fa-flag'},
        ],
        'avances': [
            {'name': 'obra_id', 'type': 'select', 'label': 'Obra', 'required': True, 'options': 'obras', 'icon': 'fas fa-building'},
            {'name': 'fecha', 'type': 'date', 'label': 'Fecha', 'required': True, 'icon': 'fas fa-calendar'},
            {'name': 'porcentaje_avance', 'type': 'number', 'label': 'Porcentaje de Avance (%)', 'required': True, 'min': '0', 'max': '100', 'step': '0.1', 'icon': 'fas fa-percentage'},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción del Avance', 'required': True, 'rows': '4', 'icon': 'fas fa-align-left'},
            {'name': 'observaciones', 'type': 'textarea', 'label': 'Observaciones', 'required': False, 'rows': '3', 'icon': 'fas fa-comment'},
        ],
        'areas': [
            {'name': 'nombre', 'type': 'text', 'label': 'Nombre del Área', 'required': True, 'icon': 'fas fa-layer-group'},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción', 'required': True, 'rows': '3', 'icon': 'fas fa-align-left'},
            {'name': 'responsable', 'type': 'text', 'label': 'Responsable', 'required': False, 'icon': 'fas fa-user-tie'},
            {'name': 'estado', 'type': 'select', 'label': 'Estado', 'required': True, 'manual_options': ['activa', 'inactiva'], 'icon': 'fas fa-flag'},
        ],
        'actividades': [
            {'name': 'nombre', 'type': 'text', 'label': 'Nombre de la Actividad', 'required': True, 'icon': 'fas fa-tasks'},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción', 'required': True, 'rows': '4', 'icon': 'fas fa-align-left'},
            {'name': 'area_id', 'type': 'select', 'label': 'Área', 'required': True, 'options': 'areas', 'icon': 'fas fa-layer-group'},
            {'name': 'duracion_estimada', 'type': 'number', 'label': 'Duración Estimada (horas)', 'required': False, 'step': '0.5', 'icon': 'fas fa-hourglass-half'},
            {'name': 'prioridad', 'type': 'select', 'label': 'Prioridad', 'required': True, 'manual_options': ['baja', 'media', 'alta', 'crítica'], 'icon': 'fas fa-exclamation-triangle'},
        ],
        'incidentes': [
            {'name': 'obra_id', 'type': 'select', 'label': 'Obra', 'required': True, 'options': 'obras', 'icon': 'fas fa-building'},
            {'name': 'empleado_id', 'type': 'select', 'label': 'Empleado Reportante', 'required': True, 'options': 'empleados', 'icon': 'fas fa-user'},
            {'name': 'fecha_incidente', 'type': 'datetime-local', 'label': 'Fecha y Hora del Incidente', 'required': True, 'icon': 'fas fa-calendar-times'},
            {'name': 'tipo_incidente', 'type': 'select', 'label': 'Tipo de Incidente', 'required': True, 'manual_options': ['accidente', 'seguridad', 'calidad', 'ambiental', 'otro'], 'icon': 'fas fa-exclamation-circle'},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción del Incidente', 'required': True, 'rows': '4', 'icon': 'fas fa-align-left'},
            {'name': 'gravedad', 'type': 'select', 'label': 'Gravedad', 'required': True, 'manual_options': ['leve', 'moderada', 'grave', 'crítica'], 'icon': 'fas fa-thermometer-half'},
        ],
        'movimientos': [
            {'name': 'bodega_id', 'type': 'select', 'label': 'Bodega', 'required': True, 'options': 'bodegas', 'icon': 'fas fa-warehouse'},
            {'name': 'material_id', 'type': 'select', 'label': 'Material', 'required': True, 'options': 'materiales', 'icon': 'fas fa-boxes'},
            {'name': 'tipo_movimiento', 'type': 'select', 'label': 'Tipo de Movimiento', 'required': True, 'manual_options': ['entrada', 'salida', 'transferencia'], 'icon': 'fas fa-exchange-alt'},
            {'name': 'cantidad', 'type': 'number', 'label': 'Cantidad', 'required': True, 'step': '0.01', 'icon': 'fas fa-sort-numeric-up'},
            {'name': 'fecha', 'type': 'date', 'label': 'Fecha', 'required': True, 'icon': 'fas fa-calendar'},
            {'name': 'responsable', 'type': 'text', 'label': 'Responsable', 'required': True, 'icon': 'fas fa-user'},
            {'name': 'observaciones', 'type': 'textarea', 'label': 'Observaciones', 'required': False, 'rows': '3', 'icon': 'fas fa-comment'},
        ],
        'permisos': [
            {'name': 'empleado_id', 'type': 'select', 'label': 'Empleado', 'required': True, 'options': 'empleados', 'icon': 'fas fa-user'},
            {'name': 'tipo_permiso', 'type': 'select', 'label': 'Tipo de Permiso', 'required': True, 'manual_options': ['vacaciones', 'enfermedad', 'personal', 'capacitacion', 'otro'], 'icon': 'fas fa-calendar-check'},
            {'name': 'fecha_inicio', 'type': 'date', 'label': 'Fecha de Inicio', 'required': True, 'icon': 'fas fa-calendar-plus'},
            {'name': 'fecha_fin', 'type': 'date', 'label': 'Fecha de Fin', 'required': True, 'icon': 'fas fa-calendar-minus'},
            {'name': 'motivo', 'type': 'textarea', 'label': 'Motivo', 'required': True, 'rows': '3', 'icon': 'fas fa-comment'},
            {'name': 'estado', 'type': 'select', 'label': 'Estado', 'required': True, 'manual_options': ['pendiente', 'aprobado', 'rechazado'], 'icon': 'fas fa-flag'},
        ],
        'requisiciones': [
            {'name': 'obra_id', 'type': 'select', 'label': 'Obra', 'required': True, 'options': 'obras', 'icon': 'fas fa-building'},
            {'name': 'empleado_id', 'type': 'select', 'label': 'Empleado Solicitante', 'required': True, 'options': 'empleados', 'icon': 'fas fa-user'},
            {'name': 'fecha_solicitud', 'type': 'date', 'label': 'Fecha de Solicitud', 'required': True, 'icon': 'fas fa-calendar'},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción', 'required': True, 'rows': '4', 'icon': 'fas fa-align-left'},
            {'name': 'cantidad_solicitada', 'type': 'number', 'label': 'Cantidad Solicitada', 'required': True, 'step': '0.01', 'icon': 'fas fa-sort-numeric-up'},
            {'name': 'prioridad', 'type': 'select', 'label': 'Prioridad', 'required': True, 'manual_options': ['baja', 'media', 'alta', 'urgente'], 'icon': 'fas fa-exclamation-triangle'},
            {'name': 'estado', 'type': 'select', 'label': 'Estado', 'required': True, 'manual_options': ['pendiente', 'aprobada', 'rechazada', 'entregada'], 'icon': 'fas fa-flag'},
        ],
        'tipos_obra': [
            {'name': 'nombre', 'type': 'text', 'label': 'Nombre del Tipo', 'required': True, 'icon': 'fas fa-tag'},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción', 'required': True, 'rows': '3', 'icon': 'fas fa-align-left'},
            {'name': 'categoria', 'type': 'select', 'label': 'Categoría', 'required': True, 'manual_options': ['residencial', 'comercial', 'industrial', 'infraestructura', 'otro'], 'icon': 'fas fa-layer-group'},
            {'name': 'duracion_promedio', 'type': 'number', 'label': 'Duración Promedio (meses)', 'required': False, 'step': '0.5', 'icon': 'fas fa-hourglass-half'},
        ]
    }
    
    campos = campos_especificos or campos_por_modulo.get(modulo, [])
    
    # Mapeo de endpoints correctos
    endpoint_map = {
        'tipos_obra': 'tipos_obra_nuevo',
        'actividades': 'crear_actividad',
        'requisiciones': 'crear_requisicion'
    }
    
    endpoint = endpoint_map.get(modulo, f'crear_{modulo.rstrip("s") if modulo.endswith("s") else modulo}')
    
    # Definir icono y título basado en el módulo
    iconos_modulos = {
        'actividades': 'fas fa-tasks',
        'areas': 'fas fa-layer-group', 
        'avances': 'fas fa-chart-line',
        'bitacoras': 'fas fa-book',
        'bodegas': 'fas fa-warehouse',
        'contratos': 'fas fa-file-contract',
        'incidentes': 'fas fa-exclamation-triangle',
        'movimientos': 'fas fa-exchange-alt',
        'permisos': 'fas fa-calendar-check',
        'requisiciones': 'fas fa-clipboard-list',
        'tipos_obra': 'fas fa-tags',
    }
    
    icono = iconos_modulos.get(modulo, 'fas fa-plus-circle')
    titulo = modulo.replace('_', ' ').title().replace('s', '') if modulo.endswith('s') else modulo.title()
    
    template = f'''{{%extends "base.html"%}}

{{%block title%}}Nuevo {titulo} - Sistema Constructora{{%endblock%}}

{{%block content%}}'''
<link rel="stylesheet" href="{{{{ url_for('static', filename='css/create-forms.css') }}}}">

<div class="create-form-container">
    <!-- Header de página estilo detalle -->
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{{{ url_for('dashboard') }}}}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{{{ url_for('listar_{modulo}') }}}}">{modulo.capitalize()}</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nuevo</span>
        </nav>
        <h1 class="create-page-title">
            <i class="{icono}"></i>
            Crear Nuevo {titulo}
        </h1>
    </div>

    <div class="container-fluid">
        <form method="POST" action="{{{{ url_for('{endpoint}') }}}}" id="create-{modulo}-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <!-- Información General -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-info-circle"></i> Información General</h5>
                    </div>
                    <div class="card-body">'''.format(modulo.capitalize(), endpoint=endpoint, titulo=titulo, icono=icono, modulo=modulo)

    # Generar campos organizados en grupos
    for i, campo in enumerate(campos):
        template += f'''
                        <div class="create-form-group">
                            <label for="{campo["name"]}" class="create-form-label">
                                <i class="{campo.get("icon", "fas fa-edit")}"></i>{campo["label"]}'''
        
        if campo.get("required"):
            template += '<span class="required">*</span>'
        
        template += '''
                            </label>'''
        
        # Generar el input según el tipo
        if campo["type"] == "select":
            template += f'''
                            <select class="create-form-control" id="{campo["name"]}" name="{campo["name"]}"'''
            if campo.get("required"):
                template += ' required'
            template += f''' placeholder="Seleccione {campo["label"].lower()}">
                                <option value="">Seleccione una opción</option>'''
            
            if campo.get("options"):
                template += f'''
                                {{%- for item in {campo["options"]} %}}
                                <option value="{{{{ item[0] }}}}" {{{{ 'selected' if request.form.{campo["name"]} == item[0]|string else '' }}}}>{{{{ item[1] }}</option>
                                {{%- endfor %}}'''
            elif campo.get("manual_options"):
                for opcion in campo["manual_options"]:
                    template += f'''
                                <option value="{opcion}" {{{{ 'selected' if request.form.{campo["name"]} == '{opcion}' else '' }}}}>{opcion.replace("_", " ").title()}</option>'''
            
            template += '''
                            </select>'''
            
        elif campo["type"] == "textarea":
            template += f'''
                            <textarea class="create-form-control" id="{campo["name"]}" name="{campo["name"]}"'''
            if campo.get("rows"):
                template += f' rows="{campo["rows"]}"'
            if campo.get("required"):
                template += ' required'
            template += f''' placeholder="Ingrese {campo["label"].lower()}">{{{{ request.form.{campo["name"]} if request.form else '' }}</textarea>'''
            
        else:
            template += f'''
                            <input type="{campo["type"]}" class="create-form-control" id="{campo["name"]}" name="{campo["name"]}"'''
            if campo.get("required"):
                template += ' required'
            if campo.get("step"):
                template += f' step="{campo["step"]}"'
            if campo.get("min"):
                template += f' min="{campo["min"]}"'
            if campo.get("max"):
                template += f' max="{campo["max"]}"'
            template += f''' placeholder="Ingrese {campo["label"].lower()}"
                                   value="{{{{ request.form.{campo["name"]} if request.form else '' }}}}">'''
        
        template += f'''
                            <div class="invalid-feedback">
                                Por favor, ingrese {campo["label"].lower()}.
                            </div>
                        </div>'''

    # Cerrar el formulario
    template += f'''
                    </div>
                </div>
            </div>
            
            <!-- Botones de acción -->
            <div class="form-actions mt-4">
                <div class="d-flex justify-content-between">
                    <a href="{{{{ url_for('listar_{modulo}') }}}}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Guardar {titulo}
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>

<script>
// Validación de formularios Bootstrap
(function() {{
    'use strict';
    window.addEventListener('load', function() {{
        var forms = document.getElementsByClassName('needs-validation');
        var validation = Array.prototype.filter.call(forms, function(form) {{
            form.addEventListener('submit', function(event) {{
                if (form.checkValidity() === false) {{
                    event.preventDefault();
                    event.stopPropagation();
                }}
                form.classList.add('was-validated');
            }}, false);
        }});
    }}, false);
}})();
</script>
{{%- endblock %}}'''
    
    return template

def actualizar_formularios_estilo_moderno():
    """Actualiza todos los formularios al estilo moderno de obras/empleados/proyectos"""
    print("🎨 Actualizando formularios al estilo visual moderno...")
    print("=" * 60)
    
    # Obtener todos los formularios excepto los que ya están bien
    formularios_excluir = ['empleados', 'proyectos', 'obras', 'vehiculos', 'materiales', 'proveedores', 'equipos', 'facturas']
    
    crear_files = glob.glob("templates/*/crear.html")
    formularios_a_actualizar = []
    
    for archivo in crear_files:
        modulo = archivo.replace("\\", "/").split("/")[-2]
        if modulo not in formularios_excluir:
            formularios_a_actualizar.append(modulo)
    
    print(f"📋 Formularios a actualizar: {len(formularios_a_actualizar)}")
    for modulo in formularios_a_actualizar:
        print(f"   • {modulo}")
    
    print("\n🔄 Iniciando actualización...")
    print("=" * 60)
    
    exitosos = 0
    fallidos = 0
    
    for modulo in formularios_a_actualizar:
        try:
            print(f"🎨 Actualizando {modulo}...")
            
            template_moderno = generar_template_estilo_moderno(modulo)
            archivo = f"templates/{modulo}/crear.html"
            
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(template_moderno)
                
            print(f"   ✅ {modulo} actualizado correctamente")
            exitosos += 1
            
        except Exception as e:
            print(f"   ❌ Error al actualizar {modulo}: {e}")
            fallidos += 1
    
    print("=" * 60)
    print("📊 Resultado final:")
    print(f"   ✅ Exitosos: {exitosos}")
    print(f"   ❌ Fallidos:  {fallidos}")
    
    if fallidos == 0:
        print("\\n🎉 ¡Todos los formularios han sido actualizados al estilo moderno!")
        print("   • Extienden base.html para navegación consistente")
        print("   • Estructura de tarjetas organizadas")
        print("   • Breadcrumb simplificado y elegante")
        print("   • Iconos Font Awesome para mejor UX")
        print("   • Validación Bootstrap integrada")

def main():
    """Función principal"""
    print("🚀 Modernizando formularios al estilo de obras/empleados/proyectos...")
    print("=" * 60)
    
    actualizar_formularios_estilo_moderno()

if __name__ == "__main__":
    main()