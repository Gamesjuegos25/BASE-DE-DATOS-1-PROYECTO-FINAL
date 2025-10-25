-- Crear tablas de asignación para obras
-- Autor: Sistema de Constructora
-- Fecha: 2024

-- Tabla para asignar empleados a obras (arquitectos, ingenieros, obreros)
CREATE TABLE IF NOT EXISTS obra_empleado (
    id_obra INTEGER NOT NULL,
    id_empleado INTEGER NOT NULL,
    tipo_asignacion VARCHAR(50) NOT NULL DEFAULT 'OBRERO', -- ARQUITECTO, INGENIERO, OBRERO, OPERARIO
    fecha_asignacion DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_fin_asignacion DATE NULL,
    salario_obra DECIMAL(12,2) NULL, -- Salario específico para esta obra (opcional)
    horas_asignadas INTEGER NULL, -- Horas programadas para la obra
    observaciones TEXT NULL,
    PRIMARY KEY (id_obra, id_empleado, tipo_asignacion),
    FOREIGN KEY (id_obra) REFERENCES obras(id_obra) ON DELETE CASCADE,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE
);

-- Tabla para asignar materiales a obras
CREATE TABLE IF NOT EXISTS obra_material (
    id_obra INTEGER NOT NULL,
    id_material INTEGER NOT NULL,
    cantidad_asignada DECIMAL(10,3) NOT NULL DEFAULT 1.0,
    cantidad_utilizada DECIMAL(10,3) DEFAULT 0.0,
    fecha_asignacion DATE NOT NULL DEFAULT CURRENT_DATE,
    precio_unitario_obra DECIMAL(12,2) NULL, -- Precio específico para esta obra
    observaciones TEXT NULL,
    PRIMARY KEY (id_obra, id_material),
    FOREIGN KEY (id_obra) REFERENCES obras(id_obra) ON DELETE CASCADE,
    FOREIGN KEY (id_material) REFERENCES materiales(id_material) ON DELETE CASCADE
);

-- Índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_obra_empleado_obra ON obra_empleado(id_obra);
CREATE INDEX IF NOT EXISTS idx_obra_empleado_empleado ON obra_empleado(id_empleado);
CREATE INDEX IF NOT EXISTS idx_obra_empleado_tipo ON obra_empleado(tipo_asignacion);
CREATE INDEX IF NOT EXISTS idx_obra_material_obra ON obra_material(id_obra);
CREATE INDEX IF NOT EXISTS idx_obra_material_material ON obra_material(id_material);

-- Comentarios para documentación
COMMENT ON TABLE obra_empleado IS 'Asignación de empleados a obras específicas con roles definidos';
COMMENT ON TABLE obra_material IS 'Asignación de materiales a obras con cantidades y precios específicos';

COMMENT ON COLUMN obra_empleado.tipo_asignacion IS 'Tipo de rol del empleado en la obra: ARQUITECTO, INGENIERO, OBRERO, OPERARIO';
COMMENT ON COLUMN obra_empleado.salario_obra IS 'Salario específico para esta obra (puede diferir del salario base)';
COMMENT ON COLUMN obra_material.cantidad_asignada IS 'Cantidad de material asignada a la obra';
COMMENT ON COLUMN obra_material.cantidad_utilizada IS 'Cantidad de material ya utilizada en la obra';