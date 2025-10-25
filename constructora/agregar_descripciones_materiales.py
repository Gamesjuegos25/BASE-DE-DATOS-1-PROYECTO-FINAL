#!/usr/bin/env python3
"""
Script para agregar descripciones y categorías a los materiales existentes
"""

from database import get_connection
import psycopg2

# Datos de materiales con descripciones y categorías
materiales_data = {
    1: {  # Cemento Gris 50kg
        'descripcion': 'Cemento gris de alta calidad para construcción general, empacado en bultos de 50 kg. Ideal para estructuras, cimentaciones y obras de concreto.',
        'categoria': 'Concreto y Cemento'
    },
    2: {  # Varilla Corrugada 1/2"
        'descripcion': 'Varilla de acero corrugada de 1/2 pulgada, grado 60, para refuerzo estructural en construcciones de concreto armado.',
        'categoria': 'Acero y Metales'
    },
    3: {  # Bloque Estructural 15x20x40
        'descripcion': 'Bloque de concreto estructural de 15x20x40 cm, para construcción de muros portantes y estructurales.',
        'categoria': 'Mampostería'
    },
    4: {  # Tubería PVC 4"
        'descripcion': 'Tubería de PVC de 4 pulgadas para sistemas de drenaje y alcantarillado, resistente a la corrosión.',
        'categoria': 'Plomería'
    },
    5: {  # Cable THHN 12 AWG
        'descripcion': 'Cable eléctrico THHN calibre 12 AWG, en rollo de 100 metros, para instalaciones eléctricas residenciales y comerciales.',
        'categoria': 'Eléctricos'
    },
    6: {  # Material Prueba 550
        'descripcion': 'Material de prueba para validación del sistema, uso temporal en desarrollo.',
        'categoria': 'Pruebas'
    },
    7: {  # Cemento Portland Tipo I Web Test
        'descripcion': 'Cemento Portland Tipo I de alta resistencia, probado para desarrollo web del sistema ERP.',
        'categoria': 'Concreto y Cemento'
    },
    8: {  # Cemento
        'descripcion': 'Cemento básico para construcción general, empacado en sacos estándar de 50 kg.',
        'categoria': 'Concreto y Cemento'
    },
    9: {  # Cable Electrico
        'descripcion': 'Cable eléctrico básico por metro lineal para instalaciones eléctricas generales.',
        'categoria': 'Eléctricos'
    }
}

def agregar_descripciones_categorias():
    """Agregar descripciones y categorías a la tabla de materiales"""
    
    print("=== AGREGANDO DESCRIPCIONES Y CATEGORÍAS ===")
    
    try:
        # Primero verificar si las columnas existen
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Verificar columnas existentes
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'materiales'
                    AND column_name IN ('descripcion_material', 'categoria_material')
                """)
                
                columnas_existentes = [row[0] for row in cursor.fetchall()]
                
                # Agregar columnas si no existen
                if 'descripcion_material' not in columnas_existentes:
                    print("Agregando columna descripcion_material...")
                    cursor.execute("""
                        ALTER TABLE materiales 
                        ADD COLUMN descripcion_material TEXT
                    """)
                    conn.commit()
                
                if 'categoria_material' not in columnas_existentes:
                    print("Agregando columna categoria_material...")
                    cursor.execute("""
                        ALTER TABLE materiales 
                        ADD COLUMN categoria_material VARCHAR(100)
                    """)
                    conn.commit()
                
                print(f"Columnas verificadas/agregadas: {len(columnas_existentes) + 2}")
                
                # Actualizar datos de materiales
                for material_id, datos in materiales_data.items():
                    print(f"Actualizando material {material_id}...")
                    
                    cursor.execute("""
                        UPDATE materiales 
                        SET descripcion_material = %s,
                            categoria_material = %s
                        WHERE id_material = %s
                    """, (
                        datos['descripcion'],
                        datos['categoria'],
                        material_id
                    ))
                    
                    if cursor.rowcount > 0:
                        print(f"  ✓ Material {material_id} actualizado")
                    else:
                        print(f"  ✗ Material {material_id} no encontrado")
                
                conn.commit()
                
                # Verificar resultados
                print(f"\n=== VERIFICACIÓN DE RESULTADOS ===")
                cursor.execute("""
                    SELECT id_material, nombre_material, categoria_material,
                           LEFT(descripcion_material, 50) || '...' as descripcion_corta
                    FROM materiales 
                    WHERE descripcion_material IS NOT NULL
                    ORDER BY id_material
                """)
                
                resultados = cursor.fetchall()
                print(f"Materiales con descripción: {len(resultados)}")
                
                for res in resultados:
                    print(f"  {res[0]}: {res[1]} [{res[2]}] - {res[3]}")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    agregar_descripciones_categorias()