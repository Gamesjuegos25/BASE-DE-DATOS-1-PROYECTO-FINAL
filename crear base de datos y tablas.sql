create database BASEdeDATOSpf;

USE BASEdeDATOSpf;

-- CLIENTE
CREATE TABLE Cliente (
  id_cliente INT PRIMARY KEY IDENTITY(1,1),
  nombre VARCHAR(100),
  contacto VARCHAR(100),
  tipo_cliente VARCHAR(50)
);

-- OBRA
CREATE TABLE Obra (
  id_obra INT PRIMARY KEY IDENTITY(1,1),
  nombre VARCHAR(100),
  ubicacion VARCHAR(150),
  tipo VARCHAR(50),
  estado VARCHAR(50),
  id_cliente INT FOREIGN KEY REFERENCES Cliente(id_cliente)
);

-- PRESUPUESTO DE OBRA
CREATE TABLE PresupuestoObra (
  id_presupuesto INT PRIMARY KEY IDENTITY(1,1),
  id_obra INT FOREIGN KEY REFERENCES Obra(id_obra),
  monto_estimado DECIMAL(12,2),
  fecha DATE
);

-- AVANCE DE OBRA
CREATE TABLE AvanceObra (
  id_avance INT PRIMARY KEY IDENTITY(1,1),
  id_obra INT FOREIGN KEY REFERENCES Obra(id_obra),
  porcentaje_fisico DECIMAL(5,2),
  porcentaje_financiero DECIMAL(5,2),
  fecha DATE
);

-- REPORTE SEMANAL
CREATE TABLE ReporteSemanal (
  id_reporte INT PRIMARY KEY IDENTITY(1,1),
  id_obra INT FOREIGN KEY REFERENCES Obra(id_obra),
  semana INT,
  resumen TEXT,
  fecha DATE
);

-- ÁREA
CREATE TABLE Area (
  id_area INT PRIMARY KEY IDENTITY(1,1),
  nombre VARCHAR(100),
  id_obra INT FOREIGN KEY REFERENCES Obra(id_obra)
);

-- PROYECTO
CREATE TABLE Proyecto (
  id_proyecto INT PRIMARY KEY IDENTITY(1,1),
  id_obra INT FOREIGN KEY REFERENCES Obra(id_obra),
  nombre VARCHAR(100),
  fecha_inicio DATE,
  fecha_fin DATE,
  estado VARCHAR(50)
);

-- ACTIVIDAD
CREATE TABLE Actividad (
  id_actividad INT PRIMARY KEY IDENTITY(1,1),
  id_area INT FOREIGN KEY REFERENCES Area(id_area),
  nombre VARCHAR(100),
  descripcion TEXT,
  fecha_programada DATE,
  estado VARCHAR(50)
);

-- EMPLEADO
CREATE TABLE Empleado (
  id_empleado INT PRIMARY KEY IDENTITY(1,1),
  nombre VARCHAR(100),
  tipo VARCHAR(50),
  salario_fijo DECIMAL(10,2),
  estado VARCHAR(50)
);

-- CONTRATO
CREATE TABLE Contrato (
  id_contrato INT PRIMARY KEY IDENTITY(1,1),
  id_empleado INT FOREIGN KEY REFERENCES Empleado(id_empleado),
  id_area INT FOREIGN KEY REFERENCES Area(id_area),
  fecha_inicio DATE,
  fecha_fin DATE,
  tipo_pago VARCHAR(50),
  estado VARCHAR(50)
);

-- TRABAJO
CREATE TABLE Trabajo (
  id_trabajo INT PRIMARY KEY IDENTITY(1,1),
  descripcion TEXT,
  unidad VARCHAR(20),
  precio_unitario DECIMAL(10,2),
  tipo_trabajo VARCHAR(50)
);

-- DETALLE DE TRABAJO
CREATE TABLE DetalleTrabajo (
  id_detalle INT PRIMARY KEY IDENTITY(1,1),
  id_contrato INT FOREIGN KEY REFERENCES Contrato(id_contrato),
  id_trabajo INT FOREIGN KEY REFERENCES Trabajo(id_trabajo),
  cantidad DECIMAL(10,2),
  total DECIMAL(12,2)
);

-- PAGO A EMPLEADO
CREATE TABLE PagoEmpleado (
  id_pago INT PRIMARY KEY IDENTITY(1,1),
  id_empleado INT FOREIGN KEY REFERENCES Empleado(id_empleado),
  fecha DATE,
  monto DECIMAL(10,2),
  estado VARCHAR(50)
);

-- PROVEEDOR
CREATE TABLE Proveedor (
  id_proveedor INT PRIMARY KEY IDENTITY(1,1),
  nombre VARCHAR(100),
  contacto VARCHAR(100)
);

-- MATERIAL
CREATE TABLE Material (
  id_material INT PRIMARY KEY IDENTITY(1,1),
  nombre VARCHAR(100),
  unidad VARCHAR(20),
  precio_unitario DECIMAL(10,2),
  tipo_material VARCHAR(50),
  estado VARCHAR(50),
  id_proveedor INT FOREIGN KEY REFERENCES Proveedor(id_proveedor)
);

-- REQUISICIÓN
CREATE TABLE Requisicion (
  id_requisicion INT PRIMARY KEY IDENTITY(1,1),
  id_area INT FOREIGN KEY REFERENCES Area(id_area),
  fecha DATE,
  estado VARCHAR(50)
);

-- DETALLE DE REQUISICIÓN
CREATE TABLE DetalleRequisicion (
  id_detalle INT PRIMARY KEY IDENTITY(1,1),
  id_requisicion INT FOREIGN KEY REFERENCES Requisicion(id_requisicion),
  id_material INT FOREIGN KEY REFERENCES Material(id_material),
  cantidad DECIMAL(10,2)
);

-- BODEGA
CREATE TABLE Bodega (
  id_bodega INT PRIMARY KEY IDENTITY(1,1),
  id_obra INT FOREIGN KEY REFERENCES Obra(id_obra),
  responsable VARCHAR(100)
);

-- INVENTARIO
CREATE TABLE Inventario (
  id_inventario INT PRIMARY KEY IDENTITY(1,1),
  id_bodega INT FOREIGN KEY REFERENCES Bodega(id_bodega),
  id_material INT FOREIGN KEY REFERENCES Material(id_material),
  cantidad DECIMAL(10,2)
);

-- MOVIMIENTO DE MATERIAL
CREATE TABLE MovimientoMaterial (
  id_movimiento INT PRIMARY KEY IDENTITY(1,1),
  id_material INT FOREIGN KEY REFERENCES Material(id_material),
  tipo VARCHAR(50),
  fecha DATE,
  cantidad DECIMAL(10,2),
  origen VARCHAR(100),
  destino VARCHAR(100)
);

-- VEHÍCULO
CREATE TABLE Vehiculo (
  id_vehiculo INT PRIMARY KEY IDENTITY(1,1),
  placa VARCHAR(20),
  tipo VARCHAR(50),
  estado VARCHAR(50),
  id_obra INT FOREIGN KEY REFERENCES Obra(id_obra)
);

-- EQUIPO
CREATE TABLE Equipo (
  id_equipo INT PRIMARY KEY IDENTITY(1,1),
  nombre VARCHAR(100),
  tipo VARCHAR(50),
  estado VARCHAR(50)
);

-- ASIGNACIÓN DE EQUIPO
CREATE TABLE AsignacionEquipo (
  id_asignacion INT PRIMARY KEY IDENTITY(1,1),
  id_empleado INT FOREIGN KEY REFERENCES Empleado(id_empleado),
  id_equipo INT FOREIGN KEY REFERENCES Equipo(id_equipo),
  fecha_inicio DATE,
  fecha_fin DATE
);

-- USUARIO DEL SISTEMA
CREATE TABLE UsuarioSistema (
  id_usuario INT PRIMARY KEY IDENTITY(1,1),
  nombre VARCHAR(100),
  rol VARCHAR(50),
  correo VARCHAR(100),
  contraseña VARCHAR(100),
  estado VARCHAR(50)
);

-- PERMISOS DE ACCESO
CREATE TABLE PermisoAcceso (
  id_permiso INT PRIMARY KEY IDENTITY(1,1),
  id_usuario INT FOREIGN KEY REFERENCES UsuarioSistema(id_usuario),
  modulo VARCHAR(50),
  nivel_acceso VARCHAR(50)
);

-- AUDITORÍA
CREATE TABLE Auditoria (
  id_auditoria INT PRIMARY KEY IDENTITY(1,1),
  id_usuario INT FOREIGN KEY REFERENCES UsuarioSistema(id_usuario),
  accion VARCHAR(100),
  fecha DATETIME,
  detalle TEXT
);

-- BITÁCORA
CREATE TABLE Bitacora (
  id_bitacora INT PRIMARY KEY IDENTITY(1,1),
  id_obra INT FOREIGN KEY REFERENCES Obra(id_obra),
  fecha DATE,
  observaciones TEXT
);

-- INCIDENTE
CREATE TABLE Incidente (
  id_incidente INT PRIMARY KEY IDENTITY(1,1),
  id_obra INT FOREIGN KEY REFERENCES Obra(id_obra),
  fecha DATE,
  descripcion TEXT,
  estado VARCHAR(50)
);

-- FACTURA DE PROVEEDOR
CREATE TABLE FacturaProveedor (
  id_factura INT PRIMARY KEY IDENTITY(1,1),
  id_proveedor INT FOREIGN KEY REFERENCES Proveedor(id_proveedor),
  fecha DATE,
  monto DECIMAL(12,2),
  estado VARCHAR(50)
);

-- ARCHIVO ADJUNTO
CREATE TABLE ArchivoAdjunto (
  id_archivo INT PRIMARY KEY IDENTITY(1,1),
  nombre VARCHAR(100),
  tipo VARCHAR(50),
  ruta TEXT,
  id_obra INT FOREIGN KEY REFERENCES Obra(id_obra),
  id_proyecto INT FOREIGN KEY REFERENCES Proyecto(id_proyecto)
);

-- EMPLEADO–ÁREA (Relación N:N → 4FN)
CREATE TABLE EmpleadoArea (
  id_empleado INT FOREIGN KEY REFERENCES Empleado(id_empleado),
  id_area INT FOREIGN KEY REFERENCES Area(id_area),
  PRIMARY KEY (id_empleado, id_area)
);
