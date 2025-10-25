# GUÍA DE ESTILO PARA FORMULARIOS DE CREAR

## Estructura Base

Todos los formularios de crear deben seguir esta estructura:

```html
{% extends "base.html" %}
{% block title %}Nuevo [Módulo] - Sistema Constructora{% endblock %}

{% block content %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/create-forms.css') }}">

<div class="create-form-container">
    <!-- Header -->
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{ url_for('listar_[modulo]') }}">[Módulo]s</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nuevo</span>
        </nav>
        <h1 class="create-page-title">
            <i class="fas fa-[icon]"></i>
            Crear Nuevo [Módulo]
        </h1>
    </div>

    <!-- Formulario -->
    <div class="container-fluid">
        <form method="POST" id="create-[modulo]-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <!-- Cards de secciones -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-[icon]"></i> [Título Sección]</h5>
                    </div>
                    <div class="card-body">
                        <!-- Campos de formulario -->
                    </div>
                </div>
            </div>
        </form>
    </div>

    <!-- Botones de acción -->
    <div class="container-fluid">
        <div class="create-form-card">
            <div class="create-form-actions">
                <a href="{{ url_for('listar_[modulo]') }}" class="create-btn create-btn-secondary">
                    <i class="fas fa-times"></i>Cancelar
                </a>
                <button type="submit" form="create-[modulo]-form" class="create-btn create-btn-primary">
                    <i class="fas fa-plus"></i>Crear [Módulo]
                </button>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## Campos de Formulario

```html
<div class="create-form-group">
    <label for="[campo]" class="create-form-label">
        <i class="fas fa-[icon]"></i>[Etiqueta]<span class="required">*</span>
    </label>
    <input type="text" class="create-form-control" id="[campo]" name="[campo]" 
           placeholder="[placeholder]" required>
    <div class="invalid-feedback">
        Mensaje de error
    </div>
</div>
```

## Iconos Recomendados por Módulo

- **Proyectos**: `fa-project-diagram`, `fa-plus-circle`
- **Obras**: `fa-building`, `fa-construction`
- **Empleados**: `fa-user-plus`, `fa-users`
- **Clientes**: `fa-handshake`, `fa-user-tie`
- **Proveedores**: `fa-truck`, `fa-industry`
- **Materiales**: `fa-boxes`, `fa-warehouse`
- **Vehículos**: `fa-car`, `fa-truck`
- **Equipos**: `fa-tools`, `fa-cogs`

## Colores de Header por Módulo

Los colores se definen automáticamente en el CSS, pero se pueden personalizar:

- **Información General**: Azul (`fa-info-circle`)
- **Asignaciones/Recursos**: Verde (`fa-users-cog`)
- **Contacto**: Cyan (`fa-contact-card`)
- **Financiero**: Amarillo (`fa-dollar-sign`)

## JavaScript de Validación

Incluir siempre al final:

```javascript
<script>
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
```
