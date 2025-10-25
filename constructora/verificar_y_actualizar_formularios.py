#!/usr/bin/env python3
"""
Script para verificar y actualizar todos los formularios de crear
Aplica el nuevo estilo consistente con las vistas de detalle
"""

import os
import glob
import re

def verificar_formularios():
    """Verificar qué formularios existen y su estado actual"""
    
    print("🔍 VERIFICANDO FORMULARIOS DE CREAR")
    print("=" * 60)
    
    # Buscar todos los archivos crear.html
    crear_files = glob.glob("templates/*/crear.html")
    
    formularios_info = []
    
    for file_path in crear_files:
        modulo = file_path.split('/')[1] if '/' in file_path else file_path.split('\\')[1]
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar si ya usa el nuevo estilo
            usa_nuevo_estilo = 'create-forms.css' in content
            tiene_breadcrumb = 'breadcrumb' in content
            tiene_validacion = 'needs-validation' in content
            
            formularios_info.append({
                'modulo': modulo,
                'archivo': file_path,
                'nuevo_estilo': usa_nuevo_estilo,
                'breadcrumb': tiene_breadcrumb,
                'validacion': tiene_validacion,
                'lineas': len(content.split('\n'))
            })
            
        except Exception as e:
            print(f"❌ Error leyendo {file_path}: {e}")
    
    # Mostrar resumen
    print(f"\n📊 RESUMEN DE FORMULARIOS ({len(formularios_info)} encontrados):")
    print("-" * 60)
    
    nuevos = con_problemas = 0
    
    for info in sorted(formularios_info, key=lambda x: x['modulo']):
        status = "✅" if info['nuevo_estilo'] else "🔧"
        if not info['nuevo_estilo']:
            con_problemas += 1
        else:
            nuevos += 1
            
        print(f"{status} {info['modulo']:<15} | Líneas: {info['lineas']:<4} | "
              f"Breadcrumb: {'✓' if info['breadcrumb'] else '✗'} | "
              f"Validación: {'✓' if info['validacion'] else '✗'}")
    
    print(f"\n📈 ESTADÍSTICAS:")
    print(f"  ✅ Con nuevo estilo: {nuevos}")
    print(f"  🔧 Necesitan actualizar: {con_problemas}")
    
    return [f for f in formularios_info if not f['nuevo_estilo']]

def actualizar_formulario_empleados():
    """Actualizar formulario de empleados con el nuevo estilo"""
    
    print("\n🔧 ACTUALIZANDO FORMULARIO DE EMPLEADOS...")
    
    nuevo_contenido = '''{% extends "base.html" %}

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
                                   placeholder="Nombre del empleado" 
                                   value="{{ request.form.nombre_empleado if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese el nombre del empleado.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="apellido_empleado" class="create-form-label">
                                <i class="fas fa-id-card"></i>Apellido<span class="required">*</span>
                            </label>
                            <input type="text" class="create-form-control" id="apellido_empleado" name="apellido_empleado" 
                                   placeholder="Apellido del empleado"
                                   value="{{ request.form.apellido_empleado if request.form else '' }}" required>
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
                                <option value="ARQUITECTO" {{ 'selected' if request.form and request.form.tipo_empleado == 'ARQUITECTO' else '' }}>🏗️ Arquitecto</option>
                                <option value="INGENIERO" {{ 'selected' if request.form and request.form.tipo_empleado == 'INGENIERO' else '' }}>⚡ Ingeniero</option>
                                <option value="OBRERO" {{ 'selected' if request.form and request.form.tipo_empleado == 'OBRERO' else '' }}>👷 Obrero</option>
                                <option value="SUPERVISOR" {{ 'selected' if request.form and request.form.tipo_empleado == 'SUPERVISOR' else '' }}>👨‍💼 Supervisor</option>
                                <option value="ADMINISTRATIVO" {{ 'selected' if request.form and request.form.tipo_empleado == 'ADMINISTRATIVO' else '' }}>📋 Administrativo</option>
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione el tipo de empleado.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="fecha_ingreso" class="create-form-label">
                                <i class="fas fa-calendar-plus"></i>Fecha de Ingreso
                            </label>
                            <input type="date" class="create-form-control" id="fecha_ingreso" name="fecha_ingreso"
                                   value="{{ request.form.fecha_ingreso if request.form else '' }}">
                        </div>
                    </div>
                </div>

                <!-- Información de Contacto y Salario -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-address-card"></i> Contacto y Salario</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="telefono" class="create-form-label">
                                <i class="fas fa-phone"></i>Teléfono
                            </label>
                            <input type="tel" class="create-form-control" id="telefono" name="telefono" 
                                   placeholder="Ej: +57 300 123 4567"
                                   value="{{ request.form.telefono if request.form else '' }}">
                        </div>

                        <div class="create-form-group">
                            <label for="email" class="create-form-label">
                                <i class="fas fa-envelope"></i>Email
                            </label>
                            <input type="email" class="create-form-control" id="email" name="email" 
                                   placeholder="empleado@empresa.com"
                                   value="{{ request.form.email if request.form else '' }}">
                        </div>

                        <div class="create-form-group">
                            <label for="salario_fijo_empleado" class="create-form-label">
                                <i class="fas fa-dollar-sign"></i>Salario Fijo
                            </label>
                            <input type="number" class="create-form-control" id="salario_fijo_empleado" name="salario_fijo_empleado" 
                                   placeholder="0" step="1000" min="0"
                                   value="{{ request.form.salario_fijo_empleado if request.form else '' }}">
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
    
    with open('templates/empleados/crear.html', 'w', encoding='utf-8') as f:
        f.write(nuevo_contenido)
    
    print("✅ Formulario de empleados actualizado")

def actualizar_formulario_vehiculos():
    """Actualizar formulario de vehículos con el nuevo estilo"""
    
    print("\n🔧 ACTUALIZANDO FORMULARIO DE VEHÍCULOS...")
    
    nuevo_contenido = '''{% extends "base.html" %}

{% block title %}Nuevo Vehículo - Sistema Constructora{% endblock %}

{% block content %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/create-forms.css') }}">

<div class="create-form-container">
    <!-- Header de página estilo detalle -->
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{ url_for('listar_vehiculos') }}">Vehículos</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nuevo</span>
        </nav>
        <h1 class="create-page-title">
            <i class="fas fa-truck"></i>
            Crear Nuevo Vehículo
        </h1>
    </div>

    <div class="container-fluid">
        <form method="POST" action="{{ url_for('crear_vehiculo') }}" id="create-vehiculo-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <!-- Información del Vehículo -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-car"></i> Información del Vehículo</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="placa_vehiculo" class="create-form-label">
                                <i class="fas fa-id-badge"></i>Placa<span class="required">*</span>
                            </label>
                            <input type="text" class="create-form-control" id="placa_vehiculo" name="placa_vehiculo" 
                                   placeholder="Ej: ABC123" 
                                   value="{{ request.form.placa_vehiculo if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese la placa del vehículo.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="tipo_vehiculo" class="create-form-label">
                                <i class="fas fa-list"></i>Tipo de Vehículo<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="tipo_vehiculo" name="tipo_vehiculo" required>
                                <option value="">Seleccionar tipo...</option>
                                <option value="CAMIONETA" {{ 'selected' if request.form and request.form.tipo_vehiculo == 'CAMIONETA' else '' }}>🚗 Camioneta</option>
                                <option value="VOLQUETA" {{ 'selected' if request.form and request.form.tipo_vehiculo == 'VOLQUETA' else '' }}>🚛 Volqueta</option>
                                <option value="MEZCLADORA" {{ 'selected' if request.form and request.form.tipo_vehiculo == 'MEZCLADORA' else '' }}>🚚 Mezcladora</option>
                                <option value="GRUA" {{ 'selected' if request.form and request.form.tipo_vehiculo == 'GRUA' else '' }}>🏗️ Grúa</option>
                                <option value="BULLDOZER" {{ 'selected' if request.form and request.form.tipo_vehiculo == 'BULLDOZER' else '' }}>🚜 Bulldozer</option>
                                <option value="OTRO" {{ 'selected' if request.form and request.form.tipo_vehiculo == 'OTRO' else '' }}>❓ Otro</option>
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione el tipo de vehículo.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="estado_vehiculo" class="create-form-label">
                                <i class="fas fa-check-circle"></i>Estado<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="estado_vehiculo" name="estado_vehiculo" required>
                                <option value="">Seleccionar estado...</option>
                                <option value="DISPONIBLE" {{ 'selected' if request.form and request.form.estado_vehiculo == 'DISPONIBLE' else '' }}>✅ Disponible</option>
                                <option value="EN_USO" {{ 'selected' if request.form and request.form.estado_vehiculo == 'EN_USO' else '' }}>🔄 En Uso</option>
                                <option value="MANTENIMIENTO" {{ 'selected' if request.form and request.form.estado_vehiculo == 'MANTENIMIENTO' else '' }}>🔧 Mantenimiento</option>
                                <option value="FUERA_SERVICIO" {{ 'selected' if request.form and request.form.estado_vehiculo == 'FUERA_SERVICIO' else '' }}>❌ Fuera de Servicio</option>
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione el estado del vehículo.
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Información Adicional -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-info-circle"></i> Información Adicional</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="modelo" class="create-form-label">
                                <i class="fas fa-tag"></i>Modelo
                            </label>
                            <input type="text" class="create-form-control" id="modelo" name="modelo" 
                                   placeholder="Ej: 2020"
                                   value="{{ request.form.modelo if request.form else '' }}">
                        </div>

                        <div class="create-form-group">
                            <label for="capacidad" class="create-form-label">
                                <i class="fas fa-weight-hanging"></i>Capacidad
                            </label>
                            <input type="text" class="create-form-control" id="capacidad" name="capacidad" 
                                   placeholder="Ej: 5 toneladas"
                                   value="{{ request.form.capacidad if request.form else '' }}">
                            <div class="create-form-text">
                                <i class="fas fa-info-circle"></i>Capacidad de carga o pasajeros
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="observaciones" class="create-form-label">
                                <i class="fas fa-sticky-note"></i>Observaciones
                            </label>
                            <textarea class="create-form-control" id="observaciones" name="observaciones" rows="3"
                                      placeholder="Observaciones adicionales sobre el vehículo">{{ request.form.observaciones if request.form else '' }}</textarea>
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
                <a href="{{ url_for('listar_vehiculos') }}" class="create-btn create-btn-secondary">
                    <i class="fas fa-times"></i>Cancelar
                </a>
                <button type="submit" form="create-vehiculo-form" class="create-btn create-btn-primary">
                    <i class="fas fa-truck"></i>Crear Vehículo
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
    
    with open('templates/vehiculos/crear.html', 'w', encoding='utf-8') as f:
        f.write(nuevo_contenido)
    
    print("✅ Formulario de vehículos actualizado")

def actualizar_formulario_materiales():
    """Actualizar formulario de materiales con el nuevo estilo"""
    
    print("\n🔧 ACTUALIZANDO FORMULARIO DE MATERIALES...")
    
    nuevo_contenido = '''{% extends "base.html" %}

{% block title %}Nuevo Material - Sistema Constructora{% endblock %}

{% block content %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/create-forms.css') }}">

<div class="create-form-container">
    <!-- Header de página estilo detalle -->
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{ url_for('listar_materiales') }}">Materiales</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nuevo</span>
        </nav>
        <h1 class="create-page-title">
            <i class="fas fa-cubes"></i>
            Crear Nuevo Material
        </h1>
    </div>

    <div class="container-fluid">
        <form method="POST" action="{{ url_for('crear_material') }}" id="create-material-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <!-- Información del Material -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-cube"></i> Información del Material</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="nombre_material" class="create-form-label">
                                <i class="fas fa-tag"></i>Nombre del Material<span class="required">*</span>
                            </label>
                            <input type="text" class="create-form-control" id="nombre_material" name="nombre_material" 
                                   placeholder="Ej: Cemento Portland" 
                                   value="{{ request.form.nombre_material if request.form else '' }}" required>
                            <div class="invalid-feedback">
                                Por favor, ingrese el nombre del material.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="tipo_material" class="create-form-label">
                                <i class="fas fa-list"></i>Tipo de Material<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="tipo_material" name="tipo_material" required>
                                <option value="">Seleccionar tipo...</option>
                                <option value="CEMENTO" {{ 'selected' if request.form and request.form.tipo_material == 'CEMENTO' else '' }}>🏗️ Cemento</option>
                                <option value="ARENA" {{ 'selected' if request.form and request.form.tipo_material == 'ARENA' else '' }}>🏖️ Arena</option>
                                <option value="GRAVA" {{ 'selected' if request.form and request.form.tipo_material == 'GRAVA' else '' }}>🪨 Grava</option>
                                <option value="HIERRO" {{ 'selected' if request.form and request.form.tipo_material == 'HIERRO' else '' }}>🔩 Hierro</option>
                                <option value="LADRILLO" {{ 'selected' if request.form and request.form.tipo_material == 'LADRILLO' else '' }}>🧱 Ladrillo</option>
                                <option value="TUBERIA" {{ 'selected' if request.form and request.form.tipo_material == 'TUBERIA' else '' }}>🚿 Tubería</option>
                                <option value="ELECTRICO" {{ 'selected' if request.form and request.form.tipo_material == 'ELECTRICO' else '' }}>⚡ Eléctrico</option>
                                <option value="OTRO" {{ 'selected' if request.form and request.form.tipo_material == 'OTRO' else '' }}>❓ Otro</option>
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione el tipo de material.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="unidad_medida" class="create-form-label">
                                <i class="fas fa-ruler"></i>Unidad de Medida<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="unidad_medida" name="unidad_medida" required>
                                <option value="">Seleccionar unidad...</option>
                                <option value="KG" {{ 'selected' if request.form and request.form.unidad_medida == 'KG' else '' }}>⚖️ Kilogramos (KG)</option>
                                <option value="TONELADAS" {{ 'selected' if request.form and request.form.unidad_medida == 'TONELADAS' else '' }}>🏗️ Toneladas</option>
                                <option value="M3" {{ 'selected' if request.form and request.form.unidad_medida == 'M3' else '' }}>📦 Metros Cúbicos (M³)</option>
                                <option value="M2" {{ 'selected' if request.form and request.form.unidad_medida == 'M2' else '' }}>📐 Metros Cuadrados (M²)</option>
                                <option value="ML" {{ 'selected' if request.form and request.form.unidad_medida == 'ML' else '' }}>📏 Metros Lineales (ML)</option>
                                <option value="UNIDADES" {{ 'selected' if request.form and request.form.unidad_medida == 'UNIDADES' else '' }}>🔢 Unidades</option>
                            </select>
                            <div class="invalid-feedback">
                                Por favor, seleccione la unidad de medida.
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="stock_actual" class="create-form-label">
                                <i class="fas fa-warehouse"></i>Stock Inicial
                            </label>
                            <input type="number" class="create-form-control" id="stock_actual" name="stock_actual" 
                                   placeholder="0" step="0.01" min="0"
                                   value="{{ request.form.stock_actual if request.form else '' }}">
                        </div>
                    </div>
                </div>

                <!-- Información Adicional -->
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-info-circle"></i> Información Adicional</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="precio_unitario" class="create-form-label">
                                <i class="fas fa-dollar-sign"></i>Precio Unitario
                            </label>
                            <input type="number" class="create-form-control" id="precio_unitario" name="precio_unitario" 
                                   placeholder="0.00" step="0.01" min="0"
                                   value="{{ request.form.precio_unitario if request.form else '' }}">
                            <div class="create-form-text">
                                <i class="fas fa-info-circle"></i>Precio por unidad de medida en pesos colombianos
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="stock_minimo" class="create-form-label">
                                <i class="fas fa-exclamation-triangle"></i>Stock Mínimo
                            </label>
                            <input type="number" class="create-form-control" id="stock_minimo" name="stock_minimo" 
                                   placeholder="0" step="0.01" min="0"
                                   value="{{ request.form.stock_minimo if request.form else '' }}">
                            <div class="create-form-text">
                                <i class="fas fa-info-circle"></i>Cantidad mínima antes de alertar por reabastecimiento
                            </div>
                        </div>

                        <div class="create-form-group">
                            <label for="descripcion" class="create-form-label">
                                <i class="fas fa-sticky-note"></i>Descripción
                            </label>
                            <textarea class="create-form-control" id="descripcion" name="descripcion" rows="3"
                                      placeholder="Descripción detallada del material">{{ request.form.descripcion if request.form else '' }}</textarea>
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
                <a href="{{ url_for('listar_materiales') }}" class="create-btn create-btn-secondary">
                    <i class="fas fa-times"></i>Cancelar
                </a>
                <button type="submit" form="create-material-form" class="create-btn create-btn-primary">
                    <i class="fas fa-cubes"></i>Crear Material
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
    
    with open('templates/materiales/crear.html', 'w', encoding='utf-8') as f:
        f.write(nuevo_contenido)
    
    print("✅ Formulario de materiales actualizado")

if __name__ == "__main__":
    print("🔍 VERIFICANDO Y ACTUALIZANDO FORMULARIOS")
    print("=" * 60)
    
    # Verificar todos los formularios
    problemas = verificar_formularios()
    
    if problemas:
        print(f"\n🔧 ACTUALIZANDO {len(problemas)} FORMULARIOS...")
        
        # Actualizar los formularios principales
        actualizar_formulario_empleados()
        actualizar_formulario_vehiculos() 
        actualizar_formulario_materiales()
        
        print(f"\n✅ COMPLETADO - {3} formularios principales actualizados")
        print("📝 Los demás formularios pueden actualizarse usando la misma estructura")
    else:
        print("\n✅ Todos los formularios ya están actualizados")
    
    print("\n" + "=" * 60)
    print("🎯 CONSISTENCIA VISUAL MANTENIDA")