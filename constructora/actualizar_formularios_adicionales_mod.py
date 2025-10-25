#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para actualizar más formularios al estilo moderno
"""

def actualizar_formulario_bitacoras():
    """Actualiza el formulario de bitácoras al estilo moderno"""
    template = '''{%extends "base.html"%}

{%block title%}Nueva Bitácora - Sistema Constructora{%endblock%}

{%block content%}
<link rel="stylesheet" href="{{ url_for('static', filename='css/create-forms.css') }}">

<div class="create-form-container">
    <!-- Header de página estilo detalle -->
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{ url_for('listar_bitacoras') }}">Bitácoras</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nueva</span>
        </nav>
        <h1 class="create-page-title">
            <i class="fas fa-book"></i>
            Crear Nueva Bitácora
        </h1>
    </div>

    <div class="container-fluid">
        <form method="POST" action="{{ url_for('crear_bitacora') }}" id="create-bitacora-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <!-- Información General -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-info-circle"></i> Información de la Bitácora</h5>
                    </div>
                    <div class="card-body">
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
                            <label for="empleado_id" class="create-form-label">
                                <i class="fas fa-user"></i>Empleado<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="empleado_id" name="empleado_id" required>
                                <option value="">Seleccione un empleado</option>
                                {%- for item in empleados %}
                                <option value="{{ item[0] }}" {{ 'selected' if request.form.empleado_id == item[0]|string else '' }}>{{ item[1] }}</option>
                                {%- endfor %}
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione un empleado.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="fecha" class="create-form-label">
                                <i class="fas fa-calendar"></i>Fecha<span class="required">*</span>
                            </label>
                            <input type="date" class="create-form-control" id="fecha" name="fecha" 
                                   value="{{ request.form.fecha if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese la fecha.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="descripcion" class="create-form-label">
                                <i class="fas fa-align-left"></i>Descripción<span class="required">*</span>
                            </label>
                            <textarea class="create-form-control" id="descripcion" name="descripcion" rows="4" 
                                      placeholder="Describe las actividades realizadas" required>{{ request.form.descripcion if request.form else '' }}</textarea>
                            <div class="invalid-feedback">
                                Por favor, ingrese la descripción.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="horas_trabajadas" class="create-form-label">
                                <i class="fas fa-clock"></i>Horas Trabajadas<span class="required">*</span>
                            </label>
                            <input type="number" step="0.5" class="create-form-control" id="horas_trabajadas" name="horas_trabajadas" 
                                   placeholder="8.0" 
                                   value="{{ request.form.horas_trabajadas if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese las horas trabajadas.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="actividad" class="create-form-label">
                                <i class="fas fa-tasks"></i>Actividad<span class="required">*</span>
                            </label>
                            <input type="text" class="create-form-control" id="actividad" name="actividad" 
                                   placeholder="Ej: Instalación de tuberías" 
                                   value="{{ request.form.actividad if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese la actividad.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Botones de acción -->
            <div class="form-actions mt-4">
                <div class="d-flex justify-content-between">
                    <a href="{{ url_for('listar_bitacoras') }}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Guardar Bitácora
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
    
    with open('templates/bitacoras/crear.html', 'w', encoding='utf-8') as f:
        f.write(template)
    print("✅ Bitácoras actualizado")

def actualizar_formulario_requisiciones():
    """Actualiza el formulario de requisiciones al estilo moderno"""
    template = '''{%extends "base.html"%}

{%block title%}Nueva Requisición - Sistema Constructora{%endblock%}

{%block content%}
<link rel="stylesheet" href="{{ url_for('static', filename='css/create-forms.css') }}">

<div class="create-form-container">
    <!-- Header de página estilo detalle -->
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{ url_for('listar_requisiciones') }}">Requisiciones</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nueva</span>
        </nav>
        <h1 class="create-page-title">
            <i class="fas fa-clipboard-list"></i>
            Crear Nueva Requisición
        </h1>
    </div>

    <div class="container-fluid">
        <form method="POST" action="{{ url_for('crear_requisicion') }}" id="create-requisicion-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <!-- Información General -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-info-circle"></i> Información de la Requisición</h5>
                    </div>
                    <div class="card-body">
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
                            <label for="empleado_id" class="create-form-label">
                                <i class="fas fa-user"></i>Empleado Solicitante<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="empleado_id" name="empleado_id" required>
                                <option value="">Seleccione un empleado</option>
                                {%- for item in empleados %}
                                <option value="{{ item[0] }}" {{ 'selected' if request.form.empleado_id == item[0]|string else '' }}>{{ item[1] }}</option>
                                {%- endfor %}
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione un empleado.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="fecha_solicitud" class="create-form-label">
                                <i class="fas fa-calendar"></i>Fecha de Solicitud<span class="required">*</span>
                            </label>
                            <input type="date" class="create-form-control" id="fecha_solicitud" name="fecha_solicitud" 
                                   value="{{ request.form.fecha_solicitud if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese la fecha de solicitud.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="descripcion" class="create-form-label">
                                <i class="fas fa-align-left"></i>Descripción<span class="required">*</span>
                            </label>
                            <textarea class="create-form-control" id="descripcion" name="descripcion" rows="4" 
                                      placeholder="Describe lo que se necesita" required>{{ request.form.descripcion if request.form else '' }}</textarea>
                            <div class="invalid-feedback">
                                Por favor, ingrese la descripción.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="cantidad_solicitada" class="create-form-label">
                                <i class="fas fa-sort-numeric-up"></i>Cantidad Solicitada<span class="required">*</span>
                            </label>
                            <input type="number" step="0.01" class="create-form-control" id="cantidad_solicitada" name="cantidad_solicitada" 
                                   placeholder="0.00" 
                                   value="{{ request.form.cantidad_solicitada if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese la cantidad solicitada.
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
                                <option value="urgente" {{ 'selected' if request.form.prioridad == 'urgente' else '' }}>Urgente</option>
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione una prioridad.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="estado" class="create-form-label">
                                <i class="fas fa-flag"></i>Estado<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="estado" name="estado" required>
                                <option value="">Seleccione un estado</option>
                                <option value="pendiente" {{ 'selected' if request.form.estado == 'pendiente' else '' }}>Pendiente</option>
                                <option value="aprobada" {{ 'selected' if request.form.estado == 'aprobada' else '' }}>Aprobada</option>
                                <option value="rechazada" {{ 'selected' if request.form.estado == 'rechazada' else '' }}>Rechazada</option>
                                <option value="entregada" {{ 'selected' if request.form.estado == 'entregada' else '' }}>Entregada</option>
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
                    <a href="{{ url_for('listar_requisiciones') }}" class="btn btn-secondary">
                        <i class="fas fa-times"></i> Cancelar
                    </a>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-save"></i> Guardar Requisición
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
    
    with open('templates/requisiciones/crear.html', 'w', encoding='utf-8') as f:
        f.write(template)
    print("✅ Requisiciones actualizado")

def main():
    """Función principal"""
    print("🚀 Actualizando más formularios al estilo moderno...")
    print("=" * 60)
    
    try:
        actualizar_formulario_bitacoras()
        actualizar_formulario_requisiciones()
        
        print("=" * 60)
        print("🎉 ¡Formularios adicionales actualizados!")
        print("   • Bitácoras: Registro de actividades con estilo moderno")
        print("   • Requisiciones: Solicitudes con validación completa")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()