// Datos de ejemplo para simular la base de datos de la constructora

const datosConstructora = {
    // Clientes
    clientes: [
        { id_cliente: 1, nombre: "Grupo Inmobiliario Central", contacto: "Juan Pérez - 2345-6789", tipo_cliente: "Corporativo" },
        { id_cliente: 2, nombre: "Desarrollos del Sur S.A.", contacto: "María García - 2456-7890", tipo_cliente: "Empresa" },
        { id_cliente: 3, nombre: "Familia Rodríguez", contacto: "Carlos Rodríguez - 2567-8901", tipo_cliente: "Particular" },
        { id_cliente: 4, nombre: "Constructora Maya", contacto: "Ana López - 2678-9012", tipo_cliente: "Corporativo" },
        { id_cliente: 5, nombre: "Inversiones Guatemala", contacto: "Pedro Morales - 2789-0123", tipo_cliente: "Empresa" }
    ],

    // Obras
    obras: [
        { 
            id_obra: 1, 
            nombre: "Residencial Las Flores", 
            ubicacion: "Zona 14, Guatemala", 
            tipo: "Casas habitacionales", 
            estado: "En Proceso", 
            id_cliente: 1,
            avance_fisico: 65.5,
            avance_financiero: 58.2
        },
        { 
            id_obra: 2, 
            nombre: "Torre Empresarial Centro", 
            ubicacion: "Zona 10, Guatemala", 
            tipo: "Edificios de oficina", 
            estado: "En Proceso", 
            id_cliente: 2,
            avance_fisico: 40.3,
            avance_financiero: 45.7
        },
        { 
            id_obra: 3, 
            nombre: "Bodega Industrial Norte", 
            ubicacion: "Villa Nueva", 
            tipo: "Bodegas", 
            estado: "Completada", 
            id_cliente: 4,
            avance_fisico: 100.0,
            avance_financiero: 100.0
        },
        { 
            id_obra: 4, 
            nombre: "Condominios El Bosque", 
            ubicacion: "Zona 16, Guatemala", 
            tipo: "Edificios habitacionales", 
            estado: "En Proceso", 
            id_cliente: 3,
            avance_fisico: 25.8,
            avance_financiero: 30.1
        },
        { 
            id_obra: 5, 
            nombre: "Centro Comercial Plaza Sur", 
            ubicacion: "Escuintla", 
            tipo: "Edificios de oficina", 
            estado: "Suspendida", 
            id_cliente: 5,
            avance_fisico: 15.2,
            avance_financiero: 12.9
        }
    ],

    // Presupuestos de obra
    presupuestosObra: [
        { id_presupuesto: 1, id_obra: 1, monto_estimado: 2500000.00, fecha: "2024-01-15" },
        { id_presupuesto: 2, id_obra: 2, monto_estimado: 8500000.00, fecha: "2024-02-20" },
        { id_presupuesto: 3, id_obra: 3, monto_estimado: 1200000.00, fecha: "2023-10-10" },
        { id_presupuesto: 4, id_obra: 4, monto_estimado: 4500000.00, fecha: "2024-06-01" },
        { id_presupuesto: 5, id_obra: 5, monto_estimado: 12000000.00, fecha: "2024-03-15" }
    ],

    // Empleados
    empleados: [
        { 
            id_empleado: 1, 
            nombre: "Ing. Roberto Méndez", 
            tipo: "Ingeniero", 
            salario_fijo: 15000.00, 
            estado: "Activo",
            ultimo_pago: "2024-09-30",
            proyectos_asignados: 2
        },
        { 
            id_empleado: 2, 
            nombre: "Arq. Laura Castillo", 
            tipo: "Arquitecto", 
            salario_fijo: 14000.00, 
            estado: "Activo",
            ultimo_pago: "2024-09-30",
            proyectos_asignados: 3
        },
        { 
            id_empleado: 3, 
            nombre: "José Hernández", 
            tipo: "Albañil", 
            salario_fijo: 0.00, 
            estado: "Activo",
            ultimo_pago: "2024-09-25",
            proyectos_asignados: 1
        },
        { 
            id_empleado: 4, 
            nombre: "Carmen Vásquez", 
            tipo: "Administrativo", 
            salario_fijo: 8500.00, 
            estado: "Activo",
            ultimo_pago: "2024-09-30",
            proyectos_asignados: 0
        },
        { 
            id_empleado: 5, 
            nombre: "Miguel Torres", 
            tipo: "Albañil", 
            salario_fijo: 0.00, 
            estado: "Activo",
            ultimo_pago: "2024-09-28",
            proyectos_asignados: 2
        },
        { 
            id_empleado: 6, 
            nombre: "Ing. Sandra López", 
            tipo: "Ingeniero", 
            salario_fijo: 16500.00, 
            estado: "Activo",
            ultimo_pago: "2024-09-30",
            proyectos_asignados: 1
        }
    ],

    // Proveedores
    proveedores: [
        { id_proveedor: 1, nombre: "Cementos Guatemala", contacto: "ventas@cemguat.com - 2234-5678" },
        { id_proveedor: 2, nombre: "Aceros del Norte", contacto: "info@aceronorte.com - 2345-6789" },
        { id_proveedor: 3, nombre: "Ferretería El Constructor", contacto: "constructor@gmail.com - 2456-7890" },
        { id_proveedor: 4, nombre: "Ladrillos San José", contacto: "sanjose@ladrillos.com - 2567-8901" },
        { id_proveedor: 5, nombre: "Materiales Premium", contacto: "premium@materiales.com - 2678-9012" }
    ],

    // Materiales
    materiales: [
        { 
            id_material: 1, 
            nombre: "Cemento Portland", 
            unidad: "Saco", 
            precio_unitario: 85.00, 
            tipo_material: "Cemento", 
            estado: "Disponible", 
            id_proveedor: 1,
            stock_total: 250
        },
        { 
            id_material: 2, 
            nombre: "Varilla #4", 
            unidad: "Quintal", 
            precio_unitario: 650.00, 
            tipo_material: "Acero", 
            estado: "Disponible", 
            id_proveedor: 2,
            stock_total: 180
        },
        { 
            id_material: 3, 
            nombre: "Ladrillo tayuyo", 
            unidad: "Millares", 
            precio_unitario: 850.00, 
            tipo_material: "Ladrillo", 
            estado: "Disponible", 
            id_proveedor: 4,
            stock_total: 45
        },
        { 
            id_material: 4, 
            nombre: "Arena de río", 
            unidad: "m³", 
            precio_unitario: 180.00, 
            tipo_material: "Agregados", 
            estado: "Disponible", 
            id_proveedor: 3,
            stock_total: 120
        },
        { 
            id_material: 5, 
            nombre: "Martillo de uña", 
            unidad: "Unidad", 
            precio_unitario: 125.00, 
            tipo_material: "Herramientas", 
            estado: "Disponible", 
            id_proveedor: 3,
            stock_total: 25
        },
        { 
            id_material: 6, 
            nombre: "Piedrín 3/4", 
            unidad: "m³", 
            precio_unitario: 220.00, 
            tipo_material: "Agregados", 
            estado: "Disponible", 
            id_proveedor: 5,
            stock_total: 85
        }
    ],

    // Áreas
    areas: [
        { id_area: 1, nombre: "Cimentación", id_obra: 1 },
        { id_area: 2, nombre: "Estructura", id_obra: 1 },
        { id_area: 3, nombre: "Mampostería", id_obra: 1 },
        { id_area: 4, nombre: "Cimentación", id_obra: 2 },
        { id_area: 5, nombre: "Estructura", id_obra: 2 },
        { id_area: 6, nombre: "Acabados", id_obra: 3 },
        { id_area: 7, nombre: "Cimentación", id_obra: 4 },
        { id_area: 8, nombre: "Instalaciones", id_obra: 5 }
    ],

    // Proyectos
    proyectos: [
        { 
            id_proyecto: 1, 
            id_obra: 1, 
            nombre: "Fase 1 - Casas A1-A10", 
            fecha_inicio: "2024-01-15", 
            fecha_fin: "2024-08-15", 
            estado: "En Proceso",
            avance: 65.5,
            actividades: 8
        },
        { 
            id_proyecto: 2, 
            id_obra: 1, 
            nombre: "Fase 2 - Casas B1-B8", 
            fecha_inicio: "2024-05-01", 
            fecha_fin: "2024-12-01", 
            estado: "En Proceso",
            avance: 35.2,
            actividades: 6
        },
        { 
            id_proyecto: 3, 
            id_obra: 2, 
            nombre: "Estructura Principal", 
            fecha_inicio: "2024-02-20", 
            fecha_fin: "2024-11-30", 
            estado: "En Proceso",
            avance: 40.3,
            actividades: 12
        },
        { 
            id_proyecto: 4, 
            id_obra: 3, 
            nombre: "Nave Industrial", 
            fecha_inicio: "2023-10-10", 
            fecha_fin: "2024-05-30", 
            estado: "Completado",
            avance: 100.0,
            actividades: 15
        },
        { 
            id_proyecto: 5, 
            id_obra: 4, 
            nombre: "Torre A", 
            fecha_inicio: "2024-06-01", 
            fecha_fin: "2025-03-01", 
            estado: "En Proceso",
            avance: 25.8,
            actividades: 10
        }
    ],

    // Bodegas
    bodegas: [
        { id_bodega: 1, id_obra: 1, responsable: "Carlos Méndez", obra_nombre: "Residencial Las Flores" },
        { id_bodega: 2, id_obra: 2, responsable: "Ana Morales", obra_nombre: "Torre Empresarial Centro" },
        { id_bodega: 3, id_obra: 3, responsable: "Luis Herrera", obra_nombre: "Bodega Industrial Norte" },
        { id_bodega: 4, id_obra: 4, responsable: "María Santos", obra_nombre: "Condominios El Bosque" },
        { id_bodega: 5, id_obra: 5, responsable: "Jorge Castillo", obra_nombre: "Centro Comercial Plaza Sur" }
    ],

    // Inventario
    inventario: [
        { 
            id_inventario: 1, 
            id_bodega: 1, 
            id_material: 1, 
            cantidad: 85.0,
            material_nombre: "Cemento Portland",
            unidad: "Saco",
            precio_unitario: 85.00
        },
        { 
            id_inventario: 2, 
            id_bodega: 1, 
            id_material: 2, 
            cantidad: 45.5,
            material_nombre: "Varilla #4",
            unidad: "Quintal",
            precio_unitario: 650.00
        },
        { 
            id_inventario: 3, 
            id_bodega: 2, 
            id_material: 1, 
            cantidad: 120.0,
            material_nombre: "Cemento Portland",
            unidad: "Saco",
            precio_unitario: 85.00
        },
        { 
            id_inventario: 4, 
            id_bodega: 2, 
            id_material: 3, 
            cantidad: 15.0,
            material_nombre: "Ladrillo tayuyo",
            unidad: "Millares",
            precio_unitario: 850.00
        },
        { 
            id_inventario: 5, 
            id_bodega: 3, 
            id_material: 4, 
            cantidad: 25.5,
            material_nombre: "Arena de río",
            unidad: "m³",
            precio_unitario: 180.00
        },
        { 
            id_inventario: 6, 
            id_bodega: 4, 
            id_material: 6, 
            cantidad: 18.0,
            material_nombre: "Piedrín 3/4",
            unidad: "m³",
            precio_unitario: 220.00
        }
    ],

    // Vehículos
    vehiculos: [
        { 
            id_vehiculo: 1, 
            placa: "P-123ABC", 
            tipo: "Pickup", 
            estado: "Operativo", 
            id_obra: 1,
            ubicacion_actual: "Zona 14, Guatemala"
        },
        { 
            id_vehiculo: 2, 
            placa: "C-456DEF", 
            tipo: "Camión", 
            estado: "Operativo", 
            id_obra: 2,
            ubicacion_actual: "Zona 10, Guatemala"
        },
        { 
            id_vehiculo: 3, 
            placa: "M-789GHI", 
            tipo: "Maquinaria", 
            estado: "En Mantenimiento", 
            id_obra: 1,
            ubicacion_actual: "Taller Central"
        },
        { 
            id_vehiculo: 4, 
            placa: "P-321JKL", 
            tipo: "Pickup", 
            estado: "Operativo", 
            id_obra: 4,
            ubicacion_actual: "Zona 16, Guatemala"
        },
        { 
            id_vehiculo: 5, 
            placa: "C-654MNO", 
            tipo: "Camión", 
            estado: "Operativo", 
            id_obra: 3,
            ubicacion_actual: "Villa Nueva"
        }
    ],

    // Equipos
    equipos: [
        { 
            id_equipo: 1, 
            nombre: "Mezcladora de concreto", 
            tipo: "Maquinaria", 
            estado: "Disponible",
            empleado_asignado: null,
            fecha_asignacion: null,
            fecha_fin: null
        },
        { 
            id_equipo: 2, 
            nombre: "Taladro percutor", 
            tipo: "Herramientas", 
            estado: "Asignado",
            empleado_asignado: "José Hernández",
            fecha_asignacion: "2024-09-15",
            fecha_fin: "2024-10-15"
        },
        { 
            id_equipo: 3, 
            nombre: "Nivel láser", 
            tipo: "Medición", 
            estado: "Asignado",
            empleado_asignado: "Ing. Roberto Méndez",
            fecha_asignacion: "2024-09-01",
            fecha_fin: "2024-11-30"
        },
        { 
            id_equipo: 4, 
            nombre: "Cortadora de azulejo", 
            tipo: "Herramientas", 
            estado: "En Mantenimiento",
            empleado_asignado: null,
            fecha_asignacion: null,
            fecha_fin: null
        },
        { 
            id_equipo: 5, 
            nombre: "Teodolito", 
            tipo: "Medición", 
            estado: "Disponible",
            empleado_asignado: null,
            fecha_asignacion: null,
            fecha_fin: null
        }
    ],

    // Reportes semanales
    reportesSemanales: [
        { 
            id_reporte: 1, 
            id_obra: 1, 
            semana: 38, 
            resumen: "Avance significativo en cimentación de casas A6-A10. Se completó excavación y se inició armado de hierro.", 
            fecha: "2024-09-22" 
        },
        { 
            id_reporte: 2, 
            id_obra: 2, 
            semana: 38, 
            resumen: "Continuación de estructura del piso 8. Problemas menores con suministro de cemento.", 
            fecha: "2024-09-22" 
        },
        { 
            id_reporte: 3, 
            id_obra: 1, 
            semana: 39, 
            resumen: "Fundición de losas en casas A6-A8. Inicio de mampostería en casas A1-A3.", 
            fecha: "2024-09-29" 
        },
        { 
            id_reporte: 4, 
            id_obra: 4, 
            semana: 39, 
            resumen: "Excavación completada. Preparación para inicio de cimentación próxima semana.", 
            fecha: "2024-09-29" 
        }
    ],

    // Pagos a empleados
    pagosEmpleados: [
        { id_pago: 1, id_empleado: 1, fecha: "2024-09-30", monto: 15000.00, estado: "Pagado", tipo: "Salario Fijo" },
        { id_pago: 2, id_empleado: 2, fecha: "2024-09-30", monto: 14000.00, estado: "Pagado", tipo: "Salario Fijo" },
        { id_pago: 3, id_empleado: 3, fecha: "2024-09-25", monto: 3250.00, estado: "Pagado", tipo: "Por Trabajo" },
        { id_pago: 4, id_empleado: 4, fecha: "2024-09-30", monto: 8500.00, estado: "Pagado", tipo: "Salario Fijo" },
        { id_pago: 5, id_empleado: 5, fecha: "2024-09-28", monto: 2850.00, estado: "Pagado", tipo: "Por Trabajo" },
        { id_pago: 6, id_empleado: 6, fecha: "2024-09-30", monto: 16500.00, estado: "Pagado", tipo: "Salario Fijo" }
    ],

    // Movimientos de material
    movimientosMaterial: [
        { 
            id_movimiento: 1, 
            id_material: 1, 
            tipo: "Ingreso", 
            fecha: "2024-09-20", 
            cantidad: 50.0, 
            origen: "Cementos Guatemala", 
            destino: "Bodega Obra 1" 
        },
        { 
            id_movimiento: 2, 
            id_material: 2, 
            tipo: "Salida", 
            fecha: "2024-09-22", 
            cantidad: 15.5, 
            origen: "Bodega Obra 1", 
            destino: "Área Cimentación" 
        },
        { 
            id_movimiento: 3, 
            id_material: 1, 
            tipo: "Ingreso", 
            fecha: "2024-09-25", 
            cantidad: 80.0, 
            origen: "Cementos Guatemala", 
            destino: "Bodega Obra 2" 
        }
    ],

    // Facturas de proveedores
    facturasProveedores: [
        { 
            id_factura: 1, 
            id_proveedor: 1, 
            fecha: "2024-09-20", 
            monto: 4250.00, 
            estado: "Pagada",
            numero_factura: "F-001-2024"
        },
        { 
            id_factura: 2, 
            id_proveedor: 2, 
            fecha: "2024-09-18", 
            monto: 29250.00, 
            estado: "Pendiente",
            numero_factura: "F-158-2024"
        },
        { 
            id_factura: 3, 
            id_proveedor: 4, 
            fecha: "2024-09-15", 
            monto: 12750.00, 
            estado: "Pagada",
            numero_factura: "F-089-2024"
        }
    ]
};

// Funciones auxiliares para obtener datos relacionados
function obtenerClientePorId(id) {
    return datosConstructora.clientes.find(cliente => cliente.id_cliente === id);
}

function obtenerObraPorId(id) {
    return datosConstructora.obras.find(obra => obra.id_obra === id);
}

function obtenerProveedorPorId(id) {
    return datosConstructora.proveedores.find(proveedor => proveedor.id_proveedor === id);
}

function obtenerMaterialPorId(id) {
    return datosConstructora.materiales.find(material => material.id_material === id);
}

function obtenerBodegaPorId(id) {
    return datosConstructora.bodegas.find(bodega => bodega.id_bodega === id);
}

function obtenerPresupuestoPorObra(id_obra) {
    return datosConstructora.presupuestosObra.find(presupuesto => presupuesto.id_obra === id_obra);
}

// Función para formatear números como moneda guatemalteca
function formatearMoneda(cantidad) {
    return new Intl.NumberFormat('es-GT', {
        style: 'currency',
        currency: 'GTQ',
        minimumFractionDigits: 2
    }).format(cantidad);
}

// Función para formatear fechas
function formatearFecha(fecha) {
    return new Date(fecha).toLocaleDateString('es-GT', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Función para obtener el estado con clase CSS
function obtenerEstadoConClase(estado) {
    const clases = {
        'Activo': 'status-activo',
        'En Proceso': 'status-proceso',
        'Completada': 'status-completado',
        'Completado': 'status-completado',
        'Suspendida': 'status-suspendido',
        'Suspendido': 'status-suspendido',
        'Inactivo': 'status-inactivo',
        'Disponible': 'status-activo',
        'Operativo': 'status-activo',
        'En Mantenimiento': 'status-proceso',
        'Asignado': 'status-proceso',
        'Pagada': 'status-completado',
        'Pagado': 'status-completado',
        'Pendiente': 'status-proceso'
    };
    
    const clase = clases[estado] || 'status-inactivo';
    return `<span class="status-badge ${clase}">${estado}</span>`;
}

// Calcular estadísticas generales
function calcularEstadisticas() {
    return {
        totalObras: datosConstructora.obras.filter(obra => obra.estado === 'En Proceso').length,
        totalEmpleados: datosConstructora.empleados.filter(empleado => empleado.estado === 'Activo').length,
        totalMateriales: datosConstructora.materiales.length,
        totalProveedores: datosConstructora.proveedores.length,
        gastosTotales: datosConstructora.facturasProveedores.reduce((total, factura) => total + factura.monto, 0),
        pagosRealizados: datosConstructora.pagosEmpleados.reduce((total, pago) => total + pago.monto, 0),
        materialesConsumidos: datosConstructora.movimientosMaterial
            .filter(mov => mov.tipo === 'Salida')
            .reduce((total, mov) => total + mov.cantidad, 0)
    };
}