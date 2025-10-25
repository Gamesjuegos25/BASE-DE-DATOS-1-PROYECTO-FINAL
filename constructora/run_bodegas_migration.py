"""
Script para ejecutar migración de expansión de BODEGAS
"""
import sys
sys.path.append('.')

from database import get_connection

def expand_bodegas_table():
    """Agregar campos completos a la tabla BODEGAS"""
    try:
        conn = get_connection()
        if not conn:
            print("❌ Error: No se pudo conectar a la base de datos")
            return False
        
        cursor = conn.cursor()
        
        print("🔄 Ejecutando migración para expandir tabla BODEGAS...")
        
        # Lista de columnas a agregar
        columns_to_add = [
            "ALTER TABLE BODEGAS ADD COLUMN ubicacion_bodega VARCHAR(200)",
            "ALTER TABLE BODEGAS ADD COLUMN capacidad_bodega VARCHAR(100)",
            "ALTER TABLE BODEGAS ADD COLUMN telefono_bodega VARCHAR(20)",
            "ALTER TABLE BODEGAS ADD COLUMN estado_bodega VARCHAR(50) DEFAULT 'Activa'",
            "ALTER TABLE BODEGAS ADD COLUMN fecha_creacion DATE DEFAULT CURRENT_DATE",
            "ALTER TABLE BODEGAS ADD COLUMN observaciones_bodega TEXT"
        ]
        
        # Ejecutar cada ALTER TABLE
        for sql in columns_to_add:
            try:
                cursor.execute(sql)
                column_name = sql.split('ADD COLUMN ')[1].split(' ')[0]
                print(f"   ✅ Columna agregada: {column_name}")
            except Exception as e:
                if "already exists" in str(e) or "ya existe" in str(e):
                    column_name = sql.split('ADD COLUMN ')[1].split(' ')[0]
                    print(f"   ⚠️  Columna ya existe: {column_name}")
                else:
                    print(f"   ❌ Error agregando columna: {e}")
        
        # Actualizar datos existentes
        print("\n📝 Actualizando datos existentes...")
        
        update_sql = """
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
        WHERE ubicacion_bodega IS NULL OR ubicacion_bodega = ''
        """
        
        cursor.execute(update_sql)
        rows_updated = cursor.rowcount
        print(f"   ✅ {rows_updated} bodegas actualizadas con información completa")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Migración completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando migración: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def verify_bodegas_structure():
    """Verificar la estructura actualizada de BODEGAS"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Obtener información de columnas
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, column_default
            FROM information_schema.columns 
            WHERE table_name = 'bodegas' 
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        
        print("\n📋 Estructura actual de tabla BODEGAS:")
        print("-" * 70)
        for col in columns:
            col_name = col[0]
            data_type = col[1]
            max_length = col[2] if col[2] else ""
            default_val = col[3] if col[3] else ""
            print(f"   {col_name:25} | {data_type}({max_length}) | {default_val}")
        
        # Mostrar datos de ejemplo
        cursor.execute("SELECT * FROM BODEGAS LIMIT 2")
        bodegas = cursor.fetchall()
        
        if bodegas:
            print("\n📦 Datos de ejemplo:")
            print("-" * 70)
            for i, bodega in enumerate(bodegas, 1):
                print(f"Bodega #{i}:")
                for j, col in enumerate(columns):
                    col_name = col[0]
                    value = bodega[j] if j < len(bodega) else "N/A"
                    print(f"   {col_name}: {value}")
                print()
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        if conn:
            conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🏗️  MIGRACIÓN: EXPANDIR TABLA BODEGAS")
    print("=" * 60)
    
    # Ejecutar migración
    success = expand_bodegas_table()
    
    if success:
        # Verificar estructura
        verify_bodegas_structure()
    
    print("\n" + "=" * 60)