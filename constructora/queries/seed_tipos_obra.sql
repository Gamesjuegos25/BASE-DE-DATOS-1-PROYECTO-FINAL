-- Semilla de TIPOS_OBRA basada en catálogo proporcionado
-- Inserta 20 tipos con unidad de medida, rango y notas.
-- Usa ON CONFLICT para evitar duplicados por nombre_tipo.

BEGIN;

INSERT INTO TIPOS_OBRA (nombre_tipo, descripcion_base, unidad_medida, rango_precio, notas, precio_min, precio_max, precio_base, activo)
VALUES
-- 1
('Construcción de Casa (Interés Social)', 'Casa de interés social con estructura básica y acabados sencillos.', 'm² de construcción', 'Q 4,000 - Q 5,200', 'Estructura básica, acabados sencillos.', 4000, 5200, 4600, TRUE),
-- 2
('Construcción de Casa (Residencial Estándar)', 'Casa residencial estándar.', 'm² de construcción', 'Q 5,600 - Q 7,500', 'Acabados de calidad media a alta.', 5600, 7500, 6550, TRUE),
-- 3
('Construcción de Casa (Alta Gama / High-end)', 'Casa de alta gama con diseño complejo y acabados de lujo.', 'm² de construcción', 'Q 7,200 - Q 10,000+', 'Diseño complejo, acabados de lujo.', 7200, 10000, 8600, TRUE),
-- 4
('Remodelación de Baño Completo', 'Remodelación integral de baño pequeño.', 'Unidad (baño pequeño)', 'Q 15,000 - Q 45,000', 'Depende de la sustitución de accesorios, azulejos y grifería.', 15000, 45000, 30000, TRUE),
-- 5
('Remodelación de Cocina', 'Remodelación integral de cocina pequeña.', 'Unidad (cocina pequeña)', 'Q 20,000 - Q 60,000+', 'Depende de gabinetes, top (encimera) y azulejos.', 20000, 60000, 40000, TRUE),
-- 6
('Muro Perimetral de Block', 'Construcción de muro perimetral con block de 14 cm.', 'Metro Lineal (ml)', 'Q 700 - Q 1,400', 'Incluye cimiento corrido, block de 14 cm, fundición de soleras y columnas.', 700, 1400, 1050, TRUE),
-- 7
('Muro Perimetral Prefabricado', 'Muro perimetral prefabricado.', 'Metro Lineal (ml)', 'Q 250 - Q 450', 'Opción más económica, solo el panel y poste (instalación sencilla).', 250, 450, 350, TRUE),
-- 8
('Levantado de Muro de Block (Solo Pared)', 'Levantado de pared de block 14x19x39 cm y mezcla, sin acabados.', 'm² de pared', 'Q 180 - Q 350', 'Mano de obra y materiales (block de 14x19x39 cm y mezcla) sin acabados.', 180, 350, 265, TRUE),
-- 9
('Construcción de Piscina Estándar (30 m²)', 'Piscina estándar aprox. 30 m² (variable).', 'Unidad/Global', 'Q 100,000 - Q 250,000+', 'Incluye casco, fundición, impermeabilización, acabados y equipo de bombeo (muy variable).', 100000, 250000, 175000, TRUE),
-- 10
('Fundición de Losa de Concreto', 'Fundición de losa de concreto con formaleta y acero.', 'm² de losa', 'Q 650 - Q 1,200', 'Incluye formaleta, hierro, concreto (puede ser prefabricada o monolítica).', 650, 1200, 925, TRUE),
-- 11
('Fundición de Piso de Concreto (Simple)', 'Piso de concreto simple 10 cm.', 'm² de piso', 'Q 150 - Q 300', 'Para patios, aceras, incluye base, plástico y concreto de 10 cm.', 150, 300, 225, TRUE),
-- 12
('Colocación de Piso Cerámico/Porcelanato', 'Colocación de revestimiento cerámico o porcelanato.', 'm² de área', 'Q 120 - Q 250', 'Solo mano de obra y pegamento (el precio del material varía mucho).', 120, 250, 185, TRUE),
-- 13
('Instalación Eléctrica Domiciliar', 'Instalación eléctrica por punto (salida).', 'Punto (salida)', 'Q 250 - Q 600', 'Cableado, toma, caja, tubería y mano de obra por cada punto.', 250, 600, 425, TRUE),
-- 14
('Instalación Hidrosanitaria', 'Instalación hidrosanitaria por punto.', 'Punto (grifo, desagüe)', 'Q 400 - Q 800', 'Tuberías y mano de obra para cada punto de agua potable o drenaje.', 400, 800, 600, TRUE),
-- 15
('Construcción de Fosa Séptica', 'Construcción de fosa séptica dimensiones estándar.', 'Unidad (típica)', 'Q 8,000 - Q 18,000', 'Dimensiones estándar, incluye excavación, block, y tapas de concreto.', 8000, 18000, 13000, TRUE),
-- 16
('Techo de Lámina (Estructura Metálica)', 'Techo de lámina calibre 26/28 con estructura metálica.', 'm² de techo', 'Q 350 - Q 600', 'Incluye estructura, lámina (calibre 26/28), canal y bajadas pluviales.', 350, 600, 475, TRUE),
-- 17
('Cisterna de Almacenamiento de Agua', 'Cisterna de concreto por m³ de capacidad.', 'm³ de capacidad', 'Q 2,500 - Q 4,500', 'Costo por m³, incluye fundición e impermeabilización.', 2500, 4500, 3500, TRUE),
-- 18
('Mantenimiento y Pintura Exterior', 'Pintura exterior con preparación de superficie.', 'm² de pared', 'Q 40 - Q 80', 'Incluye preparación de la superficie y dos manos de pintura de buena calidad.', 40, 80, 60, TRUE),
-- 19
('Construcción de Aceras y Bordillos', 'Construcción de aceras y bordillos en concreto.', 'Metro Lineal (ml)', 'Q 180 - Q 350', 'Incluye trazo, excavación y fundición de concreto.', 180, 350, 265, TRUE),
-- 20
('Instalación de Cielorraso de Tabla Yeso (Drywall)', 'Instalación de cielorraso de tabla yeso (drywall).', 'm² de cielo', 'Q 150 - Q 250', 'Incluye estructura metálica, lámina de tabla yeso y masilla/lijado.', 150, 250, 200, TRUE)
ON CONFLICT (nombre_tipo) DO UPDATE
SET
  unidad_medida = EXCLUDED.unidad_medida,
  rango_precio = EXCLUDED.rango_precio,
  notas = EXCLUDED.notas,
  precio_min = EXCLUDED.precio_min,
  precio_max = EXCLUDED.precio_max,
  precio_base = EXCLUDED.precio_base,
  descripcion_base = EXCLUDED.descripcion_base,
  activo = TRUE;

COMMIT;
