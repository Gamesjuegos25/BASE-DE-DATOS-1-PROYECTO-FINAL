-- ============================================
-- OBRAS - Campos de estimación para cotización y ajuste de trigger
-- Añade columnas y recalcula valor_obra cuando es precio fijo
-- ============================================

BEGIN;

-- 1) Nuevas columnas de estimación en OBRAS
ALTER TABLE OBRAS 
    ADD COLUMN IF NOT EXISTS area_m2 DECIMAL(12,2),
    ADD COLUMN IF NOT EXISTS cantidad_estimada DECIMAL(12,2),
    ADD COLUMN IF NOT EXISTS unidad_estimacion VARCHAR(50),
    ADD COLUMN IF NOT EXISTS precio_unitario_estimado DECIMAL(12,2),
    ADD COLUMN IF NOT EXISTS valor_estimado DECIMAL(15,2);

COMMENT ON COLUMN OBRAS.area_m2 IS 'Área estimada en m² para cotización';
COMMENT ON COLUMN OBRAS.cantidad_estimada IS 'Cantidad estimada (unidades) para cotización';
COMMENT ON COLUMN OBRAS.unidad_estimacion IS 'Unidad base de la estimación (m2, unidad, etc.)';
COMMENT ON COLUMN OBRAS.precio_unitario_estimado IS 'Precio unitario usado para la estimación';
COMMENT ON COLUMN OBRAS.valor_estimado IS 'Valor total estimado calculado (precio_unitario_estimado x cantidad/área)';

-- 2) Actualizar trigger para usar los nuevos campos al fijar precio por catálogo
CREATE OR REPLACE FUNCTION fn_aplicar_tipo_obra_fijo()
RETURNS TRIGGER AS $$
DECLARE
    v_desc TEXT;
    v_prec DECIMAL(15,2);
    v_tipo VARCHAR(150);
    v_unidad VARCHAR(100);
    v_mult DECIMAL(15,2);
    v_total DECIMAL(15,2);
    v_unidad_base VARCHAR(100);
BEGIN
    IF NEW.es_precio_fijo IS TRUE AND NEW.id_tipo_obra IS NOT NULL THEN
        SELECT t.descripcion_base, t.precio_base, t.nombre_tipo, t.unidad_medida
        INTO v_desc, v_prec, v_tipo, v_unidad
        FROM TIPOS_OBRA t
        WHERE t.id_tipo_obra = NEW.id_tipo_obra AND t.activo = TRUE;

        IF v_tipo IS NULL THEN
            RAISE EXCEPTION 'Tipo de obra % no válido o inactivo', NEW.id_tipo_obra;
        END IF;

        -- Forzar campos de catálogo
        NEW.tipo_obra := v_tipo;
        NEW.descripcion_obra := v_desc;

        -- Establecer unidad de estimación por defecto desde el catálogo si no viene
        IF NEW.unidad_estimacion IS NULL OR LENGTH(TRIM(NEW.unidad_estimacion)) = 0 THEN
            NEW.unidad_estimacion := v_unidad;
        END IF;

        -- Precio unitario desde el catálogo
        NEW.precio_unitario_estimado := v_prec;

        -- Determinar multiplicador según unidad (m2 -> usar area_m2; otro -> cantidad_estimada)
        v_unidad_base := COALESCE(NEW.unidad_estimacion, v_unidad);
        IF v_unidad_base ILIKE '%m2%' THEN
            v_mult := COALESCE(NULLIF(NEW.area_m2, 0), 1);
        ELSE
            v_mult := COALESCE(NULLIF(NEW.cantidad_estimada, 0), 1);
        END IF;

        v_total := ROUND(v_prec * v_mult, 2);
        NEW.valor_estimado := v_total;
        NEW.valor_obra := v_total;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- El trigger ya existe por obras_fijas.sql; lo reusamos sin recrearlo si ya está
-- Si no existiera previamente, lo creamos ahora para asegurar
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger WHERE tgname = 'trg_obras_aplicar_tipo_fijo'
    ) THEN
        CREATE TRIGGER trg_obras_aplicar_tipo_fijo
        BEFORE INSERT OR UPDATE ON OBRAS
        FOR EACH ROW EXECUTE FUNCTION fn_aplicar_tipo_obra_fijo();
    END IF;
END $$;

COMMIT;
