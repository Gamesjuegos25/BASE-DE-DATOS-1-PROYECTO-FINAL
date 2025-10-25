-- ============================================
-- FACTURIZAR CONTRATO: Genera factura y detalles desde un contrato
-- Requisitos previos: ejecutar queries/contratos_facturacion.sql
-- Tablas usadas: CONTRATOS, CONTRATO_OBRA, OBRAS, OBRA_CLIENTE, CLIENTES,
--                 DETALLES_TRABAJO, TRABAJOS, CONTRATO_DETALLE_TRABAJO,
--                 FACTURAS, DETALLES_FACTURA
-- ============================================

CREATE OR REPLACE FUNCTION facturizar_contrato(
    p_id_contrato INTEGER,
    p_fecha_emision DATE DEFAULT CURRENT_DATE,
    p_fecha_vencimiento DATE DEFAULT NULL,
    p_observaciones TEXT DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    v_id_factura INTEGER;
    v_numero_factura VARCHAR(50);
    v_id_cliente INTEGER;
    v_total_factura DECIMAL(15,2);
    v_puede_facturar BOOLEAN;
BEGIN
    -- Validar contrato
    IF NOT EXISTS (SELECT 1 FROM CONTRATOS c WHERE c.id_contrato = p_id_contrato) THEN
        RAISE EXCEPTION 'Contrato % no existe', p_id_contrato;
    END IF;

    -- Validar si se puede facturar (si la columna existe)
    BEGIN
        SELECT puede_facturar INTO v_puede_facturar FROM CONTRATOS WHERE id_contrato = p_id_contrato;
    EXCEPTION WHEN undefined_column THEN
        v_puede_facturar := TRUE; -- si no existe la columna, permitimos facturar
    END;

    IF v_puede_facturar = FALSE THEN
        RAISE EXCEPTION 'Contrato % no está habilitado para facturar', p_id_contrato;
    END IF;

    -- Obtener cliente a partir de la obra del contrato (toma el primero si hay varios)
    SELECT oc.id_cliente
    INTO v_id_cliente
    FROM CONTRATO_OBRA co
    JOIN OBRA_CLIENTE oc ON oc.id_obra = co.id_obra
    WHERE co.id_contrato = p_id_contrato
    LIMIT 1;

    -- Generar número de factura (usa función si existe)
    BEGIN
        v_numero_factura := generar_numero_factura();
    EXCEPTION WHEN undefined_function THEN
        -- Fallback simple: AAAAMMDD-<random>
        v_numero_factura := TO_CHAR(CURRENT_DATE, 'YYYYMMDD') || '-' || FLOOR(RANDOM() * 100000)::TEXT;
    END;

    -- Crear factura
    INSERT INTO FACTURAS (numero_factura, id_contrato, id_cliente, fecha_emision, fecha_vencimiento, estado, observaciones)
    VALUES (v_numero_factura, p_id_contrato, v_id_cliente, p_fecha_emision, p_fecha_vencimiento, 'PENDIENTE', p_observaciones)
    RETURNING id_factura INTO v_id_factura;

    -- Insertar detalles desde los trabajos del contrato
    INSERT INTO DETALLES_FACTURA (id_factura, descripcion, cantidad, precio_unitario, subtotal)
    SELECT 
        v_id_factura AS id_factura,
        'Detalle contrato #' || cdt.id_contrato || ' - ítem ' || dt.id_detalle_trabajo AS descripcion,
        COALESCE(NULLIF(dt.cantidad_trabajo,0), 1) AS cantidad,
        -- si hay total_trabajo y cantidad, inferir precio unitario, si no, usar total como precio con cantidad 1
        CASE 
            WHEN COALESCE(NULLIF(dt.cantidad_trabajo,0), 1) = 0 THEN COALESCE(dt.total_trabajo,0)
            WHEN dt.total_trabajo IS NOT NULL AND dt.cantidad_trabajo IS NOT NULL AND dt.cantidad_trabajo > 0 
                THEN dt.total_trabajo / dt.cantidad_trabajo
            ELSE 0
        END AS precio_unitario,
        COALESCE(dt.total_trabajo, 0) AS subtotal
    FROM CONTRATO_DETALLE_TRABAJO cdt
    JOIN DETALLES_TRABAJO dt ON dt.id_detalle_trabajo = cdt.id_detalle_trabajo
    WHERE cdt.id_contrato = p_id_contrato;

    -- Calcular totales
    BEGIN
        PERFORM calcular_totales_factura(v_id_factura);
    EXCEPTION WHEN undefined_function THEN
        -- Fallback: sumar subtotales e IVA 16%
        UPDATE FACTURAS f
        SET subtotal = COALESCE((SELECT SUM(subtotal) FROM DETALLES_FACTURA d WHERE d.id_factura = f.id_factura),0),
            iva = COALESCE((SELECT SUM(subtotal) FROM DETALLES_FACTURA d WHERE d.id_factura = f.id_factura),0) * 0.16,
            total = COALESCE((SELECT SUM(subtotal) FROM DETALLES_FACTURA d WHERE d.id_factura = f.id_factura),0) * 1.16
        WHERE f.id_factura = v_id_factura;
    END;

    -- Actualizar monto_facturado del contrato si existe la columna
    BEGIN
        SELECT total INTO v_total_factura FROM FACTURAS WHERE id_factura = v_id_factura;
        UPDATE CONTRATOS SET monto_facturado = COALESCE(monto_facturado,0) + COALESCE(v_total_factura,0)
        WHERE id_contrato = p_id_contrato;
    EXCEPTION WHEN undefined_column THEN
        -- ignorar si el contrato no tiene columna monto_facturado
        NULL;
    END;

    RETURN v_id_factura;
END;
$$ LANGUAGE plpgsql;