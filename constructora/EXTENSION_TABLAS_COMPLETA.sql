-- =====================================================
-- EXTENSIÓN DE BASE DE DATOS - 30 TABLAS ADICIONALES
-- Sistema ERP Constructora Completo - Total: 86 Tablas
-- =====================================================

BEGIN;

-- =====================================================
-- MÓDULO FACTURACIÓN Y PAGOS (8 TABLAS)
-- =====================================================

-- 57. FACTURAS
CREATE TABLE FACTURAS (
    id_factura SERIAL PRIMARY KEY,
    numero_factura VARCHAR(50) UNIQUE NOT NULL,
    fecha_factura DATE DEFAULT CURRENT_DATE,
    fecha_vencimiento DATE,
    subtotal DECIMAL(15,2) NOT NULL DEFAULT 0,
    impuestos DECIMAL(15,2) NOT NULL DEFAULT 0,
    descuento DECIMAL(15,2) NOT NULL DEFAULT 0,
    total DECIMAL(15,2) NOT NULL DEFAULT 0,
    estado_factura VARCHAR(50) DEFAULT 'Pendiente',
    observaciones TEXT,
    id_cliente INTEGER NOT NULL REFERENCES CLIENTES(id_cliente) ON DELETE RESTRICT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 58. DETALLES_FACTURA
CREATE TABLE DETALLES_FACTURA (
    id_detalle_factura SERIAL PRIMARY KEY,
    id_factura INTEGER REFERENCES FACTURAS(id_factura) ON DELETE CASCADE,
    concepto VARCHAR(200) NOT NULL,
    descripcion TEXT,
    cantidad DECIMAL(10,2) NOT NULL DEFAULT 1,
    precio_unitario DECIMAL(12,2) NOT NULL,
    subtotal_linea DECIMAL(15,2) NOT NULL,
    impuesto_linea DECIMAL(15,2) DEFAULT 0,
    total_linea DECIMAL(15,2) NOT NULL
);

-- 59. METODOS_PAGO
CREATE TABLE METODOS_PAGO (
    id_metodo_pago SERIAL PRIMARY KEY,
    nombre_metodo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    requiere_referencia BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE
);

-- 60. PAGOS
CREATE TABLE PAGOS (
    id_pago SERIAL PRIMARY KEY,
    numero_recibo VARCHAR(50) UNIQUE,
    fecha_pago DATE DEFAULT CURRENT_DATE,
    monto_pago DECIMAL(15,2) NOT NULL,
    id_metodo_pago INTEGER REFERENCES METODOS_PAGO(id_metodo_pago),
    referencia_pago VARCHAR(100),
    observaciones_pago TEXT,
    estado_pago VARCHAR(50) DEFAULT 'Confirmado',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 61. CUENTAS_COBRAR
CREATE TABLE CUENTAS_COBRAR (
    id_cuenta_cobrar SERIAL PRIMARY KEY,
    id_factura INTEGER REFERENCES FACTURAS(id_factura) ON DELETE CASCADE,
    monto_original DECIMAL(15,2) NOT NULL,
    monto_pendiente DECIMAL(15,2) NOT NULL,
    fecha_vencimiento DATE,
    dias_vencido INTEGER DEFAULT 0,
    estado_cobranza VARCHAR(50) DEFAULT 'Vigente'
);

-- 62. FACTURA_OBRA (Relación facturas con obras)
CREATE TABLE FACTURA_OBRA (
    id_factura INTEGER REFERENCES FACTURAS(id_factura) ON DELETE CASCADE,
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    porcentaje_obra DECIMAL(5,2) DEFAULT 100.00,
    PRIMARY KEY (id_factura, id_obra)
);

-- 63. FACTURA_PAGO (Relación facturas con pagos)
CREATE TABLE FACTURA_PAGO (
    id_factura INTEGER REFERENCES FACTURAS(id_factura) ON DELETE CASCADE,
    id_pago INTEGER REFERENCES PAGOS(id_pago) ON DELETE CASCADE,
    monto_aplicado DECIMAL(15,2) NOT NULL,
    fecha_aplicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_factura, id_pago)
);

-- 64. DESCUENTOS_FACTURA
CREATE TABLE DESCUENTOS_FACTURA (
    id_descuento SERIAL PRIMARY KEY,
    id_factura INTEGER REFERENCES FACTURAS(id_factura) ON DELETE CASCADE,
    tipo_descuento VARCHAR(50) NOT NULL, -- 'Porcentaje' o 'Valor'
    valor_descuento DECIMAL(10,2) NOT NULL,
    monto_descuento DECIMAL(15,2) NOT NULL,
    motivo_descuento TEXT,
    autorizado_por VARCHAR(100)
);

-- =====================================================
-- MÓDULO CONTABILIDAD AVANZADA (6 TABLAS)
-- =====================================================

-- 65. CUENTAS_CONTABLES
CREATE TABLE CUENTAS_CONTABLES (
    id_cuenta SERIAL PRIMARY KEY,
    codigo_cuenta VARCHAR(20) UNIQUE NOT NULL,
    nombre_cuenta VARCHAR(150) NOT NULL,
    tipo_cuenta VARCHAR(50) NOT NULL, -- Activo, Pasivo, Patrimonio, Ingreso, Gasto
    nivel INTEGER NOT NULL,
    cuenta_padre INTEGER REFERENCES CUENTAS_CONTABLES(id_cuenta),
    naturaleza VARCHAR(20) NOT NULL, -- Débito o Crédito
    activa BOOLEAN DEFAULT TRUE
);

-- 66. MOVIMIENTOS_CONTABLES
CREATE TABLE MOVIMIENTOS_CONTABLES (
    id_movimiento SERIAL PRIMARY KEY,
    numero_asiento VARCHAR(50) NOT NULL,
    fecha_movimiento DATE DEFAULT CURRENT_DATE,
    id_cuenta INTEGER REFERENCES CUENTAS_CONTABLES(id_cuenta),
    debe DECIMAL(15,2) DEFAULT 0,
    haber DECIMAL(15,2) DEFAULT 0,
    concepto TEXT NOT NULL,
    documento_soporte VARCHAR(100),
    id_obra INTEGER REFERENCES OBRAS(id_obra),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 67. CENTROS_COSTO
CREATE TABLE CENTROS_COSTO (
    id_centro_costo SERIAL PRIMARY KEY,
    codigo_centro VARCHAR(20) UNIQUE NOT NULL,
    nombre_centro VARCHAR(150) NOT NULL,
    descripcion TEXT,
    tipo_centro VARCHAR(50), -- Obra, Administrativo, Comercial
    activo BOOLEAN DEFAULT TRUE
);

-- 68. GASTOS_OBRA
CREATE TABLE GASTOS_OBRA (
    id_gasto SERIAL PRIMARY KEY,
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    id_centro_costo INTEGER REFERENCES CENTROS_COSTO(id_centro_costo),
    fecha_gasto DATE DEFAULT CURRENT_DATE,
    concepto_gasto VARCHAR(200) NOT NULL,
    descripcion_gasto TEXT,
    monto_gasto DECIMAL(15,2) NOT NULL,
    tipo_gasto VARCHAR(50), -- Material, Mano de Obra, Equipo, Administrativo
    documento_soporte VARCHAR(100),
    aprobado_por VARCHAR(100)
);

-- 69. FLUJO_CAJA
CREATE TABLE FLUJO_CAJA (
    id_flujo SERIAL PRIMARY KEY,
    fecha_flujo DATE DEFAULT CURRENT_DATE,
    tipo_movimiento VARCHAR(20) NOT NULL, -- Ingreso o Egreso
    concepto VARCHAR(200) NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    saldo_anterior DECIMAL(15,2),
    saldo_actual DECIMAL(15,2),
    categoria VARCHAR(100),
    referencia_documento VARCHAR(100)
);

-- 70. CONCILIACIONES
CREATE TABLE CONCILIACIONES (
    id_conciliacion SERIAL PRIMARY KEY,
    fecha_conciliacion DATE DEFAULT CURRENT_DATE,
    periodo_mes INTEGER NOT NULL,
    periodo_ano INTEGER NOT NULL,
    saldo_libro DECIMAL(15,2) NOT NULL,
    saldo_banco DECIMAL(15,2) NOT NULL,
    diferencia DECIMAL(15,2) NOT NULL,
    conciliado BOOLEAN DEFAULT FALSE,
    observaciones TEXT,
    responsable VARCHAR(100)
);

-- =====================================================
-- MÓDULO REPORTES AVANZADOS (4 TABLAS)
-- =====================================================

-- 71. DASHBOARDS_PERSONALIZADOS
CREATE TABLE DASHBOARDS_PERSONALIZADOS (
    id_dashboard SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES USUARIOS_SISTEMA(id_usuario) ON DELETE CASCADE,
    nombre_dashboard VARCHAR(150) NOT NULL,
    configuracion_json TEXT, -- JSON con configuración de widgets
    es_publico BOOLEAN DEFAULT FALSE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 72. METRICAS_KPI
CREATE TABLE METRICAS_KPI (
    id_metrica SERIAL PRIMARY KEY,
    nombre_metrica VARCHAR(100) NOT NULL,
    descripcion TEXT,
    formula_calculo TEXT,
    valor_actual DECIMAL(15,4),
    valor_objetivo DECIMAL(15,4),
    unidad_medida VARCHAR(50),
    frecuencia_actualizacion VARCHAR(50), -- Diario, Semanal, Mensual
    fecha_calculo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    categoria_kpi VARCHAR(100)
);

-- 73. ALERTAS_SISTEMA
CREATE TABLE ALERTAS_SISTEMA (
    id_alerta SERIAL PRIMARY KEY,
    tipo_alerta VARCHAR(100) NOT NULL,
    titulo_alerta VARCHAR(200) NOT NULL,
    mensaje_alerta TEXT NOT NULL,
    nivel_prioridad VARCHAR(20) DEFAULT 'Media', -- Baja, Media, Alta, Crítica
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento TIMESTAMP,
    leida BOOLEAN DEFAULT FALSE,
    id_usuario_destinatario INTEGER REFERENCES USUARIOS_SISTEMA(id_usuario),
    referencia_tabla VARCHAR(100),
    referencia_id INTEGER
);

-- 74. CONFIGURACION_REPORTES
CREATE TABLE CONFIGURACION_REPORTES (
    id_configuracion SERIAL PRIMARY KEY,
    nombre_reporte VARCHAR(150) NOT NULL,
    descripcion_reporte TEXT,
    consulta_sql TEXT,
    parametros_json TEXT, -- JSON con parámetros del reporte
    formato_salida VARCHAR(50) DEFAULT 'HTML', -- HTML, PDF, Excel
    programado BOOLEAN DEFAULT FALSE,
    frecuencia_programacion VARCHAR(50),
    activo BOOLEAN DEFAULT TRUE,
    creado_por INTEGER REFERENCES USUARIOS_SISTEMA(id_usuario)
);

-- =====================================================
-- MÓDULO MANTENIMIENTO (4 TABLAS)
-- =====================================================

-- 75. MANTENIMIENTOS
CREATE TABLE MANTENIMIENTOS (
    id_mantenimiento SERIAL PRIMARY KEY,
    id_equipo INTEGER REFERENCES EQUIPOS(id_equipo) ON DELETE CASCADE,
    id_vehiculo INTEGER REFERENCES VEHICULOS(id_vehiculo) ON DELETE CASCADE,
    tipo_mantenimiento VARCHAR(50) NOT NULL, -- Preventivo, Correctivo, Predictivo
    descripcion_mantenimiento TEXT NOT NULL,
    fecha_programada DATE NOT NULL,
    fecha_realizada DATE,
    costo_estimado DECIMAL(12,2),
    costo_real DECIMAL(12,2),
    estado_mantenimiento VARCHAR(50) DEFAULT 'Programado',
    observaciones TEXT,
    responsable_mantenimiento VARCHAR(100)
);

-- 76. ORDENES_TRABAJO
CREATE TABLE ORDENES_TRABAJO (
    id_orden_trabajo SERIAL PRIMARY KEY,
    numero_orden VARCHAR(50) UNIQUE NOT NULL,
    id_mantenimiento INTEGER REFERENCES MANTENIMIENTOS(id_mantenimiento),
    fecha_creacion DATE DEFAULT CURRENT_DATE,
    fecha_inicio DATE,
    fecha_fin DATE,
    prioridad VARCHAR(20) DEFAULT 'Media',
    estado_orden VARCHAR(50) DEFAULT 'Creada',
    descripcion_trabajo TEXT NOT NULL,
    asignado_a VARCHAR(100),
    tiempo_estimado INTEGER, -- En horas
    tiempo_real INTEGER -- En horas
);

-- 77. REPUESTOS
CREATE TABLE REPUESTOS (
    id_repuesto SERIAL PRIMARY KEY,
    codigo_repuesto VARCHAR(50) UNIQUE NOT NULL,
    nombre_repuesto VARCHAR(150) NOT NULL,
    descripcion_repuesto TEXT,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    precio_unitario DECIMAL(12,2),
    stock_minimo INTEGER DEFAULT 1,
    stock_actual INTEGER DEFAULT 0,
    ubicacion_bodega VARCHAR(100),
    activo BOOLEAN DEFAULT TRUE
);

-- 78. HISTORIAL_MANTENIMIENTO
CREATE TABLE HISTORIAL_MANTENIMIENTO (
    id_historial SERIAL PRIMARY KEY,
    id_mantenimiento INTEGER REFERENCES MANTENIMIENTOS(id_mantenimiento) ON DELETE CASCADE,
    fecha_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo_evento VARCHAR(50) NOT NULL, -- Inicio, Pausa, Reanudación, Finalización
    descripcion_evento TEXT,
    usuario_evento VARCHAR(100),
    costo_evento DECIMAL(12,2),
    observaciones_evento TEXT
);

-- =====================================================
-- MÓDULO COMPRAS Y PROVEEDORES EXTENDIDO (4 TABLAS)
-- =====================================================

-- 79. ORDENES_COMPRA
CREATE TABLE ORDENES_COMPRA (
    id_orden_compra SERIAL PRIMARY KEY,
    numero_orden VARCHAR(50) UNIQUE NOT NULL,
    id_proveedor INTEGER REFERENCES PROVEEDORES(id_proveedor) ON DELETE RESTRICT,
    fecha_orden DATE DEFAULT CURRENT_DATE,
    fecha_entrega_solicitada DATE,
    fecha_entrega_real DATE,
    subtotal DECIMAL(15,2) NOT NULL DEFAULT 0,
    impuestos DECIMAL(15,2) NOT NULL DEFAULT 0,
    total DECIMAL(15,2) NOT NULL DEFAULT 0,
    estado_orden VARCHAR(50) DEFAULT 'Pendiente',
    observaciones TEXT,
    aprobada_por VARCHAR(100)
);

-- 80. DETALLES_ORDEN_COMPRA
CREATE TABLE DETALLES_ORDEN_COMPRA (
    id_detalle_orden SERIAL PRIMARY KEY,
    id_orden_compra INTEGER REFERENCES ORDENES_COMPRA(id_orden_compra) ON DELETE CASCADE,
    id_material INTEGER REFERENCES MATERIALES(id_material),
    id_repuesto INTEGER REFERENCES REPUESTOS(id_repuesto),
    cantidad_solicitada DECIMAL(10,2) NOT NULL,
    cantidad_recibida DECIMAL(10,2) DEFAULT 0,
    precio_unitario DECIMAL(12,2) NOT NULL,
    subtotal_linea DECIMAL(15,2) NOT NULL
);

-- 81. RECEPCIONES
CREATE TABLE RECEPCIONES (
    id_recepcion SERIAL PRIMARY KEY,
    id_orden_compra INTEGER REFERENCES ORDENES_COMPRA(id_orden_compra) ON DELETE CASCADE,
    numero_recepcion VARCHAR(50) UNIQUE NOT NULL,
    fecha_recepcion DATE DEFAULT CURRENT_DATE,
    recibido_por VARCHAR(100) NOT NULL,
    estado_recepcion VARCHAR(50) DEFAULT 'Completa',
    observaciones_recepcion TEXT,
    numero_remision VARCHAR(100)
);

-- 82. EVALUACION_PROVEEDORES
CREATE TABLE EVALUACION_PROVEEDORES (
    id_evaluacion SERIAL PRIMARY KEY,
    id_proveedor INTEGER REFERENCES PROVEEDORES(id_proveedor) ON DELETE CASCADE,
    fecha_evaluacion DATE DEFAULT CURRENT_DATE,
    calidad_productos DECIMAL(3,2), -- De 1.00 a 5.00
    tiempo_entrega DECIMAL(3,2),
    servicio_cliente DECIMAL(3,2),
    precios_competitivos DECIMAL(3,2),
    calificacion_general DECIMAL(3,2),
    observaciones_evaluacion TEXT,
    evaluado_por VARCHAR(100)
);

-- =====================================================
-- MÓDULO NÓMINA Y RECURSOS HUMANOS EXTENDIDO (4 TABLAS)
-- =====================================================

-- 83. NOMINA
CREATE TABLE NOMINA (
    id_nomina SERIAL PRIMARY KEY,
    id_empleado INTEGER REFERENCES EMPLEADOS(id_empleado) ON DELETE CASCADE,
    periodo_mes INTEGER NOT NULL,
    periodo_ano INTEGER NOT NULL,
    salario_base DECIMAL(12,2) NOT NULL,
    horas_extras DECIMAL(8,2) DEFAULT 0,
    valor_horas_extras DECIMAL(12,2) DEFAULT 0,
    bonificaciones DECIMAL(12,2) DEFAULT 0,
    deducciones DECIMAL(12,2) DEFAULT 0,
    salario_neto DECIMAL(12,2) NOT NULL,
    fecha_pago DATE,
    estado_nomina VARCHAR(50) DEFAULT 'Calculada',
    observaciones_nomina TEXT
);

-- 84. ASISTENCIA
CREATE TABLE ASISTENCIA (
    id_asistencia SERIAL PRIMARY KEY,
    id_empleado INTEGER REFERENCES EMPLEADOS(id_empleado) ON DELETE CASCADE,
    fecha_asistencia DATE DEFAULT CURRENT_DATE,
    hora_entrada TIME,
    hora_salida TIME,
    horas_trabajadas DECIMAL(4,2),
    tipo_jornada VARCHAR(50) DEFAULT 'Normal', -- Normal, Extra, Festivo
    observaciones_asistencia TEXT,
    registrado_por VARCHAR(100)
);

-- 85. CAPACITACIONES
CREATE TABLE CAPACITACIONES (
    id_capacitacion SERIAL PRIMARY KEY,
    nombre_capacitacion VARCHAR(200) NOT NULL,
    descripcion_capacitacion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    instructor VARCHAR(100),
    costo_capacitacion DECIMAL(12,2),
    estado_capacitacion VARCHAR(50) DEFAULT 'Programada',
    certificacion BOOLEAN DEFAULT FALSE
);

-- 86. EMPLEADO_CAPACITACION
CREATE TABLE EMPLEADO_CAPACITACION (
    id_empleado INTEGER REFERENCES EMPLEADOS(id_empleado) ON DELETE CASCADE,
    id_capacitacion INTEGER REFERENCES CAPACITACIONES(id_capacitacion) ON DELETE CASCADE,
    fecha_inscripcion DATE DEFAULT CURRENT_DATE,
    asistio BOOLEAN DEFAULT FALSE,
    calificacion DECIMAL(4,2),
    certificado BOOLEAN DEFAULT FALSE,
    observaciones TEXT,
    PRIMARY KEY (id_empleado, id_capacitacion)
);

COMMIT;

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

-- Índices para módulo facturación
CREATE INDEX idx_facturas_cliente ON FACTURAS(id_cliente);
CREATE INDEX idx_facturas_fecha ON FACTURAS(fecha_factura);
CREATE INDEX idx_facturas_estado ON FACTURAS(estado_factura);
CREATE INDEX idx_pagos_fecha ON PAGOS(fecha_pago);
CREATE INDEX idx_cuentas_cobrar_vencimiento ON CUENTAS_COBRAR(fecha_vencimiento);

-- Índices para módulo contabilidad
CREATE INDEX idx_movimientos_fecha ON MOVIMIENTOS_CONTABLES(fecha_movimiento);
CREATE INDEX idx_movimientos_cuenta ON MOVIMIENTOS_CONTABLES(id_cuenta);
CREATE INDEX idx_gastos_obra ON GASTOS_OBRA(id_obra);
CREATE INDEX idx_gastos_fecha ON GASTOS_OBRA(fecha_gasto);

-- Índices para módulo mantenimiento
CREATE INDEX idx_mantenimientos_equipo ON MANTENIMIENTOS(id_equipo);
CREATE INDEX idx_mantenimientos_vehiculo ON MANTENIMIENTOS(id_vehiculo);
CREATE INDEX idx_mantenimientos_fecha ON MANTENIMIENTOS(fecha_programada);

-- Índices para módulo compras
CREATE INDEX idx_ordenes_compra_proveedor ON ORDENES_COMPRA(id_proveedor);
CREATE INDEX idx_ordenes_compra_fecha ON ORDENES_COMPRA(fecha_orden);

-- Índices para módulo nómina
CREATE INDEX idx_nomina_empleado ON NOMINA(id_empleado);
CREATE INDEX idx_nomina_periodo ON NOMINA(periodo_ano, periodo_mes);
CREATE INDEX idx_asistencia_empleado_fecha ON ASISTENCIA(id_empleado, fecha_asistencia);

-- =====================================================
-- VERIFICACIÓN FINAL
-- =====================================================

-- Consulta para verificar todas las tablas
SELECT 
    'Total de tablas creadas: ' || COUNT(*) as resumen
FROM information_schema.tables 
WHERE table_schema = 'public';

-- Mostrar tablas por módulo
SELECT 
    CASE 
        WHEN table_name IN ('facturas', 'detalles_factura', 'metodos_pago', 'pagos', 'cuentas_cobrar', 'factura_obra', 'factura_pago', 'descuentos_factura') THEN 'Facturación'
        WHEN table_name IN ('cuentas_contables', 'movimientos_contables', 'centros_costo', 'gastos_obra', 'flujo_caja', 'conciliaciones') THEN 'Contabilidad'
        WHEN table_name IN ('dashboards_personalizados', 'metricas_kpi', 'alertas_sistema', 'configuracion_reportes') THEN 'Reportes'
        WHEN table_name IN ('mantenimientos', 'ordenes_trabajo', 'repuestos', 'historial_mantenimiento') THEN 'Mantenimiento'
        WHEN table_name IN ('ordenes_compra', 'detalles_orden_compra', 'recepciones', 'evaluacion_proveedores') THEN 'Compras'
        WHEN table_name IN ('nomina', 'asistencia', 'capacitaciones', 'empleado_capacitacion') THEN 'Nómina'
        ELSE 'Módulos Base'
    END as modulo,
    COUNT(*) as cantidad_tablas
FROM information_schema.tables 
WHERE table_schema = 'public'
GROUP BY modulo
ORDER BY modulo;