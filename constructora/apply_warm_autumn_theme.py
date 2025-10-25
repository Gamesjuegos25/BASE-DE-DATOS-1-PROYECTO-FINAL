#!/usr/bin/env python3
"""
Script para aplicar el tema Warm Autumn Glow a todos los templates del ERP Constructora
Actualiza las clases CSS y colores según la nueva paleta de colores.
"""

import os
import re
from pathlib import Path

# Mapeo de clases CSS antiguas a nuevas (Warm Autumn)
CLASS_MAPPINGS = {
    # Colores Bootstrap a Warm Autumn
    'btn-primary': 'btn btn-primary',
    'btn-secondary': 'btn btn-secondary', 
    'btn-success': 'btn btn-accent',
    'btn-danger': 'btn btn-danger',
    'btn-warning': 'btn btn-secondary',
    'btn-info': 'btn btn-primary',
    
    # Cards y contenedores
    'card': 'stat-card',
    'card-header': 'stat-header',
    'card-body': 'module-content',
    'card-footer': 'module-actions',
    
    # Badges
    'badge-primary': 'badge badge-primary',
    'badge-secondary': 'badge badge-secondary',
    'badge-success': 'badge badge-success',
    'badge-danger': 'badge badge-danger',
    'badge-warning': 'badge badge-warning',
    'badge-info': 'badge badge-primary',
    
    # Alertas
    'alert-success': 'alert alert-success',
    'alert-danger': 'alert alert-danger',
    'alert-warning': 'alert alert-warning',
    'alert-info': 'alert alert-info',
    
    # Colores de texto
    'text-primary': 'text-prussian-blue',
    'text-secondary': 'text-orange-wheel',
    'text-success': 'text-success',
    'text-danger': 'text-fire-engine-red',
    'text-warning': 'text-orange-wheel',
    'text-info': 'text-prussian-blue-700',
    'text-muted': 'text-vanilla-600',
    
    # Colores de fondo
    'bg-primary': 'bg-gradient-warm-primary text-white',
    'bg-secondary': 'bg-gradient-warm-secondary text-white',
    'bg-success': 'bg-success text-white',
    'bg-danger': 'bg-gradient-warm-danger text-white',
    'bg-warning': 'bg-gradient-warm-secondary text-white',
    'bg-info': 'bg-gradient-warm-primary text-white',
    'bg-light': 'bg-vanilla-800',
    'bg-dark': 'bg-prussian-blue text-white',
    
    # Tablas
    'table-responsive': 'table-container',
    'table-striped': 'table',
    'table-hover': 'table',
    
    # Formularios
    'form-group': 'form-group',
    'form-control': 'form-control',
    'form-label': 'form-label',
    
    # Grid Bootstrap a Tailwind-like
    'container': 'max-w-7xl mx-auto px-6',
    'container-fluid': 'w-full px-4',
    'row': 'flex flex-wrap -mx-2',
    'col': 'flex-1 px-2',
    'col-12': 'w-full px-2',
    'col-md-6': 'w-full md:w-1/2 px-2',
    'col-md-4': 'w-full md:w-1/3 px-2',
    'col-md-3': 'w-full md:w-1/4 px-2',
    'col-lg-4': 'w-full lg:w-1/3 px-2',
    'col-lg-6': 'w-full lg:w-1/2 px-2',
    
    # Utilidades de espaciado
    'mb-4': 'mb-6',
    'mt-4': 'mt-6',
    'p-4': 'p-6',
    'px-4': 'px-6',
    'py-4': 'py-6',
    
    # Flexbox
    'd-flex': 'flex',
    'justify-content-between': 'justify-between',
    'justify-content-center': 'justify-center',
    'align-items-center': 'items-center',
    'flex-column': 'flex-col',
    
    # Display
    'd-none': 'hidden',
    'd-block': 'block',
    'd-inline-block': 'inline-block',
}

# Mapeo específico de iconos a colores warm autumn
ICON_COLOR_MAPPINGS = {
    'fas fa-building': 'text-prussian-blue',
    'fas fa-users': 'text-orange-wheel', 
    'fas fa-hammer': 'text-orange-wheel',
    'fas fa-boxes': 'text-vanilla-100',
    'fas fa-tools': 'text-xanthous-100',
    'fas fa-chart-line': 'text-xanthous',
    'fas fa-chart-bar': 'text-xanthous',
    'fas fa-dollar-sign': 'text-xanthous',
    'fas fa-exclamation-triangle': 'text-fire-engine-red',
    'fas fa-check-circle': 'text-success',
    'fas fa-info-circle': 'text-prussian-blue-700',
}

def find_templates_directory():
    """Encuentra el directorio de templates del proyecto."""
    current_dir = Path.cwd()
    
    # Buscar el directorio templates
    templates_dirs = list(current_dir.rglob("templates"))
    
    if not templates_dirs:
        print("❌ No se encontró el directorio templates")
        return None
        
    # Tomar el primer directorio templates encontrado
    templates_dir = templates_dirs[0]
    print(f"✅ Directorio templates encontrado: {templates_dir}")
    return templates_dir

def backup_file(file_path):
    """Crea una copia de seguridad del archivo original."""
    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
    if not backup_path.exists():
        backup_path.write_text(file_path.read_text(encoding='utf-8'), encoding='utf-8')
        print(f"💾 Backup creado: {backup_path.name}")

def apply_warm_autumn_theme(content):
    """Aplica las transformaciones del tema Warm Autumn al contenido HTML."""
    
    # Aplicar mapeos de clases
    for old_class, new_class in CLASS_MAPPINGS.items():
        # Buscar clases completas
        pattern = rf'\bclass="([^"]*)\b{re.escape(old_class)}\b([^"]*)"'
        
        def replace_class(match):
            before = match.group(1)
            after = match.group(2) 
            # Si la nueva clase ya contiene la clase antigua, no duplicar
            if old_class in new_class and old_class in f"{before}{after}":
                return f'class="{before.strip()} {new_class.strip()} {after.strip()}".replace("  ", " ").strip()'
            else:
                return f'class="{before}{new_class}{after}"'
        
        content = re.sub(pattern, replace_class, content)
    
    # Aplicar colores a iconos específicos
    for icon, color_class in ICON_COLOR_MAPPINGS.items():
        # Agregar clase de color al icono si no la tiene
        pattern = rf'<i class="([^"]*{re.escape(icon)}[^"]*)"'
        
        def add_icon_color(match):
            existing_classes = match.group(1)
            if not any(color in existing_classes for color in ['text-', 'text-']):
                return f'<i class="{existing_classes} {color_class}"'
            return match.group(0)
        
        content = re.sub(pattern, add_icon_color, content)
    
    # Actualizar CDN de FontAwesome a versión más reciente
    content = content.replace(
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/'
    )
    
    # Agregar clases de animación a elementos importantes
    content = re.sub(
        r'<div class="([^"]*card[^"]*)"',
        r'<div class="\1 fade-in-up"',
        content
    )
    
    # Mejorar botones de acción en tablas
    def improve_button_links(match):
        href_match = re.search(r'href="([^"]*)"', match.group(0))
        href_value = href_match.group(1) if href_match else "#"
        class_value = match.group(1)
        title_value = match.group(2)
        return f'<a href="{href_value}" class="{class_value} transition-all hover:scale-110 hover:-translate-y-1" title="{title_value}">'
    
    content = re.sub(
        r'<a[^>]*href="[^"]*"[^>]*class="([^"]*btn[^"]*)"[^>]*title="([^"]*)"[^>]*>',
        improve_button_links,
        content
    )
    
    return content

def process_html_file(file_path):
    """Procesa un archivo HTML individual."""
    try:
        # Leer contenido original
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Crear backup
        backup_file(file_path)
        
        # Aplicar transformaciones
        content = apply_warm_autumn_theme(content)
        
        # Solo escribir si hay cambios
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            print(f"✅ Actualizado: {file_path.name}")
            return True
        else:
            print(f"⏭️  Sin cambios: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ Error procesando {file_path.name}: {str(e)}")
        return False

def create_theme_application_script():
    """Crea un script JS para aplicar efectos dinámicos del tema."""
    
    js_content = '''
/**
 * Warm Autumn Theme - Dynamic Effects
 * Efectos dinámicos y interacciones para el tema Warm Autumn Glow
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Aplicar animaciones de entrada
    function initAnimations() {
        const elements = document.querySelectorAll('.fade-in-up, .slide-in-left');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0) translateX(0)';
                }
            });
        }, { threshold: 0.1 });
        
        elements.forEach(element => {
            element.style.opacity = '0';
            if (element.classList.contains('fade-in-up')) {
                element.style.transform = 'translateY(30px)';
            } else if (element.classList.contains('slide-in-left')) {
                element.style.transform = 'translateX(-30px)';
            }
            element.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            observer.observe(element);
        });
    }
    
    // Mejorar interacciones de botones
    function enhanceButtons() {
        const buttons = document.querySelectorAll('.btn, .btn-action');
        
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px) scale(1.05)';
                this.style.boxShadow = 'var(--shadow-lg)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = 'var(--shadow)';
            });
            
            button.addEventListener('mousedown', function() {
                this.style.transform = 'translateY(0) scale(0.98)';
            });
            
            button.addEventListener('mouseup', function() {
                this.style.transform = 'translateY(-2px) scale(1.05)';
            });
        });
    }
    
    // Mejorar tarjetas con efectos hover
    function enhanceCards() {
        const cards = document.querySelectorAll('.stat-card, .module-card, .card');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-8px) scale(1.02)';
                this.style.boxShadow = 'var(--shadow-xl)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = 'var(--shadow)';
            });
        });
    }
    
    // Efectos para tablas
    function enhanceTables() {
        const tableRows = document.querySelectorAll('.table tbody tr');
        
        tableRows.forEach(row => {
            row.addEventListener('mouseenter', function() {
                this.style.background = 'linear-gradient(135deg, var(--vanilla-800), var(--vanilla-700))';
                this.style.transform = 'translateX(4px)';
            });
            
            row.addEventListener('mouseleave', function() {
                this.style.background = '';
                this.style.transform = 'translateX(0)';
            });
        });
    }
    
    // Efectos de pulso para métricas importantes
    function pulseMetrics() {
        const metrics = document.querySelectorAll('.stat-value');
        
        setInterval(() => {
            metrics.forEach((metric, index) => {
                setTimeout(() => {
                    metric.style.animation = 'pulse-warm 0.5s ease';
                    setTimeout(() => {
                        metric.style.animation = '';
                    }, 500);
                }, index * 100);
            });
        }, 10000); // Cada 10 segundos
    }
    
    // Inicializar todas las mejoras
    initAnimations();
    enhanceButtons();
    enhanceCards();
    enhanceTables();
    pulseMetrics();
    
    // Efecto de loading para contenido dinámico
    window.showLoading = function(element) {
        element.classList.add('loading');
        setTimeout(() => {
            element.classList.remove('loading');
        }, 1000);
    };
    
    // Notificaciones toast con tema Warm Autumn
    window.showToast = function(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} fixed top-4 right-4 z-50 min-w-72 fade-in-up`;
        toast.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'} alert-icon"></i>
            <div>${message}</div>
            <button onclick="this.parentElement.remove()" class="modal-close">×</button>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-10px)';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    };
});

// Exportar funciones globales para uso en templates
window.WarmAutumnTheme = {
    showLoading: window.showLoading,
    showToast: window.showToast
};
'''
    
    return js_content

def main():
    """Función principal del script."""
    print("🎨 Aplicando tema Warm Autumn Glow al ERP Constructora")
    print("=" * 60)
    
    # Encontrar directorio templates
    templates_dir = find_templates_directory()
    if not templates_dir:
        return
    
    # Buscar todos los archivos HTML
    html_files = list(templates_dir.rglob("*.html"))
    
    if not html_files:
        print("❌ No se encontraron archivos HTML en el directorio templates")
        return
    
    print(f"📁 Encontrados {len(html_files)} archivos HTML")
    print("-" * 40)
    
    # Procesar cada archivo
    processed_count = 0
    for html_file in html_files:
        if process_html_file(html_file):
            processed_count += 1
    
    # Crear archivo JavaScript para efectos dinámicos
    js_dir = templates_dir.parent / 'static' / 'js'
    js_dir.mkdir(parents=True, exist_ok=True)
    
    js_file = js_dir / 'warm-autumn-theme.js'
    js_file.write_text(create_theme_application_script(), encoding='utf-8')
    print(f"✅ Creado archivo JS: {js_file}")
    
    # Resumen final
    print("-" * 40)
    print(f"✅ Procesamiento completado!")
    print(f"📊 Archivos procesados: {processed_count}/{len(html_files)}")
    print(f"💾 Backups creados en el mismo directorio")
    print(f"🎨 Tema Warm Autumn Glow aplicado exitosamente!")
    
    print("\n🔧 Pasos siguientes:")
    print("1. Verificar que los archivos CSS del tema estén enlazados en base.html")
    print("2. Incluir el archivo warm-autumn-theme.js en los templates")
    print("3. Revisar visualmente los cambios aplicados")
    print("4. Ajustar clases específicas si es necesario")

if __name__ == "__main__":
    main()