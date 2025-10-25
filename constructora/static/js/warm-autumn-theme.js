
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
