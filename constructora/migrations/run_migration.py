#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para ejecutar migración de base de datos
Añade columnas necesarias para tracking de materiales en movimientos e inventarios
"""
import os
import sys

# Añadir constructora al path
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from database import get_connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_migration():
    """Ejecutar migración para añadir columnas a MOVIMIENTOS_MATERIAL e INVENTARIOS"""
    migration_sql = """
    -- 1. Añadir id_material a INVENTARIOS si no existe
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = 'inventarios' AND column_name = 'id_material'
        ) THEN
            ALTER TABLE INVENTARIOS ADD COLUMN id_material INTEGER REFERENCES MATERIALES(id_material) ON DELETE CASCADE;
            RAISE NOTICE 'Columna id_material añadida a INVENTARIOS';
        END IF;
    END $$;

    -- 2. Añadir constraint UNIQUE en id_material de INVENTARIOS si no existe
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM pg_constraint 
            WHERE conname = 'inventarios_id_material_key'
        ) THEN
            ALTER TABLE INVENTARIOS ADD CONSTRAINT inventarios_id_material_key UNIQUE (id_material);
            RAISE NOTICE 'Constraint UNIQUE añadida a INVENTARIOS.id_material';
        END IF;
    END $$;

    -- 3. Añadir id_material a MOVIMIENTOS_MATERIAL si no existe
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = 'movimientos_material' AND column_name = 'id_material'
        ) THEN
            ALTER TABLE MOVIMIENTOS_MATERIAL ADD COLUMN id_material INTEGER REFERENCES MATERIALES(id_material) ON DELETE CASCADE;
            RAISE NOTICE 'Columna id_material añadida a MOVIMIENTOS_MATERIAL';
        END IF;
    END $$;

    -- 4. Añadir cantidad a MOVIMIENTOS_MATERIAL si no existe
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = 'movimientos_material' AND column_name = 'cantidad'
        ) THEN
            ALTER TABLE MOVIMIENTOS_MATERIAL ADD COLUMN cantidad INTEGER;
            RAISE NOTICE 'Columna cantidad añadida a MOVIMIENTOS_MATERIAL';
        END IF;
    END $$;

    -- 5. Añadir fecha_actualizacion a INVENTARIOS si no existe
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = 'inventarios' AND column_name = 'fecha_actualizacion'
        ) THEN
            ALTER TABLE INVENTARIOS ADD COLUMN fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            RAISE NOTICE 'Columna fecha_actualizacion añadida a INVENTARIOS';
        END IF;
    END $$;
    """

    try:
        logger.info("🔧 Iniciando migración de base de datos...")
        conn = get_connection()
        if not conn:
            logger.error("❌ No se pudo conectar a la base de datos")
            return False

        with conn:
            with conn.cursor() as cursor:
                cursor.execute(migration_sql)
                conn.commit()
                logger.info("✅ Migración completada exitosamente")
                return True

    except Exception as e:
        logger.error(f"❌ Error ejecutando migración: {e}")
        return False

if __name__ == '__main__':
    success = run_migration()
    sys.exit(0 if success else 1)
