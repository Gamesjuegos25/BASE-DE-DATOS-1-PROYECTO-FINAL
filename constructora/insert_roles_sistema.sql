-- ================================================
-- SCRIPT DE INSERCIÓN DE ROLES - SISTEMA CONSTRUCTORA
-- ================================================

-- OPCIÓN 1: Actualizar roles en usuarios existentes
-- ================================================

-- Ver usuarios actuales
SELECT id_usuario, nombre_usuario, rol_usuario 
FROM usuarios_sistema 
ORDER BY id_usuario;

-- Actualizar rol del usuario administrador existente
UPDATE usuarios_sistema 
SET rol_usuario = 'ADMINISTRADOR' 
WHERE nombre_usuario = 'admin' OR rol_usuario = 'ADMINISTRADOR';

-- OPCIÓN 2: Crear tabla de roles dedicada (RECOMENDADO)
-- ================================================

-- Crear tabla roles si no existe
CREATE TABLE IF NOT EXISTS roles (
    id_rol SERIAL PRIMARY KEY,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE,
    descripcion_rol VARCHAR(200),
    permisos TEXT[], -- Array de permisos específicos
    activo BOOLEAN DEFAULT true,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar todos los roles del sistema
INSERT INTO roles (nombre_rol, descripcion_rol, permisos, activo) VALUES
('ADMINISTRADOR', 'Administrador del sistema con acceso completo', 
 ARRAY['ADMIN_USUARIOS', 'ADMIN_SISTEMA', 'VER_REPORTES', 'GESTIONAR_OBRAS', 'GESTIONAR_EMPLEADOS', 'GESTIONAR_FINANZAS'], true),

('Ingeniero Civil', 'Ingeniero Civil especializado en construcción', 
 ARRAY['GESTIONAR_OBRAS', 'VER_REPORTES', 'CREAR_PROYECTOS', 'SUPERVISAR_CONSTRUCCION'], true),

('Arquitecto', 'Arquitecto responsable del diseño y planificación', 
 ARRAY['GESTIONAR_OBRAS', 'CREAR_PROYECTOS', 'VER_REPORTES', 'DISEÑO_ARQUITECTONICO'], true),

('Supervisor de Obra', 'Supervisor encargado del control y seguimiento de obras', 
 ARRAY['SUPERVISAR_CONSTRUCCION', 'GESTIONAR_EMPLEADOS', 'VER_REPORTES', 'CONTROL_CALIDAD'], true),

('Jefe de Proyecto', 'Jefe responsable de la gestión integral de proyectos', 
 ARRAY['GESTIONAR_PROYECTOS', 'GESTIONAR_EMPLEADOS', 'VER_REPORTES', 'PLANIFICACION'], true),

('Contador', 'Contador responsable de la gestión financiera', 
 ARRAY['GESTIONAR_FINANZAS', 'VER_REPORTES', 'CONTABILIDAD', 'FACTURACION'], true),

('Operador de Equipo', 'Operador especializado en manejo de maquinaria', 
 ARRAY['OPERAR_EQUIPOS', 'VER_REPORTES', 'MANTENIMIENTO_EQUIPOS'], true),

('Almacenista', 'Encargado del control de inventarios y almacén', 
 ARRAY['GESTIONAR_INVENTARIO', 'GESTIONAR_MATERIALES', 'VER_REPORTES'], true),

('Asistente', 'Asistente administrativo con funciones de apoyo', 
 ARRAY['VER_REPORTES', 'ASISTENCIA_ADMINISTRATIVA'], true),

('Otro', 'Rol genérico para otros cargos no especificados', 
 ARRAY['VER_REPORTES'], true)

ON CONFLICT (nombre_rol) DO UPDATE SET
    descripcion_rol = EXCLUDED.descripcion_rol,
    permisos = EXCLUDED.permisos,
    fecha_modificacion = CURRENT_TIMESTAMP;

-- OPCIÓN 3: Agregar columna id_rol a usuarios_sistema (ESTRUCTURA MEJORADA)
-- ================================================

-- Agregar columna de referencia a roles (opcional)
ALTER TABLE usuarios_sistema 
ADD COLUMN IF NOT EXISTS id_rol INTEGER REFERENCES roles(id_rol);

-- Crear índices para optimizar consultas
CREATE INDEX IF NOT EXISTS idx_usuarios_sistema_rol ON usuarios_sistema(rol_usuario);
CREATE INDEX IF NOT EXISTS idx_usuarios_sistema_id_rol ON usuarios_sistema(id_rol);
CREATE INDEX IF NOT EXISTS idx_roles_nombre ON roles(nombre_rol);
CREATE INDEX IF NOT EXISTS idx_roles_activo ON roles(activo);

-- OPCIÓN 4: Insertar usuarios de prueba con roles específicos
-- ================================================

-- Insertar usuarios de prueba para cada rol (opcional)
INSERT INTO usuarios_sistema (nombre_usuario, rol_usuario, correo_usuario, contrasena_usuario) VALUES
('ing_civil_01', 'Ingeniero Civil', 'ingeniero@constructora.com', 'password123'),
('arquitecto_01', 'Arquitecto', 'arquitecto@constructora.com', 'password123'),
('supervisor_01', 'Supervisor de Obra', 'supervisor@constructora.com', 'password123'),
('jefe_proy_01', 'Jefe de Proyecto', 'jefe@constructora.com', 'password123'),
('contador_01', 'Contador', 'contador@constructora.com', 'password123'),
('operador_01', 'Operador de Equipo', 'operador@constructora.com', 'password123'),
('almacenista_01', 'Almacenista', 'almacenista@constructora.com', 'password123'),
('asistente_01', 'Asistente', 'asistente@constructora.com', 'password123')

ON CONFLICT (nombre_usuario) DO NOTHING;

-- CONSULTAS DE VERIFICACIÓN
-- ================================================

-- Ver todos los roles creados
SELECT id_rol, nombre_rol, descripcion_rol, activo 
FROM roles 
ORDER BY id_rol;

-- Ver usuarios con sus roles
SELECT u.id_usuario, u.nombre_usuario, u.rol_usuario, u.correo_usuario
FROM usuarios_sistema u 
ORDER BY u.rol_usuario, u.nombre_usuario;

-- Contar usuarios por rol
SELECT rol_usuario, COUNT(*) as cantidad_usuarios
FROM usuarios_sistema 
WHERE rol_usuario IS NOT NULL
GROUP BY rol_usuario
ORDER BY cantidad_usuarios DESC;

-- Ver roles con permisos
SELECT nombre_rol, descripcion_rol, 
       array_to_string(permisos, ', ') as permisos_asignados
FROM roles 
WHERE activo = true
ORDER BY nombre_rol;