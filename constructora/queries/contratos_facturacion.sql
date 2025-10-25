-- ============================================
-- SISTEMA DE CONTRATOS Y FACTURACIÓN
-- Modificaciones para generar facturas desde contratos
-- ============================================

-- 1. CREAR TABLA DE FACTURAS
CREATE TABLE IF NOT EXISTS FACTURAS (
    id_factura SERIAL PRIMARY KEY,
    numero_factura VARCHAR(50) UNIQUE NOT NULL,
    id_contrato INTEGER REFERENCES CONTRATOS(id_contrato),
    id_cliente INTEGER,
    fecha_emision DATE DEFAULT CURRENT_DATE,
    fecha_vencimiento DATE,
    subtotal DECIMAL(15,2) DEFAULT 0,
    iva DECIMAL(15,2) DEFAULT 0,
    total DECIMAL(15,2) DEFAULT 0,
    estado VARCHAR(50) DEFAULT 'PENDIENTE',
    observaciones TEXT,
    metodo_pago VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. CREAR TABLA DE DETALLES DE FACTURAS
CREATE TABLE IF NOT EXISTS DETALLES_FACTURA (
    id_detalle SERIAL PRIMARY KEY,
    id_factura INTEGER REFERENCES FACTURAS(id_factura) ON DELETE CASCADE,
    descripcion VARCHAR(500) NOT NULL,
    cantidad DECIMAL(10,2) DEFAULT 1,
    precio_unitario DECIMAL(15,2) NOT NULL,
    subtotal DECIMAL(15,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. CREAR TABLA DE PAGOS
CREATE TABLE IF NOT EXISTS PAGOS (
    id_pago SERIAL PRIMARY KEY,
    id_factura INTEGER REFERENCES FACTURAS(id_factura),
    fecha_pago DATE DEFAULT CURRENT_DATE,
    monto DECIMAL(15,2) NOT NULL,
    metodo_pago VARCHAR(100),
    numero_referencia VARCHAR(100),
    observaciones TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. MODIFICAR TABLA CONTRATOS PARA FACTURACIÓN
ALTER TABLE CONTRATOS 
ADD COLUMN IF NOT EXISTS puede_facturar BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS monto_total DECIMAL(15,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS monto_facturado DECIMAL(15,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS porcentaje_iva DECIMAL(5,2) DEFAULT 16.00;

-- 5. CREAR VISTA PARA CONTRATOS FACTURABLES
CREATE OR REPLACE VIEW CONTRATOS_FACTURABLES AS
SELECT 
    c.id_contrato,
    NULL::text as tipo_contrato,
    c.fecha_inicio_contrato as fecha_inicio,
    c.fecha_fin_contrato as fecha_fin,
    c.monto_total,
    c.monto_facturado,
    c.puede_facturar,
    (c.monto_total - c.monto_facturado) as saldo_por_facturar,
    NULL::text as empleado_nombre,
    NULL::text as empleado_apellido,
    o.nombre_obra,
    CASE 
        WHEN c.monto_facturado >= c.monto_total THEN 'COMPLETAMENTE_FACTURADO'
        WHEN c.monto_facturado > 0 THEN 'PARCIALMENTE_FACTURADO'
        ELSE 'SIN_FACTURAR'
    END as estado_facturacion
FROM CONTRATOS c
LEFT JOIN CONTRATO_OBRA co ON co.id_contrato = c.id_contrato
LEFT JOIN OBRAS o ON o.id_obra = co.id_obra
WHERE c.puede_facturar = TRUE;

-- 6. CREAR FUNCIÓN PARA GENERAR NÚMERO DE FACTURA
CREATE OR REPLACE FUNCTION generar_numero_factura()
RETURNS VARCHAR(50) AS $$
DECLARE
    nuevo_numero VARCHAR(50);
    contador INTEGER;
BEGIN
    -- Obtener el último número de factura del año actual
    SELECT COALESCE(MAX(CAST(SUBSTRING(numero_factura FROM 10) AS INTEGER)), 0) + 1
    INTO contador
    FROM FACTURAS 
    WHERE numero_factura LIKE TO_CHAR(CURRENT_DATE, 'YYYY') || '-%';
    
    -- Generar nuevo número: YYYY-000001
    nuevo_numero := TO_CHAR(CURRENT_DATE, 'YYYY') || '-' || LPAD(contador::TEXT, 6, '0');
    
    RETURN nuevo_numero;
END;
$$ LANGUAGE plpgsql;

-- 7. CREAR FUNCIÓN PARA CALCULAR TOTALES DE FACTURA
CREATE OR REPLACE FUNCTION calcular_totales_factura(factura_id INTEGER)
RETURNS VOID AS $$
DECLARE
    subtotal_calc DECIMAL(15,2);
    iva_calc DECIMAL(15,2);
    total_calc DECIMAL(15,2);
    porcentaje_iva DECIMAL(5,2);
BEGIN
    -- Calcular subtotal
    SELECT COALESCE(SUM(subtotal), 0)
    INTO subtotal_calc
    FROM DETALLES_FACTURA
    WHERE id_factura = factura_id;
    
    -- Obtener porcentaje de IVA (por defecto 16%)
    SELECT COALESCE(c.porcentaje_iva, 16.00)
    INTO porcentaje_iva
    FROM FACTURAS f
    LEFT JOIN CONTRATOS c ON f.id_contrato = c.id_contrato
    WHERE f.id_factura = factura_id;
    
    -- Calcular IVA
    iva_calc := subtotal_calc * (porcentaje_iva / 100);
    
    -- Calcular total
    total_calc := subtotal_calc + iva_calc;
    
    -- Actualizar factura
    UPDATE FACTURAS 
    SET 
        subtotal = subtotal_calc,
        iva = iva_calc,
        total = total_calc,
        updated_at = CURRENT_TIMESTAMP
    WHERE id_factura = factura_id;
END;
$$ LANGUAGE plpgsql;

-- 8. TRIGGER PARA ACTUALIZAR TOTALES AUTOMÁTICAMENTE
CREATE OR REPLACE FUNCTION trigger_actualizar_totales_factura()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM calcular_totales_factura(NEW.id_factura);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger
DROP TRIGGER IF EXISTS actualizar_totales_factura ON DETALLES_FACTURA;
CREATE TRIGGER actualizar_totales_factura
    AFTER INSERT OR UPDATE OR DELETE ON DETALLES_FACTURA
    FOR EACH ROW EXECUTE FUNCTION trigger_actualizar_totales_factura();

-- 9. DATOS DE EJEMPLO PARA TESTING
INSERT INTO FACTURAS (numero_factura, fecha_emision, fecha_vencimiento, estado) VALUES 
('2025-000001', CURRENT_DATE, CURRENT_DATE + INTERVAL '30 days', 'PENDIENTE'),
('2025-000002', CURRENT_DATE - INTERVAL '15 days', CURRENT_DATE + INTERVAL '15 days', 'PAGADA');

INSERT INTO DETALLES_FACTURA (id_factura, descripcion, cantidad, precio_unitario, subtotal) VALUES 
(1, 'Servicios de construcción - Fase 1', 1, 50000.00, 50000.00),
(1, 'Materiales de construcción', 1, 25000.00, 25000.00),
(2, 'Supervisión técnica', 1, 15000.00, 15000.00);

INSERT INTO PAGOS (id_factura, monto, metodo_pago, numero_referencia) VALUES 
(2, 17400.00, 'Transferencia bancaria', 'TXN-2025-001');

-- 10. ÍNDICES PARA OPTIMIZACIÓN
CREATE INDEX IF NOT EXISTS idx_facturas_numero ON FACTURAS(numero_factura);
CREATE INDEX IF NOT EXISTS idx_facturas_fecha ON FACTURAS(fecha_emision);
CREATE INDEX IF NOT EXISTS idx_facturas_estado ON FACTURAS(estado);
CREATE INDEX IF NOT EXISTS idx_detalles_factura ON DETALLES_FACTURA(id_factura);
CREATE INDEX IF NOT EXISTS idx_pagos_factura ON PAGOS(id_factura);

-- 11. VISTA RESUMEN DE FACTURACIÓN
CREATE OR REPLACE VIEW RESUMEN_FACTURACION AS
SELECT 
    DATE_TRUNC('month', f.fecha_emision) as mes,
    COUNT(*) as total_facturas,
    SUM(f.total) as monto_total_facturado,
    SUM(CASE WHEN f.estado = 'PAGADA' THEN f.total ELSE 0 END) as monto_cobrado,
    SUM(CASE WHEN f.estado = 'PENDIENTE' THEN f.total ELSE 0 END) as monto_pendiente,
    ROUND(
        (SUM(CASE WHEN f.estado = 'PAGADA' THEN f.total ELSE 0 END) * 100.0) / 
        NULLIF(SUM(f.total), 0), 2
    ) as porcentaje_cobrado
FROM FACTURAS f
GROUP BY DATE_TRUNC('month', f.fecha_emision)
ORDER BY mes DESC;

COMMENT ON TABLE FACTURAS IS 'Tabla principal de facturas del sistema';
COMMENT ON TABLE DETALLES_FACTURA IS 'Detalles línea por línea de cada factura';
COMMENT ON TABLE PAGOS IS 'Registro de pagos realizados a las facturas';
COMMENT ON VIEW CONTRATOS_FACTURABLES IS 'Vista de contratos que pueden generar facturas';
COMMENT ON VIEW RESUMEN_FACTURACION IS 'Resumen mensual de facturación y cobranza';