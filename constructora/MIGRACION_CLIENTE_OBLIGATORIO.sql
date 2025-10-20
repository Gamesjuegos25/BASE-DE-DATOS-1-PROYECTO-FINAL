-- =============================================
-- MIGRACIÓN: Hacer Cliente Obligatorio en OBRAS
-- Para base de datos existente
-- =============================================

BEGIN;

-- 1. Agregar campos adicionales a CLIENTES (si no existen)
ALTER TABLE CLIENTES 
ADD COLUMN IF NOT EXISTS documento_cliente VARCHAR(50),
ADD COLUMN IF NOT EXISTS telefono_cliente VARCHAR(20),
ADD COLUMN IF NOT EXISTS email_cliente VARCHAR(150),
ADD COLUMN IF NOT EXISTS direccion_cliente TEXT;

-- 2. Agregar campos adicionales a OBRAS (si no existen)
ALTER TABLE OBRAS 
ADD COLUMN IF NOT EXISTS descripcion_obra TEXT,
ADD COLUMN IF NOT EXISTS fecha_inicio DATE,
ADD COLUMN IF NOT EXISTS fecha_fin DATE,
ADD COLUMN IF NOT EXISTS valor_obra DECIMAL(15,2);

-- 3. Crear cliente por defecto para obras huérfanas
INSERT INTO CLIENTES (nombre_cliente, documento_cliente, tipo_cliente) 
VALUES ('Cliente Sin Asignar', '000000000-0', 'TEMPORAL')
ON CONFLICT DO NOTHING;

-- 4. Obtener ID del cliente por defecto
DO $$
DECLARE
    cliente_default_id INTEGER;
BEGIN
    SELECT id_cliente INTO cliente_default_id 
    FROM CLIENTES 
    WHERE documento_cliente = '000000000-0' 
    LIMIT 1;
    
    -- 5. Agregar columna id_cliente a OBRAS (temporal, nullable)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'obras' AND column_name = 'id_cliente') THEN
        ALTER TABLE OBRAS ADD COLUMN id_cliente INTEGER;
    END IF;
    
    -- 6. Actualizar obras sin cliente al cliente por defecto
    UPDATE OBRAS 
    SET id_cliente = cliente_default_id 
    WHERE id_cliente IS NULL;
    
    -- 7. Hacer la columna NOT NULL y agregar FK
    ALTER TABLE OBRAS 
    ALTER COLUMN id_cliente SET NOT NULL;
    
    -- 8. Agregar constraint de FK si no existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints 
                   WHERE table_name = 'obras' AND constraint_name = 'obras_id_cliente_fkey') THEN
        ALTER TABLE OBRAS 
        ADD CONSTRAINT obras_id_cliente_fkey 
        FOREIGN KEY (id_cliente) REFERENCES CLIENTES(id_cliente) ON DELETE RESTRICT;
    END IF;
END $$;

-- 9. Eliminar tabla OBRA_CLIENTE si existe (ya no es necesaria)
DROP TABLE IF EXISTS OBRA_CLIENTE;

-- 10. Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_obras_cliente ON OBRAS(id_cliente);
CREATE INDEX IF NOT EXISTS idx_obras_estado ON OBRAS(estado_obra);
CREATE INDEX IF NOT EXISTS idx_obras_nombre ON OBRAS(nombre_obra);
CREATE INDEX IF NOT EXISTS idx_clientes_documento ON CLIENTES(documento_cliente);

-- 11. Insertar clientes de ejemplo adicionales
INSERT INTO CLIENTES (nombre_cliente, documento_cliente, telefono_cliente, email_cliente, direccion_cliente) VALUES
('Constructora ABC Ltda.', '800123456-7', '+57 301 123 4567', 'info@constructora-abc.com', 'Calle 100 #15-23, Bogotá'),
('Desarrollos XYZ S.A.S.', '900234567-8', '+57 312 234 5678', 'contacto@desarrollos-xyz.com', 'Carrera 50 #70-80, Medellín'),
('Inmobiliaria 123 S.A.', '800345678-9', '+57 323 345 6789', 'ventas@inmobiliaria123.com', 'Avenida 6 #120-45, Cali')
ON CONFLICT (documento_cliente) DO NOTHING;

COMMIT;

-- =============================================
-- VERIFICACIÓN
-- =============================================

-- Verificar que todas las obras tienen cliente
SELECT 
    COUNT(*) as total_obras,
    COUNT(id_cliente) as obras_con_cliente,
    CASE 
        WHEN COUNT(*) = COUNT(id_cliente) THEN 'TODAS LAS OBRAS TIENEN CLIENTE ✓'
        ELSE 'HAY OBRAS SIN CLIENTE ✗'
    END as estado
FROM OBRAS;

-- Mostrar distribución de obras por cliente
SELECT 
    c.nombre_cliente,
    c.documento_cliente,
    COUNT(o.id_obra) as cantidad_obras
FROM CLIENTES c
LEFT JOIN OBRAS o ON c.id_cliente = o.id_cliente
GROUP BY c.id_cliente, c.nombre_cliente, c.documento_cliente
ORDER BY cantidad_obras DESC;