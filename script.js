// Funcionalidad principal del sistema de consultas de la constructora

document.addEventListener('DOMContentLoaded', function() {
    inicializarSistema();
});

function inicializarSistema() {
    configurarNavegacion();
    cargarDashboard();
    configurarEventos();
    mostrarSeccion('dashboard');
}

// Configuración de navegación
function configurarNavegacion() {
    const menuItems = document.querySelectorAll('.menu-item');
    const navToggle = document.getElementById('navToggle');
    const sidebar = document.getElementById('sidebar');

    // Navegación del menú
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remover clase activa de todos los elementos
            menuItems.forEach(mi => mi.classList.remove('active'));
            
            // Añadir clase activa al elemento clickeado
            this.classList.add('active');
            
            // Mostrar sección correspondiente
            const seccion = this.getAttribute('data-section');
            mostrarSeccion(seccion);
            
            // Cerrar sidebar en móvil
            if (window.innerWidth <= 1024) {
                sidebar.classList.remove('active');
            }
        });
    });

    // Toggle del sidebar para móvil
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }

    // Cerrar sidebar al hacer click fuera de él
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 1024 && 
            !sidebar.contains(e.target) && 
            !navToggle.contains(e.target)) {
            sidebar.classList.remove('active');
        }
    });
}

// Mostrar sección específica
function mostrarSeccion(nombreSeccion) {
    const secciones = document.querySelectorAll('.content-section');
    
    secciones.forEach(seccion => {
        seccion.classList.remove('active');
    });
    
    const seccionActiva = document.getElementById(nombreSeccion);
    if (seccionActiva) {
        seccionActiva.classList.add('active');
    }

    // Cargar datos según la sección
    switch(nombreSeccion) {
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

// Cargar dashboard
function cargarDashboard() {
    const estadisticas = calcularEstadisticas();
    
    // Actualizar estadísticas
    document.getElementById('totalObras').textContent = estadisticas.totalObras;
    document.getElementById('totalEmpleados').textContent = estadisticas.totalEmpleados;
    document.getElementById('totalMateriales').textContent = estadisticas.totalMateriales;
    document.getElementById('totalProveedores').textContent = estadisticas.totalProveedores;

    // Cargar obras recientes
    const obrasRecientes = datosConstructora.obras.slice(0, 3);
    const contenedorObras = document.getElementById('obrasRecientes');
    contenedorObras.innerHTML = obrasRecientes.map(obra => `
        <div class="recent-item">
            <h4>${obra.nombre}</h4>
            <p>${obra.ubicacion} - ${obtenerEstadoConClase(obra.estado)}</p>
        </div>
    `).join('');

    // Cargar actividad reciente
    const actividadReciente = document.getElementById('actividadReciente');
    actividadReciente.innerHTML = `
        <div class="recent-item">
            <h4>Nuevo reporte semanal</h4>
            <p>Obra: Residencial Las Flores - Semana 39</p>
        </div>
        <div class="recent-item">
            <h4>Material ingresado</h4>
            <p>80 sacos de cemento - Torre Empresarial</p>
        </div>
        <div class="recent-item">
            <h4>Pago procesado</h4>
            <p>Ing. Sandra López - Q. 16,500.00</p>
        </div>
    `;
}

// Cargar obras
function cargarObras() {
    const tbody = document.querySelector('#tablaObras tbody');
    tbody.innerHTML = datosConstructora.obras.map(obra => {
        const cliente = obtenerClientePorId(obra.id_cliente);
        const presupuesto = obtenerPresupuestoPorObra(obra.id_obra);
        
        return `
            <tr>
                <td>${obra.id_obra}</td>
                <td><strong>${obra.nombre}</strong></td>
                <td>${obra.ubicacion}</td>
                <td>${obra.tipo}</td>
                <td>${obtenerEstadoConClase(obra.estado)}</td>
                <td>${cliente ? cliente.nombre : 'N/A'}</td>
                <td>${presupuesto ? formatearMoneda(presupuesto.monto_estimado) : 'N/A'}</td>
                <td>
                    <div class="progress-info">
                        <small>Físico: ${obra.avance_fisico}%</small><br>
                        <small>Financiero: ${obra.avance_financiero}%</small>
                    </div>
                </td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleObra(${obra.id_obra})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="action-btn btn-edit">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Cargar empleados
function cargarEmpleados() {
    const tbody = document.querySelector('#tablaEmpleados tbody');
    tbody.innerHTML = datosConstructora.empleados.map(empleado => {
        return `
            <tr>
                <td>${empleado.id_empleado}</td>
                <td><strong>${empleado.nombre}</strong></td>
                <td>${empleado.tipo}</td>
                <td>${empleado.salario_fijo > 0 ? formatearMoneda(empleado.salario_fijo) : 'Por trabajo'}</td>
                <td>${obtenerEstadoConClase(empleado.estado)}</td>
                <td>${empleado.proyectos_asignados}</td>
                <td>${formatearFecha(empleado.ultimo_pago)}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleEmpleado(${empleado.id_empleado})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="action-btn btn-edit">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Cargar materiales
function cargarMateriales() {
    const tbody = document.querySelector('#tablaMateriales tbody');
    tbody.innerHTML = datosConstructora.materiales.map(material => {
        const proveedor = obtenerProveedorPorId(material.id_proveedor);
        
        return `
            <tr>
                <td>${material.id_material}</td>
                <td><strong>${material.nombre}</strong></td>
                <td>${material.unidad}</td>
                <td>${formatearMoneda(material.precio_unitario)}</td>
                <td>${material.tipo_material}</td>
                <td>${obtenerEstadoConClase(material.estado)}</td>
                <td>${proveedor ? proveedor.nombre : 'N/A'}</td>
                <td>${material.stock_total} ${material.unidad}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleMaterial(${material.id_material})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="action-btn btn-edit">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Cargar proveedores
function cargarProveedores() {
    const tbody = document.querySelector('#tablaProveedores tbody');
    tbody.innerHTML = datosConstructora.proveedores.map(proveedor => {
        const materiales = datosConstructora.materiales.filter(m => m.id_proveedor === proveedor.id_proveedor);
        const facturas = datosConstructora.facturasProveedores.filter(f => f.id_proveedor === proveedor.id_proveedor);
        const totalFacturas = facturas.reduce((sum, f) => sum + f.monto, 0);
        
        return `
            <tr>
                <td>${proveedor.id_proveedor}</td>
                <td><strong>${proveedor.nombre}</strong></td>
                <td>${proveedor.contacto}</td>
                <td>${materiales.length} tipos</td>
                <td>${formatearMoneda(totalFacturas)}</td>
                <td>${obtenerEstadoConClase('Activo')}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleProveedor(${proveedor.id_proveedor})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="action-btn btn-edit">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Cargar inventario
function cargarInventario() {
    const tbody = document.querySelector('#tablaInventario tbody');
    
    // Llenar filtro de bodegas
    const filterBodega = document.getElementById('filterBodega');
    filterBodega.innerHTML = '<option value="">Todas las bodegas</option>' +
        datosConstructora.bodegas.map(bodega => 
            `<option value="${bodega.id_bodega}">Bodega ${bodega.id_bodega} - ${bodega.obra_nombre}</option>`
        ).join('');
    
    tbody.innerHTML = datosConstructora.inventario.map(item => {
        const bodega = obtenerBodegaPorId(item.id_bodega);
        const obra = obtenerObraPorId(bodega.id_obra);
        const valorTotal = item.cantidad * item.precio_unitario;
        
        return `
            <tr>
                <td>Bodega ${bodega.id_bodega}</td>
                <td>${obra ? obra.nombre : 'N/A'}</td>
                <td><strong>${item.material_nombre}</strong></td>
                <td>${item.cantidad}</td>
                <td>${item.unidad}</td>
                <td>${formatearMoneda(valorTotal)}</td>
                <td>${bodega.responsable}</td>
                <td>${obtenerEstadoConClase('Disponible')}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleInventario(${item.id_inventario})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="action-btn btn-edit">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Cargar proyectos
function cargarProyectos() {
    const tbody = document.querySelector('#tablaProyectos tbody');
    tbody.innerHTML = datosConstructora.proyectos.map(proyecto => {
        const obra = obtenerObraPorId(proyecto.id_obra);
        
        return `
            <tr>
                <td>${proyecto.id_proyecto}</td>
                <td><strong>${proyecto.nombre}</strong></td>
                <td>${obra ? obra.nombre : 'N/A'}</td>
                <td>${formatearFecha(proyecto.fecha_inicio)}</td>
                <td>${formatearFecha(proyecto.fecha_fin)}</td>
                <td>${obtenerEstadoConClase(proyecto.estado)}</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress" style="width: ${proyecto.avance}%"></div>
                        <span>${proyecto.avance}%</span>
                    </div>
                </td>
                <td>${proyecto.actividades}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleProyecto(${proyecto.id_proyecto})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="action-btn btn-edit">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Cargar reportes
function cargarReportes() {
    const estadisticas = calcularEstadisticas();
    
    // Actualizar resumen
    document.getElementById('gastosTotales').textContent = formatearMoneda(estadisticas.gastosTotales);
    document.getElementById('materialesConsumidos').textContent = estadisticas.materialesConsumidos.toFixed(1);
    document.getElementById('pagosRealizados').textContent = formatearMoneda(estadisticas.pagosRealizados);
    
    // Llenar filtro de obras
    const filterObraReporte = document.getElementById('filterObraReporte');
    filterObraReporte.innerHTML = '<option value="">Todas las obras</option>' +
        datosConstructora.obras.map(obra => 
            `<option value="${obra.id_obra}">${obra.nombre}</option>`
        ).join('');
    
    // Cargar reportes semanales por defecto
    cargarReportesSemanal();
}

// Cargar vehículos
function cargarVehiculos() {
    const tbody = document.querySelector('#tablaVehiculos tbody');
    tbody.innerHTML = datosConstructora.vehiculos.map(vehiculo => {
        const obra = obtenerObraPorId(vehiculo.id_obra);
        
        return `
            <tr>
                <td>${vehiculo.id_vehiculo}</td>
                <td><strong>${vehiculo.placa}</strong></td>
                <td>${vehiculo.tipo}</td>
                <td>${obtenerEstadoConClase(vehiculo.estado)}</td>
                <td>${obra ? obra.nombre : 'N/A'}</td>
                <td>${vehiculo.ubicacion_actual}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleVehiculo(${vehiculo.id_vehiculo})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="action-btn btn-edit">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Cargar equipos
function cargarEquipos() {
    const tbody = document.querySelector('#tablaEquipos tbody');
    tbody.innerHTML = datosConstructora.equipos.map(equipo => {
        return `
            <tr>
                <td>${equipo.id_equipo}</td>
                <td><strong>${equipo.nombre}</strong></td>
                <td>${equipo.tipo}</td>
                <td>${obtenerEstadoConClase(equipo.estado)}</td>
                <td>${equipo.empleado_asignado || 'Sin asignar'}</td>
                <td>${equipo.fecha_asignacion ? formatearFecha(equipo.fecha_asignacion) : 'N/A'}</td>
                <td>${equipo.fecha_fin ? formatearFecha(equipo.fecha_fin) : 'N/A'}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleEquipo(${equipo.id_equipo})">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="action-btn btn-edit">
                        <i class="fas fa-edit"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Configurar eventos de búsqueda y filtros
function configurarEventos() {
    // Eventos de búsqueda
    configurarBusqueda('searchObras', 'tablaObras');
    configurarBusqueda('searchEmpleados', 'tablaEmpleados');
    configurarBusqueda('searchMateriales', 'tablaMateriales');
    configurarBusqueda('searchProveedores', 'tablaProveedores');
    configurarBusqueda('searchInventario', 'tablaInventario');
    configurarBusqueda('searchProyectos', 'tablaProyectos');
    configurarBusqueda('searchVehiculos', 'tablaVehiculos');
    configurarBusqueda('searchEquipos', 'tablaEquipos');

    // Eventos de filtros
    configurarFiltro('filterEstadoObra', 'tablaObras', 4);
    configurarFiltro('filterTipoEmpleado', 'tablaEmpleados', 2);
    configurarFiltro('filterTipoMaterial', 'tablaMateriales', 4);
    configurarFiltro('filterBodega', 'tablaInventario', 0);
    configurarFiltro('filterEstadoProyecto', 'tablaProyectos', 5);
    configurarFiltro('filterTipoVehiculo', 'tablaVehiculos', 2);
    configurarFiltro('filterTipoEquipo', 'tablaEquipos', 2);

    // Evento para cambio de tipo de reporte
    const filterTipoReporte = document.getElementById('filterTipoReporte');
    if (filterTipoReporte) {
        filterTipoReporte.addEventListener('change', function() {
            const tipo = this.value;
            switch(tipo) {
                case 'semanal':
                    cargarReportesSemanal();
                    break;
                case 'gastos':
                    cargarReportesGastos();
                    break;
                case 'materiales':
                    cargarReportesMateriales();
                    break;
                case 'pagos':
                    cargarReportesPagos();
                    break;
            }
        });
    }

    // Evento para cerrar modal
    const closeModal = document.getElementById('closeModal');
    const modal = document.getElementById('detailModal');
    
    if (closeModal && modal) {
        closeModal.addEventListener('click', function() {
            modal.style.display = 'none';
        });
        
        window.addEventListener('click', function(event) {
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        });
    }
}

// Configurar búsqueda en tiempo real
function configurarBusqueda(inputId, tablaId) {
    const input = document.getElementById(inputId);
    if (input) {
        input.addEventListener('input', function() {
            const filtro = this.value.toLowerCase();
            const tabla = document.getElementById(tablaId);
            const filas = tabla.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
            
            for (let i = 0; i < filas.length; i++) {
                const fila = filas[i];
                const texto = fila.textContent || fila.innerText;
                
                if (texto.toLowerCase().includes(filtro)) {
                    fila.style.display = '';
                } else {
                    fila.style.display = 'none';
                }
            }
        });
    }
}

// Configurar filtros por columna
function configurarFiltro(selectId, tablaId, columna) {
    const select = document.getElementById(selectId);
    if (select) {
        select.addEventListener('change', function() {
            const filtro = this.value;
            const tabla = document.getElementById(tablaId);
            const filas = tabla.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
            
            for (let i = 0; i < filas.length; i++) {
                const fila = filas[i];
                const celda = fila.getElementsByTagName('td')[columna];
                
                if (!filtro || celda.textContent.includes(filtro)) {
                    fila.style.display = '';
                } else {
                    fila.style.display = 'none';
                }
            }
        });
    }
}

// Funciones para cargar diferentes tipos de reportes
function cargarReportesSemanal() {
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
    
    tbody.innerHTML = datosConstructora.reportesSemanales.map(reporte => {
        const obra = obtenerObraPorId(reporte.id_obra);
        
        return `
            <tr>
                <td>Semana ${reporte.semana}</td>
                <td>${obra ? obra.nombre : 'N/A'}</td>
                <td>${formatearFecha(reporte.fecha)}</td>
                <td>${reporte.resumen}</td>
                <td>
                    <button class="action-btn btn-view" onclick="verDetalleReporte(${reporte.id_reporte})">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

function cargarReportesGastos() {
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
    
    tbody.innerHTML = datosConstructora.facturasProveedores.map(factura => {
        const proveedor = obtenerProveedorPorId(factura.id_proveedor);
        
        return `
            <tr>
                <td>${proveedor ? proveedor.nombre : 'N/A'}</td>
                <td>${factura.numero_factura}</td>
                <td>${formatearFecha(factura.fecha)}</td>
                <td>${formatearMoneda(factura.monto)}</td>
                <td>${obtenerEstadoConClase(factura.estado)}</td>
            </tr>
        `;
    }).join('');
}

function cargarReportesMateriales() {
    const thead = document.getElementById('reportesHeader');
    const tbody = document.querySelector('#tablaReportes tbody');
    
    thead.innerHTML = `
        <tr>
            <th>Material</th>
            <th>Tipo</th>
            <th>Cantidad</th>
            <th>Origen</th>
            <th>Destino</th>
            <th>Fecha</th>
        </tr>
    `;
    
    tbody.innerHTML = datosConstructora.movimientosMaterial.map(movimiento => {
        const material = obtenerMaterialPorId(movimiento.id_material);
        
        return `
            <tr>
                <td>${material ? material.nombre : 'N/A'}</td>
                <td>${movimiento.tipo}</td>
                <td>${movimiento.cantidad} ${material ? material.unidad : ''}</td>
                <td>${movimiento.origen}</td>
                <td>${movimiento.destino}</td>
                <td>${formatearFecha(movimiento.fecha)}</td>
            </tr>
        `;
    }).join('');
}

function cargarReportesPagos() {
    const thead = document.getElementById('reportesHeader');
    const tbody = document.querySelector('#tablaReportes tbody');
    
    thead.innerHTML = `
        <tr>
            <th>Empleado</th>
            <th>Tipo Pago</th>
            <th>Fecha</th>
            <th>Monto</th>
            <th>Estado</th>
        </tr>
    `;
    
    tbody.innerHTML = datosConstructora.pagosEmpleados.map(pago => {
        const empleado = datosConstructora.empleados.find(e => e.id_empleado === pago.id_empleado);
        
        return `
            <tr>
                <td>${empleado ? empleado.nombre : 'N/A'}</td>
                <td>${pago.tipo}</td>
                <td>${formatearFecha(pago.fecha)}</td>
                <td>${formatearMoneda(pago.monto)}</td>
                <td>${obtenerEstadoConClase(pago.estado)}</td>
            </tr>
        `;
    }).join('');
}

// Funciones para mostrar detalles en modal
function mostrarModal(titulo, contenido) {
    const modal = document.getElementById('detailModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    modalTitle.textContent = titulo;
    modalBody.innerHTML = contenido;
    modal.style.display = 'block';
}

function verDetalleObra(id) {
    const obra = datosConstructora.obras.find(o => o.id_obra === id);
    const cliente = obtenerClientePorId(obra.id_cliente);
    const presupuesto = obtenerPresupuestoPorObra(obra.id_obra);
    
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
                <strong>Cliente:</strong> ${cliente ? cliente.nombre : 'N/A'}
            </div>
            <div class="detail-item">
                <strong>Presupuesto:</strong> ${presupuesto ? formatearMoneda(presupuesto.monto_estimado) : 'N/A'}
            </div>
            <div class="detail-item">
                <strong>Avance Físico:</strong> ${obra.avance_fisico}%
            </div>
            <div class="detail-item">
                <strong>Avance Financiero:</strong> ${obra.avance_financiero}%
            </div>
        </div>
    `;
    
    mostrarModal('Detalles de la Obra', contenido);
}

function verDetalleEmpleado(id) {
    const empleado = datosConstructora.empleados.find(e => e.id_empleado === id);
    
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
                <strong>Proyectos Asignados:</strong> ${empleado.proyectos_asignados}
            </div>
            <div class="detail-item">
                <strong>Último Pago:</strong> ${formatearFecha(empleado.ultimo_pago)}
            </div>
        </div>
    `;
    
    mostrarModal('Detalles del Empleado', contenido);
}

function verDetalleMaterial(id) {
    const material = datosConstructora.materiales.find(m => m.id_material === id);
    const proveedor = obtenerProveedorPorId(material.id_proveedor);
    
    const contenido = `
        <div class="detail-grid">
            <div class="detail-item">
                <strong>ID:</strong> ${material.id_material}
            </div>
            <div class="detail-item">
                <strong>Nombre:</strong> ${material.nombre}
            </div>
            <div class="detail-item">
                <strong>Unidad:</strong> ${material.unidad}
            </div>
            <div class="detail-item">
                <strong>Precio Unitario:</strong> ${formatearMoneda(material.precio_unitario)}
            </div>
            <div class="detail-item">
                <strong>Tipo:</strong> ${material.tipo_material}
            </div>
            <div class="detail-item">
                <strong>Estado:</strong> ${obtenerEstadoConClase(material.estado)}
            </div>
            <div class="detail-item">
                <strong>Proveedor:</strong> ${proveedor ? proveedor.nombre : 'N/A'}
            </div>
            <div class="detail-item">
                <strong>Stock Total:</strong> ${material.stock_total} ${material.unidad}
            </div>
        </div>
    `;
    
    mostrarModal('Detalles del Material', contenido);
}

function verDetalleProveedor(id) {
    const proveedor = datosConstructora.proveedores.find(p => p.id_proveedor === id);
    const materiales = datosConstructora.materiales.filter(m => m.id_proveedor === id);
    const facturas = datosConstructora.facturasProveedores.filter(f => f.id_proveedor === id);
    
    const contenido = `
        <div class="detail-grid">
            <div class="detail-item">
                <strong>ID:</strong> ${proveedor.id_proveedor}
            </div>
            <div class="detail-item">
                <strong>Nombre:</strong> ${proveedor.nombre}
            </div>
            <div class="detail-item">
                <strong>Contacto:</strong> ${proveedor.contacto}
            </div>
            <div class="detail-item">
                <strong>Materiales Suministrados:</strong> ${materiales.length}
            </div>
            <div class="detail-item">
                <strong>Facturas:</strong> ${facturas.length}
            </div>
        </div>
        <h4>Materiales:</h4>
        <ul>
            ${materiales.map(m => `<li>${m.nombre} - ${formatearMoneda(m.precio_unitario)}/${m.unidad}</li>`).join('')}
        </ul>
    `;
    
    mostrarModal('Detalles del Proveedor', contenido);
}

// Funciones adicionales para otros detalles
function verDetalleInventario(id) {
    // Implementar según necesidad
}

function verDetalleProyecto(id) {
    // Implementar según necesidad
}

function verDetalleVehiculo(id) {
    // Implementar según necesidad
}

function verDetalleEquipo(id) {
    // Implementar según necesidad
}

function verDetalleReporte(id) {
    // Implementar según necesidad
}

// Responsive: Ajustar sidebar en resize
window.addEventListener('resize', function() {
    const sidebar = document.getElementById('sidebar');
    if (window.innerWidth > 1024) {
        sidebar.classList.remove('active');
    }
});