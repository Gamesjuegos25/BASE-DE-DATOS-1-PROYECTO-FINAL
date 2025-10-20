-- PROYECTO FINAL - BASE DE DATOS
-- Sistema de Construcción - 56 Tablas
-- Base de datos: PROYECTO_FINAL_BD1
-- MODIFICADO: Relación obligatoria OBRAS-CLIENTES

-- Recrear el esquema public si no existe
CREATE SCHEMA IF NOT EXISTS public;

-- Establecer el esquema por defecto
SET search_path TO public;

BEGIN; 

-- =============================================
-- 1FN - 28 TABLAS PRINCIPALES
-- ============================================

-- 1. CLIENTES (PRIMERA - Para referencias) 
CREATE TABLE CLIENTES (
    id_cliente SERIAL PRIMARY KEY,
    nombre_cliente VARCHAR(150) NOT NULL,
    documento_cliente VARCHAR(50),
    telefono_cliente VARCHAR(20),
    email_cliente VARCHAR(150),
    direccion_cliente TEXT,
    contacto_cliente VARCHAR(100),
    tipo_cliente VARCHAR(50)
);

-- 2. OBRAS (MODIFICADA - Cliente obligatorio)
CREATE TABLE OBRAS (
    id_obra SERIAL PRIMARY KEY,
    nombre_obra VARCHAR(200) NOT NULL,
    descripcion_obra TEXT,
    tipo_obra VARCHAR(100),
    estado_obra VARCHAR(50),
    ubicacion_obra TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    valor_obra DECIMAL(15,2),
    id_cliente INTEGER NOT NULL REFERENCES CLIENTES(id_cliente) ON DELETE RESTRICT
);

-- 3. PROYECTOS
CREATE TABLE PROYECTOS (
    id_proyecto SERIAL PRIMARY KEY,
    nombre_proyecto VARCHAR(200) NOT NULL,
    fecha_inicio_proyecto DATE,
    fecha_fin_proyecto DATE,
    estado_proyecto VARCHAR(50)
);

-- 4. AREAS
CREATE TABLE AREAS (
    id_area SERIAL PRIMARY KEY,
    nombre_area VARCHAR(100) NOT NULL
);

-- 5. ACTIVIDADES
CREATE TABLE ACTIVIDADES (
    id_actividad SERIAL PRIMARY KEY,
    nombre_actividad VARCHAR(200) NOT NULL,
    descripcion_actividad TEXT,
    fecha_programada_actividad DATE
);

-- 6. EMPLEADOS
CREATE TABLE EMPLEADOS (
    id_empleado SERIAL PRIMARY KEY,
    nombre_empleado VARCHAR(150) NOT NULL,
    tipo_empleado VARCHAR(50),
    salario_fijo_empleado DECIMAL(12,2)
);

-- 7. CONTRATOS
CREATE TABLE CONTRATOS (
    id_contrato SERIAL PRIMARY KEY,
    fecha_inicio_contrato DATE NOT NULL,
    fecha_fin_contrato DATE,
    tipo_pago_contrato VARCHAR(50)
);

-- 8. DETALLES_TRABAJO
CREATE TABLE DETALLES_TRABAJO (
    id_detalle_trabajo SERIAL PRIMARY KEY,
    cantidad_trabajo DECIMAL(10,2),
    total_trabajo DECIMAL(12,2)
);

-- 9. TRABAJOS
CREATE TABLE TRABAJOS (
    id_trabajo SERIAL PRIMARY KEY,
    descripcion_trabajo TEXT,
    precio_unitario_trabajo DECIMAL(12,2),
    unidad_trabajo VARCHAR(50)
);

-- 11. MATERIALES
CREATE TABLE PROVEEDORES (
    id_proveedor SERIAL PRIMARY KEY,
    nombre_proveedor VARCHAR(150) NOT NULL,
    contacto_proveedor VARCHAR(100)
);

-- 11. MATERIALES
CREATE TABLE MATERIALES (
    id_material SERIAL PRIMARY KEY,
    nombre_material VARCHAR(150) NOT NULL,
    unidad_material VARCHAR(50),
    precio_unitario_material DECIMAL(12,2)
);

-- 12. BODEGAS
CREATE TABLE BODEGAS (
    id_bodega SERIAL PRIMARY KEY,
    responsable_bodega VARCHAR(150)
);

-- 13. INVENTARIOS
CREATE TABLE INVENTARIOS (
    id_inventario SERIAL PRIMARY KEY,
    cantidad_inventario INTEGER
);

-- 14. USUARIOS_SISTEMA
CREATE TABLE USUARIOS_SISTEMA (
    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
    rol_usuario VARCHAR(50),
    correo_usuario VARCHAR(150) UNIQUE,
    contrasena_usuario VARCHAR(255) NOT NULL
);

-- 15. PERMISOS_ACCESO
CREATE TABLE PERMISOS_ACCESO (
    id_permiso SERIAL PRIMARY KEY,
    modulo_permiso VARCHAR(100) NOT NULL,
    nivel_acceso_permiso VARCHAR(50)
);

-- 16. AUDITORIAS
CREATE TABLE AUDITORIAS (
    id_auditoria SERIAL PRIMARY KEY,
    accion_auditoria VARCHAR(200) NOT NULL,
    fecha_auditoria TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalle_auditoria TEXT
);

-- 17. VEHICULOS
CREATE TABLE VEHICULOS (
    id_vehiculo SERIAL PRIMARY KEY,
    placa_vehiculo VARCHAR(20) UNIQUE,
    estado_vehiculo VARCHAR(50),
    tipo_vehiculo VARCHAR(50)
);

-- 19. EQUIPOS
CREATE TABLE EQUIPOS (
    id_equipo SERIAL PRIMARY KEY,
    nombre_equipo VARCHAR(150) NOT NULL,
    estado_equipo VARCHAR(50),
    tipo_equipo VARCHAR(50)
);

-- 20. ASIGNACIONES_EQUIPO
CREATE TABLE ASIGNACIONES_EQUIPO (
    id_asignacion_equipo SERIAL PRIMARY KEY,
    fecha_inicio_asignacion DATE NOT NULL,
    fecha_fin_asignacion DATE
);

-- 21. BITACORAS
CREATE TABLE BITACORAS (
    id_bitacora SERIAL PRIMARY KEY,
    fecha_bitacora DATE DEFAULT CURRENT_DATE,
    observaciones_bitacora TEXT
);

-- 22. INCIDENTES
CREATE TABLE INCIDENTES (
    id_incidente SERIAL PRIMARY KEY,
    fecha_incidente DATE DEFAULT CURRENT_DATE,
    descripcion_incidente TEXT,
    estado_incidente VARCHAR(50)
);

-- 23. PRESUPUESTOS_OBRA
CREATE TABLE PRESUPUESTOS_OBRA (
    id_presupuesto SERIAL PRIMARY KEY,
    monto_estimado_presupuesto DECIMAL(15,2),
    fecha_presupuesto DATE DEFAULT CURRENT_DATE
);

-- 24. AVANCES_OBRA
CREATE TABLE AVANCES_OBRA (
    id_avance SERIAL PRIMARY KEY,
    porcentaje_fisico_avance DECIMAL(5,2),
    porcentaje_financiero_avance DECIMAL(5,2),
    fecha_avance DATE DEFAULT CURRENT_DATE
);

-- 25. REPORTES_SEMANALES
CREATE TABLE REPORTES_SEMANALES (
    id_reporte SERIAL PRIMARY KEY,
    semana_reporte VARCHAR(20),
    resumen_reporte TEXT,
    fecha_reporte DATE DEFAULT CURRENT_DATE
);

-- 26. ARCHIVOS_ADJUNTOS
CREATE TABLE ARCHIVOS_ADJUNTOS (
    id_archivo SERIAL PRIMARY KEY,
    nombre_archivo VARCHAR(255) NOT NULL,
    resumen_archivo TEXT,
    ruta_archivo TEXT NOT NULL
);

-- 27. REQUISICIONES
CREATE TABLE REQUISICIONES (
    id_requisicion SERIAL PRIMARY KEY,
    fecha_requisicion DATE DEFAULT CURRENT_DATE,
    estado_requisicion VARCHAR(50)
);

-- 28. DETALLES_REQUISICION
CREATE TABLE DETALLES_REQUISICION (
    id_detalle_requisicion SERIAL PRIMARY KEY,
    cantidad_requisicion INTEGER
);

-- 29. MOVIMIENTOS_MATERIAL
CREATE TABLE MOVIMIENTOS_MATERIAL (
    id_movimiento_material SERIAL PRIMARY KEY,
    tipo_movimiento VARCHAR(50) NOT NULL,
    fecha_movimiento DATE DEFAULT CURRENT_DATE,
    origen_movimiento VARCHAR(100),
    destino_movimiento VARCHAR(100)
);

-- =============================================
-- 2FN - 13 TABLAS (Relaciones N:M)
-- =============================================

-- 30. OBRA_AREA
CREATE TABLE OBRA_AREA (
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    id_area INTEGER REFERENCES AREAS(id_area) ON DELETE CASCADE,
    PRIMARY KEY (id_obra, id_area)
);

-- 31. AREA_ACTIVIDAD
CREATE TABLE AREA_ACTIVIDAD (
    id_area INTEGER REFERENCES AREAS(id_area) ON DELETE CASCADE,
    id_actividad INTEGER REFERENCES ACTIVIDADES(id_actividad) ON DELETE CASCADE,
    PRIMARY KEY (id_area, id_actividad)
);

-- 32. ACTIVIDAD_TRABAJO
CREATE TABLE ACTIVIDAD_TRABAJO (
    id_actividad INTEGER REFERENCES ACTIVIDADES(id_actividad) ON DELETE CASCADE,
    id_trabajo INTEGER REFERENCES TRABAJOS(id_trabajo) ON DELETE CASCADE,
    PRIMARY KEY (id_actividad, id_trabajo)
);

-- 33. CONTRATO_OBRA
CREATE TABLE CONTRATO_OBRA (
    id_contrato INTEGER REFERENCES CONTRATOS(id_contrato) ON DELETE CASCADE,
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    PRIMARY KEY (id_contrato, id_obra)
);

-- 34. CONTRATO_DETALLE_TRABAJO
CREATE TABLE CONTRATO_DETALLE_TRABAJO (
    id_contrato INTEGER REFERENCES CONTRATOS(id_contrato) ON DELETE CASCADE,
    id_detalle_trabajo INTEGER REFERENCES DETALLES_TRABAJO(id_detalle_trabajo) ON DELETE CASCADE,
    PRIMARY KEY (id_contrato, id_detalle_trabajo)
);

-- 35. AREA_EMPLEADO
CREATE TABLE AREA_EMPLEADO (
    id_area INTEGER REFERENCES AREAS(id_area) ON DELETE CASCADE,
    id_empleado INTEGER REFERENCES EMPLEADOS(id_empleado) ON DELETE CASCADE,
    PRIMARY KEY (id_area, id_empleado)
);

-- 36. AREA_REQUISICION
CREATE TABLE AREA_REQUISICION (
    id_area INTEGER REFERENCES AREAS(id_area) ON DELETE CASCADE,
    id_requisicion INTEGER REFERENCES REQUISICIONES(id_requisicion) ON DELETE CASCADE,
    PRIMARY KEY (id_area, id_requisicion)
);

-- 37. REQUISICION_DETALLE
CREATE TABLE REQUISICION_DETALLE (
    id_requisicion INTEGER REFERENCES REQUISICIONES(id_requisicion) ON DELETE CASCADE,
    id_detalle_requisicion INTEGER REFERENCES DETALLES_REQUISICION(id_detalle_requisicion) ON DELETE CASCADE,
    PRIMARY KEY (id_requisicion, id_detalle_requisicion)
);

-- 38. DETALLE_MATERIAL
CREATE TABLE DETALLE_MATERIAL (
    id_detalle_requisicion INTEGER REFERENCES DETALLES_REQUISICION(id_detalle_requisicion) ON DELETE CASCADE,
    id_material INTEGER REFERENCES MATERIALES(id_material) ON DELETE CASCADE,
    PRIMARY KEY (id_detalle_requisicion, id_material)
);

-- 39. MATERIAL_MOVIMIENTO
CREATE TABLE MATERIAL_MOVIMIENTO (
    id_material INTEGER REFERENCES MATERIALES(id_material) ON DELETE CASCADE,
    id_movimiento_material INTEGER REFERENCES MOVIMIENTOS_MATERIAL(id_movimiento_material) ON DELETE CASCADE,
    PRIMARY KEY (id_material, id_movimiento_material)
);

-- 40. OBRA_BODEGA
CREATE TABLE OBRA_BODEGA (
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    id_bodega INTEGER REFERENCES BODEGAS(id_bodega) ON DELETE CASCADE,
    PRIMARY KEY (id_obra, id_bodega)
);

-- 41. BODEGA_INVENTARIO
CREATE TABLE BODEGA_INVENTARIO (
    id_bodega INTEGER REFERENCES BODEGAS(id_bodega) ON DELETE CASCADE,
    id_inventario INTEGER REFERENCES INVENTARIOS(id_inventario) ON DELETE CASCADE,
    PRIMARY KEY (id_bodega, id_inventario)
);

-- 42. INVENTARIO_MATERIAL
CREATE TABLE INVENTARIO_MATERIAL (
    id_inventario INTEGER REFERENCES INVENTARIOS(id_inventario) ON DELETE CASCADE,
    id_material INTEGER REFERENCES MATERIALES(id_material) ON DELETE CASCADE,
    PRIMARY KEY (id_inventario, id_material)
);

-- =============================================
-- 3FN - 15 TABLAS (Relaciones específicas)
-- NOTA: Mantenemos OBRA_CLIENTE para completar 56 tablas
-- =============================================

-- 43. OBRA_CLIENTE
CREATE TABLE OBRA_CLIENTE (
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    id_cliente INTEGER REFERENCES CLIENTES(id_cliente) ON DELETE CASCADE,
    PRIMARY KEY (id_obra, id_cliente)
);

-- 44. OBRA_VEHICULO
CREATE TABLE OBRA_VEHICULO (
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    id_vehiculo INTEGER REFERENCES VEHICULOS(id_vehiculo) ON DELETE CASCADE,
    PRIMARY KEY (id_obra, id_vehiculo)
);

-- 45. PROYECTO_ACTIVIDAD
CREATE TABLE PROYECTO_ACTIVIDAD (
    id_proyecto INTEGER REFERENCES PROYECTOS(id_proyecto) ON DELETE CASCADE,
    id_actividad INTEGER REFERENCES ACTIVIDADES(id_actividad) ON DELETE CASCADE,
    PRIMARY KEY (id_proyecto, id_actividad)
);

-- 45. OBRA_PRESUPUESTO
CREATE TABLE OBRA_PRESUPUESTO (
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    id_presupuesto INTEGER REFERENCES PRESUPUESTOS_OBRA(id_presupuesto) ON DELETE CASCADE,
    PRIMARY KEY (id_obra, id_presupuesto)
);

-- 46. OBRA_AVANCE
CREATE TABLE OBRA_AVANCE (
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    id_avance INTEGER REFERENCES AVANCES_OBRA(id_avance) ON DELETE CASCADE,
    PRIMARY KEY (id_obra, id_avance)
);

-- 47. OBRA_REPORTE
CREATE TABLE OBRA_REPORTE (
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    id_reporte INTEGER REFERENCES REPORTES_SEMANALES(id_reporte) ON DELETE CASCADE,
    PRIMARY KEY (id_obra, id_reporte)
);

-- 48. OBRA_BITACORA
CREATE TABLE OBRA_BITACORA (
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    id_bitacora INTEGER REFERENCES BITACORAS(id_bitacora) ON DELETE CASCADE,
    PRIMARY KEY (id_obra, id_bitacora)
);

-- 49. OBRA_INCIDENTE
CREATE TABLE OBRA_INCIDENTE (
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    id_incidente INTEGER REFERENCES INCIDENTES(id_incidente) ON DELETE CASCADE,
    PRIMARY KEY (id_obra, id_incidente)
);

-- 50. USUARIO_PERMISO
CREATE TABLE USUARIO_PERMISO (
    id_usuario INTEGER REFERENCES USUARIOS_SISTEMA(id_usuario) ON DELETE CASCADE,
    id_permiso INTEGER REFERENCES PERMISOS_ACCESO(id_permiso) ON DELETE CASCADE,
    PRIMARY KEY (id_usuario, id_permiso)
);

-- 51. USUARIO_AUDITORIA
CREATE TABLE USUARIO_AUDITORIA (
    id_usuario INTEGER REFERENCES USUARIOS_SISTEMA(id_usuario) ON DELETE CASCADE,
    id_auditoria INTEGER REFERENCES AUDITORIAS(id_auditoria) ON DELETE CASCADE,
    PRIMARY KEY (id_usuario, id_auditoria)
);

-- 52. OBRA_AUDITORIA
CREATE TABLE OBRA_AUDITORIA (
    id_obra INTEGER REFERENCES OBRAS(id_obra) ON DELETE CASCADE,
    id_auditoria INTEGER REFERENCES AUDITORIAS(id_auditoria) ON DELETE CASCADE,
    PRIMARY KEY (id_obra, id_auditoria)
);

-- 53. PROVEEDOR_EQUIPO
CREATE TABLE PROVEEDOR_EQUIPO (
    id_proveedor INTEGER REFERENCES PROVEEDORES(id_proveedor) ON DELETE CASCADE,
    id_equipo INTEGER REFERENCES EQUIPOS(id_equipo) ON DELETE CASCADE,
    PRIMARY KEY (id_proveedor, id_equipo)
);

-- 54. PROVEEDOR_MATERIAL
CREATE TABLE PROVEEDOR_MATERIAL (
    id_proveedor INTEGER REFERENCES PROVEEDORES(id_proveedor) ON DELETE CASCADE,
    id_material INTEGER REFERENCES MATERIALES(id_material) ON DELETE CASCADE,
    PRIMARY KEY (id_proveedor, id_material)
);

-- 55. EQUIPO_ASIGNACION
CREATE TABLE EQUIPO_ASIGNACION (
    id_equipo INTEGER REFERENCES EQUIPOS(id_equipo) ON DELETE CASCADE,
    id_asignacion_equipo INTEGER REFERENCES ASIGNACIONES_EQUIPO(id_asignacion_equipo) ON DELETE CASCADE,
    PRIMARY KEY (id_equipo, id_asignacion_equipo)
);

-- 56. PROYECTO_ARCHIVO
CREATE TABLE PROYECTO_ARCHIVO (
    id_proyecto INTEGER REFERENCES PROYECTOS(id_proyecto) ON DELETE CASCADE,
    id_archivo INTEGER REFERENCES ARCHIVOS_ADJUNTOS(id_archivo) ON DELETE CASCADE,
    PRIMARY KEY (id_proyecto, id_archivo)
);

COMMIT;

