// app.js - Aplicación principal Flask Python
/**
 * Sistema de Gestión de Constructora - Versión Python Flask
 * Maneja la interfaz de usuario y las llamadas a la API REST
 */

// Estado global de la aplicación
const AppState = {
    currentSection: 'dashboard',
    apiBaseUrl: '', // Usaremos rutas relativas para Flask
    isLoading: false,
    cache: new Map()
};

// Inicialización de la aplicación
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Iniciando Sistema de Constructora - Python Flask');
    
    await detectarBackend();
    configurarNavegacion();
    configurarEventos();
    configurarBusquedas();
    mostrarSeccion('dashboard');
});

// Verificar disponibilidad del backend Flask
async function detectarBackend() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.ok) {
            mostrarNotificacion('✅ Conectado al backend Flask', 'success');
            return true;
        } else {
            throw new Error('Backend no disponible');
        }
    } catch (error) {
        mostrarNotificacion('❌ Error conectando al backend Flask', 'error');
        return false;
    }
}

// Configurar navegación del sidebar
function configurarNavegacion() {
    const menuItems = document.querySelectorAll('.menu-item');
    const navToggle = document.getElementById('navToggle');
    const sidebar = document.getElementById('sidebar');

    // Manejar clicks en elementos del menú
    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remover clase active de todos los elementos
            menuItems.forEach(mi => mi.classList.remove('active'));
            
            // Agregar clase active al elemento clickeado
            item.classList.add('active');
            
            // Mostrar sección correspondiente
            const section = item.getAttribute('data-section');
            mostrarSeccion(section);
            
            // Cerrar sidebar en móvil
            if (window.innerWidth <= 1024) {
                sidebar.classList.remove('active');
            }
        });
    });

    // Toggle del menú móvil
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
    }

    // Cerrar sidebar al hacer click fuera en móvil
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 1024 && 
            !sidebar.contains(e.target) && 
            !navToggle.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    });
}

// Configurar eventos generales
function configurarEventos() {
    // Modal de detalles
    const modal = document.getElementById('detailModal');
    const closeModal = document.getElementById('closeModal');

    if (closeModal) {
        closeModal.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    // Cerrar modal al hacer click fuera
    if (modal) {
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    }

    // Configurar filtros de reportes
    const filterTipoReporte = document.getElementById('filterTipoReporte');
    if (filterTipoReporte) {
        filterTipoReporte.addEventListener('change', cargarReportes);
    }
}

// Configurar búsquedas en tiempo real
function configurarBusquedas() {
    const busquedas = [
        { input: 'searchObras', tabla: 'tablaObras', columnas: [1, 2, 3, 4] },
        { input: 'searchEmpleados', tabla: 'tablaEmpleados', columnas: [1, 2] },
        { input: 'searchMateriales', tabla: 'tablaMateriales', columnas: [1, 2, 6] },
        { input: 'searchProveedores', tabla: 'tablaProveedores', columnas: [1, 2] },
        { input: 'searchInventario', tabla: 'tablaInventario', columnas: [2] },
        { input: 'searchProyectos', tabla: 'tablaProyectos', columnas: [1, 2] },
        { input: 'searchVehiculos', tabla: 'tablaVehiculos', columnas: [1, 2, 3] },
        { input: 'searchEquipos', tabla: 'tablaEquipos', columnas: [1, 2, 4] }
    ];

    busquedas.forEach(({ input, tabla, columnas }) => {
        const inputElement = document.getElementById(input);
        if (inputElement) {
            const debouncedFilter = debounce((e) => {
                filtrarTabla(tabla, e.target.value, columnas);
            }, 300);
            
            inputElement.addEventListener('input', debouncedFilter);
        }
    });
}

// Cambiar de sección
function mostrarSeccion(nombreSeccion) {
    // Ocultar todas las secciones
    document.querySelectorAll('.content-section').forEach(section => {
        section.classList.remove('active');
    });

    // Mostrar sección solicitada
    const seccionElement = document.getElementById(nombreSeccion);
    if (seccionElement) {
        seccionElement.classList.add('active');
        AppState.currentSection = nombreSeccion;

        // Cargar datos según la sección
        switch (nombreSeccion) {
            case 'dashboard':
                cargarDashboard();
                break;
            case 'obras':
                cargarObras();
                break;
            case 'empleados':
                cargarEmpleados();
                break;
            case 'materiales':
                cargarMateriales();
                break;
            case 'proveedores':
                cargarProveedores();
                break;
            case 'inventario':
                cargarInventario();
                break;
            case 'proyectos':
                cargarProyectos();
                break;
            case 'reportes':
                cargarReportes();
                break;
            case 'vehiculos':
                cargarVehiculos();
                break;
            case 'equipos':
                cargarEquipos();
                break;
        }
    }
}

// ========================================
// FUNCIONES DE CARGA DE DATOS
// ========================================

// Cargar Dashboard
async function cargarDashboard() {
    try {
        // Cargar estadísticas generales
        const estadisticas = await fetchAPI('/api/dashboard/estadisticas');
        
        document.getElementById('totalObras').textContent = estadisticas.obras_activas || estadisticas.total_obras || 0;
        document.getElementById('totalEmpleados').textContent = estadisticas.empleados_activos || 0;
        document.getElementById('totalMateriales').textContent = estadisticas.total_materiales || 0;
        document.getElementById('totalProveedores').textContent = estadisticas.total_proveedores || 0;

        // Cargar obras recientes
        const obras = await fetchAPI('/api/obras?limit=3');
        const obrasHtml = obras.map(obra => `
            <div class="recent-item">
                <h4>${esc(obra.nombre)}</h4>
                <p>${esc(obra.ubicacion || 'N/A')} - ${obtenerEstadoConClase(obra.estado)}</p>
            </div>
        `).join('');
        
        document.getElementById('obrasRecientes').innerHTML = obrasHtml || '<p>No hay obras recientes</p>';

    } catch (error) {
        manejarErrorAPI(error, 'cargar dashboard');
    }
}

// Cargar Obras
async function cargarObras() {
    const tbody = document.querySelector('#tablaObras tbody');
    mostrarLoader(tbody);

    try {
        const obras = await fetchAPI('/api/obras');
        
        if (!obras.length) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center">No hay obras registradas</td></tr>';
            return;
        }

        const obrasHtml = obras.map(obra => `
            <tr>
                <td>${obra.id_obra}</td>
                <td><strong>${esc(obra.nombre)}</strong></td>
                <td>${esc(obra.ubicacion || 'N/A')}</td>
                <td>${esc(obra.tipo || 'N/A')}</td>
                <td>${obtenerEstadoConClase(obra.estado || 'N/A')}</td>
                <td>${obra.id_cliente || 'N/A'}</td>
                <td>${obra.monto_estimado != null ? formatearMoneda(obra.monto_estimado) : 'N/A'}</td>
                <td>
                    <div class="progress-info">
                        <small>Físico: ${obra.avance_fisico || 0}%</small><br>
                        <small>Financiero: ${obra.avance_financiero || 0}%</small>
                    </div>
                </td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleObra(${obra.id_obra})" title="Ver detalles">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = obrasHtml;

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="9" class="text-center">Error: ${esc(error.message)}</td></tr>`;
        manejarErrorAPI(error, 'cargar obras');
    }
}

// Cargar Empleados
async function cargarEmpleados() {
    const tbody = document.querySelector('#tablaEmpleados tbody');
    mostrarLoader(tbody);

    try {
        const empleados = await fetchAPI('/api/empleados');
        
        if (!empleados.length) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center">No hay empleados registrados</td></tr>';
            return;
        }

        const empleadosHtml = empleados.map(empleado => `
            <tr>
                <td>${empleado.id_empleado}</td>
                <td><strong>${esc(empleado.nombre)}</strong></td>
                <td>${esc(empleado.tipo || 'N/A')}</td>
                <td>${empleado.salario_fijo > 0 ? formatearMoneda(empleado.salario_fijo) : 'Por trabajo'}</td>
                <td>${obtenerEstadoConClase(empleado.estado || 'Activo')}</td>
                <td>${empleado.proyectos_asignados || 0}</td>
                <td>${formatearFecha(empleado.ultimo_pago)}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleEmpleado(${empleado.id_empleado})" title="Ver detalles">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = empleadosHtml;

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center">Error: ${esc(error.message)}</td></tr>`;
        manejarErrorAPI(error, 'cargar empleados');
    }
}

// Cargar Materiales
async function cargarMateriales() {
    const tbody = document.querySelector('#tablaMateriales tbody');
    mostrarLoader(tbody);

    try {
        const materiales = await fetchAPI('/api/materiales');
        
        if (!materiales.length) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center">No hay materiales registrados</td></tr>';
            return;
        }

        const materialesHtml = materiales.map(material => `
            <tr>
                <td>${material.id_material}</td>
                <td><strong>${esc(material.nombre)}</strong></td>
                <td>${esc(material.unidad || '')}</td>
                <td>${formatearMoneda(material.precio_unitario)}</td>
                <td>${esc(material.tipo_material || 'N/A')}</td>
                <td>${obtenerEstadoConClase(material.estado || 'Activo')}</td>
                <td>${esc(material.proveedor_nombre || 'N/A')}</td>
                <td>${material.stock_total || 0} ${esc(material.unidad || '')}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleMaterial(${material.id_material})" title="Ver detalles">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = materialesHtml;

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="9" class="text-center">Error: ${esc(error.message)}</td></tr>`;
        manejarErrorAPI(error, 'cargar materiales');
    }
}

// Cargar Proveedores
async function cargarProveedores() {
    const tbody = document.querySelector('#tablaProveedores tbody');
    mostrarLoader(tbody);

    try {
        const proveedores = await fetchAPI('/api/proveedores');
        
        if (!proveedores.length) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No hay proveedores registrados</td></tr>';
            return;
        }

        const proveedoresHtml = proveedores.map(proveedor => `
            <tr>
                <td>${proveedor.id_proveedor}</td>
                <td><strong>${esc(proveedor.nombre)}</strong></td>
                <td>${esc(proveedor.contacto || 'N/A')}</td>
                <td>${obtenerEstadoConClase(proveedor.estado || 'Activo')}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleProveedor(${proveedor.id_proveedor})" title="Ver detalles">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = proveedoresHtml;

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center">Error: ${esc(error.message)}</td></tr>`;
        manejarErrorAPI(error, 'cargar proveedores');
    }
}

// Cargar Inventario
async function cargarInventario() {
    const tbody = document.querySelector('#tablaInventario tbody');
    mostrarLoader(tbody);

    try {
        const inventario = await fetchAPI('/api/inventario');
        
        if (!inventario.length) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center">No hay inventario registrado</td></tr>';
            return;
        }

        const inventarioHtml = inventario.map(item => `
            <tr>
                <td>${item.id_inventario}</td>
                <td>${item.id_bodega}</td>
                <td><strong>${esc(item.material_nombre)}</strong></td>
                <td>${item.cantidad || 0}</td>
                <td>${esc(item.unidad || '')}</td>
                <td>${formatearMoneda(item.precio_unitario)}</td>
                <td>${formatearMoneda((item.cantidad || 0) * (item.precio_unitario || 0))}</td>
                <td>${obtenerEstadoConClase(item.estado || 'Disponible')}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleInventario(${item.id_inventario})" title="Ver detalles">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = inventarioHtml;

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="9" class="text-center">Error: ${esc(error.message)}</td></tr>`;
        manejarErrorAPI(error, 'cargar inventario');
    }
}

// Cargar Proyectos
async function cargarProyectos() {
    const tbody = document.querySelector('#tablaProyectos tbody');
    mostrarLoader(tbody);

    try {
        const proyectos = await fetchAPI('/api/proyectos');
        
        if (!proyectos.length) {
            tbody.innerHTML = '<tr><td colspan="9" class="text-center">No hay proyectos registrados</td></tr>';
            return;
        }

        const proyectosHtml = proyectos.map(proyecto => `
            <tr>
                <td>${proyecto.id_proyecto}</td>
                <td><strong>${esc(proyecto.nombre)}</strong></td>
                <td>${proyecto.id_obra}</td>
                <td>${formatearFecha(proyecto.fecha_inicio)}</td>
                <td>${formatearFecha(proyecto.fecha_fin)}</td>
                <td>${obtenerEstadoConClase(proyecto.estado)}</td>
                <td>${proyecto.avance || 0}%</td>
                <td>${proyecto.actividades || 0}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleProyecto(${proyecto.id_proyecto})" title="Ver detalles">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = proyectosHtml;

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="9" class="text-center">Error: ${esc(error.message)}</td></tr>`;
        manejarErrorAPI(error, 'cargar proyectos');
    }
}

// Cargar Reportes
async function cargarReportes() {
    const tipoReporte = document.getElementById('filterTipoReporte')?.value || 'semanal';
    const tbody = document.querySelector('#tablaReportes tbody');
    const thead = document.getElementById('reportesHeader');
    
    mostrarLoader(tbody);

    try {
        let reportes = [];
        let encabezados = [];

        if (tipoReporte === 'semanal') {
            reportes = await fetchAPI('/api/reportes/semanales');
            encabezados = ['<th>ID</th>', '<th>Obra</th>', '<th>Semana</th>', '<th>Fecha</th>', '<th>Resumen</th>'];
        } else if (tipoReporte === 'materiales') {
            reportes = await fetchAPI('/api/reportes/materiales');
            encabezados = ['<th>ID</th>', '<th>Material</th>', '<th>Tipo</th>', '<th>Origen</th>', '<th>Destino</th>', '<th>Fecha</th>'];
        }

        thead.innerHTML = `<tr>${encabezados.join('')}</tr>`;
        
        if (!reportes.length) {
            tbody.innerHTML = `<tr><td colspan="${encabezados.length}" class="text-center">No hay reportes disponibles</td></tr>`;
            return;
        }

        let reportesHtml = '';
        if (tipoReporte === 'semanal') {
            reportesHtml = reportes.map(reporte => `
                <tr>
                    <td>${reporte.id_reporte}</td>
                    <td>${reporte.id_obra}</td>
                    <td>${reporte.semana}</td>
                    <td>${formatearFecha(reporte.fecha)}</td>
                    <td>${esc(reporte.resumen || 'N/A')}</td>
                </tr>
            `).join('');
        } else if (tipoReporte === 'materiales') {
            reportesHtml = reportes.map(reporte => `
                <tr>
                    <td>${reporte.id_movimiento}</td>
                    <td>${reporte.id_material}</td>
                    <td>${esc(reporte.tipo)}</td>
                    <td>${esc(reporte.origen)}</td>
                    <td>${esc(reporte.destino)}</td>
                    <td>${formatearFecha(reporte.fecha)}</td>
                </tr>
            `).join('');
        }

        tbody.innerHTML = reportesHtml;

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-center">Error: ${esc(error.message)}</td></tr>`;
        manejarErrorAPI(error, 'cargar reportes');
    }
}

// Cargar Vehículos
async function cargarVehiculos() {
    const tbody = document.querySelector('#tablaVehiculos tbody');
    mostrarLoader(tbody);

    try {
        const vehiculos = await fetchAPI('/api/vehiculos');
        
        if (!vehiculos.length) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center">No hay vehículos registrados</td></tr>';
            return;
        }

        const vehiculosHtml = vehiculos.map(vehiculo => `
            <tr>
                <td>${vehiculo.id_vehiculo}</td>
                <td><strong>${esc(vehiculo.placa)}</strong></td>
                <td>${esc(vehiculo.tipo)}</td>
                <td>${obtenerEstadoConClase(vehiculo.estado)}</td>
                <td>${vehiculo.id_obra || 'Sin asignar'}</td>
                <td>${esc(vehiculo.ubicacion_actual || 'N/A')}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleVehiculo(${vehiculo.id_vehiculo})" title="Ver detalles">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = vehiculosHtml;

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center">Error: ${esc(error.message)}</td></tr>`;
        manejarErrorAPI(error, 'cargar vehículos');
    }
}

// Cargar Equipos
async function cargarEquipos() {
    const tbody = document.querySelector('#tablaEquipos tbody');
    mostrarLoader(tbody);

    try {
        const equipos = await fetchAPI('/api/equipos');
        
        if (!equipos.length) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center">No hay equipos registrados</td></tr>';
            return;
        }

        const equiposHtml = equipos.map(equipo => `
            <tr>
                <td>${equipo.id_equipo}</td>
                <td><strong>${esc(equipo.nombre)}</strong></td>
                <td>${esc(equipo.tipo)}</td>
                <td>${obtenerEstadoConClase(equipo.estado)}</td>
                <td>${esc(equipo.empleado_asignado || 'Sin asignar')}</td>
                <td>${formatearFecha(equipo.fecha_asignacion)}</td>
                <td>${formatearFecha(equipo.fecha_fin)}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleEquipo(${equipo.id_equipo})" title="Ver detalles">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `).join('');

        tbody.innerHTML = equiposHtml;

    } catch (error) {
        tbody.innerHTML = `<tr><td colspan="8" class="text-center">Error: ${esc(error.message)}</td></tr>`;
        manejarErrorAPI(error, 'cargar equipos');
    }
}

// ========================================
// FUNCIONES DE DETALLE (MODALES)
// ========================================

function verDetalleObra(id) {
    mostrarModal('Detalle de Obra', `
        <div class="detail-grid">
            <div class="detail-item"><strong>ID:</strong> ${id}</div>
            <div class="detail-item"><strong>Información:</strong> Cargando detalles de la obra...</div>
        </div>
    `);
}

function verDetalleEmpleado(id) {
    mostrarModal('Detalle de Empleado', `
        <div class="detail-grid">
            <div class="detail-item"><strong>ID:</strong> ${id}</div>
            <div class="detail-item"><strong>Información:</strong> Cargando detalles del empleado...</div>
        </div>
    `);
}

function verDetalleMaterial(id) {
    mostrarModal('Detalle de Material', `
        <div class="detail-grid">
            <div class="detail-item"><strong>ID:</strong> ${id}</div>
            <div class="detail-item"><strong>Información:</strong> Cargando detalles del material...</div>
        </div>
    `);
}

function verDetalleProveedor(id) {
    mostrarModal('Detalle de Proveedor', `
        <div class="detail-grid">
            <div class="detail-item"><strong>ID:</strong> ${id}</div>
            <div class="detail-item"><strong>Información:</strong> Cargando detalles del proveedor...</div>
        </div>
    `);
}

function verDetalleInventario(id) {
    mostrarModal('Detalle de Inventario', `
        <div class="detail-grid">
            <div class="detail-item"><strong>ID:</strong> ${id}</div>
            <div class="detail-item"><strong>Información:</strong> Cargando detalles del inventario...</div>
        </div>
    `);
}

function verDetalleProyecto(id) {
    mostrarModal('Detalle de Proyecto', `
        <div class="detail-grid">
            <div class="detail-item"><strong>ID:</strong> ${id}</div>
            <div class="detail-item"><strong>Información:</strong> Cargando detalles del proyecto...</div>
        </div>
    `);
}

function verDetalleVehiculo(id) {
    mostrarModal('Detalle de Vehículo', `
        <div class="detail-grid">
            <div class="detail-item"><strong>ID:</strong> ${id}</div>
            <div class="detail-item"><strong>Información:</strong> Cargando detalles del vehículo...</div>
        </div>
    `);
}

function verDetalleEquipo(id) {
    mostrarModal('Detalle de Equipo', `
        <div class="detail-grid">
            <div class="detail-item"><strong>ID:</strong> ${id}</div>
            <div class="detail-item"><strong>Información:</strong> Cargando detalles del equipo...</div>
        </div>
    `);
}

// Función para mostrar modal
function mostrarModal(titulo, contenido) {
    const modal = document.getElementById('detailModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    modalTitle.textContent = titulo;
    modalBody.innerHTML = contenido;
    modal.style.display = 'block';
}

// ========================================
// FUNCIONES AUXILIARES
// ========================================

// Función para hacer peticiones a la API
async function fetchAPI(endpoint, options = {}) {
    try {
        AppState.isLoading = true;
        
        const response = await fetch(endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        AppState.isLoading = false;
        
        return data;
    } catch (error) {
        AppState.isLoading = false;
        throw error;
    }
}

// Funciones placeholder para formularios (se pueden expandir)
function mostrarFormularioObra() {
    mostrarNotificacion('Función de crear obra en desarrollo', 'info');
}

function mostrarFormularioEmpleado() {
    mostrarNotificacion('Función de crear empleado en desarrollo', 'info');
}

function mostrarFormularioMaterial() {
    mostrarNotificacion('Función de crear material en desarrollo', 'info');
}

function mostrarFormularioProveedor() {
    mostrarNotificacion('Función de crear proveedor en desarrollo', 'info');
}

// Exponer funciones globalmente para uso en HTML
if (typeof window !== 'undefined') {
    window.AppState = AppState;
    window.mostrarSeccion = mostrarSeccion;
    window.verDetalleObra = verDetalleObra;
    window.verDetalleEmpleado = verDetalleEmpleado;
    window.verDetalleMaterial = verDetalleMaterial;
    window.verDetalleProveedor = verDetalleProveedor;
    window.verDetalleInventario = verDetalleInventario;
    window.verDetalleProyecto = verDetalleProyecto;
    window.verDetalleVehiculo = verDetalleVehiculo;
    window.verDetalleEquipo = verDetalleEquipo;
    window.mostrarFormularioObra = mostrarFormularioObra;
    window.mostrarFormularioEmpleado = mostrarFormularioEmpleado;
    window.mostrarFormularioMaterial = mostrarFormularioMaterial;
    window.mostrarFormularioProveedor = mostrarFormularioProveedor;
    window.toggleUserDropdown = toggleUserDropdown;
}

// Función para controlar el dropdown de usuario
function toggleUserDropdown() {
    const dropdown = document.getElementById('userDropdown');
    const userMenu = document.querySelector('.user-menu');
    
    if (dropdown) {
        dropdown.classList.toggle('show');
        userMenu.classList.toggle('open');
    }
}

// Cerrar dropdown al hacer clic fuera
document.addEventListener('click', function(event) {
    const userMenu = document.querySelector('.user-menu');
    const dropdown = document.getElementById('userDropdown');
    
    if (userMenu && dropdown && !userMenu.contains(event.target)) {
        dropdown.classList.remove('show');
        userMenu.classList.remove('open');
    }
});