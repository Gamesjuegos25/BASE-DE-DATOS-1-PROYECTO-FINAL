-- ============================================
-- OBRAS FIJAS: Tipos de obra con precio y descripción fija
-- Compatible con esquema base (CREAR_TABLAS_OBLIGATORIO.sql)
-- ============================================

BEGIN;

-- 1) Catálogo de tipos de obra
CREATE TABLE IF NOT EXISTS TIPOS_OBRA (
    id_tipo_obra SERIAL PRIMARY KEY,
    nombre_tipo VARCHAR(150) NOT NULL UNIQUE,
    descripcion_base TEXT,
    -- Unidad de medida referencial (m², ml, unidad, etc.)
    unidad_medida VARCHAR(100),
    -- Texto del rango de precio mostrado (ej: 'Q 4,000 - Q 5,200')
    rango_precio TEXT,
    -- Notas/observaciones de referencia
    notas TEXT,
    -- Valores numéricos opcionales para rango
    precio_min DECIMAL(15,2),
    precio_max DECIMAL(15,2),
    -- Precio base aplicado cuando se marca como fijo en OBRAS
    precio_base DECIMAL(15,2) NOT NULL DEFAULT 0,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

COMMENT ON TABLE TIPOS_OBRA IS 'Catálogo de tipos de obra con precio y descripción fija.';
COMMENT ON COLUMN TIPOS_OBRA.unidad_medida IS 'Unidad de medida referencial para el tipo de obra.';
COMMENT ON COLUMN TIPOS_OBRA.rango_precio IS 'Rango de precio estimado en texto para mostrar en UI.';
COMMENT ON COLUMN TIPOS_OBRA.notas IS 'Notas de referencia para el tipo de obra.';
COMMENT ON COLUMN TIPOS_OBRA.precio_min IS 'Precio mínimo estimado (numérico)';
COMMENT ON COLUMN TIPOS_OBRA.precio_max IS 'Precio máximo estimado (numérico)';

-- 2) Extender OBRAS para enlazar con el catálogo y marcar precio fijo
ALTER TABLE OBRAS 
    ADD COLUMN IF NOT EXISTS id_tipo_obra INTEGER REFERENCES TIPOS_OBRA(id_tipo_obra),
    ADD COLUMN IF NOT EXISTS es_precio_fijo BOOLEAN NOT NULL DEFAULT FALSE;

COMMENT ON COLUMN OBRAS.id_tipo_obra IS 'Referencia opcional a TIPOS_OBRA';
COMMENT ON COLUMN OBRAS.es_precio_fijo IS 'Si TRUE, precio/descripcion/tipo se toman del catálogo y quedan fijos';

-- 3) Trigger: cuando es_precio_fijo = TRUE y hay id_tipo_obra, forzar datos fijos
CREATE OR REPLACE FUNCTION fn_aplicar_tipo_obra_fijo()
RETURNS TRIGGER AS $$
DECLARE
    v_desc TEXT;
    v_prec DECIMAL(15,2);
    v_tipo VARCHAR(150);
BEGIN
    IF NEW.es_precio_fijo IS TRUE AND NEW.id_tipo_obra IS NOT NULL THEN
        SELECT t.descripcion_base, t.precio_base, t.nombre_tipo
        INTO v_desc, v_prec, v_tipo
        FROM TIPOS_OBRA t
        WHERE t.id_tipo_obra = NEW.id_tipo_obra AND t.activo = TRUE;

        -- Si no existe/activo, impedir
        IF v_tipo IS NULL THEN
            RAISE EXCEPTION 'Tipo de obra % no válido o inactivo', NEW.id_tipo_obra;
        END IF;

        -- Forzar campos fijos
        NEW.descripcion_obra := v_desc;
        NEW.valor_obra := v_prec;
        NEW.tipo_obra := v_tipo;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_obras_aplicar_tipo_fijo ON OBRAS;
CREATE TRIGGER trg_obras_aplicar_tipo_fijo
BEFORE INSERT OR UPDATE ON OBRAS
FOR EACH ROW EXECUTE FUNCTION fn_aplicar_tipo_obra_fijo();

COMMIT;
