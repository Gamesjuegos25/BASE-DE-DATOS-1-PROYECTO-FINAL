#!/usr/bin/env python3
"""
VERIFICADOR Y CREADOR DE ÁREAS
===============================
Verifica que existan áreas en la base de datos y crea algunas básicas si no hay
"""

from database import get_connection

def verificar_y_crear_areas():
    """Verifica áreas existentes y crea básicas si no hay"""
    print("🔍 VERIFICANDO ÁREAS EN BASE DE DATOS...")
    print("=" * 40)
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Verificar áreas existentes
        cur.execute("SELECT COUNT(*) FROM areas")
        total_areas = cur.fetchone()[0]
        
        print(f"📊 Áreas encontradas: {total_areas}")
        
        if total_areas == 0:
            print("⚠️  No se encontraron áreas. Creando áreas básicas...")
            
            # Crear áreas básicas para construcción
            areas_basicas = [
                ('Estructural', 'Trabajos de estructura y cimientos'),
                ('Eléctrica', 'Instalaciones eléctricas y sistemas'),
                ('Plomería', 'Sistemas de agua y drenaje'),
                ('Acabados', 'Pintura, pisos y detalles finales'),
                ('Techos', 'Estructuras de techo y cubiertas'),
                ('Ventanas', 'Instalación de ventanas y puertas'),
                ('HVAC', 'Calefacción, ventilación y aire acondicionado'),
                ('Paisajismo', 'Jardines y áreas exteriores')
            ]
            
            for nombre, descripcion in areas_basicas:
                try:
                    cur.execute("""
                        INSERT INTO areas (nombre, descripcion) 
                        VALUES (%s, %s)
                    """, (nombre, descripcion))
                    print(f"✅ Área creada: {nombre}")
                except Exception as e:
                    print(f"❌ Error creando área {nombre}: {str(e)}")
            
            conn.commit()
            
            # Verificar nuevamente
            cur.execute("SELECT COUNT(*) FROM areas")
            total_areas = cur.fetchone()[0]
            print(f"📊 Total áreas después de creación: {total_areas}")
        
        # Mostrar todas las áreas
        cur.execute("SELECT id, nombre, descripcion FROM areas ORDER BY nombre")
        areas = cur.fetchall()
        
        print(f"\n📋 ÁREAS DISPONIBLES:")
        for area in areas:
            print(f"   {area[0]:2d}. {area[1]} - {area[2] or 'Sin descripción'}")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando áreas: {str(e)}")
        return False

def main():
    """Función principal"""
    if verificar_y_crear_areas():
        print(f"\n✅ Verificación completada")
        print("💡 Las áreas ahora deberían aparecer en el formulario de actividades")
    else:
        print(f"\n❌ Error en verificación")

if __name__ == "__main__":
    main()