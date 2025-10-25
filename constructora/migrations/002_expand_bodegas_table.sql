-- =====================================================
-- MIGRACIÓN: Expandir tabla BODEGAS con campos completos
-- =====================================================

BEGIN;

-- Agregar campos faltantes a la tabla BODEGAS (sintaxis PostgreSQL)
ALTER TABLE BODEGAS ADD COLUMN ubicacion_bodega VARCHAR(200);
ALTER TABLE BODEGAS ADD COLUMN capacidad_bodega VARCHAR(100);
ALTER TABLE BODEGAS ADD COLUMN telefono_bodega VARCHAR(20);
ALTER TABLE BODEGAS ADD COLUMN estado_bodega VARCHAR(50) DEFAULT 'Activa';
ALTER TABLE BODEGAS ADD COLUMN fecha_creacion DATE DEFAULT CURRENT_DATE;
ALTER TABLE BODEGAS ADD COLUMN observaciones_bodega TEXT;

-- Actualizar datos existentes con información completa
UPDATE BODEGAS SET 
    ubicacion_bodega = CASE id_bodega
        WHEN 1 THEN 'Sector Norte - Zona Industrial Km 15'
        WHEN 2 THEN 'Centro Comercial - Oficinas Principales'
        WHEN 3 THEN 'Zona Rural - Proyecto Las Flores'
        WHEN 4 THEN 'Bodega Central - Complejo Principal'
        ELSE 'Por definir'
    END,
    capacidad_bodega = CASE id_bodega
        WHEN 1 THEN '1500 m³ - Materiales pesados'
        WHEN 2 THEN '800 m³ - Inventario general'
        WHEN 3 THEN '500 m³ - Obra específica'
        WHEN 4 THEN '2500 m³ - Almacén principal'
        ELSE '100 m³'
    END,
    telefono_bodega = CASE id_bodega
        WHEN 1 THEN '+502 2234-5678'
        WHEN 2 THEN '+502 2234-5679'
        WHEN 3 THEN '+502 2234-5680'
        WHEN 4 THEN '+502 2234-5681'
        ELSE '+502 2234-0000'
    END,
    estado_bodega = 'Activa',
    observaciones_bodega = CASE id_bodega
        WHEN 1 THEN 'Bodega especializada en materiales de construcción pesados como cemento, hierro y agregados'
        WHEN 2 THEN 'Control centralizado de inventarios para múltiples obras urbanas'
        WHEN 3 THEN 'Almacén temporal para proyecto específico en zona rural'
        WHEN 4 THEN 'Bodega principal con área administrativa y distribución'
        ELSE 'Bodega en configuración'
    END
WHERE id_bodega <= 4;

COMMIT;

PRINT 'Migración completada: Campos agregados a tabla BODEGAS';