#!/usr/bin/env python3
"""
Script para verificar y agregar datos de ejemplo a tipos_obra si están vacíos
"""

from database import get_connection

def agregar_tipos_obra_ejemplo():
    """Agrega tipos de obra de ejemplo con precios si no existen"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Verificar cuántos tipos existen
        cur.execute("SELECT COUNT(*) FROM tipos_obra")
        count = cur.fetchone()[0]
        
        if count == 0:
            print("🏗️ Tabla tipos_obra vacía. Agregando datos de ejemplo...")
            
            tipos_ejemplo = [
                ('RESIDENCIAL', 'Construcción Residencial', 'm²', 2500.00, '2000-3000 por m²'),
                ('COMERCIAL', 'Construcción Comercial', 'm²', 3500.00, '3000-4000 por m²'),
                ('INDUSTRIAL', 'Construcción Industrial', 'm²', 4500.00, '4000-5000 por m²'),
                ('REMODELACION', 'Remodelación', 'm²', 1800.00, '1500-2500 por m²'),
                ('AMPLIACION', 'Ampliación', 'm²', 2200.00, '2000-2800 por m²'),
                ('ESTRUCTURA', 'Solo Estructura', 'm²', 1200.00, '1000-1500 por m²'),
                ('ACABADOS', 'Solo Acabados', 'm²', 800.00, '600-1000 por m²'),
                ('PISCINA', 'Construcción de Piscina', 'unidad', 25000.00, '20000-35000 por unidad')
            ]
            
            for codigo, nombre, unidad, precio, rango in tipos_ejemplo:
                cur.execute("""
                    INSERT INTO tipos_obra (codigo_tipo, nombre_tipo, unidad_medida, precio_base, rango_precio)
                    VALUES (%s, %s, %s, %s, %s)
                """, (codigo, nombre, unidad, precio, rango))
            
            conn.commit()
            print(f"✅ Agregados {len(tipos_ejemplo)} tipos de obra de ejemplo")
            
        else:
            print(f"✅ Ya existen {count} tipos de obra en la tabla")
            
            # Verificar si tienen precios definidos
            cur.execute("SELECT COUNT(*) FROM tipos_obra WHERE precio_base IS NULL OR precio_base = 0")
            sin_precio = cur.fetchone()[0]
            
            if sin_precio > 0:
                print(f"⚠️  {sin_precio} tipos sin precio definido. Actualizando...")
                
                # Actualizar precios por defecto
                cur.execute("""
                    UPDATE tipos_obra SET 
                        precio_base = 2500.00,
                        unidad_medida = 'm²',
                        rango_precio = '2000-3000 por m²'
                    WHERE precio_base IS NULL OR precio_base = 0
                """)
                
                conn.commit()
                print("✅ Precios actualizados")
        
        # Mostrar tipos disponibles
        cur.execute("SELECT * FROM tipos_obra ORDER BY nombre_tipo")
        tipos = cur.fetchall()
        
        print(f"\n📋 TIPOS DE OBRA DISPONIBLES ({len(tipos)}):")
        print("-" * 80)
        for tipo in tipos:
            # Manejar diferentes formatos de precio
            precio_str = str(tipo[4]) if tipo[4] else '0'
            try:
                # Si es formato "Q 2,500 - Q 4,500", extraer primer número
                if 'Q' in precio_str and '-' in precio_str:
                    precio_limpio = precio_str.split('-')[0].replace('Q', '').replace(',', '').strip()
                    precio = float(precio_limpio) if precio_limpio else 0
                else:
                    precio = float(precio_str)
            except:
                precio = 0
            
            print(f"• {tipo[2]} ({tipo[1]}) - Q{precio:,.0f} por {tipo[3] or 'unidad'}")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    agregar_tipos_obra_ejemplo()