#!/usr/bin/env python3
"""
Script para mejorar automáticamente las vistas de detalles de múltiples módulos
"""

import os
import re

def crear_vista_detalle_moderna(modulo, campos_principales, campo_id, icono_principal="fas fa-info-circle"):
    """
    Genera un template moderno para vista de detalles
    """
    
    # Mapear tipos de campos a iconos
    iconos = {
        'nombre': 'fas fa-tag',
        'descripcion': 'fas fa-align-left',
        'tipo': 'fas fa-layer-group',
        'categoria': 'fas fa-layer-group',
        'estado': 'fas fa-info-circle',
        'fecha': 'fas fa-calendar-alt',
        'precio': 'fas fa-coins',
        'valor': 'fas fa-coins',
        'marca': 'fas fa-certificate',
        'modelo': 'fas fa-car',
        'telefono': 'fas fa-phone',
        'email': 'fas fa-envelope',
        'direccion': 'fas fa-map-marker-alt'
    }
    
    template = f"""{% extends "base.html" %}
{% block title %}Detalle {modulo.title()}{% endblock %}
{% block content %}
<div class="page-header">
  <nav class="breadcrumb">
    <a href="{{{{ url_for('dashboard') }}}}">Dashboard</a>
    <span class="breadcrumb-separator">/</span>
    <a href="{{{{ url_for('listar_{modulo}s') }}}}">{modulo.title()}s</a>
    <span class="breadcrumb-separator">/</span>
    <span>Detalle</span>
  </nav>
  <h1 class="page-title">{icono_principal[11:]} {{{{ {modulo}.{campos_principales[0]} or '{modulo.title()}' }}}} <small class="text-muted">ID: {{{{ {modulo}.{campo_id} }}}}</small></h1>
</div>

<div class="row">
  <div class="col-md-8">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0"><i class="{icono_principal}"></i> Información Principal</h5>
      </div>
      <div class="card-body">
        <dl class="row">"""

    # Agregar campos principales
    for i, campo in enumerate(campos_principales[:6]):  # Máximo 6 campos principales
        icono = iconos.get(campo.lower().split('_')[0], 'fas fa-info')
        if 'precio' in campo.lower() or 'valor' in campo.lower():
            template += f"""
          <dt class="col-sm-4"><i class="{icono}"></i> {campo.replace('_', ' ').title()}</dt>
          <dd class="col-sm-8">
            {{% if {modulo}.{campo} is not none %}}
              <strong class="text-success">Q{{{{ "{{:,.2f}}".format({modulo}.{campo}) }}}}</strong>
            {{% else %}}
              <span class="text-muted">N/D</span>
            {{% endif %}}
          </dd>"""
        elif 'estado' in campo.lower():
            template += f"""
          <dt class="col-sm-4"><i class="{icono}"></i> {campo.replace('_', ' ').title()}</dt>
          <dd class="col-sm-8">
            <span class="badge badge-primary">{{{{ {modulo}.{campo} or 'N/D' }}}}</span>
          </dd>"""
        else:
            template += f"""
          <dt class="col-sm-4"><i class="{icono}"></i> {campo.replace('_', ' ').title()}</dt>
          <dd class="col-sm-8">
            <strong>{{{{ {modulo}.{campo} or 'N/D' }}}}</strong>
          </dd>"""

    template += """
        </dl>
      </div>
    </div>
  </div>
  
  <div class="col-md-4">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0"><i class="fas fa-cogs"></i> Acciones</h5>
      </div>
      <div class="card-body">
        <div class="d-flex flex-column gap-2">"""

    template += f"""
          <a class="btn btn-primary" href="{{{{ url_for('editar_{modulo}', id={modulo}.{campo_id}) }}}}">
            <i class="fas fa-edit"></i> Editar {modulo.title()}
          </a>
          <a class="btn btn-secondary" href="{{{{ url_for('listar_{modulo}s') }}}}">
            <i class="fas fa-arrow-left"></i> Volver a Lista
          </a>
          <form action="{{{{ url_for('eliminar_{modulo}', id={modulo}.{campo_id}) }}}}" method="post" onsubmit="return confirm('¿Eliminar este {modulo}?');" class="mt-2">
            <button class="btn btn-danger w-100" type="submit">
              <i class="fas fa-trash"></i> Eliminar
            </button>
          </form>"""

    template += """
        </div>
      </div>
    </div>
  </div>
</div>

<style>
.card-header h5 {
  color: #495057;
}

.badge {
  font-size: 0.9rem;
}

.gap-2 > * + * {
  margin-top: 0.5rem;
}
</style>
{% endblock %}"""

    return template

# Configuración de módulos a actualizar
modulos_config = {
    'equipo': {
        'campos': ['nombre', 'marca', 'modelo', 'tipo_equipo', 'estado_actual', 'capacidad'],
        'campo_id': 'id_equipo',
        'icono': '🔧'
    },
    'vehiculo': {
        'campos': ['modelo', 'marca', 'anio', 'placa', 'tipo_vehiculo', 'estado'],
        'campo_id': 'id_vehiculo', 
        'icono': '🚛'
    },
    'contrato': {
        'campos': ['numero_contrato', 'tipo_contrato', 'fecha_inicio', 'fecha_fin', 'valor_contrato', 'estado'],
        'campo_id': 'id_contrato',
        'icono': '📋'
    }
}

def actualizar_modulos():
    print("🔄 Iniciando actualización masiva de vistas de detalles...")
    
    for modulo, config in modulos_config.items():
        try:
            # Generar template
            template_content = crear_vista_detalle_moderna(
                modulo, 
                config['campos'], 
                config['campo_id'],
                f"fas fa-{modulo.lower()}"
            )
            
            # Escribir archivo
            template_path = f"templates/{modulo}s/detalle.html"
            
            print(f"✅ Template generado para {modulo}: {len(template_content)} caracteres")
            print(f"   📂 Archivo: {template_path}")
            print(f"   🎯 Campos: {', '.join(config['campos'][:3])}...")
            
        except Exception as e:
            print(f"❌ Error con {modulo}: {e}")
    
    print(f"\n🎉 Proceso completado para {len(modulos_config)} módulos")
    print("📝 Los templates están listos para aplicar manualmente")

if __name__ == "__main__":
    actualizar_modulos()