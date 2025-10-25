-- Migración: Añadir columnas para normalizar MOVIMIENTOS_MATERIAL e INVENTARIOS
-- Fecha: 2025-10-22
-- Propósito: Permitir tracking de materiales en movimientos e inventarios

-- 1. Añadir id_material a INVENTARIOS si no existe
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'inventarios' AND column_name = 'id_material'
    ) THEN
        ALTER TABLE INVENTARIOS ADD COLUMN id_material INTEGER REFERENCES MATERIALES(id_material) ON DELETE CASCADE;
        RAISE NOTICE 'Columna id_material añadida a INVENTARIOS';
    END IF;
END $$;

-- 2. Añadir id_material a MOVIMIENTOS_MATERIAL si no existe
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'movimientos_material' AND column_name = 'id_material'
    ) THEN
        ALTER TABLE MOVIMIENTOS_MATERIAL ADD COLUMN id_material INTEGER REFERENCES MATERIALES(id_material) ON DELETE CASCADE;
        RAISE NOTICE 'Columna id_material añadida a MOVIMIENTOS_MATERIAL';
    END IF;
END $$;

-- 3. Añadir cantidad a MOVIMIENTOS_MATERIAL si no existe
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'movimientos_material' AND column_name = 'cantidad'
    ) THEN
        ALTER TABLE MOVIMIENTOS_MATERIAL ADD COLUMN cantidad INTEGER;
        RAISE NOTICE 'Columna cantidad añadida a MOVIMIENTOS_MATERIAL';
    END IF;
END $$;

-- 4. Añadir fecha_actualizacion a INVENTARIOS si no existe (útil para auditoría)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'inventarios' AND column_name = 'fecha_actualizacion'
    ) THEN
        ALTER TABLE INVENTARIOS ADD COLUMN fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        RAISE NOTICE 'Columna fecha_actualizacion añadida a INVENTARIOS';
    END IF;
END $$;

-- Comentario: Esta migración es idempotente (se puede ejecutar varias veces sin efecto)
