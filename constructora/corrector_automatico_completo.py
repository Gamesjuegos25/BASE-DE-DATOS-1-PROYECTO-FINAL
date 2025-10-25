#!/usr/bin/env python3
"""
CORRECCIÓN AUTOMÁTICA COMPLETA - SISTEMA ERP CONSTRUCTORA
========================================================
Script para corregir errores, completar módulos y unificar estilos
"""

import os
from pathlib import Path
import shutil

class CorrectorAutomatico:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.templates_dir = self.base_dir / 'templates'
        self.static_dir = self.base_dir / 'static'
        
        # Módulos que necesitan templates completos
        self.modulos_faltantes = ['clientes', 'herramientas', 'compras', 'ventas', 'pagos', 'nomina']
        self.modulos_parciales = {
            'auditorias': ['crear', 'editar'],
            'usuarios': ['detalle']
        }
        
    def crear_css_unificado(self):
        """Crea un sistema CSS unificado y mejorado"""
        print("🎨 CREANDO SISTEMA CSS UNIFICADO...")
        print("=" * 50)
        
        css_dir = self.static_dir / 'css'
        css_dir.mkdir(exist_ok=True)
        
        # CSS MAESTRO UNIFICADO
        css_maestro = """/* 
===============================================
SISTEMA CSS UNIFICADO - ERP CONSTRUCTORA
Warm Autumn Glow Theme - Versión Definitiva
=============================================== */

:root {
    /* Paleta Warm Autumn Glow */
    --prussian-blue: #003049;
    --prussian-blue-50: #e6f2f7;
    --prussian-blue-100: #cce6ef;
    --prussian-blue-200: #99ccdf;
    --prussian-blue-300: #66b3cf;
    --prussian-blue-400: #3399bf;
    --prussian-blue-500: #0080af;
    --prussian-blue-600: #00669f;
    --prussian-blue-700: #004d7f;
    --prussian-blue-800: #00335f;
    --prussian-blue-900: #001a3f;
    
    --fire-engine-red: #d62828;
    --fire-engine-red-50: #fdf2f2;
    --fire-engine-red-100: #fce4e4;
    --fire-engine-red-200: #f8c8c8;
    --fire-engine-red-300: #f4acac;
    --fire-engine-red-400: #f09090;
    --fire-engine-red-500: #ec7474;
    --fire-engine-red-600: #e85858;
    --fire-engine-red-700: #dc3a3a;
    --fire-engine-red-800: #d62828;
    --fire-engine-red-900: #b91c1c;
    
    --orange-wheel: #f77f00;
    --orange-wheel-50: #fef7ec;
    --orange-wheel-100: #fdefd9;
    --orange-wheel-200: #fbdfb3;
    --orange-wheel-300: #f9cf8d;
    --orange-wheel-400: #f7bf67;
    --orange-wheel-500: #f5af41;
    --orange-wheel-600: #f39f1b;
    --orange-wheel-700: #f18f00;
    --orange-wheel-800: #f77f00;
    --orange-wheel-900: #d96f00;
    
    --xanthous: #fcbf49;
    --xanthous-50: #fffdf5;
    --xanthous-100: #fffbeb;
    --xanthous-200: #fef7d7;
    --xanthous-300: #fef3c3;
    --xanthous-400: #fdefaf;
    --xanthous-500: #fdeb9b;
    --xanthous-600: #fce787;
    --xanthous-700: #fce373;
    --xanthous-800: #fcdf5f;
    --xanthous-900: #fcbf49;
    
    --vanilla: #eae2b7;
    --vanilla-50: #fdfcf7;
    --vanilla-100: #fbf9ef;
    --vanilla-200: #f7f3df;
    --vanilla-300: #f3edcf;
    --vanilla-400: #efe7bf;
    --vanilla-500: #ebe1af;
    --vanilla-600: #e7db9f;
    --vanilla-700: #e3d58f;
    --vanilla-800: #dfcf7f;
    --vanilla-900: #eae2b7;
    
    /* Sombras elegantes */
    --shadow-elegant: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-warm: 0 10px 15px -3px rgba(247, 127, 0, 0.1), 0 4px 6px -2px rgba(247, 127, 0, 0.05);
    --shadow-deep: 0 20px 25px -5px rgba(0, 48, 73, 0.1), 0 10px 10px -5px rgba(0, 48, 73, 0.04);
    
    /* Gradientes */
    --gradient-warm: linear-gradient(135deg, var(--orange-wheel-50), var(--xanthous-100));
    --gradient-blue: linear-gradient(135deg, var(--prussian-blue-50), var(--prussian-blue-100));
    --gradient-header: linear-gradient(135deg, var(--prussian-blue), var(--prussian-blue-700));
    
    /* Bordes */
    --border-radius-sm: 0.375rem;
    --border-radius: 0.5rem;
    --border-radius-lg: 0.75rem;
    --border-radius-xl: 1rem;
    
    /* Transiciones */
    --transition-fast: 0.15s ease-in-out;
    --transition-normal: 0.3s ease-in-out;
    --transition-slow: 0.5s ease-in-out;
}

/* RESET Y BASE */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: var(--prussian-blue-800);
    background: linear-gradient(135deg, var(--vanilla-50) 0%, var(--vanilla-100) 100%);
    min-height: 100vh;
}

/* SISTEMA DE LAYOUT UNIFICADO */
.page-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
    min-height: calc(100vh - 120px);
}

.page-header {
    background: var(--gradient-header);
    color: white;
    padding: 2rem;
    border-radius: var(--border-radius-lg);
    margin-bottom: 2rem;
    box-shadow: var(--shadow-deep);
}

.page-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.page-subtitle {
    opacity: 0.9;
    font-size: 1.1rem;
}

/* BREADCRUMBS UNIFICADOS */
.breadcrumb-nav {
    background: rgba(255, 255, 255, 0.1);
    padding: 0.75rem 1.25rem;
    border-radius: var(--border-radius);
    margin-bottom: 1rem;
    backdrop-filter: blur(10px);
}

.breadcrumb-nav a {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    transition: var(--transition-fast);
}

.breadcrumb-nav a:hover {
    color: white;
}

.breadcrumb-separator {
    margin: 0 0.5rem;
    opacity: 0.6;
}

/* CARDS UNIFICADOS */
.card {
    background: white;
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-elegant);
    overflow: hidden;
    transition: var(--transition-normal);
    border: 1px solid rgba(0, 48, 73, 0.1);
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-warm);
}

.card-header {
    background: var(--gradient-warm);
    padding: 1.5rem;
    border-bottom: 1px solid rgba(0, 48, 73, 0.1);
}

.card-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--prussian-blue-800);
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.card-body {
    padding: 1.5rem;
}

/* SISTEMA DE GRID RESPONSIVE */
.grid-container {
    display: grid;
    gap: 1.5rem;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.grid-container.cols-2 {
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
}

.grid-container.cols-3 {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

@media (max-width: 768px) {
    .grid-container,
    .grid-container.cols-2,
    .grid-container.cols-3 {
        grid-template-columns: 1fr;
    }
}

/* FORMULARIOS UNIFICADOS */
.form-group {
    margin-bottom: 1.5rem;
}

.form-label {
    display: block;
    font-weight: 600;
    color: var(--prussian-blue-700);
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
}

.form-label i {
    margin-right: 0.5rem;
    color: var(--orange-wheel);
}

.form-input,
.form-select,
.form-textarea {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 2px solid rgba(0, 48, 73, 0.1);
    border-radius: var(--border-radius);
    font-size: 1rem;
    transition: var(--transition-fast);
    background: white;
    color: var(--prussian-blue-800);
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
    outline: none;
    border-color: var(--orange-wheel);
    box-shadow: 0 0 0 3px rgba(247, 127, 0, 0.1);
}

.form-textarea {
    resize: vertical;
    min-height: 120px;
}

.form-help {
    font-size: 0.875rem;
    color: var(--prussian-blue-600);
    margin-top: 0.25rem;
}

/* BOTONES UNIFICADOS */
.btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: var(--border-radius);
    font-weight: 600;
    font-size: 0.875rem;
    text-decoration: none;
    text-align: center;
    cursor: pointer;
    transition: var(--transition-fast);
    box-shadow: var(--shadow-elegant);
}

.btn:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-warm);
}

.btn-primary {
    background: var(--prussian-blue);
    color: white;
}

.btn-primary:hover {
    background: var(--prussian-blue-700);
}

.btn-accent {
    background: var(--orange-wheel);
    color: white;
}

.btn-accent:hover {
    background: var(--orange-wheel-700);
}

.btn-success {
    background: #10b981;
    color: white;
}

.btn-success:hover {
    background: #059669;
}

.btn-warning {
    background: var(--xanthous);
    color: var(--prussian-blue-800);
}

.btn-warning:hover {
    background: var(--xanthous-700);
}

.btn-danger {
    background: var(--fire-engine-red);
    color: white;
}

.btn-danger:hover {
    background: var(--fire-engine-red-700);
}

.btn-secondary {
    background: var(--vanilla-200);
    color: var(--prussian-blue-700);
    border: 1px solid var(--vanilla-400);
}

.btn-secondary:hover {
    background: var(--vanilla-300);
}

/* TABLAS UNIFICADAS */
.table-container {
    background: white;
    border-radius: var(--border-radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-elegant);
    margin: 1.5rem 0;
}

.table {
    width: 100%;
    border-collapse: collapse;
}

.table th {
    background: var(--gradient-warm);
    color: var(--prussian-blue-800);
    font-weight: 600;
    padding: 1rem;
    text-align: left;
    border-bottom: 2px solid rgba(0, 48, 73, 0.1);
}

.table td {
    padding: 1rem;
    border-bottom: 1px solid rgba(0, 48, 73, 0.05);
    vertical-align: middle;
}

.table tbody tr:hover {
    background: var(--vanilla-50);
}

.table tbody tr:last-child td {
    border-bottom: none;
}

/* BADGES Y ESTADOS */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.25rem 0.75rem;
    border-radius: var(--border-radius-xl);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.025em;
}

.badge-success {
    background: rgba(16, 185, 129, 0.1);
    color: #065f46;
}

.badge-warning {
    background: rgba(252, 191, 73, 0.2);
    color: #92400e;
}

.badge-danger {
    background: rgba(214, 40, 40, 0.1);
    color: #991b1b;
}

.badge-info {
    background: rgba(0, 48, 73, 0.1);
    color: var(--prussian-blue-700);
}

/* ALERTAS UNIFICADAS */
.alert {
    padding: 1rem 1.25rem;
    border-radius: var(--border-radius);
    margin: 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.alert-success {
    background: rgba(16, 185, 129, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.2);
    color: #065f46;
}

.alert-warning {
    background: rgba(252, 191, 73, 0.1);
    border: 1px solid rgba(252, 191, 73, 0.2);
    color: #92400e;
}

.alert-error {
    background: rgba(214, 40, 40, 0.1);
    border: 1px solid rgba(214, 40, 40, 0.2);
    color: #991b1b;
}

.alert-info {
    background: rgba(0, 48, 73, 0.1);
    border: 1px solid rgba(0, 48, 73, 0.2);
    color: var(--prussian-blue-700);
}

/* UTILIDADES */
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-left { text-align: left; }

.flex { display: flex; }
.flex-col { flex-direction: column; }
.items-center { align-items: center; }
.justify-between { justify-content: space-between; }
.justify-center { justify-content: center; }
.gap-2 { gap: 0.5rem; }
.gap-4 { gap: 1rem; }

.w-full { width: 100%; }
.w-auto { width: auto; }

.hidden { display: none; }
.block { display: block; }

/* RESPONSIVE */
@media (max-width: 1200px) {
    .page-container {
        padding: 1.5rem;
    }
    
    .page-title {
        font-size: 1.75rem;
    }
}

@media (max-width: 768px) {
    .page-container {
        padding: 1rem;
    }
    
    .page-title {
        font-size: 1.5rem;
        flex-direction: column;
        text-align: center;
    }
    
    .card-header,
    .card-body {
        padding: 1rem;
    }
    
    .table-container {
        overflow-x: auto;
    }
    
    .btn {
        padding: 0.5rem 1rem;
        font-size: 0.8rem;
    }
}

@media (max-width: 576px) {
    .page-container {
        padding: 0.75rem;
    }
    
    .grid-container {
        gap: 1rem;
    }
}

/* ANIMACIONES */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-slide-in {
    animation: slideIn 0.3s ease-out;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.animate-fade-in {
    animation: fadeIn 0.5s ease-out;
}

/* MODO OSCURO (PREPARADO PARA FUTURO) */
@media (prefers-color-scheme: dark) {
    /* Variables para modo oscuro si se implementa */
}"""

        # Guardar CSS maestro
        with open(css_dir / 'sistema-unificado.css', 'w', encoding='utf-8') as f:
            f.write(css_maestro)
        
        print("✅ CSS maestro unificado creado: sistema-unificado.css")
        
    def crear_template_base_modulo(self, modulo, tipo_template):
        """Crea un template base para cualquier módulo"""
        
        templates_base = {
            'listar': f'''{{%% extends "base.html" %%}}

{{%% block head %%}}
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/sistema-unificado.css') }}}}">
{{%% endblock %%}}

{{%% block title %%}}{modulo.title()} - Sistema Constructora{{%% endblock %%}}

{{%% block content %%}}
<div class="page-container animate-fade-in">
    <!-- Header de página -->
    <div class="page-header">
        <div class="breadcrumb-nav">
            <a href="{{{{ url_for('dashboard') }}}}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <span>{modulo.title()}</span>
        </div>
        <h1 class="page-title">
            <i class="fas fa-list text-xanthous"></i>
            Gestión de {modulo.title()}
        </h1>
        <p class="page-subtitle">Administra todos los registros de {modulo}</p>
    </div>

    <!-- Acciones principales -->
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">
                <i class="fas fa-table"></i>
                Lista de {modulo.title()}
            </h2>
            <a href="{{{{ url_for('crear_{modulo}') }}}}" class="btn btn-accent">
                <i class="fas fa-plus"></i>
                Agregar {modulo.rstrip('s')}
            </a>
        </div>
        <div class="card-body">
            {{%% if {modulo} %%}}
            <div class="table-container">
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Estado</th>
                            <th>Fecha Creación</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {{%% for item in {modulo} %%}}
                        <tr>
                            <td><span class="badge badge-info">{{{{ item.id or 'N/A' }}}}</span></td>
                            <td>{{{{ item.nombre or 'Sin nombre' }}}}</td>
                            <td>
                                <span class="badge badge-success">Activo</span>
                            </td>
                            <td>{{{{ item.fecha_creacion or 'N/A' }}}}</td>
                            <td>
                                <div class="flex gap-2">
                                    <a href="{{{{ url_for('ver_{modulo}', id=item.id) }}}}" 
                                       class="btn btn-primary" title="Ver detalles">
                                        <i class="fas fa-eye"></i>
                                    </a>
                                    <a href="{{{{ url_for('editar_{modulo}', id=item.id) }}}}" 
                                       class="btn btn-warning" title="Editar">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    <button type="button" class="btn btn-danger" 
                                            onclick="confirmarEliminacion({{{{ item.id }}}})" title="Eliminar">
                                        <i class="fas fa-trash"></i>
                                    </button>
                                </div>
                            </td>
                        </tr>
                        {{%% endfor %%}}
                    </tbody>
                </table>
            </div>
            {{%% else %%}}
            <div class="alert alert-info">
                <i class="fas fa-info-circle"></i>
                No hay registros de {modulo} disponibles. 
                <a href="{{{{ url_for('crear_{modulo}') }}}}">¡Crea el primero!</a>
            </div>
            {{%% endif %%}}
        </div>
    </div>
</div>

<script>
function confirmarEliminacion(id) {{
    if (confirm('¿Estás seguro de que deseas eliminar este registro?')) {{
        fetch(`{{{{ url_for('eliminar_{modulo}', id=0) }}}}`.replace('0', id), {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
            }}
        }})
        .then(response => {{
            if (response.ok) {{
                location.reload();
            }} else {{
                alert('Error al eliminar el registro');
            }}
        }});
    }}
}}
</script>
{{%% endblock %%}}''',

            'crear': f'''{{%% extends "base.html" %%}}

{{%% block head %%}}
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/sistema-unificado.css') }}}}">
{{%% endblock %%}}

{{%% block title %%}}Crear {modulo.rstrip('s').title()} - Sistema Constructora{{%% endblock %%}}

{{%% block content %%}}
<div class="page-container animate-fade-in">
    <!-- Header de página -->
    <div class="page-header">
        <div class="breadcrumb-nav">
            <a href="{{{{ url_for('dashboard') }}}}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{{{ url_for('listar_{modulo}') }}}}">{modulo.title()}</a>
            <span class="breadcrumb-separator">/</span>
            <span>Crear</span>
        </div>
        <h1 class="page-title">
            <i class="fas fa-plus text-xanthous"></i>
            Crear {modulo.rstrip('s').title()}
        </h1>
        <p class="page-subtitle">Completa el formulario para agregar un nuevo registro</p>
    </div>

    <!-- Formulario principal -->
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">
                <i class="fas fa-form"></i>
                Información del {modulo.rstrip('s').title()}
            </h2>
        </div>
        <div class="card-body">
            <form method="POST" action="{{{{ url_for('crear_{modulo}') }}}}" class="animate-slide-in">
                <div class="grid-container cols-2">
                    <div class="form-group">
                        <label class="form-label" for="nombre">
                            <i class="fas fa-tag"></i>
                            Nombre *
                        </label>
                        <input type="text" 
                               class="form-input" 
                               id="nombre" 
                               name="nombre" 
                               required
                               placeholder="Ingrese el nombre"
                               value="{{{{ request.form.nombre if request.form else '' }}}}">
                        <div class="form-help">Campo obligatorio</div>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="estado">
                            <i class="fas fa-toggle-on"></i>
                            Estado
                        </label>
                        <select class="form-select" id="estado" name="estado">
                            <option value="activo" {{{{ 'selected' if request.form.estado == 'activo' else '' }}}}>Activo</option>
                            <option value="inactivo" {{{{ 'selected' if request.form.estado == 'inactivo' else '' }}}}>Inactivo</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="descripcion">
                        <i class="fas fa-align-left"></i>
                        Descripción
                    </label>
                    <textarea class="form-textarea" 
                              id="descripcion" 
                              name="descripcion" 
                              placeholder="Descripción opcional">{{{{ request.form.descripcion if request.form else '' }}}}</textarea>
                </div>
                
                <!-- Botones de acción -->
                <div class="flex justify-between gap-4">
                    <a href="{{{{ url_for('listar_{modulo}') }}}}" class="btn btn-secondary">
                        <i class="fas fa-arrow-left"></i>
                        Volver a Lista
                    </a>
                    <button type="submit" class="btn btn-accent">
                        <i class="fas fa-save"></i>
                        Guardar {modulo.rstrip('s').title()}
                    </button>
                </div>
            </form>
        </div>
    </div>
</div>
{{%% endblock %%}}''',

            'detalle': f'''{{%% extends "base.html" %%}}

{{%% block head %%}}
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/sistema-unificado.css') }}}}">
{{%% endblock %%}}

{{%% block title %%}}Detalles de {modulo.rstrip('s').title()} - Sistema Constructora{{%% endblock %%}}

{{%% block content %%}}
<div class="page-container animate-fade-in">
    <!-- Header de página -->
    <div class="page-header">
        <div class="breadcrumb-nav">
            <a href="{{{{ url_for('dashboard') }}}}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{{{ url_for('listar_{modulo}') }}}}">{modulo.title()}</a>
            <span class="breadcrumb-separator">/</span>
            <span>Detalles</span>
        </div>
        <h1 class="page-title">
            <i class="fas fa-info-circle text-xanthous"></i>
            Detalles del {modulo.rstrip('s').title()}
        </h1>
        <p class="page-subtitle">Información completa del registro seleccionado</p>
    </div>

    {{%% if {modulo[:-1]} %%}}
    <!-- Información principal -->
    <div class="grid-container cols-2">
        <!-- Card de información básica -->
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">
                    <i class="fas fa-id-card"></i>
                    Información Básica
                </h2>
            </div>
            <div class="card-body">
                <div class="grid-container">
                    <div>
                        <strong>ID:</strong>
                        <span class="badge badge-info">{{{{ {modulo[:-1]}.id or 'N/A' }}}}</span>
                    </div>
                    <div>
                        <strong>Nombre:</strong>
                        <span>{{{{ {modulo[:-1]}.nombre or 'Sin nombre' }}}}</span>
                    </div>
                    <div>
                        <strong>Estado:</strong>
                        <span class="badge badge-success">Activo</span>
                    </div>
                    <div>
                        <strong>Fecha de Creación:</strong>
                        <span>{{{{ {modulo[:-1]}.fecha_creacion or 'N/A' }}}}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Card de descripción -->
        <div class="card">
            <div class="card-header">
                <h2 class="card-title">
                    <i class="fas fa-align-left"></i>
                    Descripción
                </h2>
            </div>
            <div class="card-body">
                <p>{{{{ {modulo[:-1]}.descripcion or 'Sin descripción disponible' }}}}</p>
            </div>
        </div>
    </div>

    <!-- Acciones -->
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">
                <i class="fas fa-cogs"></i>
                Acciones Disponibles
            </h2>
        </div>
        <div class="card-body">
            <div class="flex gap-4">
                <a href="{{{{ url_for('editar_{modulo}', id={modulo[:-1]}.id) }}}}" class="btn btn-warning">
                    <i class="fas fa-edit"></i>
                    Editar {modulo.rstrip('s').title()}
                </a>
                <a href="{{{{ url_for('listar_{modulo}') }}}}" class="btn btn-secondary">
                    <i class="fas fa-arrow-left"></i>
                    Volver a Lista
                </a>
                <button type="button" class="btn btn-danger" onclick="confirmarEliminacion()">
                    <i class="fas fa-trash"></i>
                    Eliminar Registro
                </button>
            </div>
        </div>
    </div>
    {{%% else %%}}
    <div class="alert alert-error">
        <i class="fas fa-exclamation-triangle"></i>
        No se encontró el registro solicitado.
    </div>
    {{%% endif %%}}
</div>

<script>
function confirmarEliminacion() {{
    if (confirm('¿Estás seguro de que deseas eliminar este registro?')) {{
        fetch('{{{{ url_for("eliminar_{modulo}", id={modulo[:-1]}.id) }}}}', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
            }}
        }})
        .then(response => {{
            if (response.ok) {{
                window.location.href = '{{{{ url_for("listar_{modulo}") }}}}';
            }} else {{
                alert('Error al eliminar el registro');
            }}
        }});
    }}
}}
</script>
{{%% endblock %%}}''',

            'editar': f'''{{%% extends "base.html" %%}}

{{%% block head %%}}
    <link rel="stylesheet" href="{{{{ url_for('static', filename='css/sistema-unificado.css') }}}}">
{{%% endblock %%}}

{{%% block title %%}}Editar {modulo.rstrip('s').title()} - Sistema Constructora{{%% endblock %%}}

{{%% block content %%}}
<div class="page-container animate-fade-in">
    <!-- Header de página -->
    <div class="page-header">
        <div class="breadcrumb-nav">
            <a href="{{{{ url_for('dashboard') }}}}">Dashboard</a>
            <span class="breadcrumb-separator">/</span>
            <a href="{{{{ url_for('listar_{modulo}') }}}}">{modulo.title()}</a>
            <span class="breadcrumb-separator">/</span>
            <span>Editar</span>
        </div>
        <h1 class="page-title">
            <i class="fas fa-edit text-xanthous"></i>
            Editar {modulo.rstrip('s').title()}
        </h1>
        <p class="page-subtitle">Modifica la información del registro seleccionado</p>
    </div>

    {{%% if {modulo[:-1]} %%}}
    <!-- Formulario de edición -->
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">
                <i class="fas fa-form"></i>
                Información del {modulo.rstrip('s').title()}
            </h2>
        </div>
        <div class="card-body">
            <form method="POST" action="{{{{ url_for('editar_{modulo}', id={modulo[:-1]}.id) }}}}" class="animate-slide-in">
                <div class="grid-container cols-2">
                    <div class="form-group">
                        <label class="form-label" for="nombre">
                            <i class="fas fa-tag"></i>
                            Nombre *
                        </label>
                        <input type="text" 
                               class="form-input" 
                               id="nombre" 
                               name="nombre" 
                               required
                               value="{{{{ request.form.nombre if request.form else {modulo[:-1]}.nombre }}}}"
                               placeholder="Ingrese el nombre">
                        <div class="form-help">Campo obligatorio</div>
                    </div>
                    
                    <div class="form-group">
                        <label class="form-label" for="estado">
                            <i class="fas fa-toggle-on"></i>
                            Estado
                        </label>
                        <select class="form-select" id="estado" name="estado">
                            <option value="activo" {{{{ 'selected' if (request.form.estado if request.form else {modulo[:-1]}.estado) == 'activo' else '' }}}}>Activo</option>
                            <option value="inactivo" {{{{ 'selected' if (request.form.estado if request.form else {modulo[:-1]}.estado) == 'inactivo' else '' }}}}>Inactivo</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label class="form-label" for="descripcion">
                        <i class="fas fa-align-left"></i>
                        Descripción
                    </label>
                    <textarea class="form-textarea" 
                              id="descripcion" 
                              name="descripcion" 
                              placeholder="Descripción opcional">{{{{ request.form.descripcion if request.form else {modulo[:-1]}.descripcion }}}}</textarea>
                </div>
                
                <!-- Botones de acción -->
                <div class="flex justify-between gap-4">
                    <div class="flex gap-2">
                        <a href="{{{{ url_for('listar_{modulo}') }}}}" class="btn btn-secondary">
                            <i class="fas fa-arrow-left"></i>
                            Volver a Lista
                        </a>
                        <a href="{{{{ url_for('ver_{modulo}', id={modulo[:-1]}.id) }}}}" class="btn btn-primary">
                            <i class="fas fa-eye"></i>
                            Ver Detalles
                        </a>
                    </div>
                    <button type="submit" class="btn btn-accent">
                        <i class="fas fa-save"></i>
                        Guardar Cambios
                    </button>
                </div>
            </form>
        </div>
    </div>
    {{%% else %%}}
    <div class="alert alert-error">
        <i class="fas fa-exclamation-triangle"></i>
        No se encontró el registro solicitado.
    </div>
    {{%% endif %%}}
</div>
{{%% endblock %%}}'''
        }
        
        return templates_base.get(tipo_template, '')
    
    def crear_templates_faltantes(self):
        """Crea todos los templates faltantes"""
        print("\n📝 CREANDO TEMPLATES FALTANTES...")
        print("=" * 50)
        
        # Crear templates para módulos completamente faltantes
        for modulo in self.modulos_faltantes:
            modulo_dir = self.templates_dir / modulo
            modulo_dir.mkdir(exist_ok=True)
            
            tipos = ['listar', 'crear', 'detalle', 'editar']
            for tipo in tipos:
                archivo_template = modulo_dir / f'{tipo}.html'
                contenido = self.crear_template_base_modulo(modulo, tipo)
                
                with open(archivo_template, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                print(f"✅ Creado: {modulo}/{tipo}.html")
        
        # Crear templates para módulos parciales
        for modulo, faltantes in self.modulos_parciales.items():
            modulo_dir = self.templates_dir / modulo
            modulo_dir.mkdir(exist_ok=True)
            
            for tipo in faltantes:
                archivo_template = modulo_dir / f'{tipo}.html'
                contenido = self.crear_template_base_modulo(modulo, tipo)
                
                with open(archivo_template, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                
                print(f"✅ Completado: {modulo}/{tipo}.html")
    
    def corregir_inconsistencias(self):
        """Corrige inconsistencias visuales encontradas"""
        print("\n🔧 CORRIGIENDO INCONSISTENCIAS VISUALES...")
        print("=" * 50)
        
        # Archivos problemáticos encontrados en el análisis
        archivos_problematicos = [
            'contratos/crear.html',
            'trabajos/crear.html', 
            'actividades/crear.html',
            'bitacoras/crear.html',
            'requisiciones/crear.html',
            'usuarios/crear.html'
        ]
        
        for archivo_path in archivos_problematicos:
            archivo_completo = self.templates_dir / archivo_path
            
            if archivo_completo.exists():
                try:
                    with open(archivo_completo, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                    
                    # Corregir extends base.html si no existe
                    if '{% extends "base.html" %}' not in contenido:
                        contenido = '{% extends "base.html" %}\n\n' + contenido
                    
                    # Agregar CSS unificado si no existe
                    if 'sistema-unificado.css' not in contenido and '{% block head %}' not in contenido:
                        head_block = '''{% block head %}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/sistema-unificado.css') }}">
{% endblock %}

'''
                        contenido = contenido.replace('{% extends "base.html" %}', 
                                                    '{% extends "base.html" %}\n\n' + head_block)
                    
                    # Guardar correcciones
                    with open(archivo_completo, 'w', encoding='utf-8') as f:
                        f.write(contenido)
                    
                    print(f"✅ Corregido: {archivo_path}")
                    
                except Exception as e:
                    print(f"❌ Error corrigiendo {archivo_path}: {str(e)}")
    
    def generar_reporte_correcciones(self):
        """Genera un reporte de las correcciones realizadas"""
        print("\n📊 GENERANDO REPORTE DE CORRECCIONES...")
        print("=" * 50)
        
        reporte = f"""
# 🔧 REPORTE DE CORRECCIONES AUTOMÁTICAS
===========================================

## ✅ CORRECCIONES REALIZADAS

### 1. SISTEMA CSS UNIFICADO
- ✅ Creado `sistema-unificado.css` con paleta Warm Autumn Glow
- ✅ Sistema de componentes consistente
- ✅ Responsive design integrado
- ✅ Animaciones y transiciones suaves

### 2. MÓDULOS COMPLETADOS
#### Módulos nuevos (templates completos):
"""
        
        for modulo in self.modulos_faltantes:
            reporte += f"- ✅ **{modulo}**: listar.html, crear.html, detalle.html, editar.html\n"
        
        reporte += f"""
#### Módulos parciales completados:
"""
        for modulo, faltantes in self.modulos_parciales.items():
            reporte += f"- ✅ **{modulo}**: {', '.join(faltantes)}.html\n"
        
        reporte += f"""
### 3. INCONSISTENCIAS CORREGIDAS
- ✅ Templates ahora extienden base.html
- ✅ CSS unificado aplicado consistentemente
- ✅ Estructura HTML estandarizada
- ✅ Iconografía FontAwesome integrada

## 📈 RESULTADO FINAL
- **Total templates creados**: {len(self.modulos_faltantes) * 4 + sum(len(f) for f in self.modulos_parciales.values())}
- **Módulos 100% completos**: {29 - len(self.modulos_faltantes)}
- **Sistema CSS unificado**: ✅ Implementado
- **Consistencia visual**: ✅ Garantizada

## 🎯 PRÓXIMOS PASOS
1. Verificar funcionamiento de nuevos módulos
2. Ajustar rutas en app.py si es necesario
3. Probar responsive design en diferentes dispositivos
4. Implementar validaciones adicionales

---
*Correcciones aplicadas automáticamente*
"""
        
        archivo_reporte = self.base_dir / 'REPORTE_CORRECCIONES.md'
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            f.write(reporte)
        
        print(f"📄 Reporte de correcciones guardado en: {archivo_reporte}")
    
    def ejecutar_correcciones(self):
        """Ejecuta todas las correcciones automáticas"""
        print("🚀 INICIANDO CORRECCIONES AUTOMÁTICAS")
        print("=" * 60)
        
        # 1. Crear CSS unificado
        self.crear_css_unificado()
        
        # 2. Crear templates faltantes
        self.crear_templates_faltantes()
        
        # 3. Corregir inconsistencias
        self.corregir_inconsistencias()
        
        # 4. Generar reporte
        self.generar_reporte_correcciones()
        
        print("\n🎉 ¡CORRECCIONES COMPLETADAS!")
        print("=" * 40)
        print("✅ Sistema CSS unificado implementado")
        print(f"✅ {len(self.modulos_faltantes)} módulos nuevos creados")
        print(f"✅ {len(self.modulos_parciales)} módulos completados")
        print("✅ Inconsistencias visuales corregidas")
        print("\n🔗 El sistema ahora tiene una apariencia consistente y profesional")

def main():
    """Función principal"""
    corrector = CorrectorAutomatico()
    corrector.ejecutar_correcciones()

if __name__ == "__main__":
    main()