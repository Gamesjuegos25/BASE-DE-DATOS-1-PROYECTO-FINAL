/**
 * Dynamic Color Applicator - Warm Autumn Theme
 * Aplica dinámicamente los colores del tema a todos los elementos
 */

(function() {
    'use strict';
    
    // Paleta de colores Warm Autumn Glow
    const colors = {
        prussianBlue: '#003049',
        fireEngineRed: '#d62828',
        orangeWheel: '#f77f00',
        xanthous: '#fcbf49',
        vanilla: '#eae2b7'
    };
    
    // Variaciones de colores
    const colorVariations = {
        prussianBlue: {
            100: '#00090e', 200: '#00131d', 300: '#001c2b', 400: '#002539',
            500: '#003049', 600: '#00679f', 700: '#00a0f7', 800: '#50c2ff', 900: '#a7e0ff'
        },
        fireEngineRed: {
            100: '#2b0808', 200: '#561010', 300: '#811818', 400: '#ac2020',
            500: '#d62828', 600: '#df5353', 700: '#e77e7e', 800: '#efa9a9', 900: '#f7d4d4'
        },
        orangeWheel: {
            100: '#311900', 200: '#623300', 300: '#934c00', 400: '#c46500',
            500: '#f77f00', 600: '#ff982b', 700: '#ffb260', 800: '#ffcc95', 900: '#ffe5ca'
        },
        xanthous: {
            100: '#402b01', 200: '#815602', 300: '#c18203', 400: '#fd9d04',
            500: '#fcbf49', 600: '#fdcc6a', 700: '#fdd98b', 800: '#fee5ac', 900: '#fef2cd'
        },
        vanilla: {
            100: '#2e2a1f', 200: '#5c543e', 300: '#8a7f5d', 400: '#b8a97c',
            500: '#eae2b7', 600: '#eee8c5', 700: '#f2eed3', 800: '#f6f3e1', 900: '#faf9ef'
        }
    };
    
    // Función para aplicar colores dinámicamente
    function applyWarmAutumnColors() {
        // Aplicar colores a elementos específicos
        const elementsToStyle = [
            // Botones
            { selector: 'button, .btn, input[type="submit"], input[type="button"]', 
              styles: {
                  backgroundColor: colors.prussianBlue,
                  color: colors.vanilla,
                  border: `2px solid ${colorVariations.prussianBlue[400]}`
              }
            },
            
            // Enlaces
            { selector: 'a', 
              styles: {
                  color: colorVariations.prussianBlue[600]
              }
            },
            
            // Tarjetas
            { selector: '.card, .content-card, .info-card', 
              styles: {
                  backgroundColor: colors.vanilla,
                  borderColor: colorVariations.prussianBlue[200],
                  boxShadow: '0 4px 15px rgba(0, 48, 73, 0.1)'
              }
            },
            
            // Formularios
            { selector: 'input, textarea, select', 
              styles: {
                  backgroundColor: colorVariations.vanilla[100],
                  borderColor: colorVariations.prussianBlue[200],
                  color: colorVariations.prussianBlue[700]
              }
            },
            
            // Tablas
            { selector: 'table th, .table th', 
              styles: {
                  backgroundColor: colorVariations.prussianBlue[400],
                  color: colors.vanilla,
                  borderBottomColor: colors.orangeWheel
              }
            }
        ];
        
        // Aplicar estilos
        elementsToStyle.forEach(({ selector, styles }) => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                Object.assign(element.style, styles);
            });
        });
        
        // Aplicar efectos hover dinámicamente
        applyHoverEffects();
        
        // Aplicar gradientes a elementos específicos
        applyGradients();
        
        // Actualizar iconos con colores del tema
        updateIcons();
    }
    
    // Función para aplicar efectos hover
    function applyHoverEffects() {
        const buttons = document.querySelectorAll('button, .btn, input[type="submit"], input[type="button"]');
        
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.background = `linear-gradient(135deg, ${colors.orangeWheel}, ${colorVariations.orangeWheel[600]})`;
                this.style.transform = 'translateY(-2px)';
                this.style.boxShadow = '0 8px 25px rgba(247, 127, 0, 0.3)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.background = `linear-gradient(135deg, ${colors.prussianBlue}, ${colorVariations.prussianBlue[600]})`;
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = 'none';
            });
        });
        
        // Efectos hover para tarjetas
        const cards = document.querySelectorAll('.card, .content-card, .info-card, .module-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px) scale(1.02)';
                this.style.boxShadow = '0 8px 25px rgba(0, 48, 73, 0.2)';
                this.style.borderColor = colors.orangeWheel;
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
                this.style.boxShadow = '0 4px 15px rgba(0, 48, 73, 0.1)';
                this.style.borderColor = colorVariations.prussianBlue[200];
            });
        });
    }
    
    // Función para aplicar gradientes
    function applyGradients() {
        // Header
        const headers = document.querySelectorAll('.header, header');
        headers.forEach(header => {
            header.style.background = `linear-gradient(135deg, ${colors.prussianBlue}, ${colorVariations.prussianBlue[600]})`;
        });
        
        // Sidebar
        const sidebars = document.querySelectorAll('.sidebar');
        sidebars.forEach(sidebar => {
            sidebar.style.background = `linear-gradient(180deg, ${colorVariations.prussianBlue[300]}, ${colors.prussianBlue})`;
        });
        
        // Card headers
        const cardHeaders = document.querySelectorAll('.card-header');
        cardHeaders.forEach(header => {
            header.style.background = `linear-gradient(90deg, ${colorVariations.prussianBlue[100]}, ${colorVariations.prussianBlue[200]})`;
            header.style.color = colors.vanilla;
            header.style.borderBottom = `2px solid ${colorVariations.orangeWheel[300]}`;
        });
    }
    
    // Función para actualizar iconos
    function updateIcons() {
        // Iconos en navegación
        const navIcons = document.querySelectorAll('.nav-icon');
        navIcons.forEach(icon => {
            icon.style.transition = 'all 0.3s ease';
        });
        
        // Iconos específicos con colores
        const coloredIcons = {
            '.text-prussian-blue, .fas.fa-building': colors.prussianBlue,
            '.text-orange-wheel, .fas.fa-users, .fas.fa-hammer': colors.orangeWheel,
            '.text-xanthous, .fas.fa-chart-line, .fas.fa-chart-bar, .fas.fa-tools': colors.xanthous,
            '.text-fire-engine-red, .fas.fa-exclamation-triangle': colors.fireEngineRed,
            '.text-vanilla': colors.vanilla
        };
        
        Object.entries(coloredIcons).forEach(([selector, color]) => {
            const icons = document.querySelectorAll(selector);
            icons.forEach(icon => {
                icon.style.color = color;
            });
        });
    }
    
    // Función para forzar la actualización de elementos dinámicos
    function forceColorUpdate() {
        // Buscar elementos con estilos en línea que puedan estar interfiriendo
        const allElements = document.querySelectorAll('*');
        
        allElements.forEach(element => {
            const computedStyle = window.getComputedStyle(element);
            
            // Si el elemento tiene un color de fondo que no es del tema, actualizarlo
            if (element.style.backgroundColor && 
                !element.style.backgroundColor.includes('var(--') &&
                element.style.backgroundColor !== 'transparent' &&
                element.style.backgroundColor !== 'inherit') {
                
                // Determinar el tipo de elemento y aplicar color apropiado
                if (element.matches('button, .btn, input[type="submit"], input[type="button"]')) {
                    element.style.backgroundColor = colors.prussianBlue;
                } else if (element.matches('.card, .content-card, .info-card')) {
                    element.style.backgroundColor = colors.vanilla;
                } else if (element.matches('.alert')) {
                    element.style.backgroundColor = colorVariations.vanilla[100];
                }
            }
        });
    }
    
    // Observador de mutaciones para elementos dinámicos
    function setupMutationObserver() {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length) {
                    // Aplicar colores a nuevos elementos
                    setTimeout(() => {
                        applyWarmAutumnColors();
                    }, 100);
                }
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
    
    // Función principal de inicialización
    function initWarmAutumnTheme() {
        // Aplicar colores inmediatamente
        applyWarmAutumnColors();
        
        // Forzar actualización después de que todos los estilos se carguen
        setTimeout(() => {
            forceColorUpdate();
        }, 500);
        
        // Configurar observador para elementos dinámicos
        setupMutationObserver();
        
        // Reaplizar colores cada vez que se redimensione la ventana
        window.addEventListener('resize', () => {
            setTimeout(applyWarmAutumnColors, 100);
        });
        
        // Aplicar colores cuando se haga foco en la ventana
        window.addEventListener('focus', applyWarmAutumnColors);
    }
    
    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWarmAutumnTheme);
    } else {
        initWarmAutumnTheme();
    }
    
    // Exponer función global para reaplaicar colores manualmente
    window.reapplyWarmAutumnColors = applyWarmAutumnColors;
    
})();