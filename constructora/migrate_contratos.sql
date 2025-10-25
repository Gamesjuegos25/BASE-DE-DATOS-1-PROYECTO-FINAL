-- Migración para extender tabla CONTRATOS con campos de gestión
-- Agregar campos faltantes para el formulario de contratos

BEGIN;

-- Verificar si las columnas no existen antes de agregarlas
DO $$ 
BEGIN
    -- Agregar numero_contrato si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='contratos' AND column_name='numero_contrato') THEN
        ALTER TABLE CONTRATOS ADD COLUMN numero_contrato VARCHAR(50);
        ALTER TABLE CONTRATOS ADD CONSTRAINT uk_numero_contrato UNIQUE (numero_contrato);
    END IF;
    
    -- Agregar id_cliente si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='contratos' AND column_name='id_cliente') THEN
        ALTER TABLE CONTRATOS ADD COLUMN id_cliente INTEGER;
        ALTER TABLE CONTRATOS ADD CONSTRAINT fk_contratos_cliente 
            FOREIGN KEY (id_cliente) REFERENCES CLIENTES(id_cliente);
    END IF;
    
    -- Agregar valor_total si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='contratos' AND column_name='valor_total') THEN
        ALTER TABLE CONTRATOS ADD COLUMN valor_total DECIMAL(15,2);
    END IF;
    
    -- Agregar estado si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='contratos' AND column_name='estado') THEN
        ALTER TABLE CONTRATOS ADD COLUMN estado VARCHAR(50) DEFAULT 'activo';
    END IF;
    
    -- Agregar descripcion si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='contratos' AND column_name='descripcion') THEN
        ALTER TABLE CONTRATOS ADD COLUMN descripcion TEXT;
    END IF;
    
    -- Agregar observaciones si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name='contratos' AND column_name='observaciones') THEN
        ALTER TABLE CONTRATOS ADD COLUMN observaciones TEXT;
    END IF;
END $$;

-- Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_contratos_numero ON CONTRATOS(numero_contrato);
CREATE INDEX IF NOT EXISTS idx_contratos_cliente ON CONTRATOS(id_cliente);
CREATE INDEX IF NOT EXISTS idx_contratos_estado ON CONTRATOS(estado);
CREATE INDEX IF NOT EXISTS idx_contratos_fecha_inicio ON CONTRATOS(fecha_inicio_contrato);

COMMIT;

-- Verificar que las columnas se agregaron correctamente
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'contratos' 
AND table_schema = 'public'
ORDER BY ordinal_position;