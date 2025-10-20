-- =====================================================
-- SCRIPT DE DATOS REALISTAS - SISTEMA INTEGRAL CONSTRUCTORA
-- Demuestra el uso técnico de las 56 tablas
-- Escenario: Construcción de Edificio Residencial "Torres del Norte"
-- =====================================================

-- NOTA: Ejecutar después de CREAR_TABLAS_OBLIGATORIO.sql

BEGIN;

-- =====================================================
-- 1. MÓDULO COMERCIAL Y CLIENTES
-- =====================================================

-- CLIENTES
INSERT INTO CLIENTES (nombre_cliente, documento_cliente, telefono_cliente, email_cliente, direccion_cliente, contacto_cliente, tipo_cliente) VALUES
('Inversiones La Montaña SAS', '900.123.456-7', '+57-301-234-5678', 'contacto@lamontana.com', 'Av. El Poblado #45-67, Medellín', 'Ana María Jiménez', 'Corporativo'),
('Constructora Urbana Ltda', '800.987.654-3', '+57-302-987-6543', 'proyectos@urbana.com', 'Calle 72 #10-34, Bogotá', 'Carlos Mendoza', 'Empresarial'),
('Familia Rodríguez González', '1.234.567.890', '+57-315-456-7890', 'rodriguez.familia@email.com', 'Carrera 15 #23-45, Bucaramanga', 'Luis Rodríguez', 'Residencial');

-- CONTRATOS
INSERT INTO CONTRATOS (fecha_inicio_contrato, fecha_fin_contrato, tipo_pago_contrato) VALUES
('2024-01-15', '2024-12-31', 'Mensual progresivo'),
('2024-02-01', '2025-01-31', 'Por hitos de avance'),
('2024-03-10', '2024-11-30', 'Pago único al 50% y saldo contra entrega');

-- OBRAS (Con relación obligatoria a clientes)
INSERT INTO OBRAS (nombre_obra, descripcion_obra, tipo_obra, estado_obra, ubicacion_obra, fecha_inicio, fecha_fin, valor_obra, id_cliente) VALUES
('Torres del Norte - Fase 1', 'Construcción de 2 torres residenciales de 15 pisos cada una con 120 apartamentos', 'Residencial', 'En Progreso', 'Zona Norte, Barranquilla', '2024-01-15', '2024-12-31', 8500000000.00, 1),
('Centro Comercial Urbano', 'Centro comercial de 3 pisos con 80 locales comerciales y parqueadero', 'Comercial', 'Planeación', 'Centro, Bogotá', '2024-02-01', '2025-01-31', 12000000000.00, 2),
('Casa Campestre Los Nogales', 'Casa de campo con piscina, jardines y zona de BBQ', 'Residencial', 'En Progreso', 'Vereda Los Nogales, Bucaramanga', '2024-03-10', '2024-11-30', 450000000.00, 3);

-- =====================================================
-- 2. MÓDULO GESTIÓN DE PROYECTOS
-- =====================================================

-- PROYECTOS
INSERT INTO PROYECTOS (nombre_proyecto, fecha_inicio_proyecto, fecha_fin_proyecto, estado_proyecto) VALUES
('Desarrollo Habitacional Norte', '2024-01-01', '2025-06-30', 'En Ejecución'),
('Expansión Comercial Centro', '2024-02-01', '2025-02-28', 'Planeación'),
('Proyectos Residenciales Rurales', '2024-03-01', '2024-12-31', 'En Ejecución');

-- AREAS
INSERT INTO AREAS (nombre_area) VALUES
('Estructura y Cimentación'),
('Mampostería y Acabados'),
('Instalaciones Eléctricas'),
('Instalaciones Hidráulicas'),
('Acabados y Pintura'),
('Jardines y Exteriores'),
('Supervisión Técnica'),
('Control de Calidad');

-- ACTIVIDADES
INSERT INTO ACTIVIDADES (nombre_actividad, descripcion_actividad, fecha_programada_actividad) VALUES
('Excavación y Cimentación', 'Excavación del terreno y fundición de cimientos', '2024-01-20'),
('Estructura de Concreto', 'Levantamiento de estructura en concreto reforzado', '2024-02-15'),
('Instalación de Tuberías', 'Instalación de sistema hidráulico y sanitario', '2024-03-01'),
('Cableado Eléctrico', 'Instalación de sistema eléctrico completo', '2024-03-15'),
('Mampostería General', 'Levantamiento de muros y tabiques', '2024-04-01'),
('Aplicación de Acabados', 'Enchapes, pisos y acabados generales', '2024-05-01'),
('Pintura y Detalles', 'Pintura interior y exterior, detalles finales', '2024-06-01'),
('Paisajismo', 'Diseño e implementación de jardines', '2024-06-15');

-- TRABAJOS
INSERT INTO TRABAJOS (descripcion_trabajo, precio_unitario_trabajo, unidad_trabajo) VALUES
('Excavación manual', 45000.00, 'metro cúbico'),
('Fundición de concreto', 350000.00, 'metro cúbico'),
('Instalación punto hidráulico', 85000.00, 'unidad'),
('Instalación punto eléctrico', 65000.00, 'unidad'),
('Mampostería ladrillo', 95000.00, 'metro cuadrado'),
('Enchape cerámico', 120000.00, 'metro cuadrado'),
('Pintura dos manos', 25000.00, 'metro cuadrado'),
('Siembra de césped', 35000.00, 'metro cuadrado');

-- =====================================================
-- 3. MÓDULO RECURSOS HUMANOS
-- =====================================================

-- EMPLEADOS
INSERT INTO EMPLEADOS (nombre_empleado, tipo_empleado, salario_fijo_empleado) VALUES
('Carlos Martínez López', 'Ingeniero Civil', 4500000.00),
('Ana Sofía Herrera', 'Arquitecta', 4200000.00),
('Miguel Ángel Ruiz', 'Maestro de Obra', 2800000.00),
('Javier Morales Castro', 'Electricista', 2500000.00),
('Pedro Pablo Sánchez', 'Plomero', 2400000.00),
('Luisa Fernanda Torres', 'Supervisora de Calidad', 3200000.00),
('Roberto Carlos Díaz', 'Operario General', 1800000.00),
('María Elena Vargas', 'Administradora de Obra', 3800000.00);

-- DETALLES_TRABAJO
INSERT INTO DETALLES_TRABAJO (cantidad_trabajo, total_trabajo) VALUES
(150.5, 6772500.00),  -- Excavación
(45.2, 15820000.00),  -- Concreto
(28.0, 2380000.00),   -- Puntos hidráulicos
(35.0, 2275000.00),   -- Puntos eléctricos
(180.3, 17128500.00), -- Mampostería
(95.7, 11484000.00),  -- Enchapes
(250.8, 6270000.00),  -- Pintura
(120.0, 4200000.00);  -- Césped

-- =====================================================
-- 4. MÓDULO SUPPLY CHAIN
-- =====================================================

-- PROVEEDORES
INSERT INTO PROVEEDORES (nombre_proveedor, contacto_proveedor) VALUES
('Cementos del Caribe S.A.', 'Departamento Comercial - Tel: 310-555-0101'),
('Hierros y Aceros del Norte', 'Ing. Patricia Luna - Tel: 320-555-0202'),
('Materiales Eléctricos La Central', 'Carlos Pérez - Tel: 315-555-0303'),
('Tuberías y Conexiones Hídro', 'María Gómez - Tel: 301-555-0404'),
('Acabados Premium Ltda', 'Roberto Silva - Tel: 318-555-0505'),
('Maquinaria Pesada del Atlántico', 'Área de Alquileres - Tel: 312-555-0606'),
('Transportes y Logística Norte', 'Coordinación - Tel: 305-555-0707');

-- MATERIALES
INSERT INTO MATERIALES (nombre_material, unidad_material, precio_unitario_material) VALUES
('Cemento Portland Tipo I', 'Bulto 50kg', 28500.00),
('Hierro corrugado 1/2 pulgada', 'Varilla 12m', 45000.00),
('Arena lavada construcción', 'Metro cúbico', 85000.00),
('Gravilla triturada', 'Metro cúbico', 95000.00),
('Ladrillo común #5', 'Unidad', 850.00),
('Tubería PVC 4 pulgadas', 'Metro lineal', 25000.00),
('Cable eléctrico #12 AWG', 'Metro lineal', 4500.00),
('Cerámica para piso 60x60', 'Metro cuadrado', 85000.00),
('Pintura acrílica interior', 'Galón', 120000.00),
('Césped San Agustín', 'Metro cuadrado', 18000.00);

-- BODEGAS
INSERT INTO BODEGAS (responsable_bodega) VALUES
('Carlos Mendoza - Jefe de Almacén Obra Norte'),
('Ana Patricia López - Control de Inventarios Centro'),
('Miguel Torres - Responsable Bodega Rural'),
('Supervisión General - Bodega Central');

-- INVENTARIOS
INSERT INTO INVENTARIOS (cantidad_inventario) VALUES
(500),  -- Cemento
(200),  -- Hierro
(50),   -- Arena m3
(45),   -- Gravilla m3
(15000), -- Ladrillos
(150),  -- Tubería PVC metros
(500),  -- Cable eléctrico metros
(80),   -- Cerámica m2
(25),   -- Pintura galones
(100);  -- Césped m2

-- REQUISICIONES
INSERT INTO REQUISICIONES (fecha_requisicion, estado_requisicion) VALUES
('2024-01-18', 'Aprobada'),
('2024-02-02', 'En Proceso'),
('2024-02-15', 'Pendiente'),
('2024-03-01', 'Aprobada');

-- DETALLES_REQUISICION
INSERT INTO DETALLES_REQUISICION (cantidad_requisicion) VALUES
(100), -- Cemento
(50),  -- Hierro
(20),  -- Arena
(18),  -- Gravilla
(5000), -- Ladrillos
(75),  -- Tubería
(200), -- Cable
(40),  -- Cerámica
(10),  -- Pintura
(50);  -- Césped

-- MOVIMIENTOS_MATERIAL
INSERT INTO MOVIMIENTOS_MATERIAL (tipo_movimiento, fecha_movimiento, origen_movimiento, destino_movimiento) VALUES
('Entrada', '2024-01-19', 'Proveedor Cementos del Caribe', 'Bodega Central Obra Norte'),
('Salida', '2024-01-22', 'Bodega Central', 'Area Estructura Torre A'),
('Entrada', '2024-02-05', 'Proveedor Hierros y Aceros', 'Bodega Central Obra Norte'),
('Salida', '2024-02-10', 'Bodega Central', 'Area Estructura Torre B'),
('Transferencia', '2024-02-20', 'Bodega Central', 'Bodega Temporal Piso 5'),
('Entrada', '2024-03-01', 'Proveedor Materiales Eléctricos', 'Bodega Instalaciones'),
('Salida', '2024-03-05', 'Bodega Instalaciones', 'Area Instalaciones Torre A');

-- =====================================================
-- 5. MÓDULO ACTIVOS Y EQUIPOS
-- =====================================================

-- VEHICULOS
INSERT INTO VEHICULOS (placa_vehiculo, estado_vehiculo, tipo_vehiculo) VALUES
('ABC-123', 'Operativo', 'Camión Mixer'),
('DEF-456', 'Operativo', 'Volqueta'),
('GHI-789', 'Mantenimiento', 'Camioneta Supervisión'),
('JKL-012', 'Operativo', 'Montacargas'),
('MNO-345', 'Operativo', 'Grúa Torre');

-- EQUIPOS
INSERT INTO EQUIPOS (nombre_equipo, estado_equipo, tipo_equipo) VALUES
('Mezcladora Concreto MX-500', 'Operativo', 'Mezcladora'),
('Vibrador Concreto VB-2000', 'Operativo', 'Vibrador'),
('Soldadora Eléctrica SE-300', 'Operativo', 'Soldadora'),
('Compresor Aire CA-150', 'Mantenimiento', 'Compresor'),
('Martillo Neumático MN-80', 'Operativo', 'Herramienta Neumática'),
('Andamio Metálico Set-20', 'Operativo', 'Andamio'),
('Elevador Materiales EM-1000', 'Operativo', 'Elevador');

-- ASIGNACIONES_EQUIPO
INSERT INTO ASIGNACIONES_EQUIPO (fecha_inicio_asignacion, fecha_fin_asignacion) VALUES
('2024-01-20', '2024-03-20'),
('2024-02-01', '2024-04-01'),
('2024-02-15', '2024-05-15'),
('2024-03-01', '2024-06-01'),
('2024-01-25', '2024-12-31');

-- =====================================================
-- 6. MÓDULO FINANCIERO Y CONTROL
-- =====================================================

-- PRESUPUESTOS_OBRA
INSERT INTO PRESUPUESTOS_OBRA (monto_estimado_presupuesto, fecha_presupuesto) VALUES
(8500000000.00, '2024-01-10'),
(12000000000.00, '2024-01-25'),
(450000000.00, '2024-02-28'),
(2500000000.00, '2024-03-15');

-- AVANCES_OBRA
INSERT INTO AVANCES_OBRA (porcentaje_fisico_avance, porcentaje_financiero_avance, fecha_avance) VALUES
(15.5, 18.2, '2024-02-29'),
(8.3, 10.1, '2024-02-29'),
(35.7, 32.4, '2024-02-29'),
(45.2, 47.8, '2024-03-31'),
(52.8, 50.9, '2024-04-30');

-- REPORTES_SEMANALES
INSERT INTO REPORTES_SEMANALES (semana_reporte, resumen_reporte, fecha_reporte) VALUES
('Semana 8 - 2024', 'Avance normal en excavación Torre A. Inicio cimentación Torre B. Problemas menor con proveedor hierro, solucionado.', '2024-02-25'),
('Semana 9 - 2024', 'Fundición exitosa cimientos Torre A. Entrega materiales eléctricos completa. Clima favorable.', '2024-03-03'),
('Semana 10 - 2024', 'Inicio estructura Torre A nivel 1. Retraso menor por lluvias. Recuperación programada fin de semana.', '2024-03-10'),
('Semana 11 - 2024', 'Avance acelerado. Torres A y B en cronograma. Inspección técnica aprobada sin observaciones.', '2024-03-17');

-- =====================================================
-- 7. MÓDULO SEGUIMIENTO Y CONTROL
-- =====================================================

-- BITACORAS
INSERT INTO BITACORAS (fecha_bitacora, observaciones_bitacora) VALUES
('2024-02-25', 'Fundición exitosa zapata Z-1 Torre A. Concreto 3000 PSI. Temperatura ambiente 28°C. Sin novedad.'),
('2024-02-26', 'Inicio armado hierro columnas C1-C8. Verificación diámetros según plano. Todo conforme.'),
('2024-02-27', 'Lluvia intensa 2:00-4:00 PM. Suspensión temporal fundición. Protección área con plásticos.'),
('2024-02-28', 'Reanudación normal. Fundición columnas C1-C4. Inspección estructural programada mañana.'),
('2024-03-01', 'Visita inspector estructura. Aprobación sin observaciones. Inicio nivel 2 Torre A autorizado.');

-- INCIDENTES
INSERT INTO INCIDENTES (fecha_incidente, descripcion_incidente, estado_incidente) VALUES
('2024-02-20', 'Retraso entrega hierro por bloqueos vía. Reprogramación para 22/02. Impacto mínimo cronograma.', 'Resuelto'),
('2024-02-25', 'Falla menor mezcladora concreto. Reparación inmediata. Backup disponible. Sin retrasos.', 'Resuelto'),
('2024-03-02', 'Trabajador Carlos Ruiz - golpe menor mano derecha. Primeros auxilios. Incapacidad 2 días.', 'Seguimiento'),
('2024-03-05', 'Derrame menor combustible montacargas. Limpieza inmediata protocolos ambientales. Sin contaminación.', 'Resuelto');

-- ARCHIVOS_ADJUNTOS
INSERT INTO ARCHIVOS_ADJUNTOS (nombre_archivo, resumen_archivo, ruta_archivo) VALUES
('Planos_Estructurales_Torres_Norte.pdf', 'Planos arquitectónicos y estructurales completos', '/docs/obras/torres_norte/planos/estructurales.pdf'),
('Informe_Suelos_Geotecnico.pdf', 'Estudio geotécnico del terreno y recomendaciones cimentación', '/docs/obras/torres_norte/estudios/geotecnico.pdf'),
('Licencia_Construccion_2024.pdf', 'Licencia de construcción aprobada por alcaldía', '/docs/obras/torres_norte/legal/licencia.pdf'),
('Fotos_Avance_Marzo_2024.zip', 'Registro fotográfico avance obra semanas 9-12', '/docs/obras/torres_norte/fotos/marzo_2024.zip'),
('Especificaciones_Tecnicas.pdf', 'Especificaciones técnicas materiales y acabados', '/docs/obras/torres_norte/especificaciones/tecnicas.pdf');

-- =====================================================
-- 8. MÓDULO SEGURIDAD Y AUDITORÍA
-- =====================================================

-- USUARIOS_SISTEMA
INSERT INTO USUARIOS_SISTEMA (nombre_usuario, rol_usuario, correo_usuario, contrasena_usuario) VALUES
('admin_general', 'Administrador', 'admin@constructora.com', '$2b$12$hash_seguro_admin'),
('carlos_martinez', 'Ingeniero', 'carlos.martinez@constructora.com', '$2b$12$hash_seguro_carlos'),
('ana_herrera', 'Arquitecta', 'ana.herrera@constructora.com', '$2b$12$hash_seguro_ana'),
('miguel_ruiz', 'Supervisor', 'miguel.ruiz@constructora.com', '$2b$12$hash_seguro_miguel'),
('maria_vargas', 'Administrador Obra', 'maria.vargas@constructora.com', '$2b$12$hash_seguro_maria');

-- PERMISOS_ACCESO
INSERT INTO PERMISOS_ACCESO (modulo_permiso, nivel_acceso_permiso) VALUES
('Obras', 'Total'),
('Empleados', 'Lectura/Escritura'),
('Materiales', 'Lectura/Escritura'),
('Reportes', 'Solo Lectura'),
('Auditorías', 'Solo Lectura'),
('Presupuestos', 'Lectura/Escritura'),
('Bitácoras', 'Escritura'),
('Configuración', 'Solo Administrador');

-- AUDITORIAS
INSERT INTO AUDITORIAS (accion_auditoria, fecha_auditoria, detalle_auditoria) VALUES
('Creación Obra', '2024-01-15 09:30:00', 'Usuario carlos_martinez creó obra "Torres del Norte - Fase 1"'),
('Modificación Empleado', '2024-01-20 14:15:00', 'Usuario admin_general actualizó salario empleado ID 3'),
('Consulta Reporte', '2024-02-01 10:45:00', 'Usuario maria_vargas generó reporte avances obra ID 1'),
('Creación Material', '2024-02-05 16:20:00', 'Usuario miguel_ruiz agregó material "Cemento Portland Tipo I"'),
('Movimiento Inventario', '2024-02-10 11:30:00', 'Sistema registró salida automática 50 bultos cemento'),
('Incidente Reportado', '2024-03-02 08:45:00', 'Usuario miguel_ruiz reportó incidente seguridad ID 3');

-- =====================================================
-- 9. RELACIONES ENTRE TABLAS (Uso técnico completo)
-- =====================================================

-- OBRA_CLIENTE (Múltiples clientes por obra si aplica)
INSERT INTO OBRA_CLIENTE (id_obra, id_cliente) VALUES
(1, 1), -- Torres del Norte con Inversiones La Montaña
(2, 2), -- Centro Comercial con Constructora Urbana
(3, 3); -- Casa Campestre con Familia Rodríguez

-- CONTRATO_OBRA
INSERT INTO CONTRATO_OBRA (id_contrato, id_obra) VALUES
(1, 1), -- Contrato 1 para Torres del Norte
(2, 2), -- Contrato 2 para Centro Comercial
(3, 3); -- Contrato 3 para Casa Campestre

-- OBRA_AREA
INSERT INTO OBRA_AREA (id_obra, id_area) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), -- Torres del Norte: todas las áreas
(2, 1), (2, 2), (2, 3), (2, 4), -- Centro Comercial: áreas principales
(3, 1), (3, 2), (3, 6); -- Casa Campestre: estructura, acabados, jardines

-- AREA_ACTIVIDAD
INSERT INTO AREA_ACTIVIDAD (id_area, id_actividad) VALUES
(1, 1), (1, 2), -- Estructura: excavación y concreto
(2, 5), (2, 6), -- Mampostería: muros y acabados
(3, 4), -- Eléctrica: cableado
(4, 3), -- Hidráulica: tuberías
(5, 6), (5, 7), -- Acabados: aplicación y pintura
(6, 8); -- Exteriores: paisajismo

-- ACTIVIDAD_TRABAJO
INSERT INTO ACTIVIDAD_TRABAJO (id_actividad, id_trabajo) VALUES
(1, 1), (1, 2), -- Excavación: excavación manual y fundición
(2, 2), -- Estructura de concreto: fundición
(3, 3), -- Tuberías: instalación puntos hidráulicos
(4, 4), -- Cableado: instalación puntos eléctricos
(5, 5), -- Mampostería: ladrillo
(6, 6), -- Acabados: enchapes
(7, 7), -- Pintura: dos manos
(8, 8); -- Paisajismo: siembra césped

-- PROYECTO_ACTIVIDAD
INSERT INTO PROYECTO_ACTIVIDAD (id_proyecto, id_actividad) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), -- Proyecto Norte: actividades principales
(2, 1), (2, 2), (2, 3), (2, 4), -- Proyecto Centro: actividades comerciales
(3, 1), (3, 5), (3, 6), (3, 8); -- Proyecto Rural: actividades residenciales

-- AREA_EMPLEADO
INSERT INTO AREA_EMPLEADO (id_area, id_empleado) VALUES
(1, 1), (1, 3), -- Estructura: ingeniero y maestro
(2, 2), (2, 7), -- Mampostería: arquitecta y operario
(3, 4), -- Eléctrica: electricista
(4, 5), -- Hidráulica: plomero
(7, 6), -- Supervisión: supervisora calidad
(8, 8); -- Control: administradora

-- CONTRATO_DETALLE_TRABAJO
INSERT INTO CONTRATO_DETALLE_TRABAJO (id_contrato, id_detalle_trabajo) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), -- Contrato 1: múltiples trabajos
(2, 1), (2, 2), (2, 6), -- Contrato 2: trabajos comerciales
(3, 7), (3, 8); -- Contrato 3: trabajos residenciales

-- PROVEEDOR_MATERIAL
INSERT INTO PROVEEDOR_MATERIAL (id_proveedor, id_material) VALUES
(1, 1), -- Cementos del Caribe: cemento
(2, 2), -- Hierros y Aceros: hierro
(1, 3), (1, 4), -- Cementos: arena y gravilla
(3, 7), -- Eléctricos: cable
(4, 6), -- Tuberías: PVC
(5, 8), (5, 9), -- Acabados: cerámica y pintura
(1, 5); -- Cementos: ladrillo

-- PROVEEDOR_EQUIPO
INSERT INTO PROVEEDOR_EQUIPO (id_proveedor, id_equipo) VALUES
(6, 1), (6, 2), -- Maquinaria Pesada: mezcladora y vibrador
(3, 3), (3, 4), -- Eléctricos: soldadora y compresor
(6, 5), (6, 6), (6, 7); -- Maquinaria: herramientas y andamios

-- EQUIPO_ASIGNACION
INSERT INTO EQUIPO_ASIGNACION (id_equipo, id_asignacion_equipo) VALUES
(1, 1), -- Mezcladora: asignación 1
(2, 1), -- Vibrador: asignación 1
(3, 2), -- Soldadora: asignación 2
(4, 3), -- Compresor: asignación 3
(5, 4), (6, 4), (7, 5); -- Herramientas: múltiples asignaciones

-- OBRA_VEHICULO
INSERT INTO OBRA_VEHICULO (id_obra, id_vehiculo) VALUES
(1, 1), (1, 2), (1, 5), -- Torres del Norte: mixer, volqueta, grúa
(2, 1), (2, 4), -- Centro Comercial: mixer, montacargas
(3, 3); -- Casa Campestre: camioneta supervisión

-- OBRA_BODEGA
INSERT INTO OBRA_BODEGA (id_obra, id_bodega) VALUES
(1, 1), (1, 4), -- Torres del Norte: bodega obra y central
(2, 2), -- Centro Comercial: bodega centro
(3, 3); -- Casa Campestre: bodega rural

-- BODEGA_INVENTARIO
INSERT INTO BODEGA_INVENTARIO (id_bodega, id_inventario) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), -- Bodega Norte: inventarios principales
(2, 6), (2, 7), (2, 8), -- Bodega Centro: instalaciones y acabados
(3, 9), (3, 10), -- Bodega Rural: pintura y césped
(4, 1), (4, 2); -- Bodega Central: materiales principales

-- INVENTARIO_MATERIAL
INSERT INTO INVENTARIO_MATERIAL (id_inventario, id_material) VALUES
(1, 1), -- Inventario cemento
(2, 2), -- Inventario hierro
(3, 3), -- Inventario arena
(4, 4), -- Inventario gravilla
(5, 5), -- Inventario ladrillo
(6, 6), -- Inventario tubería
(7, 7), -- Inventario cable
(8, 8), -- Inventario cerámica
(9, 9), -- Inventario pintura
(10, 10); -- Inventario césped

-- AREA_REQUISICION
INSERT INTO AREA_REQUISICION (id_area, id_requisicion) VALUES
(1, 1), -- Estructura: requisición materiales básicos
(2, 2), -- Mampostería: requisición ladrillos
(3, 3), -- Eléctrica: requisición cables
(4, 4); -- Hidráulica: requisición tuberías

-- REQUISICION_DETALLE
INSERT INTO REQUISICION_DETALLE (id_requisicion, id_detalle_requisicion) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), -- Req 1: cemento, hierro, arena, gravilla
(2, 5), -- Req 2: ladrillos
(3, 7), -- Req 3: cable
(4, 6); -- Req 4: tubería

-- DETALLE_MATERIAL
INSERT INTO DETALLE_MATERIAL (id_detalle_requisicion, id_material) VALUES
(1, 1), -- Detalle cemento
(2, 2), -- Detalle hierro
(3, 3), -- Detalle arena
(4, 4), -- Detalle gravilla
(5, 5), -- Detalle ladrillo
(6, 6), -- Detalle tubería
(7, 7); -- Detalle cable

-- MATERIAL_MOVIMIENTO
INSERT INTO MATERIAL_MOVIMIENTO (id_material, id_movimiento_material) VALUES
(1, 1), (1, 2), -- Cemento: entrada y salida
(2, 3), (2, 4), -- Hierro: entrada y salida
(7, 6), (7, 7); -- Cable: entrada y salida

-- OBRA_PRESUPUESTO
INSERT INTO OBRA_PRESUPUESTO (id_obra, id_presupuesto) VALUES
(1, 1), -- Torres del Norte: presupuesto principal
(2, 2), -- Centro Comercial: presupuesto
(3, 3); -- Casa Campestre: presupuesto

-- OBRA_AVANCE
INSERT INTO OBRA_AVANCE (id_obra, id_avance) VALUES
(1, 1), (1, 4), (1, 5), -- Torres del Norte: múltiples mediciones
(2, 2), -- Centro Comercial: avance inicial
(3, 3); -- Casa Campestre: avance intermedio

-- OBRA_REPORTE
INSERT INTO OBRA_REPORTE (id_obra, id_reporte) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), -- Torres del Norte: reportes semanales
(2, 2), -- Centro Comercial: reportes
(3, 3), (3, 4); -- Casa Campestre: reportes

-- OBRA_BITACORA
INSERT INTO OBRA_BITACORA (id_obra, id_bitacora) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5); -- Torres del Norte: bitácoras diarias

-- OBRA_INCIDENTE
INSERT INTO OBRA_INCIDENTE (id_obra, id_incidente) VALUES
(1, 1), (1, 2), (1, 3), (1, 4); -- Torres del Norte: todos los incidentes

-- PROYECTO_ARCHIVO
INSERT INTO PROYECTO_ARCHIVO (id_proyecto, id_archivo) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), -- Proyecto Norte: todos los archivos
(2, 1), (2, 5), -- Proyecto Centro: planos y especificaciones
(3, 4), (3, 5); -- Proyecto Rural: fotos y especificaciones

-- USUARIO_PERMISO
INSERT INTO USUARIO_PERMISO (id_usuario, id_permiso) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), -- Admin: todos los permisos
(2, 1), (2, 2), (2, 6), (2, 7), -- Ingeniero: obras, empleados, presupuestos, bitácoras
(3, 1), (3, 4), -- Arquitecta: obras y reportes
(4, 2), (4, 3), (4, 7), -- Supervisor: empleados, materiales, bitácoras
(5, 1), (5, 4), (5, 6); -- Admin Obra: obras, reportes, presupuestos

-- USUARIO_AUDITORIA
INSERT INTO USUARIO_AUDITORIA (id_usuario, id_auditoria) VALUES
(2, 1), -- Carlos: creación obra
(1, 2), -- Admin: modificación empleado
(5, 3), -- María: consulta reporte
(4, 4), (4, 6), -- Miguel: creación material e incidente
(1, 5); -- Admin: movimiento inventario

-- OBRA_AUDITORIA
INSERT INTO OBRA_AUDITORIA (id_obra, id_auditoria) VALUES
(1, 1), (1, 5), (1, 6), -- Torres del Norte: auditorías relacionadas
(2, 3), -- Centro Comercial: reporte
(3, 4); -- Casa Campestre: materiales

COMMIT;

-- =====================================================
-- VERIFICACIÓN DE INTEGRIDAD DE DATOS
-- =====================================================

-- Consulta de verificación: obras con todos sus elementos
SELECT 
    o.nombre_obra,
    c.nombre_cliente,
    COUNT(DISTINCT oa.id_area) as areas_asignadas,
    COUNT(DISTINCT ob.id_bitacora) as bitacoras_registradas,
    COUNT(DISTINCT oi.id_incidente) as incidentes_reportados,
    COUNT(DISTINCT or_tbl.id_reporte) as reportes_generados,
    COUNT(DISTINCT ov.id_vehiculo) as vehiculos_asignados
FROM OBRAS o
LEFT JOIN CLIENTES c ON o.id_cliente = c.id_cliente
LEFT JOIN OBRA_AREA oa ON o.id_obra = oa.id_obra
LEFT JOIN OBRA_BITACORA ob ON o.id_obra = ob.id_obra
LEFT JOIN OBRA_INCIDENTE oi ON o.id_obra = oi.id_obra
LEFT JOIN OBRA_REPORTE or_tbl ON o.id_obra = or_tbl.id_obra
LEFT JOIN OBRA_VEHICULO ov ON o.id_obra = ov.id_obra
GROUP BY o.id_obra, o.nombre_obra, c.nombre_cliente
ORDER BY o.id_obra;

ANALYZE;