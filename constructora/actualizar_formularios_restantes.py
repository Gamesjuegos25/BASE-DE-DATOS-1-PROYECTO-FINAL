#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar los formularios de creación restantes con el estilo moderno
"""
import os
import glob
import re

def verificar_formularios_actualizados():
    """Verifica cuáles formularios ya están actualizados con el nuevo estilo"""
    
    formularios_actualizados = []
    formularios_pendientes = []
    
    crear_files = glob.glob("templates/*/crear.html")
    
    print("🔍 Verificando estado de formularios de creación...")
    print("=" * 60)
    
    for archivo in crear_files:
        # Normalizar la ruta para trabajar con ambos separadores
        archivo_normalizado = archivo.replace("\\", "/")
        modulo = archivo_normalizado.split("/")[-2]  # Extrae el nombre del módulo
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
                
            # Verificar si ya tiene el nuevo estilo
            tiene_nuevo_css = 'create-forms.css' in contenido
            tiene_estructura_moderna = 'create-form-container' in contenido
            
            if tiene_nuevo_css and tiene_estructura_moderna:
                formularios_actualizados.append(modulo)
                print(f"✅ {modulo:15} - Ya actualizado")
            else:
                formularios_pendientes.append(modulo)
                print(f"❌ {modulo:15} - Pendiente de actualización")
                
        except Exception as e:
            print(f"⚠️  {modulo:15} - Error al verificar: {e}")
            formularios_pendientes.append(modulo)
    
    print("=" * 60)
    print(f"📊 Resumen:")
    print(f"   ✅ Actualizados: {len(formularios_actualizados)}")
    print(f"   ❌ Pendientes:   {len(formularios_pendientes)}")
    
    return formularios_actualizados, formularios_pendientes

def generar_template_moderno(modulo, campos_especificos=None):
    """Genera un template moderno para el módulo especificado"""
    
    # Campos comunes para diferentes módulos
    campos_por_modulo = {
        'contratos': [
            {'name': 'numero_contrato', 'type': 'text', 'label': 'Número de Contrato', 'required': True},
            {'name': 'cliente_id', 'type': 'select', 'label': 'Cliente', 'required': True, 'options': 'clientes'},
            {'name': 'obra_id', 'type': 'select', 'label': 'Obra', 'required': True, 'options': 'obras'},
            {'name': 'fecha_inicio', 'type': 'date', 'label': 'Fecha de Inicio', 'required': True},
            {'name': 'fecha_fin', 'type': 'date', 'label': 'Fecha de Fin', 'required': True},
            {'name': 'valor_total', 'type': 'number', 'label': 'Valor Total', 'required': True, 'step': '0.01'},
            {'name': 'estado', 'type': 'select', 'label': 'Estado', 'required': True, 'manual_options': ['activo', 'inactivo', 'completado']},
        ],
        'bitacoras': [
            {'name': 'obra_id', 'type': 'select', 'label': 'Obra', 'required': True, 'options': 'obras'},
            {'name': 'empleado_id', 'type': 'select', 'label': 'Empleado', 'required': True, 'options': 'empleados'},
            {'name': 'fecha', 'type': 'date', 'label': 'Fecha', 'required': True},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción', 'required': True, 'rows': '4'},
            {'name': 'horas_trabajadas', 'type': 'number', 'label': 'Horas Trabajadas', 'required': True, 'step': '0.5'},
            {'name': 'actividad', 'type': 'text', 'label': 'Actividad', 'required': True},
        ],
        'bodegas': [
            {'name': 'nombre', 'type': 'text', 'label': 'Nombre de la Bodega', 'required': True},
            {'name': 'ubicacion', 'type': 'text', 'label': 'Ubicación', 'required': True},
            {'name': 'capacidad_maxima', 'type': 'number', 'label': 'Capacidad Máxima', 'required': True},
            {'name': 'encargado', 'type': 'text', 'label': 'Encargado', 'required': False},
            {'name': 'telefono', 'type': 'tel', 'label': 'Teléfono', 'required': False},
            {'name': 'estado', 'type': 'select', 'label': 'Estado', 'required': True, 'manual_options': ['activa', 'inactiva', 'mantenimiento']},
        ],
        'avances': [
            {'name': 'obra_id', 'type': 'select', 'label': 'Obra', 'required': True, 'options': 'obras'},
            {'name': 'fecha', 'type': 'date', 'label': 'Fecha', 'required': True},
            {'name': 'porcentaje_avance', 'type': 'number', 'label': 'Porcentaje de Avance (%)', 'required': True, 'min': '0', 'max': '100', 'step': '0.1'},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción del Avance', 'required': True, 'rows': '4'},
            {'name': 'observaciones', 'type': 'textarea', 'label': 'Observaciones', 'required': False, 'rows': '3'},
        ],
        'areas': [
            {'name': 'nombre', 'type': 'text', 'label': 'Nombre del Área', 'required': True},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción', 'required': True, 'rows': '3'},
            {'name': 'responsable', 'type': 'text', 'label': 'Responsable', 'required': False},
            {'name': 'estado', 'type': 'select', 'label': 'Estado', 'required': True, 'manual_options': ['activa', 'inactiva']},
        ],
        'actividades': [
            {'name': 'nombre', 'type': 'text', 'label': 'Nombre de la Actividad', 'required': True},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción', 'required': True, 'rows': '4'},
            {'name': 'area_id', 'type': 'select', 'label': 'Área', 'required': True, 'options': 'areas'},
            {'name': 'duracion_estimada', 'type': 'number', 'label': 'Duración Estimada (horas)', 'required': False, 'step': '0.5'},
            {'name': 'prioridad', 'type': 'select', 'label': 'Prioridad', 'required': True, 'manual_options': ['baja', 'media', 'alta', 'crítica']},
        ],
        'incidentes': [
            {'name': 'obra_id', 'type': 'select', 'label': 'Obra', 'required': True, 'options': 'obras'},
            {'name': 'empleado_id', 'type': 'select', 'label': 'Empleado Reportante', 'required': True, 'options': 'empleados'},
            {'name': 'fecha_incidente', 'type': 'datetime-local', 'label': 'Fecha y Hora del Incidente', 'required': True},
            {'name': 'tipo_incidente', 'type': 'select', 'label': 'Tipo de Incidente', 'required': True, 'manual_options': ['accidente', 'seguridad', 'calidad', 'ambiental', 'otro']},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción del Incidente', 'required': True, 'rows': '4'},
            {'name': 'gravedad', 'type': 'select', 'label': 'Gravedad', 'required': True, 'manual_options': ['leve', 'moderada', 'grave', 'crítica']},
        ],
        'movimientos': [
            {'name': 'bodega_id', 'type': 'select', 'label': 'Bodega', 'required': True, 'options': 'bodegas'},
            {'name': 'material_id', 'type': 'select', 'label': 'Material', 'required': True, 'options': 'materiales'},
            {'name': 'tipo_movimiento', 'type': 'select', 'label': 'Tipo de Movimiento', 'required': True, 'manual_options': ['entrada', 'salida', 'transferencia']},
            {'name': 'cantidad', 'type': 'number', 'label': 'Cantidad', 'required': True, 'step': '0.01'},
            {'name': 'fecha', 'type': 'date', 'label': 'Fecha', 'required': True},
            {'name': 'responsable', 'type': 'text', 'label': 'Responsable', 'required': True},
            {'name': 'observaciones', 'type': 'textarea', 'label': 'Observaciones', 'required': False, 'rows': '3'},
        ],
        'obras': [
            {'name': 'nombre', 'type': 'text', 'label': 'Nombre de la Obra', 'required': True},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción', 'required': True, 'rows': '4'},
            {'name': 'ubicacion', 'type': 'text', 'label': 'Ubicación', 'required': True},
            {'name': 'fecha_inicio', 'type': 'date', 'label': 'Fecha de Inicio', 'required': True},
            {'name': 'fecha_fin_estimada', 'type': 'date', 'label': 'Fecha de Fin Estimada', 'required': True},
            {'name': 'presupuesto', 'type': 'number', 'label': 'Presupuesto', 'required': True, 'step': '0.01'},
            {'name': 'tipo_obra_id', 'type': 'select', 'label': 'Tipo de Obra', 'required': True, 'options': 'tipos_obra'},
            {'name': 'estado', 'type': 'select', 'label': 'Estado', 'required': True, 'manual_options': ['planificada', 'en_progreso', 'suspendida', 'completada']},
        ],
        'permisos': [
            {'name': 'empleado_id', 'type': 'select', 'label': 'Empleado', 'required': True, 'options': 'empleados'},
            {'name': 'tipo_permiso', 'type': 'select', 'label': 'Tipo de Permiso', 'required': True, 'manual_options': ['vacaciones', 'enfermedad', 'personal', 'capacitacion', 'otro']},
            {'name': 'fecha_inicio', 'type': 'date', 'label': 'Fecha de Inicio', 'required': True},
            {'name': 'fecha_fin', 'type': 'date', 'label': 'Fecha de Fin', 'required': True},
            {'name': 'motivo', 'type': 'textarea', 'label': 'Motivo', 'required': True, 'rows': '3'},
            {'name': 'estado', 'type': 'select', 'label': 'Estado', 'required': True, 'manual_options': ['pendiente', 'aprobado', 'rechazado']},
        ],
        'requisiciones': [
            {'name': 'obra_id', 'type': 'select', 'label': 'Obra', 'required': True, 'options': 'obras'},
            {'name': 'empleado_id', 'type': 'select', 'label': 'Empleado Solicitante', 'required': True, 'options': 'empleados'},
            {'name': 'fecha_solicitud', 'type': 'date', 'label': 'Fecha de Solicitud', 'required': True},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción', 'required': True, 'rows': '4'},
            {'name': 'cantidad_solicitada', 'type': 'number', 'label': 'Cantidad Solicitada', 'required': True, 'step': '0.01'},
            {'name': 'prioridad', 'type': 'select', 'label': 'Prioridad', 'required': True, 'manual_options': ['baja', 'media', 'alta', 'urgente']},
            {'name': 'estado', 'type': 'select', 'label': 'Estado', 'required': True, 'manual_options': ['pendiente', 'aprobada', 'rechazada', 'entregada']},
        ],
        'tipos_obra': [
            {'name': 'nombre', 'type': 'text', 'label': 'Nombre del Tipo', 'required': True},
            {'name': 'descripcion', 'type': 'textarea', 'label': 'Descripción', 'required': True, 'rows': '3'},
            {'name': 'categoria', 'type': 'select', 'label': 'Categoría', 'required': True, 'manual_options': ['residencial', 'comercial', 'industrial', 'infraestructura', 'otro']},
            {'name': 'duracion_promedio', 'type': 'number', 'label': 'Duración Promedio (meses)', 'required': False, 'step': '0.5'},
        ]
    }
    
    campos = campos_especificos or campos_por_modulo.get(modulo, [])
    
    template = f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crear {modulo.capitalize()} - Sistema Constructora</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="{{{{ url_for('static', filename='css/styles.css') }}}}" rel="stylesheet">
    <link href="{{{{ url_for('static', filename='css/create-forms.css') }}}}" rel="stylesheet">
</head>
<body>
    <div class="create-form-container">
        <!-- Header -->
        <div class="create-page-header">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item">
                        <a href="{{{{ url_for('dashboard') }}}}">
                            <i class="fas fa-home"></i> Dashboard
                        </a>
                    </li>
                    <li class="breadcrumb-item">
                        <a href="{{{{ url_for('listar_{modulo}') }}}}">
                            <i class="fas fa-list"></i> {modulo.capitalize()}
                        </a>
                    </li>
                    <li class="breadcrumb-item active" aria-current="page">
                        <i class="fas fa-plus"></i> Crear {modulo.capitalize()[:-1] if modulo.endswith('s') else modulo.capitalize()}
                    </li>
                </ol>
            </nav>
            
            <div class="create-title-section">
                <h1 class="create-title">
                    <i class="fas fa-plus-circle"></i>
                    Crear {modulo.capitalize()[:-1] if modulo.endswith('s') else modulo.capitalize()}
                </h1>
                <p class="create-subtitle">Complete el formulario para registrar {('un nuevo ' if modulo in ['contratos', 'equipos', 'materiales', 'vehiculos', 'empleados', 'proveedores', 'proyectos'] else 'una nueva ') + (modulo[:-1] if modulo.endswith('s') else modulo)}</p>
            </div>
        </div>

        <!-- Formulario -->
        <div class="create-form-card">
            <form method="POST" action="{{{{ url_for('crear_{modulo.rstrip("s") if modulo.endswith("s") else modulo}') }}}}" class="needs-validation" novalidate>
'''

    # Generar campos en filas de 2 columnas
    for i in range(0, len(campos), 2):
        template += '                <div class="create-form-row">\n'
        
        for j in range(2):
            if i + j < len(campos):
                campo = campos[i + j]
                template += f'                    <div class="create-form-group">\n'
                template += f'                        <label for="{campo["name"]}" class="form-label">\n'
                template += f'                            {campo["label"]}'
                if campo.get("required"):
                    template += ' <span class="required">*</span>'
                template += '\n                        </label>\n'
                
                # Generar el input según el tipo
                if campo["type"] == "select":
                    template += f'                        <select class="form-select" id="{campo["name"]}" name="{campo["name"]}"'
                    if campo.get("required"):
                        template += ' required'
                    template += '>\n'
                    template += '                            <option value="">Seleccione una opción</option>\n'
                    
                    if campo.get("options"):
                        template += f'                            {{%- for item in {campo["options"]} %}}\n'
                        template += '                            <option value="{{ item[0] }}">{{ item[1] }}</option>\n'
                        template += '                            {%- endfor %}\n'
                    elif campo.get("manual_options"):
                        for opcion in campo["manual_options"]:
                            template += f'                            <option value="{opcion}">{opcion.replace("_", " ").title()}</option>\n'
                    
                    template += '                        </select>\n'
                    
                elif campo["type"] == "textarea":
                    template += f'                        <textarea class="form-control" id="{campo["name"]}" name="{campo["name"]}"'
                    if campo.get("rows"):
                        template += f' rows="{campo["rows"]}"'
                    if campo.get("required"):
                        template += ' required'
                    template += f' placeholder="Ingrese {campo["label"].lower()}"></textarea>\n'
                    
                else:
                    template += f'                        <input type="{campo["type"]}" class="form-control" id="{campo["name"]}" name="{campo["name"]}"'
                    if campo.get("required"):
                        template += ' required'
                    if campo.get("step"):
                        template += f' step="{campo["step"]}"'
                    if campo.get("min"):
                        template += f' min="{campo["min"]}"'
                    if campo.get("max"):
                        template += f' max="{campo["max"]}"'
                    template += f' placeholder="Ingrese {campo["label"].lower()}">\n'
                
                template += '                        <div class="invalid-feedback">\n'
                template += f'                            Por favor ingrese {campo["label"].lower()}.\n'
                template += '                        </div>\n'
                template += '                    </div>\n'
        
        template += '                </div>\n'

    # Cerrar el formulario
    template += '''
                <!-- Botones de acción -->
                <div class="create-form-actions">
                    <div class="action-buttons">
                        <a href="{{ url_for('listar_''' + modulo + '''') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-times"></i> Cancelar
                        </a>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save"></i> Guardar ''' + (modulo.capitalize()[:-1] if modulo.endswith('s') else modulo.capitalize()) + '''
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Validación de formularios Bootstrap
        (function() {
            'use strict';
            window.addEventListener('load', function() {
                var forms = document.getElementsByClassName('needs-validation');
                var validation = Array.prototype.filter.call(forms, function(form) {
                    form.addEventListener('submit', function(event) {
                        if (form.checkValidity() === false) {
                            event.preventDefault();
                            event.stopPropagation();
                        }
                        form.classList.add('was-validated');
                    }, false);
                });
            }, false);
        })();
    </script>
</body>
</html>'''
    
    return template

def actualizar_formulario(modulo):
    """Actualiza un formulario específico"""
    print(f"🔄 Actualizando formulario: {modulo}")
    
    template_moderno = generar_template_moderno(modulo)
    archivo = f"templates/{modulo}/crear.html"
    
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            f.write(template_moderno)
        print(f"   ✅ {modulo} actualizado correctamente")
        return True
    except Exception as e:
        print(f"   ❌ Error al actualizar {modulo}: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando actualización de formularios restantes...")
    print("=" * 60)
    
    # Verificar estado actual
    actualizados, pendientes = verificar_formularios_actualizados()
    
    if not pendientes:
        print("🎉 ¡Todos los formularios ya están actualizados!")
        return
    
    print(f"\n🎯 Actualizando {len(pendientes)} formularios pendientes...")
    print("=" * 60)
    
    exitosos = 0
    fallidos = 0
    
    for modulo in pendientes:
        if actualizar_formulario(modulo):
            exitosos += 1
        else:
            fallidos += 1
    
    print("=" * 60)
    print("📊 Resultado final:")
    print(f"   ✅ Exitosos: {exitosos}")
    print(f"   ❌ Fallidos:  {fallidos}")
    print(f"   📈 Total formularios modernizados: {len(actualizados) + exitosos}")
    
    if fallidos == 0:
        print("\n🎉 ¡Todos los formularios han sido actualizados exitosamente!")
        print("   Los formularios ahora tienen un diseño moderno y consistente")
        print("   que coincide con el estilo de las vistas de detalles.")

if __name__ == "__main__":
    main()