#!/usr/bin/env python3
"""
Script para verificar y migrar la base de datos
"""
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de conexión
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', '123'),
    'database': os.getenv('DB_NAME', 'PROYECTO_FINAL_BD1'),
    'client_encoding': 'LATIN1'
}

def verificar_estructura():
    """Verificar si las columnas necesarias existen"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        print("🔍 Verificando estructura de la base de datos...")
        
        # Verificar columnas en CLIENTES
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'clientes'
            ORDER BY column_name
        """)
        columnas_clientes = [row['column_name'] for row in cursor.fetchall()]
        print(f"📋 Columnas en CLIENTES: {columnas_clientes}")
        
        # Verificar columnas en OBRAS
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'obras'
            ORDER BY column_name
        """)
        columnas_obras = [row['column_name'] for row in cursor.fetchall()]
        print(f"📋 Columnas en OBRAS: {columnas_obras}")
        
        # Verificar si existen las columnas necesarias
        columnas_necesarias_clientes = ['documento_cliente', 'telefono_cliente', 'email_cliente', 'direccion_cliente']
        columnas_necesarias_obras = ['descripcion_obra', 'fecha_inicio', 'fecha_fin', 'valor_obra', 'id_cliente']
        
        falta_clientes = [col for col in columnas_necesarias_clientes if col not in columnas_clientes]
        falta_obras = [col for col in columnas_necesarias_obras if col not in columnas_obras]
        
        if falta_clientes or falta_obras:
            print("\n❌ FALTAN COLUMNAS:")
            if falta_clientes:
                print(f"   En CLIENTES: {falta_clientes}")
            if falta_obras:
                print(f"   En OBRAS: {falta_obras}")
            return False
        else:
            print("\n✅ Todas las columnas necesarias existen")
            return True
            
    except Exception as e:
        print(f"❌ Error verificando estructura: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def aplicar_migracion():
    """Aplicar migración para agregar columnas faltantes"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("\n🔧 Aplicando migración...")
        
        # Agregar columnas a CLIENTES si no existen
        print("📝 Agregando columnas a CLIENTES...")
        cursor.execute("""
            ALTER TABLE CLIENTES 
            ADD COLUMN IF NOT EXISTS documento_cliente VARCHAR(50),
            ADD COLUMN IF NOT EXISTS telefono_cliente VARCHAR(20),
            ADD COLUMN IF NOT EXISTS email_cliente VARCHAR(150),
            ADD COLUMN IF NOT EXISTS direccion_cliente TEXT
        """)
        
        # Agregar columnas a OBRAS si no existen
        print("📝 Agregando columnas a OBRAS...")
        cursor.execute("""
            ALTER TABLE OBRAS 
            ADD COLUMN IF NOT EXISTS descripcion_obra TEXT,
            ADD COLUMN IF NOT EXISTS fecha_inicio DATE,
            ADD COLUMN IF NOT EXISTS fecha_fin DATE,
            ADD COLUMN IF NOT EXISTS valor_obra DECIMAL(15,2),
            ADD COLUMN IF NOT EXISTS id_cliente INTEGER
        """)
        
        # Crear cliente por defecto si no existe
        print("👤 Creando cliente por defecto...")
        cursor.execute("""
            INSERT INTO CLIENTES (nombre_cliente, documento_cliente, tipo_cliente) 
            VALUES ('Cliente Sin Asignar', '000000000-0', 'TEMPORAL')
            ON CONFLICT (documento_cliente) DO NOTHING
        """)
        
        # Obtener ID del cliente por defecto
        cursor.execute("""
            SELECT id_cliente FROM CLIENTES 
            WHERE documento_cliente = '000000000-0' 
            LIMIT 1
        """)
        cliente_default = cursor.fetchone()
        
        if cliente_default:
            cliente_default_id = cliente_default[0]
            print(f"🔑 Cliente por defecto ID: {cliente_default_id}")
            
            # Actualizar obras sin cliente
            cursor.execute("""
                UPDATE OBRAS 
                SET id_cliente = %s 
                WHERE id_cliente IS NULL
            """, (cliente_default_id,))
            
            print(f"🔄 Obras actualizadas: {cursor.rowcount}")
        
        print("✅ Migración completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error aplicando migración: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def insertar_datos_ejemplo():
    """Insertar algunos clientes de ejemplo"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("\n📊 Insertando datos de ejemplo...")
        
        clientes_ejemplo = [
            ('Juan Pérez Construction', '12345678-9', '+57 300 123 4567', 'juan.perez@email.com', 'Calle 123 #45-67, Bogotá'),
            ('María García Desarrollos', '23456789-0', '+57 310 234 5678', 'maria.garcia@email.com', 'Carrera 78 #90-12, Medellín'),
            ('Carlos López Inversiones', '34567890-1', '+57 320 345 6789', 'carlos.lopez@email.com', 'Avenida 15 #34-56, Cali')
        ]
        
        for nombre, documento, telefono, email, direccion in clientes_ejemplo:
            try:
                cursor.execute("""
                    INSERT INTO CLIENTES (nombre_cliente, documento_cliente, telefono_cliente, email_cliente, direccion_cliente)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombre, documento, telefono, email, direccion))
                print(f"✅ Cliente insertado: {nombre}")
            except psycopg2.IntegrityError:
                print(f"⚠️  Cliente ya existe: {nombre}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error insertando datos: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    print("🚀 MIGRADOR DE BASE DE DATOS - Sistema Constructora")
    print("=" * 60)
    
    # Verificar estructura actual
    if verificar_estructura():
        print("\n🎉 La base de datos ya está actualizada")
        
        # Preguntar si insertar datos de ejemplo
        resp = input("\n¿Insertar datos de ejemplo? (s/n): ").lower().strip()
        if resp in ['s', 'si', 'sí', 'y', 'yes']:
            insertar_datos_ejemplo()
    else:
        print("\n🔧 Es necesario aplicar migración")
        resp = input("¿Aplicar migración ahora? (s/n): ").lower().strip()
        
        if resp in ['s', 'si', 'sí', 'y', 'yes']:
            if aplicar_migracion():
                print("\n🎉 Migración completada. Verificando...")
                if verificar_estructura():
                    print("✅ Base de datos actualizada correctamente")
                    insertar_datos_ejemplo()
                else:
                    print("❌ Aún hay problemas en la estructura")
            else:
                print("❌ Error en la migración")
        else:
            print("⚠️  Migración cancelada. El sistema puede no funcionar correctamente.")
    
    print("\n" + "=" * 60)
    print("🏁 Proceso completado")

if __name__ == "__main__":
    main()