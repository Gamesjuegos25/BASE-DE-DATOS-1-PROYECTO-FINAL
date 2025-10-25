-- Crear tablas de asignación para proyectos
-- Sistema de Constructora - Asignaciones de Proyectos
-- Fecha: 2024

-- Tabla para asignar proyectos a obras específicas
CREATE TABLE IF NOT EXISTS proyecto_obra (
    id_proyecto INTEGER NOT NULL,
    id_obra INTEGER NOT NULL,
    fecha_asignacion DATE NOT NULL DEFAULT CURRENT_DATE,
    observaciones TEXT NULL,
    PRIMARY KEY (id_proyecto, id_obra),
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE,
    FOREIGN KEY (id_obra) REFERENCES obras(id_obra) ON DELETE CASCADE
);

-- Tabla para asignar empleados específicos (arquitectos e ingenieros) a proyectos
CREATE TABLE IF NOT EXISTS proyecto_empleado (
    id_proyecto INTEGER NOT NULL,
    id_empleado INTEGER NOT NULL,
    tipo_asignacion VARCHAR(50) NOT NULL DEFAULT 'COLABORADOR', -- ARQUITECTO, INGENIERO, COORDINADOR
    fecha_asignacion DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_fin_asignacion DATE NULL,
    responsabilidad TEXT NULL, -- Descripción de responsabilidades específicas
    observaciones TEXT NULL,
    PRIMARY KEY (id_proyecto, id_empleado, tipo_asignacion),
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado) ON DELETE CASCADE
);

-- Tabla para asignar vehículos a proyectos
CREATE TABLE IF NOT EXISTS proyecto_vehiculo (
    id_proyecto INTEGER NOT NULL,
    id_vehiculo INTEGER NOT NULL,
    fecha_asignacion DATE NOT NULL DEFAULT CURRENT_DATE,
    fecha_fin_asignacion DATE NULL,
    proposito TEXT NULL, -- Para qué se usará el vehículo en el proyecto
    observaciones TEXT NULL,
    PRIMARY KEY (id_proyecto, id_vehiculo),
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto) ON DELETE CASCADE,
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo) ON DELETE CASCADE
);

-- Índices para mejorar rendimiento de consultas
CREATE INDEX IF NOT EXISTS idx_proyecto_obra_proyecto ON proyecto_obra(id_proyecto);
CREATE INDEX IF NOT EXISTS idx_proyecto_obra_obra ON proyecto_obra(id_obra);
CREATE INDEX IF NOT EXISTS idx_proyecto_empleado_proyecto ON proyecto_empleado(id_proyecto);
CREATE INDEX IF NOT EXISTS idx_proyecto_empleado_empleado ON proyecto_empleado(id_empleado);
CREATE INDEX IF NOT EXISTS idx_proyecto_empleado_tipo ON proyecto_empleado(tipo_asignacion);
CREATE INDEX IF NOT EXISTS idx_proyecto_vehiculo_proyecto ON proyecto_vehiculo(id_proyecto);
CREATE INDEX IF NOT EXISTS idx_proyecto_vehiculo_vehiculo ON proyecto_vehiculo(id_vehiculo);

-- Comentarios para documentación
COMMENT ON TABLE proyecto_obra IS 'Asignación de obras específicas a proyectos';
COMMENT ON TABLE proyecto_empleado IS 'Asignación de arquitectos, ingenieros y otros empleados a proyectos';
COMMENT ON TABLE proyecto_vehiculo IS 'Asignación de vehículos y equipos a proyectos específicos';

COMMENT ON COLUMN proyecto_empleado.tipo_asignacion IS 'Tipo de rol del empleado en el proyecto: ARQUITECTO, INGENIERO, COORDINADOR';
COMMENT ON COLUMN proyecto_empleado.responsabilidad IS 'Descripción específica de las responsabilidades del empleado en el proyecto';
COMMENT ON COLUMN proyecto_vehiculo.proposito IS 'Descripción del uso específico del vehículo en el proyecto';