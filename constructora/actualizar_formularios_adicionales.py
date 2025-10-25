#!/usr/bin/env python3
"""
Script completo para actualizar TODOS los formularios faltantes
"""

def actualizar_formulario_proveedores():
    """Actualizar formulario de proveedores"""
    
    contenido = '''{% extends "base.html" %}

{% block title %}Nuevo Proveedor - Sistema Constructora{% endblock %}

{% block content %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/create-forms.css') }}">

<div class="create-form-container">
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{ url_for('listar_proveedores') }}">Proveedores</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nuevo</span>
        </nav>
        <h1 class="create-page-title">
            <i class="fas fa-industry"></i>
            Crear Nuevo Proveedor
        </h1>
    </div>

    <div class="container-fluid">
        <form method="POST" action="{{ url_for('crear_proveedor') }}" id="create-proveedor-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-building"></i> Información de la Empresa</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="nombre_proveedor" class="create-form-label">
                                <i class="fas fa-tag"></i>Nombre del Proveedor<span class="required">*</span>
                            </label>
                            <input type="text" class="create-form-control" id="nombre_proveedor" name="nombre_proveedor" 
                                   placeholder="Ej: Materiales El Constructor S.A.S." required>
                        </div>

                        <div class="create-form-group">
                            <label for="nit_proveedor" class="create-form-label">
                                <i class="fas fa-id-card"></i>NIT
                            </label>
                            <input type="text" class="create-form-control" id="nit_proveedor" name="nit_proveedor" 
                                   placeholder="Ej: 123456789-1">
                        </div>

                        <div class="create-form-group">
                            <label for="tipo_proveedor" class="create-form-label">
                                <i class="fas fa-list"></i>Tipo de Proveedor<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="tipo_proveedor" name="tipo_proveedor" required>
                                <option value="">Seleccionar tipo...</option>
                                <option value="MATERIALES">🏗️ Materiales de Construcción</option>
                                <option value="EQUIPOS">🔧 Equipos y Maquinaria</option>
                                <option value="SERVICIOS">🛠️ Servicios Especializados</option>
                                <option value="TRANSPORTE">🚚 Transporte y Logística</option>
                                <option value="OTRO">❓ Otro</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-address-book"></i> Información de Contacto</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="telefono_proveedor" class="create-form-label">
                                <i class="fas fa-phone"></i>Teléfono
                            </label>
                            <input type="tel" class="create-form-control" id="telefono_proveedor" name="telefono_proveedor" 
                                   placeholder="Ej: +57 1 234 5678">
                        </div>

                        <div class="create-form-group">
                            <label for="email_proveedor" class="create-form-label">
                                <i class="fas fa-envelope"></i>Email
                            </label>
                            <input type="email" class="create-form-control" id="email_proveedor" name="email_proveedor" 
                                   placeholder="contacto@proveedor.com">
                        </div>

                        <div class="create-form-group">
                            <label for="direccion_proveedor" class="create-form-label">
                                <i class="fas fa-map-marker-alt"></i>Dirección
                            </label>
                            <input type="text" class="create-form-control" id="direccion_proveedor" name="direccion_proveedor" 
                                   placeholder="Dirección completa">
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>

    <div class="container-fluid">
        <div class="create-form-card">
            <div class="create-form-actions">
                <a href="{{ url_for('listar_proveedores') }}" class="create-btn create-btn-secondary">
                    <i class="fas fa-times"></i>Cancelar
                </a>
                <button type="submit" form="create-proveedor-form" class="create-btn create-btn-primary">
                    <i class="fas fa-industry"></i>Crear Proveedor
                </button>
            </div>
        </div>
    </div>
</div>

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
{% endblock %}'''
    
    with open('templates/proveedores/crear.html', 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("✅ Proveedor actualizado")

def actualizar_formulario_equipos():
    """Actualizar formulario de equipos"""
    
    contenido = '''{% extends "base.html" %}

{% block title %}Nuevo Equipo - Sistema Constructora{% endblock %}

{% block content %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/create-forms.css') }}">

<div class="create-form-container">
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{ url_for('listar_equipos') }}">Equipos</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nuevo</span>
        </nav>
        <h1 class="create-page-title">
            <i class="fas fa-tools"></i>
            Crear Nuevo Equipo
        </h1>
    </div>

    <div class="container-fluid">
        <form method="POST" action="{{ url_for('crear_equipo') }}" id="create-equipo-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-cog"></i> Información del Equipo</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="nombre_equipo" class="create-form-label">
                                <i class="fas fa-tag"></i>Nombre del Equipo<span class="required">*</span>
                            </label>
                            <input type="text" class="create-form-control" id="nombre_equipo" name="nombre_equipo" 
                                   placeholder="Ej: Taladro Industrial Bosch" required>
                        </div>

                        <div class="create-form-group">
                            <label for="tipo_equipo" class="create-form-label">
                                <i class="fas fa-list"></i>Tipo de Equipo<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="tipo_equipo" name="tipo_equipo" required>
                                <option value="">Seleccionar tipo...</option>
                                <option value="HERRAMIENTA_MANUAL">🔨 Herramienta Manual</option>
                                <option value="HERRAMIENTA_ELECTRICA">⚡ Herramienta Eléctrica</option>
                                <option value="MAQUINARIA_PESADA">🏗️ Maquinaria Pesada</option>
                                <option value="EQUIPO_SEGURIDAD">🦺 Equipo de Seguridad</option>
                                <option value="EQUIPO_MEDICION">📏 Equipo de Medición</option>
                                <option value="OTRO">❓ Otro</option>
                            </select>
                        </div>

                        <div class="create-form-group">
                            <label for="estado_equipo" class="create-form-label">
                                <i class="fas fa-check-circle"></i>Estado<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="estado_equipo" name="estado_equipo" required>
                                <option value="">Seleccionar estado...</option>
                                <option value="DISPONIBLE">✅ Disponible</option>
                                <option value="EN_USO">🔄 En Uso</option>
                                <option value="MANTENIMIENTO">🔧 Mantenimiento</option>
                                <option value="FUERA_SERVICIO">❌ Fuera de Servicio</option>
                            </select>
                        </div>
                    </div>
                </div>

                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-info-circle"></i> Detalles Adicionales</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="marca_equipo" class="create-form-label">
                                <i class="fas fa-copyright"></i>Marca
                            </label>
                            <input type="text" class="create-form-control" id="marca_equipo" name="marca_equipo" 
                                   placeholder="Ej: Bosch, DeWalt, Caterpillar">
                        </div>

                        <div class="create-form-group">
                            <label for="modelo_equipo" class="create-form-label">
                                <i class="fas fa-code"></i>Modelo
                            </label>
                            <input type="text" class="create-form-control" id="modelo_equipo" name="modelo_equipo" 
                                   placeholder="Ej: HD-2020">
                        </div>

                        <div class="create-form-group">
                            <label for="numero_serie" class="create-form-label">
                                <i class="fas fa-barcode"></i>Número de Serie
                            </label>
                            <input type="text" class="create-form-control" id="numero_serie" name="numero_serie" 
                                   placeholder="Número de serie único">
                        </div>

                        <div class="create-form-group">
                            <label for="fecha_compra" class="create-form-label">
                                <i class="fas fa-calendar-plus"></i>Fecha de Compra
                            </label>
                            <input type="date" class="create-form-control" id="fecha_compra" name="fecha_compra">
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>

    <div class="container-fluid">
        <div class="create-form-card">
            <div class="create-form-actions">
                <a href="{{ url_for('listar_equipos') }}" class="create-btn create-btn-secondary">
                    <i class="fas fa-times"></i>Cancelar
                </a>
                <button type="submit" form="create-equipo-form" class="create-btn create-btn-primary">
                    <i class="fas fa-tools"></i>Crear Equipo
                </button>
            </div>
        </div>
    </div>
</div>

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
{% endblock %}'''
    
    with open('templates/equipos/crear.html', 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("✅ Equipos actualizado")

def actualizar_formulario_facturas():
    """Actualizar formulario de facturas"""
    
    contenido = '''{% extends "base.html" %}

{% block title %}Nueva Factura - Sistema Constructora{% endblock %}

{% block content %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/create-forms.css') }}">

<div class="create-form-container">
    <div class="create-page-header">
        <nav class="breadcrumb">
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{ url_for('listar_facturas') }}">Facturas</a>
            <span class="breadcrumb-separator">/</span>
            <span>Nueva</span>
        </nav>
        <h1 class="create-page-title">
            <i class="fas fa-file-invoice"></i>
            Crear Nueva Factura
        </h1>
    </div>

    <div class="container-fluid">
        <form method="POST" action="{{ url_for('crear_factura') }}" id="create-factura-form" class="needs-validation" novalidate>
            <div class="create-form-row">
                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-file-alt"></i> Información de la Factura</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="numero_factura" class="create-form-label">
                                <i class="fas fa-hashtag"></i>Número de Factura<span class="required">*</span>
                            </label>
                            <input type="text" class="create-form-control" id="numero_factura" name="numero_factura" 
                                   placeholder="Ej: FAC-2025-001" required>
                        </div>

                        <div class="create-form-group">
                            <label for="fecha_factura" class="create-form-label">
                                <i class="fas fa-calendar"></i>Fecha de Facturación<span class="required">*</span>
                            </label>
                            <input type="date" class="create-form-control" id="fecha_factura" name="fecha_factura" required>
                        </div>

                        <div class="create-form-group">
                            <label for="fecha_vencimiento" class="create-form-label">
                                <i class="fas fa-calendar-times"></i>Fecha de Vencimiento
                            </label>
                            <input type="date" class="create-form-control" id="fecha_vencimiento" name="fecha_vencimiento">
                        </div>
                    </div>
                </div>

                <div class="create-form-card">
                    <div class="card-header">
                        <h5><i class="fas fa-dollar-sign"></i> Información Financiera</h5>
                    </div>
                    <div class="card-body">
                        <div class="create-form-group">
                            <label for="valor_bruto" class="create-form-label">
                                <i class="fas fa-calculator"></i>Valor Bruto<span class="required">*</span>
                            </label>
                            <input type="number" class="create-form-control" id="valor_bruto" name="valor_bruto" 
                                   placeholder="0.00" step="0.01" min="0" required>
                        </div>

                        <div class="create-form-group">
                            <label for="iva" class="create-form-label">
                                <i class="fas fa-percentage"></i>IVA (%)
                            </label>
                            <input type="number" class="create-form-control" id="iva" name="iva" 
                                   placeholder="19" step="0.01" min="0" max="100">
                        </div>

                        <div class="create-form-group">
                            <label for="estado_factura" class="create-form-label">
                                <i class="fas fa-check-circle"></i>Estado<span class="required">*</span>
                            </label>
                            <select class="create-form-control" id="estado_factura" name="estado_factura" required>
                                <option value="">Seleccionar estado...</option>
                                <option value="PENDIENTE">⏳ Pendiente</option>
                                <option value="PAGADA">✅ Pagada</option>
                                <option value="VENCIDA">❌ Vencida</option>
                                <option value="ANULADA">🚫 Anulada</option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>

    <div class="container-fluid">
        <div class="create-form-card">
            <div class="create-form-actions">
                <a href="{{ url_for('listar_facturas') }}" class="create-btn create-btn-secondary">
                    <i class="fas fa-times"></i>Cancelar
                </a>
                <button type="submit" form="create-factura-form" class="create-btn create-btn-primary">
                    <i class="fas fa-file-invoice"></i>Crear Factura
                </button>
            </div>
        </div>
    </div>
</div>

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
{% endblock %}'''
    
    with open('templates/facturas/crear.html', 'w', encoding='utf-8') as f:
        f.write(contenido)
    print("✅ Facturas actualizado")

if __name__ == "__main__":
    print("🔄 ACTUALIZANDO FORMULARIOS RESTANTES...")
    print("=" * 50)
    
    actualizar_formulario_proveedores()
    actualizar_formulario_equipos()
    actualizar_formulario_facturas()
    
    print("\n✅ COMPLETADO - 3 formularios adicionales actualizados")
    print("🎯 Total de formularios modernizados: 6/19")
    print("📋 Formularios listos: Proyectos, Obras, Empleados, Vehículos, Materiales, Proveedores, Equipos, Facturas")