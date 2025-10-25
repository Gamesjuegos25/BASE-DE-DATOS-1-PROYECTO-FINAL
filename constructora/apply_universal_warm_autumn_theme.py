#!/usr/bin/env python3
"""
Aplicador Universal de Tema Warm Autumn Glow
Asegura que todos los elementos del sistema usen los colores del tema
"""

import os
import re
import glob
from pathlib import Path

class WarmAutumnThemeApplicator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.templates_dir = self.base_dir / "templates"
        self.static_dir = self.base_dir / "static"
        
        # Mapeo de colores originales a colores del tema
        self.color_mappings = {
            # Colores básicos a Warm Autumn
            'blue': 'prussian-blue',
            'red': 'fire-engine-red', 
            'orange': 'orange-wheel',
            'yellow': 'xanthous',
            'beige': 'vanilla',
            'white': 'vanilla',
            
            # Colores específicos de Bootstrap/CSS
            'primary': 'prussian-blue',
            'secondary': 'orange-wheel',
            'success': 'xanthous-600',
            'danger': 'fire-engine-red',
            'warning': 'xanthous',
            'info': 'prussian-blue-400',
            'light': 'vanilla-200',
            'dark': 'prussian-blue-700'
        }
        
        # Clases CSS a reemplazar
        self.class_replacements = {
            # Bootstrap colors
            'btn-primary': 'btn btn-warm-primary',
            'btn-secondary': 'btn btn-warm-secondary',
            'btn-success': 'btn btn-warm-success',
            'btn-danger': 'btn btn-warm-danger',
            'btn-warning': 'btn btn-warm-warning',
            'btn-info': 'btn btn-warm-info',
            
            # Card colors
            'card-primary': 'card card-warm-primary',
            'card-secondary': 'card card-warm-secondary',
            
            # Text colors
            'text-primary': 'text-prussian-blue-600',
            'text-secondary': 'text-orange-wheel',
            'text-success': 'text-xanthous-600',
            'text-danger': 'text-fire-engine-red',
            'text-warning': 'text-xanthous',
            'text-info': 'text-prussian-blue-400',
            
            # Background colors
            'bg-primary': 'bg-prussian-blue',
            'bg-secondary': 'bg-orange-wheel',
            'bg-success': 'bg-xanthous-200',
            'bg-danger': 'bg-fire-engine-red-200',
            'bg-warning': 'bg-xanthous-200',
            'bg-info': 'bg-prussian-blue-200',
            'bg-light': 'bg-vanilla-200',
            'bg-dark': 'bg-prussian-blue-700'
        }
        
    def apply_color_variables_to_css(self):
        """Aplica variables de color a archivos CSS existentes"""
        print("🎨 Aplicando variables de color a archivos CSS...")
        
        css_files = list(self.static_dir.glob("**/*.css"))
        
        for css_file in css_files:
            if 'warm-autumn' in css_file.name or 'theme-override' in css_file.name:
                continue  # Skip theme files
                
            try:
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Replace common color values with CSS variables
                color_replacements = {
                    '#007bff': 'var(--prussian-blue)',
                    '#6c757d': 'var(--orange-wheel-300)',
                    '#28a745': 'var(--xanthous-600)',
                    '#dc3545': 'var(--fire-engine-red)',
                    '#ffc107': 'var(--xanthous)',
                    '#17a2b8': 'var(--prussian-blue-400)',
                    '#f8f9fa': 'var(--vanilla-100)',
                    '#343a40': 'var(--prussian-blue-700)',
                    
                    # More specific colors
                    'color: blue': 'color: var(--prussian-blue)',
                    'color: red': 'color: var(--fire-engine-red)',
                    'color: orange': 'color: var(--orange-wheel)',
                    'color: yellow': 'color: var(--xanthous)',
                    
                    'background-color: blue': 'background-color: var(--prussian-blue)',
                    'background-color: red': 'background-color: var(--fire-engine-red)',
                    'background-color: orange': 'background-color: var(--orange-wheel)',
                    'background-color: yellow': 'background-color: var(--xanthous)',
                    
                    'border-color: blue': 'border-color: var(--prussian-blue)',
                    'border-color: red': 'border-color: var(--fire-engine-red)',
                    'border-color: orange': 'border-color: var(--orange-wheel)',
                    'border-color: yellow': 'border-color: var(--xanthous)',
                }
                
                for old_color, new_color in color_replacements.items():
                    content = content.replace(old_color, new_color)
                
                # Only write if content changed
                if content != original_content:
                    with open(css_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"   ✅ Actualizado: {css_file.name}")
                        
            except Exception as e:
                print(f"   ❌ Error procesando {css_file}: {e}")
    
    def apply_theme_classes_to_templates(self):
        """Aplica clases del tema a templates HTML"""
        print("🏗️  Aplicando clases del tema a templates...")
        
        html_files = list(self.templates_dir.glob("**/*.html"))
        updated_count = 0
        
        for html_file in html_files:
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply class replacements
                for old_class, new_class in self.class_replacements.items():
                    # Replace class="old-class" with class="new-class"
                    content = re.sub(
                        rf'class="([^"]*\b){re.escape(old_class)}(\b[^"]*)"',
                        lambda m: f'class="{m.group(1)}{new_class}{m.group(2)}"',
                        content
                    )
                    
                    # Replace class='old-class' with class='new-class'
                    content = re.sub(
                        rf"class='([^']*\b){re.escape(old_class)}(\b[^']*)'",
                        lambda m: f"class='{m.group(1)}{new_class}{m.group(2)}'",
                        content
                    )
                
                # Add theme classes to common elements if not present
                theme_additions = {
                    '<button(?![^>]*class="[^"]*btn)': '<button class="btn btn-warm-primary"',
                    '<table(?![^>]*class="[^"]*table)': '<table class="table table-warm"',
                    '<div class="card"(?![^>]*warm)': '<div class="card card-warm"',
                    '<input(?![^>]*class="[^"]*form-control)': '<input class="form-control form-warm"',
                    '<select(?![^>]*class="[^"]*form-control)': '<select class="form-control form-warm"',
                    '<textarea(?![^>]*class="[^"]*form-control)': '<textarea class="form-control form-warm"'
                }
                
                for pattern, replacement in theme_additions.items():
                    content = re.sub(pattern, replacement, content)
                
                # Add fade-in animations to major sections
                if 'fade-in-up' not in content:
                    content = re.sub(
                        r'<div class="(content-wrapper|main-content|card-body)"',
                        r'<div class="\1 fade-in-up"',
                        content
                    )
                
                # Only write if content changed
                if content != original_content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_count += 1
                    print(f"   ✅ Actualizado: {html_file.name}")
                        
            except Exception as e:
                print(f"   ❌ Error procesando {html_file}: {e}")
        
        print(f"📊 Templates actualizados: {updated_count}")
    
    def inject_theme_meta_tags(self):
        """Inyecta meta tags del tema en base.html"""
        print("🏷️  Inyectando meta tags del tema...")
        
        base_html = self.templates_dir / "base.html"
        
        if not base_html.exists():
            print("   ❌ No se encontró base.html")
            return
        
        try:
            with open(base_html, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Theme meta tags
            theme_meta = '''    <!-- Warm Autumn Glow Theme Meta -->
    <meta name="theme-color" content="#003049">
    <meta name="msapplication-navbutton-color" content="#003049">
    <meta name="apple-mobile-web-app-status-bar-style" content="#003049">
    <style>
        /* Immediate color application to prevent flashing */
        body { background-color: #eae2b7 !important; }
        .header { background: linear-gradient(135deg, #003049, #00679f) !important; }
        .sidebar { background: linear-gradient(180deg, #001c2b, #003049) !important; }
    </style>'''
            
            # Insert after viewport meta tag
            if 'theme-color' not in content:
                content = re.sub(
                    r'(<meta name="viewport"[^>]*>)',
                    f'\\1\n{theme_meta}',
                    content
                )
                
                with open(base_html, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("   ✅ Meta tags del tema añadidos")
            else:
                print("   ✅ Meta tags ya presentes")
                
        except Exception as e:
            print(f"   ❌ Error inyectando meta tags: {e}")
    
    def create_css_custom_properties_file(self):
        """Crea archivo con propiedades CSS personalizadas adicionales"""
        print("🎯 Creando propiedades CSS personalizadas adicionales...")
        
        css_content = ''':root {
    /* Warm Autumn Glow - Extended Properties */
    
    /* Component-specific colors */
    --navbar-bg: linear-gradient(135deg, var(--prussian-blue), var(--prussian-blue-600));
    --sidebar-bg: linear-gradient(180deg, var(--prussian-blue-300), var(--prussian-blue));
    --content-bg: var(--vanilla-100);
    --card-bg: linear-gradient(135deg, var(--vanilla), var(--vanilla-200));
    --button-primary: linear-gradient(135deg, var(--prussian-blue), var(--prussian-blue-600));
    --button-secondary: linear-gradient(135deg, var(--orange-wheel), var(--orange-wheel-600));
    --button-success: linear-gradient(135deg, var(--xanthous-600), var(--xanthous));
    --button-danger: linear-gradient(135deg, var(--fire-engine-red), var(--fire-engine-red-600));
    
    /* Interactive states */
    --hover-transform: translateY(-2px) scale(1.02);
    --hover-shadow: 0 8px 25px rgba(0, 48, 73, 0.2);
    --focus-outline: 0 0 0 3px rgba(247, 127, 0, 0.2);
    
    /* Animations */
    --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    --transition-bounce: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    
    /* Spacing using theme multipliers */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 2rem;
    --spacing-2xl: 3rem;
    
    /* Border radius */
    --radius-sm: 0.25rem;
    --radius-md: 0.375rem;
    --radius-lg: 0.5rem;
    --radius-xl: 0.75rem;
    --radius-full: 9999px;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 48, 73, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 48, 73, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 48, 73, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 48, 73, 0.1);
    
    /* Typography */
    --font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-size-xs: 0.75rem;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.25rem;
    --font-size-2xl: 1.5rem;
    --font-size-3xl: 1.875rem;
    
    /* Z-index layers */
    --z-dropdown: 1000;
    --z-sticky: 1020;
    --z-fixed: 1030;
    --z-modal-backdrop: 1040;
    --z-modal: 1050;
    --z-popover: 1060;
    --z-tooltip: 1070;
}

/* Global classes using custom properties */
.warm-gradient-primary {
    background: var(--button-primary);
}

.warm-gradient-secondary {
    background: var(--button-secondary);
}

.warm-hover-effect:hover {
    transform: var(--hover-transform);
    box-shadow: var(--hover-shadow);
}

.warm-transition {
    transition: var(--transition-smooth);
}

.warm-transition-bounce {
    transition: var(--transition-bounce);
}

.warm-focus:focus {
    outline: none;
    box-shadow: var(--focus-outline);
}

.warm-card {
    background: var(--card-bg);
    border: 1px solid var(--prussian-blue-200);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
}

.warm-button {
    background: var(--button-primary);
    color: var(--vanilla);
    border: 2px solid var(--prussian-blue-400);
    border-radius: var(--radius-md);
    padding: var(--spacing-sm) var(--spacing-md);
    font-family: var(--font-family);
    font-weight: 600;
    transition: var(--transition-smooth);
    cursor: pointer;
}

.warm-button:hover {
    background: var(--button-secondary);
    transform: var(--hover-transform);
    box-shadow: var(--hover-shadow);
}

/* Utility classes */
.text-warm-primary { color: var(--prussian-blue) !important; }
.text-warm-secondary { color: var(--orange-wheel) !important; }
.text-warm-accent { color: var(--xanthous) !important; }
.text-warm-danger { color: var(--fire-engine-red) !important; }
.text-warm-light { color: var(--vanilla) !important; }

.bg-warm-primary { background-color: var(--prussian-blue) !important; }
.bg-warm-secondary { background-color: var(--orange-wheel) !important; }
.bg-warm-accent { background-color: var(--xanthous) !important; }
.bg-warm-danger { background-color: var(--fire-engine-red) !important; }
.bg-warm-light { background-color: var(--vanilla) !important; }

.border-warm-primary { border-color: var(--prussian-blue) !important; }
.border-warm-secondary { border-color: var(--orange-wheel) !important; }
.border-warm-accent { border-color: var(--xanthous) !important; }
.border-warm-danger { border-color: var(--fire-engine-red) !important; }
.border-warm-light { border-color: var(--vanilla) !important; }'''
        
        custom_props_file = self.static_dir / "css" / "warm-autumn-custom-properties.css"
        
        try:
            with open(custom_props_file, 'w', encoding='utf-8') as f:
                f.write(css_content)
            print("   ✅ Propiedades personalizadas creadas")
        except Exception as e:
            print(f"   ❌ Error creando propiedades: {e}")
    
    def run_full_application(self):
        """Ejecuta la aplicación completa del tema"""
        print("🚀 INICIANDO APLICACIÓN UNIVERSAL DEL TEMA WARM AUTUMN GLOW")
        print("=" * 60)
        
        # 1. Aplicar variables a CSS existentes
        self.apply_color_variables_to_css()
        print()
        
        # 2. Aplicar clases del tema a templates
        self.apply_theme_classes_to_templates()
        print()
        
        # 3. Inyectar meta tags
        self.inject_theme_meta_tags()
        print()
        
        # 4. Crear propiedades personalizadas
        self.create_css_custom_properties_file()
        print()
        
        print("🎉 APLICACIÓN DEL TEMA COMPLETADA EXITOSAMENTE!")
        print("=" * 60)
        print("📋 Próximos pasos:")
        print("   1. Reinicia la aplicación Flask")
        print("   2. Verifica que todos los archivos CSS del tema estén enlazados")
        print("   3. Revisa visualmente la aplicación del tema")
        print("   4. Reporta cualquier elemento que no tenga los colores correctos")
        print()
        print("🎨 Paleta de colores aplicada:")
        print("   • Prussian Blue: #003049 (Elementos principales)")
        print("   • Fire Engine Red: #d62828 (Alertas y peligro)")
        print("   • Orange Wheel: #f77f00 (Elementos secundarios)")
        print("   • Xanthous: #fcbf49 (Destacados y éxito)")
        print("   • Vanilla: #eae2b7 (Fondos y contenido)")

if __name__ == "__main__":
    applicator = WarmAutumnThemeApplicator()
    applicator.run_full_application()