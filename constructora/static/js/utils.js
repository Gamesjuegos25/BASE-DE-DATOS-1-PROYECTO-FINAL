// utils.js - Funciones de utilidad para la aplicación Flask
/**
 * Funciones de utilidad para formateo y manejo de datos
 */

// Función para escapar HTML
function esc(str) {
    if (str == null || str === undefined) return '';
    return String(str).replace(/[&<>"']/g, function(match) {
        const escapeMap = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        };
        return escapeMap[match];
    });
}

// Función para formatear moneda en quetzales
function formatearMoneda(valor) {
    if (valor == null || valor === undefined || isNaN(valor)) {
        return 'Q. 0.00';
    }
    return 'Q. ' + Number(valor).toLocaleString('es-GT', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}

// Función para formatear fechas
function formatearFecha(fecha) {
    if (!fecha) return 'N/A';
    
    try {
        const d = new Date(fecha);
        if (isNaN(d.getTime())) return 'N/A';
        
        const dia = String(d.getDate()).padStart(2, '0');
        const mes = String(d.getMonth() + 1).padStart(2, '0');
        const anio = d.getFullYear();
        
        return `${dia}/${mes}/${anio}`;
    } catch (e) {
        return 'N/A';
    }
}

// Función para obtener badge de estado con clases CSS
function obtenerEstadoConClase(estado) {
    if (!estado) return '<span class="status-badge">N/A</span>';
    
    const estadoLower = estado.toLowerCase();
    let clase = 'status-badge';
    
    if (estadoLower.includes('activ') || estadoLower.includes('disponible')) {
        clase += ' status-activo';
    } else if (estadoLower.includes('proceso') || estadoLower.includes('progreso')) {
        clase += ' status-proceso';
    } else if (estadoLower.includes('completad') || estadoLower.includes('terminad')) {
        clase += ' status-completado';
    } else if (estadoLower.includes('suspendid') || estadoLower.includes('inactiv')) {
        clase += ' status-suspendido';
    }
    
    return `<span class="${clase}">${esc(estado)}</span>`;
}

// Función para mostrar notificaciones
function mostrarNotificacion(mensaje, tipo = 'info') {
    // Crear elemento de notificación
    const notif = document.createElement('div');
    notif.className = `notification notification--${tipo}`;
    notif.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${tipo === 'success' ? 'check-circle' : tipo === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${esc(mensaje)}</span>
        </div>
        <button class="notification-close">&times;</button>
    `;
    
    // Agregar estilos si no existen
    if (!document.getElementById('notification-styles')) {
        const styles = document.createElement('style');
        styles.id = 'notification-styles';
        styles.textContent = `
            .notification {
                position: fixed;
                top: 100px;
                right: 20px;
                z-index: 10000;
                padding: 1rem 1.5rem;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                max-width: 400px;
                animation: slideInRight 0.3s ease;
            }
            .notification--success { background: #d5f4e6; color: #27ae60; border-left: 4px solid #27ae60; }
            .notification--error { background: #fadbd8; color: #e74c3c; border-left: 4px solid #e74c3c; }
            .notification--info { background: #ebf3fd; color: #3498db; border-left: 4px solid #3498db; }
            .notification-content { display: flex; align-items: center; gap: 0.5rem; }
            .notification-close { 
                background: none; border: none; font-size: 1.2rem; cursor: pointer; 
                opacity: 0.7; transition: opacity 0.3s;
            }
            .notification-close:hover { opacity: 1; }
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(styles);
    }
    
    // Agregar al DOM
    document.body.appendChild(notif);
    
    // Manejar cierre
    const closeBtn = notif.querySelector('.notification-close');
    const cerrarNotificacion = () => {
        notif.style.animation = 'slideInRight 0.3s ease reverse';
        setTimeout(() => notif.remove(), 300);
    };
    
    closeBtn.addEventListener('click', cerrarNotificacion);
    
    // Auto-cierre después de 5 segundos
    setTimeout(cerrarNotificacion, 5000);
}

// Función para mostrar loader
function mostrarLoader(elemento, mostrar = true) {
    if (!elemento) return;
    
    if (mostrar) {
        elemento.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <span>Cargando datos...</span>
            </div>
        `;
    }
}

// Función para manejar errores de API
function manejarErrorAPI(error, contexto = 'operación') {
    console.error(`Error en ${contexto}:`, error);
    
    let mensaje = `Error en ${contexto}`;
    if (error.message) {
        mensaje += `: ${error.message}`;
    }
    
    mostrarNotificacion(mensaje, 'error');
}

// Función para confirmar acciones destructivas
function confirmarAccion(mensaje, callback) {
    if (confirm(mensaje)) {
        callback();
    }
}

// Función para filtrar tablas
function filtrarTabla(tablaId, filtroTexto, columnas = []) {
    const tabla = document.getElementById(tablaId);
    if (!tabla) return;
    
    const filas = tabla.querySelectorAll('tbody tr');
    const filtro = filtroTexto.toLowerCase();
    
    filas.forEach(fila => {
        const celdas = fila.querySelectorAll('td');
        let coincidir = false;
        
        if (columnas.length === 0) {
            // Buscar en todas las columnas
            coincidir = Array.from(celdas).some(celda => 
                celda.textContent.toLowerCase().includes(filtro)
            );
        } else {
            // Buscar solo en columnas especificadas
            coincidir = columnas.some(indice => {
                const celda = celdas[indice];
                return celda && celda.textContent.toLowerCase().includes(filtro);
            });
        }
        
        fila.style.display = coincidir ? '' : 'none';
    });
}

// Función para exportar tabla a CSV
function exportarTablaCSV(tablaId, nombreArchivo = 'datos') {
    const tabla = document.getElementById(tablaId);
    if (!tabla) return;
    
    let csv = [];
    
    // Encabezados
    const encabezados = tabla.querySelectorAll('thead th');
    const filaEncabezados = Array.from(encabezados).map(th => `"${th.textContent.trim()}"`);
    csv.push(filaEncabezados.join(','));
    
    // Datos
    const filas = tabla.querySelectorAll('tbody tr');
    filas.forEach(fila => {
        if (fila.style.display !== 'none') { // Solo filas visibles
            const celdas = fila.querySelectorAll('td');
            const filaDatos = Array.from(celdas).map(td => {
                let texto = td.textContent.trim();
                // Limpiar texto de acciones/botones
                if (td.querySelector('.action-btn')) {
                    texto = 'Acciones';
                }
                return `"${texto.replace(/"/g, '""')}"`;
            });
            csv.push(filaDatos.join(','));
        }
    });
    
    // Descargar
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    
    if (navigator.msSaveBlob) {
        navigator.msSaveBlob(blob, `${nombreArchivo}.csv`);
    } else {
        link.href = URL.createObjectURL(blob);
        link.download = `${nombreArchivo}.csv`;
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}

// Función para generar ID único
function generarId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Función para debounce (evitar múltiples llamadas rápidas)
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Exponer funciones globalmente para compatibilidad
if (typeof window !== 'undefined') {
    window.esc = esc;
    window.formatearMoneda = formatearMoneda;
    window.formatearFecha = formatearFecha;
    window.obtenerEstadoConClase = obtenerEstadoConClase;
    window.mostrarNotificacion = mostrarNotificacion;
    window.mostrarLoader = mostrarLoader;
    window.manejarErrorAPI = manejarErrorAPI;
    window.confirmarAccion = confirmarAccion;
    window.filtrarTabla = filtrarTabla;
    window.exportarTablaCSV = exportarTablaCSV;
    window.generarId = generarId;
    window.debounce = debounce;
}