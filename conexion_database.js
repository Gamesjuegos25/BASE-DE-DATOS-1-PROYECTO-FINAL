// =================================================================
// CONEXIÓN CON BASE DE DATOS - REEMPLAZO DE DATOS ESTÁTICOS
// =================================================================
// Este archivo muestra cómo modificar el sistema para conectarse
// con una base de datos real en lugar de usar datos estáticos
// =================================================================

// Configuración de la API/Backend
const API_CONFIG = {
    baseURL: 'http://localhost:3000/api', // Cambiar por tu servidor
    endpoints: {
        // Dashboard
        estadisticas: '/dashboard/estadisticas',
        obrasRecientes: '/dashboard/obras-recientes',
        
        // Módulos principales
        obras: '/obras',
        empleados: '/empleados',
        materiales: '/materiales',
        proveedores: '/proveedores',
        inventario: '/inventario',
        proyectos: '/proyectos',
        vehiculos: '/vehiculos',
        equipos: '/equipos',
        
        // Reportes
        reportesSemanales: '/reportes/semanales',
        reportesGastos: '/reportes/gastos',
        reportesMateriales: '/reportes/materiales',
        reportesPagos: '/reportes/pagos',
        
        // Filtros y catálogos
        bodegas: '/catalogos/bodegas',
        obrasCatalogo: '/catalogos/obras',
        
        // Detalles específicos
        detalleObra: '/obras/{id}',
        detalleEmpleado: '/empleados/{id}',
        detalleMaterial: '/materiales/{id}',
        detalleProveedor: '/proveedores/{id}'
    }
};

// =================================================================
// FUNCIONES DE CONEXIÓN CON LA API
// =================================================================

// Función genérica para hacer peticiones HTTP
async function apiRequest(endpoint, options = {}) {
    try {
        const url = `${API_CONFIG.baseURL}${endpoint}`;
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                // Agregar token de autenticación si es necesario
                // 'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        };
        
        const response = await fetch(url, { ...defaultOptions, ...options });
        
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error en petición API:', error);
        mostrarError(`Error al conectar con el servidor: ${error.message}`);
        return null;
    }
}

// =================================================================
// FUNCIONES MODIFICADAS PARA USAR BASE DE DATOS
// =================================================================

// Reemplazar la función cargarDashboard()
async function cargarDashboardDB() {
    try {
        // Obtener estadísticas desde la API
        const estadisticas = await apiRequest(API_CONFIG.endpoints.estadisticas);
        
        if (estadisticas) {
            document.getElementById('totalObras').textContent = estadisticas.obras_activas;
            document.getElementById('totalEmpleados').textContent = estadisticas.empleados_activos;
            document.getElementById('totalMateriales').textContent = estadisticas.total_materiales;
            document.getElementById('totalProveedores').textContent = estadisticas.total_proveedores;
        }

        // Cargar obras recientes
        const obrasRecientes = await apiRequest(API_CONFIG.endpoints.obrasRecientes);
        
        if (obrasRecientes && obrasRecientes.length > 0) {
            const contenedorObras = document.getElementById('obrasRecientes');
            contenedorObras.innerHTML = obrasRecientes.map(obra => `
                <div class="recent-item">
                    <h4>${obra.nombre}</h4>
                    <p>${obra.ubicacion} - ${obtenerEstadoConClase(obra.estado)}</p>
                </div>
            `).join('');
        }

    } catch (error) {
        console.error('Error cargando dashboard:', error);
        // Fallback a datos estáticos si falla la conexión
        cargarDashboard();
    }
}

// Reemplazar la función cargarObras()
async function cargarObrasDB() {
    try {
        mostrarCargando('tablaObras');
        
        const obras = await apiRequest(API_CONFIG.endpoints.obras);
        
        if (obras && obras.length > 0) {
            const tbody = document.querySelector('#tablaObras tbody');
            tbody.innerHTML = obras.map(obra => `
                <tr>
                    <td>${obra.id_obra}</td>
                    <td><strong>${obra.nombre}</strong></td>
                    <td>${obra.ubicacion}</td>
                    <td>${obra.tipo}</td>
                    <td>${obtenerEstadoConClase(obra.estado)}</td>
                    <td>${obra.cliente_nombre || 'N/A'}</td>
                    <td>${obra.presupuesto ? formatearMoneda(obra.presupuesto) : 'N/A'}</td>
                    <td>
                        <div class="progress-info">
                            <small>Físico: ${obra.porcentaje_fisico || 0}%</small><br>
                            <small>Financiero: ${obra.porcentaje_financiero || 0}%</small>
                        </div>
                    </td>
                    <td>
                        <button class="action-btn btn-view" onclick="verDetalleObraDB(${obra.id_obra})">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="action-btn btn-edit" onclick="editarObra(${obra.id_obra})">
                            <i class="fas fa-edit"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        }
        
        ocultarCargando('tablaObras');
        
    } catch (error) {
        console.error('Error cargando obras:', error);
        ocultarCargando('tablaObras');
        // Fallback a datos estáticos si falla la conexión
        cargarObras();
    }
}

// Reemplazar la función cargarEmpleados()
async function cargarEmpleadosDB() {
    try {
        mostrarCargando('tablaEmpleados');
        
        const empleados = await apiRequest(API_CONFIG.endpoints.empleados);
        
        if (empleados && empleados.length > 0) {
            const tbody = document.querySelector('#tablaEmpleados tbody');
            tbody.innerHTML = empleados.map(empleado => `
                <tr>
                    <td>${empleado.id_empleado}</td>
                    <td><strong>${empleado.nombre}</strong></td>
                    <td>${empleado.tipo}</td>
                    <td>${empleado.salario_fijo > 0 ? formatearMoneda(empleado.salario_fijo) : 'Por trabajo'}</td>
                    <td>${obtenerEstadoConClase(empleado.estado)}</td>
                    <td>${empleado.proyectos_asignados || 0}</td>
                    <td>${empleado.ultimo_pago ? formatearFecha(empleado.ultimo_pago) : 'N/A'}</td>
                    <td>
                        <button class="action-btn btn-view" onclick="verDetalleEmpleadoDB(${empleado.id_empleado})">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="action-btn btn-edit" onclick="editarEmpleado(${empleado.id_empleado})">
                            <i class="fas fa-edit"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        }
        
        ocultarCargando('tablaEmpleados');
        
    } catch (error) {
        console.error('Error cargando empleados:', error);
        ocultarCargando('tablaEmpleados');
        // Fallback a datos estáticos si falla la conexión
        cargarEmpleados();
    }
}

// Reemplazar la función cargarMateriales()
async function cargarMaterialesDB() {
    try {
        mostrarCargando('tablaMateriales');
        
        const materiales = await apiRequest(API_CONFIG.endpoints.materiales);
        
        if (materiales && materiales.length > 0) {
            const tbody = document.querySelector('#tablaMateriales tbody');
            tbody.innerHTML = materiales.map(material => `
                <tr>
                    <td>${material.id_material}</td>
                    <td><strong>${material.nombre}</strong></td>
                    <td>${material.unidad}</td>
                    <td>${formatearMoneda(material.precio_unitario)}</td>
                    <td>${material.tipo_material}</td>
                    <td>${obtenerEstadoConClase(material.estado)}</td>
                    <td>${material.proveedor_nombre || 'N/A'}</td>
                    <td>${material.stock_total || 0} ${material.unidad}</td>
                    <td>
                        <button class="action-btn btn-view" onclick="verDetalleMaterialDB(${material.id_material})">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="action-btn btn-edit" onclick="editarMaterial(${material.id_material})">
                            <i class="fas fa-edit"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        }
        
        ocultarCargando('tablaMateriales');
        
    } catch (error) {
        console.error('Error cargando materiales:', error);
        ocultarCargando('tablaMateriales');
        // Fallback a datos estáticos si falla la conexión
        cargarMateriales();
    }
}

// =================================================================
// FUNCIONES PARA DETALLES ESPECÍFICOS CON BASE DE DATOS
// =================================================================

async function verDetalleObraDB(id) {
    try {
        const obra = await apiRequest(API_CONFIG.endpoints.detalleObra.replace('{id}', id));
        
        if (obra) {
            const contenido = `
                <div class="detail-grid">
                    <div class="detail-item">
                        <strong>ID:</strong> ${obra.id_obra}
                    </div>
                    <div class="detail-item">
                        <strong>Nombre:</strong> ${obra.nombre}
                    </div>
                    <div class="detail-item">
                        <strong>Ubicación:</strong> ${obra.ubicacion}
                    </div>
                    <div class="detail-item">
                        <strong>Tipo:</strong> ${obra.tipo}
                    </div>
                    <div class="detail-item">
                        <strong>Estado:</strong> ${obtenerEstadoConClase(obra.estado)}
                    </div>
                    <div class="detail-item">
                        <strong>Cliente:</strong> ${obra.cliente_nombre || 'N/A'}
                    </div>
                    <div class="detail-item">
                        <strong>Contacto Cliente:</strong> ${obra.cliente_contacto || 'N/A'}
                    </div>
                    <div class="detail-item">
                        <strong>Presupuesto:</strong> ${obra.monto_estimado ? formatearMoneda(obra.monto_estimado) : 'N/A'}
                    </div>
                    <div class="detail-item">
                        <strong>Avance Físico:</strong> ${obra.porcentaje_fisico || 0}%
                    </div>
                    <div class="detail-item">
                        <strong>Avance Financiero:</strong> ${obra.porcentaje_financiero || 0}%
                    </div>
                </div>
            `;
            
            mostrarModal('Detalles de la Obra', contenido);
        }
        
    } catch (error) {
        console.error('Error obteniendo detalle de obra:', error);
        mostrarError('No se pudo cargar el detalle de la obra');
    }
}

async function verDetalleEmpleadoDB(id) {
    try {
        const empleado = await apiRequest(API_CONFIG.endpoints.detalleEmpleado.replace('{id}', id));
        
        if (empleado) {
            const contenido = `
                <div class="detail-grid">
                    <div class="detail-item">
                        <strong>ID:</strong> ${empleado.id_empleado}
                    </div>
                    <div class="detail-item">
                        <strong>Nombre:</strong> ${empleado.nombre}
                    </div>
                    <div class="detail-item">
                        <strong>Tipo:</strong> ${empleado.tipo}
                    </div>
                    <div class="detail-item">
                        <strong>Salario:</strong> ${empleado.salario_fijo > 0 ? formatearMoneda(empleado.salario_fijo) : 'Por trabajo realizado'}
                    </div>
                    <div class="detail-item">
                        <strong>Estado:</strong> ${obtenerEstadoConClase(empleado.estado)}
                    </div>
                    <div class="detail-item">
                        <strong>Proyectos Asignados:</strong> ${empleado.proyectos_asignados || 0}
                    </div>
                    <div class="detail-item">
                        <strong>Último Pago:</strong> ${empleado.ultimo_pago ? formatearFecha(empleado.ultimo_pago) : 'N/A'}
                    </div>
                    <div class="detail-item">
                        <strong>Último Monto:</strong> ${empleado.ultimo_monto ? formatearMoneda(empleado.ultimo_monto) : 'N/A'}
                    </div>
                </div>
            `;
            
            mostrarModal('Detalles del Empleado', contenido);
        }
        
    } catch (error) {
        console.error('Error obteniendo detalle de empleado:', error);
        mostrarError('No se pudo cargar el detalle del empleado');
    }
}

// =================================================================
// FUNCIONES PARA REPORTES CON BASE DE DATOS
// =================================================================

async function cargarReportesSemanalDB() {
    try {
        const reportes = await apiRequest(API_CONFIG.endpoints.reportesSemanales);
        
        if (reportes && reportes.length > 0) {
            const thead = document.getElementById('reportesHeader');
            const tbody = document.querySelector('#tablaReportes tbody');
            
            thead.innerHTML = `
                <tr>
                    <th>Semana</th>
                    <th>Obra</th>
                    <th>Fecha</th>
                    <th>Resumen</th>
                    <th>Acciones</th>
                </tr>
            `;
            
            tbody.innerHTML = reportes.map(reporte => `
                <tr>
                    <td>Semana ${reporte.semana}</td>
                    <td>${reporte.obra_nombre || 'N/A'}</td>
                    <td>${formatearFecha(reporte.fecha)}</td>
                    <td>${reporte.resumen}</td>
                    <td>
                        <button class="action-btn btn-view" onclick="verDetalleReporte(${reporte.id_reporte})">
                            <i class="fas fa-eye"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        }
        
    } catch (error) {
        console.error('Error cargando reportes semanales:', error);
        // Fallback a función original
        cargarReportesSemanal();
    }
}

async function cargarReportesGastosDB() {
    try {
        const gastos = await apiRequest(API_CONFIG.endpoints.reportesGastos);
        
        if (gastos && gastos.length > 0) {
            const thead = document.getElementById('reportesHeader');
            const tbody = document.querySelector('#tablaReportes tbody');
            
            thead.innerHTML = `
                <tr>
                    <th>Proveedor</th>
                    <th>Número Factura</th>
                    <th>Fecha</th>
                    <th>Monto</th>
                    <th>Estado</th>
                </tr>
            `;
            
            tbody.innerHTML = gastos.map(gasto => `
                <tr>
                    <td>${gasto.proveedor_nombre || 'N/A'}</td>
                    <td>${gasto.numero_factura}</td>
                    <td>${formatearFecha(gasto.fecha)}</td>
                    <td>${formatearMoneda(gasto.monto)}</td>
                    <td>${obtenerEstadoConClase(gasto.estado)}</td>
                </tr>
            `).join('');
        }
        
    } catch (error) {
        console.error('Error cargando reportes de gastos:', error);
        // Fallback a función original
        cargarReportesGastos();
    }
}

// =================================================================
// FUNCIONES AUXILIARES PARA LA CONEXIÓN
// =================================================================

function mostrarCargando(tablaId) {
    const tabla = document.getElementById(tablaId);
    if (tabla) {
        const tbody = tabla.querySelector('tbody');
        tbody.innerHTML = `
            <tr>
                <td colspan="100%" class="loading">
                    <div class="spinner"></div>
                    Cargando datos...
                </td>
            </tr>
        `;
    }
}

function ocultarCargando(tablaId) {
    // La tabla se llena con datos reales, así que no hay que hacer nada específico
}

function mostrarError(mensaje) {
    // Mostrar mensaje de error al usuario
    console.error(mensaje);
    
    // Podrías crear un elemento de notificación en la UI
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-notification';
    errorDiv.textContent = mensaje;
    errorDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #e74c3c;
        color: white;
        padding: 1rem;
        border-radius: 5px;
        z-index: 10000;
    `;
    
    document.body.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// =================================================================
// FUNCIÓN PRINCIPAL MODIFICADA
// =================================================================

function inicializarSistemaConDB() {
    configurarNavegacion();
    cargarDashboardDB(); // Usar la versión con base de datos
    configurarEventos();
    mostrarSeccion('dashboard');
}

// Función modificada para mostrar sección
function mostrarSeccionConDB(nombreSeccion) {
    const secciones = document.querySelectorAll('.content-section');
    
    secciones.forEach(seccion => {
        seccion.classList.remove('active');
    });
    
    const seccionActiva = document.getElementById(nombreSeccion);
    if (seccionActiva) {
        seccionActiva.classList.add('active');
    }

    // Cargar datos desde la base de datos según la sección
    switch(nombreSeccion) {
        case 'dashboard':
            cargarDashboardDB();
            break;
        case 'obras':
            cargarObrasDB();
            break;
        case 'empleados':
            cargarEmpleadosDB();
            break;
        case 'materiales':
            cargarMaterialesDB();
            break;
        case 'proveedores':
            cargarProveedoresDB();
            break;
        case 'inventario':
            cargarInventarioDB();
            break;
        case 'proyectos':
            cargarProyectosDB();
            break;
        case 'reportes':
            cargarReportesDB();
            break;
        case 'vehiculos':
            cargarVehiculosDB();
            break;
        case 'equipos':
            cargarEquiposDB();
            break;
    }
}

// =================================================================
// INSTRUCCIONES PARA IMPLEMENTAR
// =================================================================

/*
PASOS PARA CONECTAR CON BASE DE DATOS REAL:

1. BACKEND/API:
   - Crear un servidor backend (Node.js, PHP, ASP.NET, etc.)
   - Implementar los endpoints definidos en API_CONFIG
   - Conectar el backend con la base de datos SQL Server
   - Usar las consultas del archivo "consultas_extraer_datos.sql"

2. MODIFICAR EL FRONTEND:
   - Reemplazar las funciones existentes por las versiones "DB"
   - Cambiar la URL base en API_CONFIG.baseURL
   - Agregar manejo de errores y loading states

3. SEGURIDAD:
   - Implementar autenticación (JWT, OAuth, etc.)
   - Validar permisos de usuario por módulo
   - Sanitizar datos de entrada
   - Usar HTTPS en producción

4. EJEMPLO DE ENDPOINT EN BACKEND (Node.js + Express):

   app.get('/api/obras', async (req, res) => {
       try {
           const result = await sql.query(`
               SELECT 
                   o.id_obra,
                   o.nombre,
                   o.ubicacion,
                   o.tipo,
                   o.estado,
                   c.nombre AS cliente_nombre,
                   p.monto_estimado AS presupuesto,
                   a.porcentaje_fisico,
                   a.porcentaje_financiero
               FROM Obra o
               LEFT JOIN Cliente c ON o.id_cliente = c.id_cliente
               LEFT JOIN PresupuestoObra p ON o.id_obra = p.id_obra
               LEFT JOIN AvanceObra a ON o.id_obra = a.id_obra
               ORDER BY o.id_obra
           `);
           
           res.json(result.recordset);
       } catch (error) {
           console.error(error);
           res.status(500).json({ error: 'Error interno del servidor' });
       }
   });

5. PARA ACTIVAR LA CONEXIÓN CON DB:
   - Cambiar en index.html:
     document.addEventListener('DOMContentLoaded', inicializarSistemaConDB);
   - Reemplazar las funciones mostrarSeccion por mostrarSeccionConDB
*/