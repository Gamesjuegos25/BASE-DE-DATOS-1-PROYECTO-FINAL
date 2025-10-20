-- =================================================================
-- QUERIES PARA EXTRAER DATOS DEL SISTEMA DE CONSTRUCTORA
-- =================================================================
-- Este archivo contiene todas las consultas SELECT necesarias para
-- extraer los datos desde la base de datos y mostrarlos en el sistema web
-- =================================================================

USE BASEdeDATOSpf;

-- =================================================================
-- 1. CONSULTAS PARA EL DASHBOARD
-- =================================================================

-- Estadísticas generales para el dashboard
SELECT 
    (SELECT COUNT(*) FROM Obra WHERE estado = 'En Proceso') AS obras_activas,
    (SELECT COUNT(*) FROM Empleado WHERE estado = 'Activo') AS empleados_activos,
    (SELECT COUNT(*) FROM Material) AS total_materiales,
    (SELECT COUNT(*) FROM Proveedor) AS total_proveedores,
    (SELECT ISNULL(SUM(monto), 0) FROM FacturaProveedor) AS gastos_totales,
    (SELECT ISNULL(SUM(monto), 0) FROM PagoEmpleado WHERE estado = 'Pagado') AS pagos_realizados;

-- Obras recientes para dashboard
SELECT TOP 3 
    o.id_obra,
    o.nombre,
    o.ubicacion,
    o.estado,
    c.nombre AS cliente_nombre
FROM Obra o
LEFT JOIN Cliente c ON o.id_cliente = c.id_cliente
ORDER BY o.id_obra DESC;

-- =================================================================
-- 2. CONSULTA COMPLETA DE OBRAS
-- =================================================================
SELECT 
    o.id_obra,
    o.nombre,
    o.ubicacion,
    o.tipo,
    o.estado,
    c.nombre AS cliente_nombre,
    c.contacto AS cliente_contacto,
    p.monto_estimado AS presupuesto,
    a.porcentaje_fisico,
    a.porcentaje_financiero,
    o.id_cliente
FROM Obra o
LEFT JOIN Cliente c ON o.id_cliente = c.id_cliente
LEFT JOIN PresupuestoObra p ON o.id_obra = p.id_obra
LEFT JOIN AvanceObra a ON o.id_obra = a.id_obra
ORDER BY o.id_obra;

-- =================================================================
-- 3. CONSULTA COMPLETA DE EMPLEADOS
-- =================================================================
SELECT 
    e.id_empleado,
    e.nombre,
    e.tipo,
    e.salario_fijo,
    e.estado,
    COUNT(DISTINCT c.id_contrato) AS proyectos_asignados,
    (SELECT TOP 1 fecha FROM PagoEmpleado WHERE id_empleado = e.id_empleado ORDER BY fecha DESC) AS ultimo_pago,
    (SELECT TOP 1 monto FROM PagoEmpleado WHERE id_empleado = e.id_empleado ORDER BY fecha DESC) AS ultimo_monto
FROM Empleado e
LEFT JOIN Contrato c ON e.id_empleado = c.id_empleado AND c.estado = 'Activo'
GROUP BY e.id_empleado, e.nombre, e.tipo, e.salario_fijo, e.estado
ORDER BY e.id_empleado;

-- =================================================================
-- 4. CONSULTA COMPLETA DE MATERIALES
-- =================================================================
SELECT 
    m.id_material,
    m.nombre,
    m.unidad,
    m.precio_unitario,
    m.tipo_material,
    m.estado,
    p.nombre AS proveedor_nombre,
    p.contacto AS proveedor_contacto,
    ISNULL(SUM(i.cantidad), 0) AS stock_total
FROM Material m
LEFT JOIN Proveedor p ON m.id_proveedor = p.id_proveedor
LEFT JOIN Inventario i ON m.id_material = i.id_material
GROUP BY m.id_material, m.nombre, m.unidad, m.precio_unitario, m.tipo_material, m.estado, p.nombre, p.contacto
ORDER BY m.id_material;

-- =================================================================
-- 5. CONSULTA COMPLETA DE PROVEEDORES
-- =================================================================
SELECT 
    p.id_proveedor,
    p.nombre,
    p.contacto,
    COUNT(DISTINCT m.id_material) AS materiales_suministrados,
    ISNULL(SUM(f.monto), 0) AS total_facturas,
    'Activo' AS estado
FROM Proveedor p
LEFT JOIN Material m ON p.id_proveedor = m.id_proveedor
LEFT JOIN FacturaProveedor f ON p.id_proveedor = f.id_proveedor
GROUP BY p.id_proveedor, p.nombre, p.contacto
ORDER BY p.id_proveedor;

-- =================================================================
-- 6. CONSULTA COMPLETA DE INVENTARIO
-- =================================================================
SELECT 
    i.id_inventario,
    b.id_bodega,
    o.nombre AS obra_nombre,
    m.nombre AS material_nombre,
    i.cantidad,
    m.unidad,
    m.precio_unitario,
    (i.cantidad * m.precio_unitario) AS valor_total,
    b.responsable,
    m.estado
FROM Inventario i
JOIN Bodega b ON i.id_bodega = b.id_bodega
JOIN Obra o ON b.id_obra = o.id_obra
JOIN Material m ON i.id_material = m.id_material
ORDER BY b.id_bodega, m.nombre;

-- =================================================================
-- 7. CONSULTA COMPLETA DE PROYECTOS
-- =================================================================
SELECT 
    pr.id_proyecto,
    pr.nombre,
    o.nombre AS obra_nombre,
    pr.fecha_inicio,
    pr.fecha_fin,
    pr.estado,
    -- Calcular avance basado en actividades completadas
    CASE 
        WHEN COUNT(a.id_actividad) > 0 THEN 
            (COUNT(CASE WHEN a.estado = 'Completado' THEN 1 END) * 100.0 / COUNT(a.id_actividad))
        ELSE 0 
    END AS avance,
    COUNT(a.id_actividad) AS total_actividades
FROM Proyecto pr
LEFT JOIN Obra o ON pr.id_obra = o.id_obra
LEFT JOIN Area ar ON o.id_obra = ar.id_obra
LEFT JOIN Actividad a ON ar.id_area = a.id_area
GROUP BY pr.id_proyecto, pr.nombre, o.nombre, pr.fecha_inicio, pr.fecha_fin, pr.estado
ORDER BY pr.id_proyecto;

-- =================================================================
-- 8. CONSULTAS PARA REPORTES
-- =================================================================

-- Reportes semanales
SELECT 
    r.id_reporte,
    r.semana,
    o.nombre AS obra_nombre,
    r.fecha,
    r.resumen
FROM ReporteSemanal r
JOIN Obra o ON r.id_obra = o.id_obra
ORDER BY r.fecha DESC;

-- Reporte de gastos (facturas de proveedores)
SELECT 
    f.id_factura,
    p.nombre AS proveedor_nombre,
    f.fecha,
    f.monto,
    f.estado,
    'F-' + RIGHT('000' + CAST(f.id_factura AS VARCHAR), 3) + '-2024' AS numero_factura
FROM FacturaProveedor f
JOIN Proveedor p ON f.id_proveedor = p.id_proveedor
ORDER BY f.fecha DESC;

-- Reporte de uso de materiales
SELECT 
    m.nombre AS material_nombre,
    mov.tipo,
    mov.cantidad,
    m.unidad,
    mov.origen,
    mov.destino,
    mov.fecha
FROM MovimientoMaterial mov
JOIN Material m ON mov.id_material = m.id_material
ORDER BY mov.fecha DESC;

-- Reporte de pagos a empleados
SELECT 
    e.nombre AS empleado_nombre,
    CASE 
        WHEN e.salario_fijo > 0 THEN 'Salario Fijo'
        ELSE 'Por Trabajo'
    END AS tipo_pago,
    p.fecha,
    p.monto,
    p.estado
FROM PagoEmpleado p
JOIN Empleado e ON p.id_empleado = e.id_empleado
ORDER BY p.fecha DESC;

-- =================================================================
-- 9. CONSULTA COMPLETA DE VEHÍCULOS
-- =================================================================
SELECT 
    v.id_vehiculo,
    v.placa,
    v.tipo,
    v.estado,
    o.nombre AS obra_asignada,
    o.ubicacion AS ubicacion_actual
FROM Vehiculo v
LEFT JOIN Obra o ON v.id_obra = o.id_obra
ORDER BY v.id_vehiculo;

-- =================================================================
-- 10. CONSULTA COMPLETA DE EQUIPOS
-- =================================================================
SELECT 
    eq.id_equipo,
    eq.nombre,
    eq.tipo,
    eq.estado,
    e.nombre AS empleado_asignado,
    ae.fecha_inicio AS fecha_asignacion,
    ae.fecha_fin
FROM Equipo eq
LEFT JOIN AsignacionEquipo ae ON eq.id_equipo = ae.id_equipo
LEFT JOIN Empleado e ON ae.id_empleado = e.id_empleado
ORDER BY eq.id_equipo;

-- =================================================================
-- 11. CONSULTAS ESPECÍFICAS PARA FILTROS
-- =================================================================

-- Lista de bodegas para filtro
SELECT 
    b.id_bodega,
    'Bodega ' + CAST(b.id_bodega AS VARCHAR) + ' - ' + o.nombre AS bodega_descripcion
FROM Bodega b
JOIN Obra o ON b.id_obra = o.id_obra
ORDER BY b.id_bodega;

-- Lista de obras para filtro de reportes
SELECT 
    id_obra,
    nombre
FROM Obra
ORDER BY nombre;

-- =================================================================
-- 12. CONSULTAS PARA DETALLES ESPECÍFICOS
-- =================================================================

-- Detalle completo de una obra específica
-- (Usar con parámetro @id_obra)
/*
DECLARE @id_obra INT = 1;

SELECT 
    o.id_obra,
    o.nombre,
    o.ubicacion,
    o.tipo,
    o.estado,
    c.nombre AS cliente_nombre,
    c.contacto AS cliente_contacto,
    c.tipo_cliente,
    p.monto_estimado,
    p.fecha AS fecha_presupuesto,
    a.porcentaje_fisico,
    a.porcentaje_financiero,
    a.fecha AS fecha_ultimo_avance
FROM Obra o
LEFT JOIN Cliente c ON o.id_cliente = c.id_cliente
LEFT JOIN PresupuestoObra p ON o.id_obra = p.id_obra
LEFT JOIN AvanceObra a ON o.id_obra = a.id_obra
WHERE o.id_obra = @id_obra;
*/

-- Materiales de un proveedor específico
-- (Usar con parámetro @id_proveedor)
/*
DECLARE @id_proveedor INT = 1;

SELECT 
    m.nombre,
    m.unidad,
    m.precio_unitario,
    m.tipo_material,
    m.estado
FROM Material m
WHERE m.id_proveedor = @id_proveedor
ORDER BY m.nombre;
*/

-- =================================================================
-- 13. CONSULTAS PARA ESTADÍSTICAS AVANZADAS
-- =================================================================

-- Resumen financiero por obra
SELECT 
    o.nombre AS obra_nombre,
    p.monto_estimado AS presupuesto,
    ISNULL(SUM(fp.monto), 0) AS gastos_materiales,
    ISNULL(SUM(pe.monto), 0) AS gastos_personal,
    (p.monto_estimado - ISNULL(SUM(fp.monto), 0) - ISNULL(SUM(pe.monto), 0)) AS saldo_disponible
FROM Obra o
LEFT JOIN PresupuestoObra p ON o.id_obra = p.id_obra
LEFT JOIN Bodega b ON o.id_obra = b.id_obra
LEFT JOIN Inventario i ON b.id_bodega = i.id_bodega
LEFT JOIN Material m ON i.id_material = m.id_material
LEFT JOIN FacturaProveedor fp ON m.id_proveedor = fp.id_proveedor
LEFT JOIN Area ar ON o.id_obra = ar.id_obra
LEFT JOIN Contrato c ON ar.id_area = c.id_area
LEFT JOIN PagoEmpleado pe ON c.id_empleado = pe.id_empleado
GROUP BY o.nombre, p.monto_estimado
ORDER BY o.nombre;

-- Productividad por empleado
SELECT 
    e.nombre,
    e.tipo,
    COUNT(DISTINCT c.id_contrato) AS contratos_activos,
    COUNT(DISTINCT dt.id_detalle) AS trabajos_realizados,
    ISNULL(SUM(dt.total), 0) AS ingresos_por_trabajo,
    ISNULL(SUM(pe.monto), 0) AS total_pagado
FROM Empleado e
LEFT JOIN Contrato c ON e.id_empleado = c.id_empleado
LEFT JOIN DetalleTrabajo dt ON c.id_contrato = dt.id_contrato
LEFT JOIN PagoEmpleado pe ON e.id_empleado = pe.id_empleado
WHERE e.estado = 'Activo'
GROUP BY e.nombre, e.tipo
ORDER BY total_pagado DESC;

-- =================================================================
-- 14. CONSULTAS PARA VALIDACIONES
-- =================================================================

-- Verificar integridad de datos
SELECT 
    'Obras sin presupuesto' AS tipo_verificacion,
    COUNT(*) AS cantidad
FROM Obra o
LEFT JOIN PresupuestoObra p ON o.id_obra = p.id_obra
WHERE p.id_presupuesto IS NULL

UNION ALL

SELECT 
    'Materiales sin proveedor' AS tipo_verificacion,
    COUNT(*) AS cantidad
FROM Material m
LEFT JOIN Proveedor p ON m.id_proveedor = p.id_proveedor
WHERE p.id_proveedor IS NULL

UNION ALL

SELECT 
    'Empleados sin contratos' AS tipo_verificacion,
    COUNT(*) AS cantidad
FROM Empleado e
LEFT JOIN Contrato c ON e.id_empleado = c.id_empleado AND c.estado = 'Activo'
WHERE c.id_contrato IS NULL AND e.estado = 'Activo';

-- =================================================================
-- FIN DE LAS CONSULTAS
-- =================================================================

/*
NOTAS PARA LA IMPLEMENTACIÓN:

1. Estas consultas están optimizadas para SQL Server
2. Usar parámetros en lugar de valores fijos para consultas específicas
3. Implementar paginación para tablas con muchos registros
4. Considerar índices en columnas frecuentemente consultadas
5. Para el sistema web, convertir estas consultas a procedimientos almacenados o vistas

EJEMPLOS DE USO EN APLICACIÓN WEB:
- Para cargar la tabla de obras: usar consulta #2
- Para el dashboard: usar consulta #1
- Para filtros dinámicos: usar consultas #11
- Para detalles específicos: usar consultas #12 con parámetros
*/