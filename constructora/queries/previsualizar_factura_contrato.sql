-- Previsualización de lo que se facturaría para un contrato (sin insertar)
-- Uso: ajustar el WHERE con el id de contrato

WITH datos AS (
    SELECT 
        c.id_contrato,
        o.id_obra,
        cli.id_cliente,
        COALESCE(cli.nombre_cliente, 'N/D') AS nombre_cliente,
        dt.id_detalle_trabajo,
        dt.cantidad_trabajo,
        dt.total_trabajo,
        -- precio unitario inferido
        CASE WHEN dt.cantidad_trabajo IS NOT NULL AND dt.cantidad_trabajo > 0
             THEN dt.total_trabajo / dt.cantidad_trabajo
             ELSE dt.total_trabajo END AS precio_unitario,
        -- descripción genérica
        'Detalle contrato #' || c.id_contrato || ' - ítem ' || dt.id_detalle_trabajo AS descripcion
    FROM CONTRATOS c
    LEFT JOIN CONTRATO_OBRA co ON co.id_contrato = c.id_contrato
    LEFT JOIN OBRAS o ON o.id_obra = co.id_obra
    LEFT JOIN OBRA_CLIENTE oc ON oc.id_obra = o.id_obra
    LEFT JOIN CLIENTES cli ON cli.id_cliente = oc.id_cliente
    JOIN CONTRATO_DETALLE_TRABAJO cdt ON cdt.id_contrato = c.id_contrato
    JOIN DETALLES_TRABAJO dt ON dt.id_detalle_trabajo = cdt.id_detalle_trabajo
    WHERE c.id_contrato = 1 -- <-- CAMBIAR AQUÍ
)
SELECT 
    id_contrato,
    id_obra,
    id_cliente,
    nombre_cliente,
    descripcion,
    COALESCE(cantidad_trabajo,1) AS cantidad,
    COALESCE(precio_unitario,0) AS precio_unitario,
    COALESCE(total_trabajo, COALESCE(cantidad_trabajo,1) * COALESCE(precio_unitario,0)) AS subtotal
FROM datos
ORDER BY id_detalle_trabajo;