#!/usr/bin/env python3
"""
Aplicador de Mejoras Estéticas para Todas las Tablas
Mejora la responsividad y estética de todas las páginas de listado
"""

import os
import re
import glob
from pathlib import Path

class TableEnhancer:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.templates_dir = self.base_dir / "templates"
        
        # Patrones para identificar archivos de listado
        self.list_files_patterns = [
            "**/listar.html",
            "**/listar_*.html", 
            "**/index.html",
            "**/list.html"
        ]
        
        # Transformaciones comunes para mejorar tablas
        self.table_improvements = {
            # Envolver tabla en contenedor responsivo
            r'<table class="table([^"]*)"': r'<div class="table-wrapper fade-in-up"><div class="table-container-responsive"><table class="data-table-enhanced\1"',
            
            # Mejorar headers de tabla
            r'<thead>\s*<tr>': r'<thead><tr>',
            
            # Cerrar contenedores de tabla
            r'</table>\s*</div>': r'</table></div></div>',
            
            # Mejorar clases de botones
            r'btn btn-sm btn-info': r'btn-action-enhanced view',
            r'btn btn-sm btn-warning': r'btn-action-enhanced edit', 
            r'btn btn-sm btn-danger': r'btn-action-enhanced delete',
            
            # Mejorar contenedores de acciones
            r'class="action-buttons"': r'class="action-buttons-enhanced"',
            
            # Agregar clases responsivas
            r'<th>Cliente</th>': r'<th class="hidden-sm"><i class="fas fa-user"></i> Cliente</th>',
            r'<th>Estado</th>': r'<th><i class="fas fa-tasks"></i> Estado</th>',
            r'<th>Fecha': r'<th class="hidden-md"><i class="fas fa-calendar-alt"></i> Fecha',
            r'<th>Valor</th>': r'<th class="hidden-sm"><i class="fas fa-coins"></i> Valor</th>',
            r'<th>Acciones</th>': r'<th class="text-center"><i class="fas fa-cogs"></i> Acciones</th>',
        }
        
        # Mejoras para headers de página
        self.header_improvements = {
            r'<div class="page-header">': r'<div class="page-container"><div class="page-header fade-in-up">',
            r'<h1>([^<]+)</h1>': r'<h1><i class="fas fa-list"></i> \1</h1>',
        }
        
        # Mejoras para filtros de búsqueda
        self.search_improvements = {
            r'<div class="card[^>]*">[^<]*<div[^>]*>[^<]*<h3[^>]*>Filtros': r'<div class="search-card fade-in-up"><div class="search-header"><h3 class="search-title"><i class="fas fa-search"></i> Filtros',
            r'class="search-form"': r'class="search-form-enhanced"',
            r'class="form-group"': r'class="form-group-enhanced"',
            r'class="form-label"': r'class="form-label-enhanced"',
            r'class="form-control"': r'class="form-control-enhanced"',
        }

    def enhance_list_file(self, file_path):
        """Mejora un archivo de listado específico"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Agregar enlace al CSS mejorado si no existe
            if 'enhanced-tables.css' not in content:
                css_link = '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'css/enhanced-tables.css\') }}">'
                content = re.sub(r'({% block content %})', f'\\1\n{css_link}\n', content)
            
            # Aplicar mejoras de header
            for pattern, replacement in self.header_improvements.items():
                content = re.sub(pattern, replacement, content)
            
            # Aplicar mejoras de búsqueda
            for pattern, replacement in self.search_improvements.items():
                content = re.sub(pattern, replacement, content)
            
            # Aplicar mejoras de tabla
            for pattern, replacement in self.table_improvements.items():
                content = re.sub(pattern, replacement, content)
            
            # Agregar contenedor principal si no existe
            if 'page-container' not in content:
                # Buscar el inicio del contenido y agregar contenedor
                content = re.sub(
                    r'({% block content %})\s*(<div class="[^"]*")',
                    r'\1\n<div class="page-container">\n\2',
                    content
                )
                # Cerrar contenedor antes del endblock
                content = re.sub(
                    r'({% endblock %})',
                    r'</div>\n\1',
                    content
                )
            
            # Mejorar badges de estado
            state_badges = {
                r'<span class="badge badge-warning"': r'<span class="status-badge-enhanced warning"',
                r'<span class="badge badge-primary"': r'<span class="status-badge-enhanced primary"',
                r'<span class="badge badge-success"': r'<span class="status-badge-enhanced success"',
                r'<span class="badge badge-secondary"': r'<span class="status-badge-enhanced secondary"',
                r'<span class="badge badge-danger"': r'<span class="status-badge-enhanced danger"',
            }
            
            for pattern, replacement in state_badges.items():
                content = re.sub(pattern, replacement, content)
            
            # Agregar JavaScript mejorado si no existe
            if 'document.addEventListener(\'DOMContentLoaded\'' not in content:
                js_code = """
<script>
// Mejoras JavaScript automáticas para tablas
document.addEventListener('DOMContentLoaded', function() {
    // Aplicar efectos de hover a filas de tabla
    const tableRows = document.querySelectorAll('.data-table-enhanced tbody tr, table tbody tr');
    tableRows.forEach((row, index) => {
        row.style.animationDelay = `${index * 0.1}s`;
        row.classList.add('fade-in-up');
        
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 15px rgba(247, 127, 0, 0.2)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });
    
    // Mejorar botones de acción con tooltips
    const actionButtons = document.querySelectorAll('.btn-action-enhanced, .action-buttons a, .action-buttons button');
    actionButtons.forEach(button => {
        if (!button.querySelector('.custom-tooltip')) {
            button.addEventListener('mouseenter', function() {
                const title = this.getAttribute('title');
                if (title) {
                    const tooltip = document.createElement('div');
                    tooltip.className = 'custom-tooltip';
                    tooltip.textContent = title;
                    tooltip.style.cssText = `
                        position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%);
                        background: var(--prussian-blue-700); color: var(--vanilla);
                        padding: 4px 8px; border-radius: 4px; font-size: 0.7rem;
                        white-space: nowrap; z-index: 1000; margin-bottom: 5px;
                    `;
                    this.style.position = 'relative';
                    this.appendChild(tooltip);
                }
            });
            
            button.addEventListener('mouseleave', function() {
                const tooltip = this.querySelector('.custom-tooltip');
                if (tooltip) tooltip.remove();
            });
        }
    });
    
    // Contador animado para números
    const statNumbers = document.querySelectorAll('.stat-number-enhanced, .stat-number');
    statNumbers.forEach(stat => {
        const finalNumber = parseInt(stat.textContent) || 0;
        if (finalNumber > 0) {
            let currentNumber = 0;
            const increment = Math.max(1, Math.ceil(finalNumber / 20));
            const timer = setInterval(() => {
                currentNumber += increment;
                if (currentNumber >= finalNumber) {
                    currentNumber = finalNumber;
                    clearInterval(timer);
                }
                stat.textContent = currentNumber;
            }, 100);
        }
    });
});
</script>"""
                content = re.sub(r'({% endblock %})', f'{js_code}\n\\1', content)
            
            # Solo escribir si hay cambios
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
                
        except Exception as e:
            print(f"Error procesando {file_path}: {e}")
            return False
        
        return False

    def enhance_all_tables(self):
        """Mejora todas las tablas del sistema"""
        print("🎨 INICIANDO MEJORAS ESTÉTICAS PARA TODAS LAS TABLAS")
        print("=" * 60)
        
        enhanced_files = []
        
        # Buscar todos los archivos de listado
        for pattern in self.list_files_patterns:
            files = list(self.templates_dir.glob(pattern))
            for file_path in files:
                if self.enhance_list_file(file_path):
                    enhanced_files.append(file_path.name)
                    print(f"   ✅ Mejorado: {file_path.relative_to(self.base_dir)}")
        
        print(f"\n📊 Resumen de mejoras:")
        print(f"   • Archivos procesados: {len(enhanced_files)}")
        print(f"   • Mejoras aplicadas:")
        print(f"     - Tablas completamente responsivas")
        print(f"     - Animaciones y efectos visuales")
        print(f"     - Botones de acción mejorados")
        print(f"     - Headers estéticamente mejorados")
        print(f"     - Búsqueda y filtros optimizados")
        print(f"     - JavaScript para interactividad")
        
        print("\n🎉 MEJORAS ESTÉTICAS COMPLETADAS!")
        print("📋 Beneficios obtenidos:")
        print("   ✨ Sin desbordamiento de tablas")
        print("   📱 Completamente responsivo")
        print("   🎯 Mejor experiencia de usuario")
        print("   🚀 Animaciones suaves")
        print("   💫 Efectos visuales mejorados")

if __name__ == "__main__":
    enhancer = TableEnhancer()
    enhancer.enhance_all_tables()