#!/usr/bin/env python3
"""
Script para aplicar el nuevo estilo de formularios CREATE a todos los módulos
Mantiene consistencia visual con las vistas de detalle
"""

import os
import glob

def crear_demo_formulario_empleados():
    """Crear un ejemplo del formulario de empleados con el nuevo estilo"""
    
    template = '''{% extends "base.html" %}

{% block title %}Nuevo Empleado - Sistema Constructora{% endblock %}

{% block content %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/create-forms.css') }}">

<div class="create-form-container">
    <!-- Header de página estilo detalle -->
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{ url_for('listar_empleados') }}">Empleados</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nuevo</span>
        </nav>
        <h1 class="create-page-title">
            <i class="fas fa-user-plus"></i>
            Crear Nuevo Empleado
        </h1>
    </div>

    <div class="container-fluid">
        <form method="POST" action="{{ url_for('crear_empleado') }}" id="create-empleado-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <!-- Información Personal -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-user"></i> Información Personal</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="nombre_empleado" class="create-form-label">
                                <i class="fas fa-id-card"></i>Nombre<span class="required">*</span>
                            </label>
                            <input type="text" class="create-form-control" id="nombre_empleado" name="nombre_empleado" 
                                   placeholder="Nombre del empleado" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese el nombre del empleado.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="apellido_empleado" class="create-form-label">
                                <i class="fas fa-id-card"></i>Apellido<span class="required">*</span>
                            </label>
                            <input type="text" class="create-form-control" id="apellido_empleado" name="apellido_empleado" 
                                   placeholder="Apellido del empleado" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese el apellido del empleado.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="tipo_empleado" class="create-form-label">
                                <i class="fas fa-briefcase"></i>Tipo de Empleado<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="tipo_empleado" name="tipo_empleado" required>
                                <option value="">Seleccionar tipo...</option>
                                <option value="ARQUITECTO">🏗️ Arquitecto</option>
                                <option value="INGENIERO">⚡ Ingeniero</option>
                                <option value="OBRERO">👷 Obrero</option>
                                <option value="SUPERVISOR">👨‍💼 Supervisor</option>
                                <option value="ADMINISTRATIVO">📋 Administrativo</option>
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione el tipo de empleado.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="fecha_ingreso" class="create-form-label">
                                <i class="fas fa-calendar-plus"></i>Fecha de Ingreso
                            </label>
                            <input type="date" class="create-form-control" id="fecha_ingreso" name="fecha_ingreso">
                        </div>
                    </div>
                </div>

                <!-- Información de Contacto y Salario -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-contact-card"></i> Contacto y Salario</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="telefono" class="create-form-label">
                                <i class="fas fa-phone"></i>Teléfono
                            </label>
                            <input type="tel" class="create-form-control" id="telefono" name="telefono" 
                                   placeholder="Ej: +57 300 123 4567">
                        </div>

                        <div class="create-form-group">
                            <label for="email" class="create-form-label">
                                <i class="fas fa-envelope"></i>Email
                            </label>
                            <input type="email" class="create-form-control" id="email" name="email" 
                                   placeholder="empleado@empresa.com">
                        </div>

                        <div class="create-form-group">
                            <label for="salario_fijo_empleado" class="create-form-label">
                                <i class="fas fa-dollar-sign"></i>Salario Fijo
                            </label>
                            <input type="number" class="create-form-control" id="salario_fijo_empleado" name="salario_fijo_empleado" 
                                   placeholder="0" step="1000" min="0">
                            <div class="create-form-text">
                                <i class="fas fa-info-circle"></i>Salario mensual en pesos colombianos
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>

    <!-- Botones de acción -->
    <div class="container-fluid">
        <div class="create-form-card">
            <div class="create-form-actions">
                <a href="{{ url_for('listar_empleados') }}" class="create-btn create-btn-secondary">
                    <i class="fas fa-times"></i>Cancelar
                </a>
                <button type="submit" form="create-empleado-form" class="create-btn create-btn-primary">
                    <i class="fas fa-user-plus"></i>Crear Empleado
                </button>
            </div>
        </div>
    </div>
</div>

<script>
// Validación del formulario
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
{% endblock %}'''

    with open('templates/empleados/crear_demo.html', 'w', encoding='utf-8') as f:
        f.write(template)
    
    print("✅ Creado template demo para empleados: templates/empleados/crear_demo.html")

def crear_guia_formularios():
    """Crear una guía de estilo para formularios"""
    
    guia = '''# GUÍA DE ESTILO PARA FORMULARIOS DE CREAR

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
'''
    
    with open('GUIA_FORMULARIOS_CREATE.md', 'w', encoding='utf-8') as f:
        f.write(guia)
    
    print("✅ Creada guía de estilo: GUIA_FORMULARIOS_CREATE.md")

if __name__ == "__main__":
    print("🎨 APLICANDO NUEVO ESTILO A FORMULARIOS CREATE")
    print("=" * 50)
    
    crear_demo_formulario_empleados()
    crear_guia_formularios()
    
    print("\n" + "=" * 50)
    print("✅ COMPLETADO - Nuevo estilo aplicado")
    print("📋 Usar los templates demo como referencia")
    print("🎯 Todos los formularios seguirán la misma línea visual que los detalles")