#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplificado para actualizar formularios al estilo moderno
"""
import os
import glob

def actualizar_formulario_contratos():
    """Actualiza el formulario de contratos al estilo moderno"""
    template = '''{%extends "base.html"%}

{%block title%}Nuevo Contrato - Sistema Constructora{%endblock%}

{%block content%}
<link rel="stylesheet" href="{{ url_for('static', filename='css/create-forms.css') }}">

<div class="create-form-container">
    <!-- Header de página estilo detalle -->
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{ url_for('listar_contratos') }}">Contratos</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nuevo</span>
        </nav>
        <h1 class="create-page-title">
            <i class="fas fa-file-contract"></i>
            Crear Nuevo Contrato
        </h1>
    </div>

    <div class="container-fluid">
        <form method="POST" action="{{ url_for('crear_contrato') }}" id="create-contrato-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <!-- Información General -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-info-circle"></i> Información del Contrato</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="numero_contrato" class="create-form-label">
                                <i class="fas fa-file-contract"></i>Número de Contrato<span class="required">*</span>
                            </label>
                            <input type="text" class="create-form-control" id="numero_contrato" name="numero_contrato" 
                                   placeholder="Ej: CON-2024-001" 
                                   value="{{ request.form.numero_contrato if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese el número del contrato.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="cliente_id" class="create-form-label">
                                <i class="fas fa-user-tie"></i>Cliente<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="cliente_id" name="cliente_id" required>
                                <option value="">Seleccione un cliente</option>
                                {%- for item in clientes %}
                                <option value="{{ item[0] }}" {{ 'selected' if request.form.cliente_id == item[0]|string else '' }}>{{ item[1] }}</option>
                                {%- endfor %}
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione un cliente.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="obra_id" class="create-form-label">
                                <i class="fas fa-building"></i>Obra<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="obra_id" name="obra_id" required>
                                <option value="">Seleccione una obra</option>
                                {%- for item in obras %}
                                <option value="{{ item[0] }}" {{ 'selected' if request.form.obra_id == item[0]|string else '' }}>{{ item[1] }}</option>
                                {%- endfor %}
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione una obra.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="fecha_inicio" class="create-form-label">
                                <i class="fas fa-calendar-plus"></i>Fecha de Inicio<span class="required">*</span>
                            </label>
                            <input type="date" class="create-form-control" id="fecha_inicio" name="fecha_inicio" 
                                   value="{{ request.form.fecha_inicio if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese la fecha de inicio.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="fecha_fin" class="create-form-label">
                                <i class="fas fa-calendar-check"></i>Fecha de Fin<span class="required">*</span>
                            </label>
                            <input type="date" class="create-form-control" id="fecha_fin" name="fecha_fin" 
                                   value="{{ request.form.fecha_fin if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese la fecha de fin.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="valor_total" class="create-form-label">
                                <i class="fas fa-dollar-sign"></i>Valor Total<span class="required">*</span>
                            </label>
                            <input type="number" step="0.01" class="create-form-control" id="valor_total" name="valor_total" 
                                   placeholder="0.00" 
                                   value="{{ request.form.valor_total if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese el valor total.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="estado" class="create-form-label">
                                <i class="fas fa-flag"></i>Estado<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="estado" name="estado" required>
                                <option value="">Seleccione un estado</option>
                                <option value="activo" {{ 'selected' if request.form.estado == 'activo' else '' }}>Activo</option>
                                <option value="inactivo" {{ 'selected' if request.form.estado == 'inactivo' else '' }}>Inactivo</option>
                                <option value="completado" {{ 'selected' if request.form.estado == 'completado' else '' }}>Completado</option>
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione un estado.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Botones de acción -->
            <div class="form-actions mt-4">
                <div class="d-flex justify-content-between">
                    <a href="{{ url_for('listar_contratos') }}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Guardar Contrato
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>

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
{%endblock%}'''
    
    with open('templates/contratos/crear.html', 'w', encoding='utf-8') as f:
        f.write(template)
    print("✅ Contratos actualizado")

def actualizar_formulario_actividades():
    """Actualiza el formulario de actividades al estilo moderno"""
    template = '''{%extends "base.html"%}

{%block title%}Nueva Actividad - Sistema Constructora{%endblock%}

{%block content%}
<link rel="stylesheet" href="{{ url_for('static', filename='css/create-forms.css') }}">

<div class="create-form-container">
    <!-- Header de página estilo detalle -->
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{ url_for('listar_actividades') }}">Actividades</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nueva</span>
        </nav>
        <h1 class="create-page-title">
            <i class="fas fa-tasks"></i>
            Crear Nueva Actividad
        </h1>
    </div>

    <div class="container-fluid">
        <form method="POST" action="{{ url_for('crear_actividad') }}" id="create-actividad-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <!-- Información General -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-info-circle"></i> Información de la Actividad</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="nombre" class="create-form-label">
                                <i class="fas fa-tasks"></i>Nombre de la Actividad<span class="required">*</span>
                            </label>
                            <input type="text" class="create-form-control" id="nombre" name="nombre" 
                                   placeholder="Ej: Instalación eléctrica principal" 
                                   value="{{ request.form.nombre if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese el nombre de la actividad.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="descripcion" class="create-form-label">
                                <i class="fas fa-align-left"></i>Descripción<span class="required">*</span>
                            </label>
                            <textarea class="create-form-control" id="descripcion" name="descripcion" rows="4" 
                                      placeholder="Describe los detalles de la actividad" required>{{ request.form.descripcion if request.form else '' }}</textarea>
                            <div class="invalid-feedback">
                                Por favor, ingrese la descripción de la actividad.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="area_id" class="create-form-label">
                                <i class="fas fa-layer-group"></i>Área<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="area_id" name="area_id" required>
                                <option value="">Seleccione un área</option>
                                {%- for item in areas %}
                                <option value="{{ item[0] }}" {{ 'selected' if request.form.area_id == item[0]|string else '' }}>{{ item[1] }}</option>
                                {%- endfor %}
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione un área.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="duracion_estimada" class="create-form-label">
                                <i class="fas fa-hourglass-half"></i>Duración Estimada (horas)
                            </label>
                            <input type="number" step="0.5" class="create-form-control" id="duracion_estimada" name="duracion_estimada" 
                                   placeholder="8.0" 
                                   value="{{ request.form.duracion_estimada if request.form else '' }}">
                            <div class="invalid-feedback">
                                Por favor, ingrese la duración estimada.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="prioridad" class="create-form-label">
                                <i class="fas fa-exclamation-triangle"></i>Prioridad<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="prioridad" name="prioridad" required>
                                <option value="">Seleccione una prioridad</option>
                                <option value="baja" {{ 'selected' if request.form.prioridad == 'baja' else '' }}>Baja</option>
                                <option value="media" {{ 'selected' if request.form.prioridad == 'media' else '' }}>Media</option>
                                <option value="alta" {{ 'selected' if request.form.prioridad == 'alta' else '' }}>Alta</option>
                                <option value="crítica" {{ 'selected' if request.form.prioridad == 'crítica' else '' }}>Crítica</option>
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione una prioridad.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Botones de acción -->
            <div class="form-actions mt-4">
                <div class="d-flex justify-content-between">
                    <a href="{{ url_for('listar_actividades') }}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Guardar Actividad
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>

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
{%endblock%}'''
    
    with open('templates/actividades/crear.html', 'w', encoding='utf-8') as f:
        f.write(template)
    print("✅ Actividades actualizado")

def main():
    """Función principal"""
    print("🚀 Actualizando formularios clave al estilo moderno...")
    print("=" * 60)
    
    try:
        actualizar_formulario_contratos()
        actualizar_formulario_actividades()
        
        print("=" * 60)
        print("🎉 ¡Formularios actualizados exitosamente!")
        print("   • Estilo consistente con obras/empleados/proyectos")
        print("   • Extienden base.html para navegación unificada")
        print("   • Estructura de tarjetas organizadas")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()