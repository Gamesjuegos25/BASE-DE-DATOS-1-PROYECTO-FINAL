-- =====================================================
-- INSERCIÓN DE DATOS DE EJEMPLO PARA LAS 30 NUEVAS TABLAS
-- Sistema ERP Constructora Completo - 86 Tablas
-- =====================================================

BEGIN;

-- =====================================================
-- DATOS PARA MÓDULO FACTURACIÓN Y PAGOS
-- =====================================================

-- Métodos de Pago
INSERT INTO METODOS_PAGO (nombre_metodo, descripcion, requiere_referencia, activo) VALUES
('Efectivo', 'Pago en efectivo', FALSE, TRUE),
('Transferencia Bancaria', 'Transferencia bancaria nacional', TRUE, TRUE),
('Cheque', 'Pago con cheque', TRUE, TRUE),
('Tarjeta de Crédito', 'Pago con tarjeta de crédito', TRUE, TRUE),
('Tarjeta de Débito', 'Pago con tarjeta de débito', TRUE, TRUE);

-- Facturas (usando clientes existentes)
INSERT INTO FACTURAS (numero_factura, fecha_factura, fecha_vencimiento, subtotal, impuestos, descuento, total, estado_factura, id_cliente, observaciones) VALUES
('FAC-2024-001', '2024-01-15', '2024-02-15', 5000000.00, 950000.00, 0.00, 5950000.00, 'Pagada', 1, 'Factura por obra residencial'),
('FAC-2024-002', '2024-01-20', '2024-02-20', 8500000.00, 1615000.00, 500000.00, 9615000.00, 'Pendiente', 2, 'Factura por edificio comercial'),
('FAC-2024-003', '2024-02-01', '2024-03-01', 3200000.00, 608000.00, 0.00, 3808000.00, 'Pendiente', 3, 'Remodelación de oficinas'),
('FAC-2024-004', '2024-02-10', '2024-03-10', 12000000.00, 2280000.00, 1000000.00, 13280000.00, 'Pendiente', 1, 'Proyecto de infraestructura'),
('FAC-2024-005', '2024-02-15', '2024-03-15', 6750000.00, 1282500.00, 250000.00, 7782500.00, 'Vencida', 4, 'Construcción residencial');

-- Detalles de Factura
INSERT INTO DETALLES_FACTURA (id_factura, concepto, descripcion, cantidad, precio_unitario, subtotal_linea, impuesto_linea, total_linea) VALUES
(1, 'Construcción base', 'Construcción de estructura base', 1.00, 3000000.00, 3000000.00, 570000.00, 3570000.00),
(1, 'Acabados', 'Acabados interiores y exteriores', 1.00, 2000000.00, 2000000.00, 380000.00, 2380000.00),
(2, 'Estructura principal', 'Construcción de estructura principal', 1.00, 6000000.00, 6000000.00, 1140000.00, 7140000.00),
(2, 'Instalaciones', 'Instalaciones eléctricas y sanitarias', 1.00, 2500000.00, 2500000.00, 475000.00, 2975000.00),
(3, 'Remodelación', 'Remodelación completa de espacios', 1.00, 3200000.00, 3200000.00, 608000.00, 3808000.00);

-- Pagos
INSERT INTO PAGOS (numero_recibo, fecha_pago, monto_pago, id_metodo_pago, referencia_pago, observaciones_pago, estado_pago) VALUES
('REC-2024-001', '2024-02-15', 5950000.00, 2, 'TRF-20240215-001', 'Pago completo factura FAC-2024-001', 'Confirmado'),
('REC-2024-002', '2024-02-01', 3000000.00, 1, '', 'Anticipo factura FAC-2024-002', 'Confirmado'),
('REC-2024-003', '2024-02-20', 1500000.00, 3, 'CHE-789456', 'Abono a cuenta factura FAC-2024-004', 'Confirmado');

-- Cuentas por Cobrar
INSERT INTO CUENTAS_COBRAR (id_factura, monto_original, monto_pendiente, fecha_vencimiento, dias_vencido, estado_cobranza) VALUES
(2, 9615000.00, 6615000.00, '2024-02-20', 0, 'Vigente'),
(3, 3808000.00, 3808000.00, '2024-03-01', 0, 'Vigente'),
(4, 13280000.00, 11780000.00, '2024-03-10', 0, 'Vigente'),
(5, 7782500.00, 7782500.00, '2024-03-15', 5, 'Vencida');

-- Relación Factura-Obra
INSERT INTO FACTURA_OBRA (id_factura, id_obra, porcentaje_obra) VALUES
(1, 1, 100.00),
(2, 2, 60.00),
(3, 3, 100.00),
(4, 1, 40.00);

-- Relación Factura-Pago
INSERT INTO FACTURA_PAGO (id_factura, id_pago, monto_aplicado) VALUES
(1, 1, 5950000.00),
(2, 2, 3000000.00),
(4, 3, 1500000.00);

-- =====================================================
-- DATOS PARA MÓDULO CONTABILIDAD AVANZADA
-- =====================================================

-- Cuentas Contables
INSERT INTO CUENTAS_CONTABLES (codigo_cuenta, nombre_cuenta, tipo_cuenta, nivel, cuenta_padre, naturaleza, activa) VALUES
('1', 'ACTIVOS', 'Activo', 1, NULL, 'Débito', TRUE),
('11', 'ACTIVO CORRIENTE', 'Activo', 2, 1, 'Débito', TRUE),
('1105', 'Caja', 'Activo', 3, 2, 'Débito', TRUE),
('1110', 'Bancos', 'Activo', 3, 2, 'Débito', TRUE),
('1305', 'Clientes', 'Activo', 3, 2, 'Débito', TRUE),
('2', 'PASIVOS', 'Pasivo', 1, NULL, 'Crédito', TRUE),
('21', 'PASIVO CORRIENTE', 'Pasivo', 2, 6, 'Crédito', TRUE),
('2205', 'Proveedores', 'Pasivo', 3, 7, 'Crédito', TRUE),
('4', 'INGRESOS', 'Ingreso', 1, NULL, 'Crédito', TRUE),
('4135', 'Ingresos por Construcción', 'Ingreso', 2, 9, 'Crédito', TRUE);

-- Centros de Costo
INSERT INTO CENTROS_COSTO (codigo_centro, nombre_centro, descripcion, tipo_centro, activo) VALUES
('CC001', 'Obra Residencial Norte', 'Centro de costo para obras residenciales zona norte', 'Obra', TRUE),
('CC002', 'Obra Comercial Centro', 'Centro de costo para obras comerciales centro', 'Obra', TRUE),
('CC003', 'Administración General', 'Gastos administrativos generales', 'Administrativo', TRUE),
('CC004', 'Departamento Comercial', 'Gastos del departamento comercial', 'Comercial', TRUE),
('CC005', 'Mantenimiento General', 'Gastos de mantenimiento general', 'Administrativo', TRUE);

-- Movimientos Contables
INSERT INTO MOVIMIENTOS_CONTABLES (numero_asiento, fecha_movimiento, id_cuenta, debe, haber, concepto, documento_soporte, id_obra) VALUES
('ASI-001', '2024-01-15', 3, 5950000.00, 0.00, 'Pago recibido factura FAC-2024-001', 'FAC-2024-001', 1),
('ASI-001', '2024-01-15', 10, 0.00, 5950000.00, 'Pago recibido factura FAC-2024-001', 'FAC-2024-001', 1),
('ASI-002', '2024-02-01', 4, 9615000.00, 0.00, 'Facturación obra comercial', 'FAC-2024-002', 2),
('ASI-002', '2024-02-01', 10, 0.00, 9615000.00, 'Facturación obra comercial', 'FAC-2024-002', 2);

-- Gastos por Obra
INSERT INTO GASTOS_OBRA (id_obra, id_centro_costo, fecha_gasto, concepto_gasto, descripcion_gasto, monto_gasto, tipo_gasto, documento_soporte, aprobado_por) VALUES
(1, 1, '2024-01-10', 'Materiales de construcción', 'Cemento, varillas, blocks', 2500000.00, 'Material', 'COMP-001', 'Juan Pérez'),
(1, 1, '2024-01-15', 'Mano de obra', 'Pago albañiles semana 1', 1800000.00, 'Mano de Obra', 'NOM-001', 'Juan Pérez'),
(2, 2, '2024-01-20', 'Alquiler de equipo', 'Grúa torre por 1 mes', 3200000.00, 'Equipo', 'ALQ-001', 'María García'),
(2, 2, '2024-01-25', 'Materiales especializados', 'Estructuras metálicas', 4500000.00, 'Material', 'COMP-002', 'María García');

-- Flujo de Caja
INSERT INTO FLUJO_CAJA (fecha_flujo, tipo_movimiento, concepto, monto, saldo_anterior, saldo_actual, categoria, referencia_documento) VALUES
('2024-01-01', 'Ingreso', 'Saldo inicial', 10000000.00, 0.00, 10000000.00, 'Inicial', 'SALDO-INI'),
('2024-01-15', 'Ingreso', 'Cobro factura FAC-2024-001', 5950000.00, 10000000.00, 15950000.00, 'Ventas', 'FAC-2024-001'),
('2024-01-20', 'Egreso', 'Compra materiales', 2500000.00, 15950000.00, 13450000.00, 'Compras', 'COMP-001'),
('2024-02-01', 'Ingreso', 'Anticipo obra comercial', 3000000.00, 13450000.00, 16450000.00, 'Ventas', 'FAC-2024-002'),
('2024-02-05', 'Egreso', 'Pago nómina enero', 8500000.00, 16450000.00, 7950000.00, 'Nómina', 'NOM-ENE-2024');

-- =====================================================
-- DATOS PARA MÓDULO MANTENIMIENTO
-- =====================================================

-- Repuestos
INSERT INTO REPUESTOS (codigo_repuesto, nombre_repuesto, descripcion_repuesto, marca, modelo, precio_unitario, stock_minimo, stock_actual, ubicacion_bodega, activo) VALUES
('REP-001', 'Filtro de aceite', 'Filtro de aceite para maquinaria pesada', 'CATERPILLAR', 'CAT-1R-0750', 85000.00, 5, 12, 'BODEGA-A-EST-1', TRUE),
('REP-002', 'Correa de transmisión', 'Correa para sistema de transmisión', 'GATES', 'GT-4568', 120000.00, 3, 8, 'BODEGA-A-EST-2', TRUE),
('REP-003', 'Pastillas de freno', 'Pastillas de freno vehículos pesados', 'BENDIX', 'BX-789', 95000.00, 4, 2, 'BODEGA-B-EST-1', TRUE),
('REP-004', 'Aceite hidráulico', 'Aceite hidráulico ISO 46', 'SHELL', 'TELLUS-46', 45000.00, 10, 15, 'BODEGA-A-EST-3', TRUE),
('REP-005', 'Bujías', 'Bujías para motor diésel', 'NGK', 'D-POWER-48', 25000.00, 8, 20, 'BODEGA-B-EST-2', TRUE);

-- Mantenimientos (usando equipos y vehículos existentes)
INSERT INTO MANTENIMIENTOS (id_equipo, id_vehiculo, tipo_mantenimiento, descripcion_mantenimiento, fecha_programada, fecha_realizada, costo_estimado, costo_real, estado_mantenimiento, observaciones, responsable_mantenimiento) VALUES
(1, NULL, 'Preventivo', 'Cambio de aceite y filtros', '2024-03-01', NULL, 350000.00, NULL, 'Programado', 'Mantenimiento rutinario según horas de uso', 'Carlos Méndez'),
(2, NULL, 'Correctivo', 'Reparación sistema hidráulico', '2024-02-20', '2024-02-22', 800000.00, 920000.00, 'Realizado', 'Fuga en cilindro hidráulico principal', 'Ana López'),
(NULL, 1, 'Preventivo', 'Revisión general y cambio de llantas', '2024-03-05', NULL, 450000.00, NULL, 'Programado', 'Mantenimiento cada 10,000 km', 'Pedro Rodríguez'),
(3, NULL, 'Predictivo', 'Análisis de vibraciones', '2024-02-28', NULL, 200000.00, NULL, 'Programado', 'Análisis preventivo de componentes', 'Luis Herrera'),
(NULL, 2, 'Correctivo', 'Reparación sistema eléctrico', '2024-02-15', '2024-02-16', 300000.00, 285000.00, 'Realizado', 'Falla en alternador', 'María Fernández');

-- Órdenes de Trabajo
INSERT INTO ORDENES_TRABAJO (numero_orden, id_mantenimiento, fecha_creacion, fecha_inicio, fecha_fin, prioridad, estado_orden, descripcion_trabajo, asignado_a, tiempo_estimado, tiempo_real) VALUES
('OT-2024-001', 1, '2024-02-25', NULL, NULL, 'Media', 'Creada', 'Cambio de aceite, filtro aire y filtro combustible', 'Carlos Méndez', 4, NULL),
('OT-2024-002', 2, '2024-02-18', '2024-02-20', '2024-02-22', 'Alta', 'Finalizada', 'Desmonte y reparación cilindro hidráulico', 'Ana López', 12, 14),
('OT-2024-003', 3, '2024-02-28', NULL, NULL, 'Media', 'Creada', 'Inspección general y cambio de neumáticos', 'Pedro Rodríguez', 6, NULL),
('OT-2024-004', 4, '2024-02-26', NULL, NULL, 'Baja', 'Creada', 'Medición de vibraciones en puntos críticos', 'Luis Herrera', 3, NULL),
('OT-2024-005', 5, '2024-02-14', '2024-02-15', '2024-02-16', 'Alta', 'Finalizada', 'Reemplazo de alternador y revisión sistema', 'María Fernández', 8, 7);

-- Historial de Mantenimiento
INSERT INTO HISTORIAL_MANTENIMIENTO (id_mantenimiento, fecha_evento, tipo_evento, descripcion_evento, usuario_evento, costo_evento, observaciones_evento) VALUES
(2, '2024-02-20 08:00:00', 'Inicio', 'Inicio de reparación sistema hidráulico', 'Ana López', 0.00, 'Equipo trasladado a taller'),
(2, '2024-02-21 14:30:00', 'Pausa', 'Pausa por espera de repuesto', 'Ana López', 0.00, 'Esperando cilindro de repuesto'),
(2, '2024-02-22 09:00:00', 'Reanudación', 'Continúa reparación con repuesto', 'Ana López', 520000.00, 'Repuesto instalado'),
(2, '2024-02-22 17:00:00', 'Finalización', 'Mantenimiento completado exitosamente', 'Ana López', 400000.00, 'Equipo probado y operativo'),
(5, '2024-02-15 10:00:00', 'Inicio', 'Inicio reparación sistema eléctrico', 'María Fernández', 0.00, 'Diagnóstico inicial completado');

-- =====================================================
-- DATOS PARA MÓDULO COMPRAS EXTENDIDO
-- =====================================================

-- Órdenes de Compra (usando proveedores existentes)
INSERT INTO ORDENES_COMPRA (numero_orden, id_proveedor, fecha_orden, fecha_entrega_solicitada, fecha_entrega_real, subtotal, impuestos, total, estado_orden, observaciones, aprobada_por) VALUES
('OC-2024-001', 1, '2024-01-15', '2024-01-25', '2024-01-24', 2500000.00, 475000.00, 2975000.00, 'Entregada', 'Materiales para obra residencial', 'Juan Pérez'),
('OC-2024-002', 2, '2024-01-20', '2024-02-05', NULL, 1800000.00, 342000.00, 2142000.00, 'Pendiente', 'Herramientas especializadas', 'María García'),
('OC-2024-003', 3, '2024-02-01', '2024-02-15', '2024-02-14', 950000.00, 180500.00, 1130500.00, 'Entregada', 'Repuestos para mantenimiento', 'Carlos Méndez'),
('OC-2024-004', 1, '2024-02-10', '2024-02-28', NULL, 3200000.00, 608000.00, 3808000.00, 'Aprobada', 'Materiales estructurales especiales', 'Juan Pérez'),
('OC-2024-005', 4, '2024-02-15', '2024-03-01', NULL, 1250000.00, 237500.00, 1487500.00, 'Pendiente', 'Equipos de seguridad', 'Ana López');

-- Detalles de Orden de Compra
INSERT INTO DETALLES_ORDEN_COMPRA (id_orden_compra, id_material, id_repuesto, cantidad_solicitada, cantidad_recibida, precio_unitario, subtotal_linea) VALUES
(1, 1, NULL, 50.00, 50.00, 35000.00, 1750000.00),
(1, 2, NULL, 25.00, 25.00, 30000.00, 750000.00),
(2, 3, NULL, 15.00, 0.00, 120000.00, 1800000.00),
(3, NULL, 1, 10.00, 10.00, 85000.00, 850000.00),
(3, NULL, 2, 1.00, 1.00, 100000.00, 100000.00),
(4, 1, NULL, 80.00, 0.00, 40000.00, 3200000.00);

-- Recepciones
INSERT INTO RECEPCIONES (id_orden_compra, numero_recepcion, fecha_recepcion, recibido_por, estado_recepcion, observaciones_recepcion, numero_remision) VALUES
(1, 'REC-2024-001', '2024-01-24', 'Pedro Rodríguez', 'Completa', 'Todos los materiales recibidos en buen estado', 'REM-5847'),
(3, 'REC-2024-002', '2024-02-14', 'Carlos Méndez', 'Completa', 'Repuestos verificados y almacenados', 'REM-5963'),
(2, 'REC-2024-003', '2024-02-05', 'Ana López', 'Parcial', 'Recibido 10 de 15 herramientas solicitadas', 'REM-6024');

-- Evaluación de Proveedores
INSERT INTO EVALUACION_PROVEEDORES (id_proveedor, fecha_evaluacion, calidad_productos, tiempo_entrega, servicio_cliente, precios_competitivos, calificacion_general, observaciones_evaluacion, evaluado_por) VALUES
(1, '2024-01-31', 4.5, 4.8, 4.2, 4.0, 4.4, 'Excelente calidad y puntualidad en entregas', 'Juan Pérez'),
(2, '2024-02-05', 4.0, 3.5, 4.5, 3.8, 3.9, 'Buena calidad pero demoras en entregas', 'María García'),
(3, '2024-02-20', 4.8, 4.9, 4.7, 4.3, 4.7, 'Proveedor muy confiable para repuestos', 'Carlos Méndez'),
(4, '2024-02-28', 4.2, 4.0, 4.0, 4.5, 4.2, 'Buenos precios, calidad aceptable', 'Ana López');

-- =====================================================
-- DATOS PARA MÓDULO NÓMINA EXTENDIDO
-- =====================================================

-- Nómina (usando empleados existentes)
INSERT INTO NOMINA (id_empleado, periodo_mes, periodo_ano, salario_base, horas_extras, valor_horas_extras, bonificaciones, deducciones, salario_neto, fecha_pago, estado_nomina, observaciones_nomina) VALUES
(1, 1, 2024, 3500000.00, 10.00, 250000.00, 200000.00, 890000.00, 3060000.00, '2024-02-01', 'Pagada', 'Nómina enero 2024'),
(2, 1, 2024, 2800000.00, 5.00, 150000.00, 0.00, 680000.00, 2270000.00, '2024-02-01', 'Pagada', 'Nómina enero 2024'),
(3, 1, 2024, 1800000.00, 15.00, 180000.00, 100000.00, 420000.00, 1660000.00, '2024-02-01', 'Pagada', 'Nómina enero 2024'),
(1, 2, 2024, 3500000.00, 8.00, 200000.00, 150000.00, 890000.00, 2960000.00, NULL, 'Calculada', 'Nómina febrero 2024'),
(2, 2, 2024, 2800000.00, 12.00, 300000.00, 200000.00, 680000.00, 2620000.00, NULL, 'Calculada', 'Nómina febrero 2024');

-- Asistencia
INSERT INTO ASISTENCIA (id_empleado, fecha_asistencia, hora_entrada, hora_salida, horas_trabajadas, tipo_jornada, observaciones_asistencia, registrado_por) VALUES
(1, '2024-02-19', '07:30:00', '17:30:00', 9.00, 'Normal', 'Jornada completa', 'Sistema'),
(1, '2024-02-20', '07:45:00', '19:00:00', 10.25, 'Extra', 'Horas extras por urgencia en obra', 'Juan Pérez'),
(2, '2024-02-19', '08:00:00', '17:00:00', 8.00, 'Normal', 'Jornada normal', 'Sistema'),
(2, '2024-02-20', '08:00:00', '20:00:00', 11.00, 'Extra', 'Supervisión nocturna', 'María García'),
(3, '2024-02-19', '06:00:00', '15:00:00', 8.00, 'Normal', 'Turno madrugada', 'Sistema'),
(3, '2024-02-20', '06:00:00', '18:00:00', 11.00, 'Extra', 'Trabajo adicional fines de semana', 'Pedro Rodríguez');

-- Capacitaciones
INSERT INTO CAPACITACIONES (nombre_capacitacion, descripcion_capacitacion, fecha_inicio, fecha_fin, instructor, costo_capacitacion, estado_capacitacion, certificacion) VALUES
('Seguridad Industrial', 'Capacitación en normas de seguridad para construcción', '2024-03-01', '2024-03-03', 'Ing. Roberto Silva', 1500000.00, 'Programada', TRUE),
('Manejo de Equipos Pesados', 'Certificación para operación de maquinaria pesada', '2024-03-15', '2024-03-20', 'Téc. Fernando López', 2800000.00, 'Programada', TRUE),
('Primeros Auxilios', 'Curso básico de primeros auxilios en obra', '2024-02-25', '2024-02-26', 'Dr. Sandra Ruiz', 800000.00, 'En Curso', TRUE),
('Soldadura Especializada', 'Técnicas avanzadas de soldadura estructural', '2024-04-01', '2024-04-10', 'Mst. Carlos Vargas', 3200000.00, 'Programada', TRUE),
('Gestión de Proyectos', 'Metodologías para gestión eficiente de proyectos', '2024-03-10', '2024-03-12', 'Ing. Patricia Morales', 1800000.00, 'Programada', FALSE);

-- Empleado-Capacitación
INSERT INTO EMPLEADO_CAPACITACION (id_empleado, id_capacitacion, fecha_inscripcion, asistio, calificacion, certificado, observaciones) VALUES
(1, 3, '2024-02-20', TRUE, 4.5, FALSE, 'Participación activa en el curso'),
(2, 3, '2024-02-20', TRUE, 4.8, FALSE, 'Excelente desempeño en prácticas'),
(3, 3, '2024-02-20', FALSE, NULL, FALSE, 'No pudo asistir por trabajo en obra'),
(1, 1, '2024-02-25', FALSE, NULL, FALSE, 'Inscrito para próxima capacitación'),
(2, 2, '2024-02-28', FALSE, NULL, FALSE, 'Pre-inscrito para certificación'),
(3, 2, '2024-02-28', FALSE, NULL, FALSE, 'Requiere esta certificación para su cargo');

-- =====================================================
-- DATOS PARA MÓDULO REPORTES AVANZADOS
-- =====================================================

-- Métricas KPI
INSERT INTO METRICAS_KPI (nombre_metrica, descripcion, formula_calculo, valor_actual, valor_objetivo, unidad_medida, frecuencia_actualizacion, categoria_kpi) VALUES
('Rentabilidad de Proyectos', 'Porcentaje de rentabilidad promedio de proyectos', '(Ingresos - Costos) / Ingresos * 100', 18.5, 20.0, 'Porcentaje', 'Mensual', 'Financiero'),
('Tiempo Promedio de Obra', 'Días promedio para completar una obra', 'SUM(días_proyecto) / COUNT(proyectos)', 85.0, 75.0, 'Días', 'Mensual', 'Operacional'),
('Satisfacción Cliente', 'Calificación promedio de satisfacción', 'AVG(calificaciones_cliente)', 4.3, 4.5, 'Escala 1-5', 'Trimestral', 'Calidad'),
('Eficiencia Equipos', 'Porcentaje de tiempo operativo de equipos', 'Tiempo_operativo / Tiempo_disponible * 100', 78.5, 85.0, 'Porcentaje', 'Semanal', 'Operacional'),
('Rotación Personal', 'Porcentaje anual de rotación de personal', 'Empleados_que_salen / Total_empleados * 100', 12.0, 8.0, 'Porcentaje', 'Mensual', 'RRHH'),
('Cumplimiento Entregas', 'Porcentaje de obras entregadas a tiempo', 'Obras_a_tiempo / Total_obras * 100', 88.0, 95.0, 'Porcentaje', 'Mensual', 'Operacional');

-- Alertas del Sistema
INSERT INTO ALERTAS_SISTEMA (tipo_alerta, titulo_alerta, mensaje_alerta, nivel_prioridad, fecha_creacion, fecha_vencimiento, leida, id_usuario_destinatario, referencia_tabla, referencia_id) VALUES
('Mantenimiento', 'Mantenimiento Vencido', 'El equipo Excavadora CAT 320D tiene mantenimiento vencido desde hace 5 días', 'Alta', '2024-02-20 10:30:00', '2024-02-25 23:59:59', FALSE, 1, 'EQUIPOS', 1),
('Facturación', 'Factura Vencida', 'La factura FAC-2024-005 está vencida por $7,782,500', 'Crítica', '2024-02-20 09:00:00', '2024-02-28 23:59:59', FALSE, 1, 'FACTURAS', 5),
('Inventario', 'Stock Bajo', 'El repuesto "Pastillas de freno" tiene stock bajo (2 unidades)', 'Media', '2024-02-19 14:20:00', '2024-02-25 23:59:59', FALSE, 1, 'REPUESTOS', 3),
('Seguridad', 'Capacitación Pendiente', 'El empleado Juan Pérez tiene capacitación de seguridad pendiente', 'Media', '2024-02-18 16:45:00', '2024-03-01 23:59:59', TRUE, 1, 'EMPLEADOS', 1),
('Proyecto', 'Retraso en Obra', 'La obra "Edificio Comercial Plaza Norte" presenta retraso de 10 días', 'Alta', '2024-02-17 11:00:00', '2024-02-22 23:59:59', FALSE, 1, 'OBRAS', 2);

-- Configuración de Reportes
INSERT INTO CONFIGURACION_REPORTES (nombre_reporte, descripcion_reporte, consulta_sql, parametros_json, formato_salida, programado, frecuencia_programacion, activo, creado_por) VALUES
('Reporte Financiero Mensual', 'Resumen financiero mensual con ingresos y gastos', 'SELECT * FROM vista_financiera_mensual WHERE mes = ?', '{"mes": "int", "año": "int"}', 'PDF', TRUE, 'Mensual', TRUE, 1),
('Estado de Obras', 'Reporte del estado actual de todas las obras', 'SELECT * FROM OBRAS WHERE estado IN (?)', '{"estados": "array"}', 'Excel', FALSE, NULL, TRUE, 1),
('Inventario Crítico', 'Materiales y repuestos con stock bajo', 'SELECT * FROM vista_inventario_critico', '{}', 'HTML', TRUE, 'Semanal', TRUE, 1),
('Productividad Empleados', 'Reporte de productividad por empleado', 'SELECT * FROM vista_productividad_empleados WHERE periodo = ?', '{"periodo": "string"}', 'PDF', TRUE, 'Mensual', TRUE, 1),
('Análisis de Rentabilidad', 'Análisis detallado de rentabilidad por proyecto', 'SELECT * FROM vista_rentabilidad_proyectos WHERE fecha_inicio >= ?', '{"fecha_inicio": "date", "fecha_fin": "date"}', 'Excel', FALSE, NULL, TRUE, 1);

-- Dashboards Personalizados
INSERT INTO DASHBOARDS_PERSONALIZADOS (id_usuario, nombre_dashboard, configuracion_json, es_publico, fecha_creacion) VALUES
(1, 'Dashboard Gerencial', '{"widgets": [{"tipo": "kpi", "titulo": "Ingresos Mes", "valor": "facturacion_mes"}, {"tipo": "grafico", "titulo": "Obras por Estado", "datos": "obras_estado"}], "layout": "2x2"}', TRUE, '2024-02-15 10:00:00'),
(1, 'Control de Obra', '{"widgets": [{"tipo": "tabla", "titulo": "Obras Activas", "datos": "obras_activas"}, {"tipo": "alerta", "titulo": "Alertas Críticas", "filtro": "criticas"}], "layout": "2x1"}', FALSE, '2024-02-18 14:30:00');

COMMIT;

-- =====================================================
-- VERIFICACIÓN DE DATOS INSERTADOS
-- =====================================================

-- Resumen de registros insertados por módulo
SELECT 'FACTURACIÓN' as modulo, 
       (SELECT COUNT(*) FROM FACTURAS) as facturas,
       (SELECT COUNT(*) FROM PAGOS) as pagos,
       (SELECT COUNT(*) FROM METODOS_PAGO) as metodos_pago
UNION ALL
SELECT 'CONTABILIDAD' as modulo,
       (SELECT COUNT(*) FROM CUENTAS_CONTABLES) as cuentas,
       (SELECT COUNT(*) FROM MOVIMIENTOS_CONTABLES) as movimientos,
       (SELECT COUNT(*) FROM GASTOS_OBRA) as gastos_obra
UNION ALL
SELECT 'MANTENIMIENTO' as modulo,
       (SELECT COUNT(*) FROM MANTENIMIENTOS) as mantenimientos,
       (SELECT COUNT(*) FROM REPUESTOS) as repuestos,
       (SELECT COUNT(*) FROM ORDENES_TRABAJO) as ordenes_trabajo
UNION ALL
SELECT 'COMPRAS' as modulo,
       (SELECT COUNT(*) FROM ORDENES_COMPRA) as ordenes_compra,
       (SELECT COUNT(*) FROM RECEPCIONES) as recepciones,
       (SELECT COUNT(*) FROM EVALUACION_PROVEEDORES) as evaluaciones
UNION ALL
SELECT 'NÓMINA' as modulo,
       (SELECT COUNT(*) FROM NOMINA) as nomina,
       (SELECT COUNT(*) FROM ASISTENCIA) as asistencia,
       (SELECT COUNT(*) FROM CAPACITACIONES) as capacitaciones
UNION ALL
SELECT 'REPORTES' as modulo,
       (SELECT COUNT(*) FROM METRICAS_KPI) as metricas_kpi,
       (SELECT COUNT(*) FROM ALERTAS_SISTEMA) as alertas,
       (SELECT COUNT(*) FROM CONFIGURACION_REPORTES) as config_reportes;