-- =================================================================
-- SCRIPT DE INSERCIÓN DE DATOS PARA EL SISTEMA DE CONSTRUCTORA
-- =================================================================
-- Este script inserta todos los datos de ejemplo necesarios para
-- el funcionamiento del sistema web de consultas de la constructora
-- =================================================================

USE BASEdeDATOSpf;

-- Limpiar tablas existentes (opcional, para reiniciar datos)
-- TRUNCATE TABLE ArchivoAdjunto;
-- TRUNCATE TABLE EmpleadoArea;
-- TRUNCATE TABLE Auditoria;
-- TRUNCATE TABLE PermisoAcceso;
-- TRUNCATE TABLE UsuarioSistema;
-- TRUNCATE TABLE AsignacionEquipo;
-- TRUNCATE TABLE Equipo;
-- TRUNCATE TABLE Vehiculo;
-- TRUNCATE TABLE MovimientoMaterial;
-- TRUNCATE TABLE Inventario;
-- TRUNCATE TABLE Bodega;
-- TRUNCATE TABLE DetalleRequisicion;
-- TRUNCATE TABLE Requisicion;
-- TRUNCATE TABLE Material;
-- TRUNCATE TABLE Proveedor;
-- TRUNCATE TABLE PagoEmpleado;
-- TRUNCATE TABLE DetalleTrabajo;
-- TRUNCATE TABLE Trabajo;
-- TRUNCATE TABLE Contrato;
-- TRUNCATE TABLE Empleado;
-- TRUNCATE TABLE Actividad;
-- TRUNCATE TABLE Proyecto;
-- TRUNCATE TABLE Area;
-- TRUNCATE TABLE ReporteSemanal;
-- TRUNCATE TABLE AvanceObra;
-- TRUNCATE TABLE PresupuestoObra;
-- TRUNCATE TABLE Obra;
-- TRUNCATE TABLE Cliente;

-- =================================================================
-- 1. INSERTAR CLIENTES
-- =================================================================
INSERT INTO Cliente (nombre, contacto, tipo_cliente) VALUES
('Grupo Inmobiliario Central', 'Juan Pérez - 2345-6789', 'Corporativo'),
('Desarrollos del Sur S.A.', 'María García - 2456-7890', 'Empresa'),
('Familia Rodríguez', 'Carlos Rodríguez - 2567-8901', 'Particular'),
('Constructora Maya', 'Ana López - 2678-9012', 'Corporativo'),
('Inversiones Guatemala', 'Pedro Morales - 2789-0123', 'Empresa');

-- =================================================================
-- 2. INSERTAR OBRAS
-- =================================================================
INSERT INTO Obra (nombre, ubicacion, tipo, estado, id_cliente) VALUES
('Residencial Las Flores', 'Zona 14, Guatemala', 'Casas habitacionales', 'En Proceso', 1),
('Torre Empresarial Centro', 'Zona 10, Guatemala', 'Edificios de oficina', 'En Proceso', 2),
('Bodega Industrial Norte', 'Villa Nueva', 'Bodegas', 'Completada', 4),
('Condominios El Bosque', 'Zona 16, Guatemala', 'Edificios habitacionales', 'En Proceso', 3),
('Centro Comercial Plaza Sur', 'Escuintla', 'Edificios de oficina', 'Suspendida', 5);

-- =================================================================
-- 3. INSERTAR PRESUPUESTOS DE OBRA
-- =================================================================
INSERT INTO PresupuestoObra (id_obra, monto_estimado, fecha) VALUES
(1, 2500000.00, '2024-01-15'),
(2, 8500000.00, '2024-02-20'),
(3, 1200000.00, '2023-10-10'),
(4, 4500000.00, '2024-06-01'),
(5, 12000000.00, '2024-03-15');

-- =================================================================
-- 4. INSERTAR AVANCES DE OBRA
-- =================================================================
INSERT INTO AvanceObra (id_obra, porcentaje_fisico, porcentaje_financiero, fecha) VALUES
(1, 65.50, 58.20, '2024-09-30'),
(2, 40.30, 45.70, '2024-09-30'),
(3, 100.00, 100.00, '2024-05-30'),
(4, 25.80, 30.10, '2024-09-30'),
(5, 15.20, 12.90, '2024-09-30');

-- =================================================================
-- 5. INSERTAR REPORTES SEMANALES
-- =================================================================
INSERT INTO ReporteSemanal (id_obra, semana, resumen, fecha) VALUES
(1, 38, 'Avance significativo en cimentación de casas A6-A10. Se completó excavación y se inició armado de hierro.', '2024-09-22'),
(2, 38, 'Continuación de estructura del piso 8. Problemas menores con suministro de cemento.', '2024-09-22'),
(1, 39, 'Fundición de losas en casas A6-A8. Inicio de mampostería en casas A1-A3.', '2024-09-29'),
(4, 39, 'Excavación completada. Preparación para inicio de cimentación próxima semana.', '2024-09-29');

-- =================================================================
-- 6. INSERTAR ÁREAS DE TRABAJO
-- =================================================================
INSERT INTO Area (nombre, id_obra) VALUES
('Cimentación', 1),
('Estructura', 1),
('Mampostería', 1),
('Cimentación', 2),
('Estructura', 2),
('Acabados', 3),
('Cimentación', 4),
('Instalaciones', 5);

-- =================================================================
-- 7. INSERTAR PROYECTOS
-- =================================================================
INSERT INTO Proyecto (id_obra, nombre, fecha_inicio, fecha_fin, estado) VALUES
(1, 'Fase 1 - Casas A1-A10', '2024-01-15', '2024-08-15', 'En Proceso'),
(1, 'Fase 2 - Casas B1-B8', '2024-05-01', '2024-12-01', 'En Proceso'),
(2, 'Estructura Principal', '2024-02-20', '2024-11-30', 'En Proceso'),
(3, 'Nave Industrial', '2023-10-10', '2024-05-30', 'Completado'),
(4, 'Torre A', '2024-06-01', '2025-03-01', 'En Proceso');

-- =================================================================
-- 8. INSERTAR ACTIVIDADES
-- =================================================================
INSERT INTO Actividad (id_area, nombre, descripcion, fecha_programada, estado) VALUES
(1, 'Excavación general', 'Excavación para cimentación de casas A1-A5', '2024-01-20', 'Completado'),
(1, 'Armado de hierro', 'Colocación de varillas para cimientos', '2024-02-05', 'En Proceso'),
(2, 'Fundición columnas', 'Fundición de columnas principales', '2024-03-10', 'En Proceso'),
(3, 'Levantado de paredes', 'Mampostería primer nivel', '2024-04-15', 'Planificado'),
(4, 'Excavación torre', 'Excavación para cimientos de torre', '2024-02-25', 'Completado'),
(5, 'Estructura nivel 8', 'Construcción piso 8 de torre', '2024-09-20', 'En Proceso'),
(6, 'Instalación puertas', 'Colocación de puertas finales', '2024-05-15', 'Completado'),
(7, 'Preparación terreno', 'Nivelación y preparación', '2024-06-10', 'Completado');

-- =================================================================
-- 9. INSERTAR EMPLEADOS
-- =================================================================
INSERT INTO Empleado (nombre, tipo, salario_fijo, estado) VALUES
('Ing. Roberto Méndez', 'Ingeniero', 15000.00, 'Activo'),
('Arq. Laura Castillo', 'Arquitecto', 14000.00, 'Activo'),
('José Hernández', 'Albañil', 0.00, 'Activo'),
('Carmen Vásquez', 'Administrativo', 8500.00, 'Activo'),
('Miguel Torres', 'Albañil', 0.00, 'Activo'),
('Ing. Sandra López', 'Ingeniero', 16500.00, 'Activo');

-- =================================================================
-- 10. INSERTAR CONTRATOS
-- =================================================================
INSERT INTO Contrato (id_empleado, id_area, fecha_inicio, fecha_fin, tipo_pago, estado) VALUES
(1, 1, '2024-01-15', '2024-12-31', 'Salario Fijo', 'Activo'),
(1, 4, '2024-02-20', '2024-12-31', 'Salario Fijo', 'Activo'),
(2, 2, '2024-01-15', '2024-12-31', 'Salario Fijo', 'Activo'),
(2, 5, '2024-02-20', '2024-12-31', 'Salario Fijo', 'Activo'),
(3, 3, '2024-03-01', '2024-10-31', 'Por Trabajo', 'Activo'),
(4, 1, '2024-01-01', '2024-12-31', 'Salario Fijo', 'Activo'),
(5, 1, '2024-01-15', '2024-11-30', 'Por Trabajo', 'Activo'),
(5, 3, '2024-04-01', '2024-12-31', 'Por Trabajo', 'Activo'),
(6, 7, '2024-06-01', '2025-03-31', 'Salario Fijo', 'Activo');

-- =================================================================
-- 11. INSERTAR TIPOS DE TRABAJO
-- =================================================================
INSERT INTO Trabajo (descripcion, unidad, precio_unitario, tipo_trabajo) VALUES
('Excavación manual', 'm³', 25.00, 'Movimiento de tierras'),
('Armado de hierro', 'quintal', 45.00, 'Estructura'),
('Levantado de pared', 'm²', 50.00, 'Mampostería'),
('Fundición de concreto', 'm³', 120.00, 'Estructura'),
('Instalación eléctrica', 'punto', 85.00, 'Instalaciones'),
('Colocación de azulejo', 'm²', 65.00, 'Acabados');

-- =================================================================
-- 12. INSERTAR DETALLES DE TRABAJO
-- =================================================================
INSERT INTO DetalleTrabajo (id_contrato, id_trabajo, cantidad, total) VALUES
(3, 1, 45.50, 1137.50),
(5, 3, 65.00, 3250.00),
(7, 1, 28.50, 712.50),
(8, 3, 57.00, 2850.00);

-- =================================================================
-- 13. INSERTAR PAGOS A EMPLEADOS
-- =================================================================
INSERT INTO PagoEmpleado (id_empleado, fecha, monto, estado) VALUES
(1, '2024-09-30', 15000.00, 'Pagado'),
(2, '2024-09-30', 14000.00, 'Pagado'),
(3, '2024-09-25', 3250.00, 'Pagado'),
(4, '2024-09-30', 8500.00, 'Pagado'),
(5, '2024-09-28', 2850.00, 'Pagado'),
(6, '2024-09-30', 16500.00, 'Pagado');

-- =================================================================
-- 14. INSERTAR PROVEEDORES
-- =================================================================
INSERT INTO Proveedor (nombre, contacto) VALUES
('Cementos Guatemala', 'ventas@cemguat.com - 2234-5678'),
('Aceros del Norte', 'info@aceronorte.com - 2345-6789'),
('Ferretería El Constructor', 'constructor@gmail.com - 2456-7890'),
('Ladrillos San José', 'sanjose@ladrillos.com - 2567-8901'),
('Materiales Premium', 'premium@materiales.com - 2678-9012');

-- =================================================================
-- 15. INSERTAR MATERIALES
-- =================================================================
INSERT INTO Material (nombre, unidad, precio_unitario, tipo_material, estado, id_proveedor) VALUES
('Cemento Portland', 'Saco', 85.00, 'Cemento', 'Disponible', 1),
('Varilla #4', 'Quintal', 650.00, 'Acero', 'Disponible', 2),
('Ladrillo tayuyo', 'Millares', 850.00, 'Ladrillo', 'Disponible', 4),
('Arena de río', 'm³', 180.00, 'Agregados', 'Disponible', 3),
('Martillo de uña', 'Unidad', 125.00, 'Herramientas', 'Disponible', 3),
('Piedrín 3/4', 'm³', 220.00, 'Agregados', 'Disponible', 5);

-- =================================================================
-- 16. INSERTAR REQUISICIONES
-- =================================================================
INSERT INTO Requisicion (id_area, fecha, estado) VALUES
(1, '2024-09-15', 'Aprobada'),
(2, '2024-09-20', 'Aprobada'),
(4, '2024-09-18', 'Aprobada'),
(3, '2024-09-22', 'Pendiente');

-- =================================================================
-- 17. INSERTAR DETALLES DE REQUISICIÓN
-- =================================================================
INSERT INTO DetalleRequisicion (id_requisicion, id_material, cantidad) VALUES
(1, 1, 50.00),
(1, 4, 15.50),
(2, 2, 25.00),
(2, 1, 35.00),
(3, 1, 80.00),
(3, 3, 12.00),
(4, 6, 20.00);

-- =================================================================
-- 18. INSERTAR BODEGAS
-- =================================================================
INSERT INTO Bodega (id_obra, responsable) VALUES
(1, 'Carlos Méndez'),
(2, 'Ana Morales'),
(3, 'Luis Herrera'),
(4, 'María Santos'),
(5, 'Jorge Castillo');

-- =================================================================
-- 19. INSERTAR INVENTARIO
-- =================================================================
INSERT INTO Inventario (id_bodega, id_material, cantidad) VALUES
(1, 1, 85.0),
(1, 2, 45.5),
(2, 1, 120.0),
(2, 3, 15.0),
(3, 4, 25.5),
(4, 6, 18.0);

-- =================================================================
-- 20. INSERTAR MOVIMIENTOS DE MATERIAL
-- =================================================================
INSERT INTO MovimientoMaterial (id_material, tipo, fecha, cantidad, origen, destino) VALUES
(1, 'Ingreso', '2024-09-20', 50.0, 'Cementos Guatemala', 'Bodega Obra 1'),
(2, 'Salida', '2024-09-22', 15.5, 'Bodega Obra 1', 'Área Cimentación'),
(1, 'Ingreso', '2024-09-25', 80.0, 'Cementos Guatemala', 'Bodega Obra 2'),
(4, 'Salida', '2024-09-23', 8.5, 'Bodega Obra 3', 'Área Acabados'),
(6, 'Ingreso', '2024-09-21', 25.0, 'Materiales Premium', 'Bodega Obra 4');

-- =================================================================
-- 21. INSERTAR VEHÍCULOS
-- =================================================================
INSERT INTO Vehiculo (placa, tipo, estado, id_obra) VALUES
('P-123ABC', 'Pickup', 'Operativo', 1),
('C-456DEF', 'Camión', 'Operativo', 2),
('M-789GHI', 'Maquinaria', 'En Mantenimiento', 1),
('P-321JKL', 'Pickup', 'Operativo', 4),
('C-654MNO', 'Camión', 'Operativo', 3);

-- =================================================================
-- 22. INSERTAR EQUIPOS
-- =================================================================
INSERT INTO Equipo (nombre, tipo, estado) VALUES
('Mezcladora de concreto', 'Maquinaria', 'Disponible'),
('Taladro percutor', 'Herramientas', 'Asignado'),
('Nivel láser', 'Medición', 'Asignado'),
('Cortadora de azulejo', 'Herramientas', 'En Mantenimiento'),
('Teodolito', 'Medición', 'Disponible');

-- =================================================================
-- 23. INSERTAR ASIGNACIONES DE EQUIPO
-- =================================================================
INSERT INTO AsignacionEquipo (id_empleado, id_equipo, fecha_inicio, fecha_fin) VALUES
(3, 2, '2024-09-15', '2024-10-15'),
(1, 3, '2024-09-01', '2024-11-30');

-- =================================================================
-- 24. INSERTAR USUARIOS DEL SISTEMA
-- =================================================================
INSERT INTO UsuarioSistema (nombre, rol, correo, contraseña, estado) VALUES
('Administrador Sistema', 'Admin', 'admin@constructora.com', 'admin123', 'Activo'),
('Roberto Méndez', 'Ingeniero', 'rmendez@constructora.com', 'ing123', 'Activo'),
('Laura Castillo', 'Arquitecto', 'lcastillo@constructora.com', 'arq123', 'Activo'),
('Carmen Vásquez', 'Administrativo', 'cvasquez@constructora.com', 'adm123', 'Activo');

-- =================================================================
-- 25. INSERTAR PERMISOS DE ACCESO
-- =================================================================
INSERT INTO PermisoAcceso (id_usuario, modulo, nivel_acceso) VALUES
(1, 'Todos', 'Total'),
(2, 'Obras', 'Lectura/Escritura'),
(2, 'Proyectos', 'Lectura/Escritura'),
(2, 'Empleados', 'Lectura'),
(3, 'Obras', 'Lectura/Escritura'),
(3, 'Proyectos', 'Lectura/Escritura'),
(4, 'Reportes', 'Lectura/Escritura'),
(4, 'Empleados', 'Lectura/Escritura'),
(4, 'Materiales', 'Lectura');

-- =================================================================
-- 26. INSERTAR FACTURAS DE PROVEEDORES
-- =================================================================
INSERT INTO FacturaProveedor (id_proveedor, fecha, monto, estado) VALUES
(1, '2024-09-20', 4250.00, 'Pagada'),
(2, '2024-09-18', 29250.00, 'Pendiente'),
(4, '2024-09-15', 12750.00, 'Pagada'),
(3, '2024-09-22', 2890.00, 'Pagada'),
(5, '2024-09-25', 5500.00, 'Pendiente');

-- =================================================================
-- 27. INSERTAR BITÁCORA
-- =================================================================
INSERT INTO Bitacora (id_obra, fecha, observaciones) VALUES
(1, '2024-09-30', 'Avance normal en todas las áreas. Clima favorable.'),
(2, '2024-09-30', 'Retraso menor en piso 8 por falta de material.'),
(4, '2024-09-30', 'Inicio de excavación según cronograma.'),
(3, '2024-05-30', 'Obra completada satisfactoriamente.');

-- =================================================================
-- 28. INSERTAR INCIDENTES
-- =================================================================
INSERT INTO Incidente (id_obra, fecha, descripcion, estado) VALUES
(2, '2024-09-25', 'Retraso en entrega de cemento por parte del proveedor', 'Resuelto'),
(1, '2024-09-28', 'Lluvias intensas pararon trabajo por 2 horas', 'Cerrado'),
(4, '2024-09-20', 'Falla menor en equipo de excavación', 'En Seguimiento');

-- =================================================================
-- 29. INSERTAR ARCHIVOS ADJUNTOS
-- =================================================================
INSERT INTO ArchivoAdjunto (nombre, tipo, ruta, id_obra, id_proyecto) VALUES
('Planos_Residencial_LasFlores.pdf', 'Plano', '/documentos/obras/1/planos/', 1, 1),
('Cronograma_Torre_Centro.xlsx', 'Cronograma', '/documentos/obras/2/cronogramas/', 2, 3),
('Presupuesto_Condominios_Bosque.pdf', 'Presupuesto', '/documentos/obras/4/presupuestos/', 4, 5),
('Fotos_Avance_Bodega_Norte.zip', 'Fotografía', '/documentos/obras/3/fotos/', 3, 4);

-- =================================================================
-- 30. INSERTAR RELACIÓN EMPLEADO-ÁREA (N:N)
-- =================================================================
INSERT INTO EmpleadoArea (id_empleado, id_area) VALUES
(1, 1),
(1, 4),
(2, 2),
(2, 5),
(3, 3),
(4, 1),
(5, 1),
(5, 3),
(6, 7);

-- =================================================================
-- 31. INSERTAR AUDITORÍA
-- =================================================================
INSERT INTO Auditoria (id_usuario, accion, fecha, detalle) VALUES
(1, 'Login Sistema', '2024-09-30 08:00:00', 'Acceso al sistema administrativo'),
(2, 'Consulta Obras', '2024-09-30 09:15:00', 'Revisión de avance Obra ID: 1'),
(3, 'Actualizar Proyecto', '2024-09-30 10:30:00', 'Modificación estado Proyecto ID: 3'),
(4, 'Generar Reporte', '2024-09-30 14:45:00', 'Reporte semanal Obra ID: 2'),
(1, 'Backup Datos', '2024-09-30 18:00:00', 'Respaldo automático de base de datos');

-- =================================================================
-- FIN DEL SCRIPT DE INSERCIÓN
-- =================================================================

PRINT 'Datos insertados correctamente en la base de datos BASEdeDATOSpf';
PRINT 'Total de registros insertados:';
PRINT '- Clientes: 5';
PRINT '- Obras: 5';
PRINT '- Empleados: 6';
PRINT '- Materiales: 6';
PRINT '- Proveedores: 5';
PRINT '- Y muchos más registros relacionados...';
PRINT '';
PRINT 'La base de datos está lista para conectarse con el sistema web.';