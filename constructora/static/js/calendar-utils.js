/**
 * Utilidades de Calendario Estandarizadas para Sistema Constructora
 * 
 * Este archivo proporciona funciones estandarizadas para:
 * - Configuración de calendarios
 * - Validaciones de fechas
 * - Formato consistente de fechas
 * - Restricciones de fechas
 */

// Configuración global de calendarios
const CALENDAR_CONFIG = {
    dateFormat: 'YYYY-MM-DD',
    displayFormat: 'DD/MM/YYYY',
    minDate: '2020-01-01', // Fecha mínima permitida
    maxDate: '2030-12-31', // Fecha máxima permitida
    locale: 'es',
    weekStart: 1, // Lunes
    restrictPastDates: false, // Por defecto no restringir fechas pasadas
    restrictFutureDates: false // Por defecto no restringir fechas futuras
};

// Tipos de campos de fecha con sus configuraciones específicas
const DATE_FIELD_TYPES = {
    // Fechas de inicio de proyectos/obras
    fecha_inicio: {
        label: '📅 Fecha de Inicio',
        icon: 'fas fa-play-circle',
        restrictPastDates: false,
        placeholder: 'Seleccionar fecha de inicio',
        required: true
    },
    
    // Fechas de finalización/entrega
    fecha_fin: {
        label: '🏁 Fecha de Finalización',
        icon: 'fas fa-flag-checkered',
        restrictPastDates: false,
        placeholder: 'Seleccionar fecha de finalización',
        required: false,
        dependsOn: 'fecha_inicio' // Debe ser posterior a fecha_inicio
    },
    
    // Fechas de entrega/vencimiento
    fecha_entrega: {
        label: '📦 Fecha de Entrega',
        icon: 'fas fa-shipping-fast',
        restrictPastDates: true,
        placeholder: 'Seleccionar fecha de entrega',
        required: true
    },
    
    // Fechas de programación/planificación
    fecha_programada: {
        label: '⏰ Fecha Programada',
        icon: 'fas fa-calendar-alt',
        restrictPastDates: true,
        placeholder: 'Seleccionar fecha programada',
        required: false
    },
    
    // Fechas de vencimiento
    fecha_vencimiento: {
        label: '⚠️ Fecha de Vencimiento',
        icon: 'fas fa-exclamation-triangle',
        restrictPastDates: true,
        placeholder: 'Seleccionar fecha de vencimiento',
        required: true
    },
    
    // Fechas de emisión/creación
    fecha_emision: {
        label: '📋 Fecha de Emisión',
        icon: 'fas fa-calendar-plus',
        restrictPastDates: false,
        restrictFutureDates: true,
        placeholder: 'Fecha de emisión',
        defaultToday: true,
        required: true
    },
    
    // Fechas de pago
    fecha_pago: {
        label: '💰 Fecha de Pago',
        icon: 'fas fa-money-bill-wave',
        restrictPastDates: false,
        placeholder: 'Seleccionar fecha de pago',
        required: false
    },
    
    // Fechas de incidentes/eventos
    fecha_incidente: {
        label: '🚨 Fecha del Incidente',
        icon: 'fas fa-exclamation-circle',
        restrictPastDates: false,
        restrictFutureDates: true,
        placeholder: 'Fecha del incidente',
        required: true
    },
    
    // Fechas de mantenimiento
    fecha_mantenimiento: {
        label: '🔧 Fecha de Mantenimiento',
        icon: 'fas fa-tools',
        restrictPastDates: true,
        placeholder: 'Programar mantenimiento',
        required: false
    },
    
    // Fechas de presupuesto
    fecha_presupuesto: {
        label: '💼 Fecha del Presupuesto',
        icon: 'fas fa-calculator',
        restrictPastDates: false,
        restrictFutureDates: true,
        placeholder: 'Fecha del presupuesto',
        defaultToday: true,
        required: true
    }
};

/**
 * Genera HTML estandarizado para un campo de fecha
 * @param {string} fieldName - Nombre del campo (debe estar en DATE_FIELD_TYPES)
 * @param {object} options - Opciones adicionales
 * @returns {string} HTML del campo de fecha
 */
function generateDateField(fieldName, options = {}) {
    const config = DATE_FIELD_TYPES[fieldName] || DATE_FIELD_TYPES.fecha_programada;
    const value = options.value || (config.defaultToday ? getTodayDate() : '');
    const disabled = options.disabled || false;
    const additionalClasses = options.classes || '';
    
    const minDate = config.restrictPastDates ? getTodayDate() : CALENDAR_CONFIG.minDate;
    const maxDate = config.restrictFutureDates ? getTodayDate() : CALENDAR_CONFIG.maxDate;
    
    return `
        <div class="form-group calendar-field-group">
            <label for="${fieldName}" class="form-label">
                <i class="${config.icon} text-xanthous-600"></i> ${config.label}
                ${config.required ? '<span class="required-mark text-red-500 ml-1">*</span>' : ''}
            </label>
            <div class="input-wrapper date-input-wrapper">
                <input 
                    type="date" 
                    class="form-input date-picker-input standardized-calendar ${additionalClasses}" 
                    name="${fieldName}" 
                    id="${fieldName}"
                    value="${value}"
                    placeholder="${config.placeholder}"
                    min="${minDate}"
                    max="${maxDate}"
                    ${config.required ? 'required' : ''}
                    ${disabled ? 'disabled' : ''}
                    data-field-type="${fieldName}"
                    data-depends-on="${config.dependsOn || ''}"
                />
                <i class="fas fa-calendar-alt input-icon"></i>
            </div>
            <small class="form-help text-vanilla-600">
                ${getFieldHelpText(fieldName, config)}
            </small>
        </div>
    `;
}

/**
 * Obtiene la fecha actual en formato YYYY-MM-DD
 */
function getTodayDate() {
    return new Date().toISOString().split('T')[0];
}

/**
 * Genera texto de ayuda para el campo de fecha
 */
function getFieldHelpText(fieldName, config) {
    let helpText = config.placeholder;
    
    if (config.restrictPastDates && config.restrictFutureDates) {
        helpText += ' (solo fecha actual)';
    } else if (config.restrictPastDates) {
        helpText += ' (no fechas pasadas)';
    } else if (config.restrictFutureDates) {
        helpText += ' (no fechas futuras)';
    }
    
    if (config.dependsOn) {
        helpText += ` (debe ser posterior a ${config.dependsOn})`;
    }
    
    return helpText;
}

/**
 * Inicializa validaciones para campos de fecha dependientes
 */
function initializeDateValidations() {
    document.addEventListener('DOMContentLoaded', function() {
        // Validación de fechas dependientes
        const dateInputs = document.querySelectorAll('.standardized-calendar[data-depends-on]');
        
        dateInputs.forEach(input => {
            const dependsOn = input.getAttribute('data-depends-on');
            if (dependsOn) {
                const dependentField = document.getElementById(dependsOn);
                
                if (dependentField) {
                    // Validar cuando cambie el campo dependiente
                    dependentField.addEventListener('change', function() {
                        validateDependentDate(input, dependentField);
                    });
                    
                    // Validar cuando cambie el campo actual
                    input.addEventListener('change', function() {
                        validateDependentDate(input, dependentField);
                    });
                }
            }
        });
        
        // Aplicar configuraciones específicas
        document.querySelectorAll('.standardized-calendar').forEach(input => {
            const fieldType = input.getAttribute('data-field-type');
            const config = DATE_FIELD_TYPES[fieldType];
            
            if (config && config.defaultToday && !input.value) {
                input.value = getTodayDate();
            }
        });
    });
}

/**
 * Valida que una fecha sea posterior a otra
 */
function validateDependentDate(targetInput, dependentInput) {
    const targetDate = new Date(targetInput.value);
    const dependentDate = new Date(dependentInput.value);
    
    if (targetInput.value && dependentInput.value && targetDate <= dependentDate) {
        targetInput.setCustomValidity(`La fecha debe ser posterior a ${dependentInput.getAttribute('data-field-type')}`);
        targetInput.classList.add('error');
    } else {
        targetInput.setCustomValidity('');
        targetInput.classList.remove('error');
    }
}

/**
 * Formatea una fecha para mostrar
 */
function formatDateForDisplay(dateString) {
    if (!dateString) return 'Sin fecha';
    
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

/**
 * Calcula la diferencia en días entre dos fechas
 */
function calculateDaysDifference(startDate, endDate) {
    if (!startDate || !endDate) return null;
    
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffTime = Math.abs(end - start);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    return diffDays;
}

// Inicializar automáticamente cuando se cargue el script
initializeDateValidations();

// Exportar funciones para uso global
window.CalendarUtils = {
    generateDateField,
    formatDateForDisplay,
    calculateDaysDifference,
    getTodayDate,
    validateDependentDate,
    DATE_FIELD_TYPES,
    CALENDAR_CONFIG
};