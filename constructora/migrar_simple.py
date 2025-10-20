#!/usr/bin/env python3
"""
Script de migración simplificado
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

def main():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("🔧 Aplicando migración simplificada...")
        
        # Agregar columnas a CLIENTES
        print("📝 Agregando columnas a CLIENTES...")
        cursor.execute("ALTER TABLE CLIENTES ADD COLUMN IF NOT EXISTS documento_cliente VARCHAR(50)")
        cursor.execute("ALTER TABLE CLIENTES ADD COLUMN IF NOT EXISTS telefono_cliente VARCHAR(20)")
        cursor.execute("ALTER TABLE CLIENTES ADD COLUMN IF NOT EXISTS email_cliente VARCHAR(150)")
        cursor.execute("ALTER TABLE CLIENTES ADD COLUMN IF NOT EXISTS direccion_cliente TEXT")
        
        # Agregar columnas a OBRAS
        print("📝 Agregando columnas a OBRAS...")
        cursor.execute("ALTER TABLE OBRAS ADD COLUMN IF NOT EXISTS descripcion_obra TEXT")
        cursor.execute("ALTER TABLE OBRAS ADD COLUMN IF NOT EXISTS fecha_inicio DATE")
        cursor.execute("ALTER TABLE OBRAS ADD COLUMN IF NOT EXISTS fecha_fin DATE")
        cursor.execute("ALTER TABLE OBRAS ADD COLUMN IF NOT EXISTS valor_obra DECIMAL(15,2)")
        cursor.execute("ALTER TABLE OBRAS ADD COLUMN IF NOT EXISTS id_cliente INTEGER")
        
        # Verificar si existe cliente por defecto
        cursor.execute("SELECT id_cliente FROM CLIENTES WHERE nombre_cliente = 'Cliente Sin Asignar' LIMIT 1")
        cliente_default = cursor.fetchone()
        
        if not cliente_default:
            print("👤 Creando cliente por defecto...")
            cursor.execute("""
                INSERT INTO CLIENTES (nombre_cliente, documento_cliente, tipo_cliente) 
                VALUES ('Cliente Sin Asignar', '000000000-0', 'TEMPORAL')
            """)
            cursor.execute("SELECT id_cliente FROM CLIENTES WHERE nombre_cliente = 'Cliente Sin Asignar' LIMIT 1")
            cliente_default = cursor.fetchone()
        
        cliente_default_id = cliente_default[0]
        print(f"🔑 Cliente por defecto ID: {cliente_default_id}")
        
        # Actualizar obras sin cliente
        cursor.execute("UPDATE OBRAS SET id_cliente = %s WHERE id_cliente IS NULL", (cliente_default_id,))
        print(f"🔄 Obras actualizadas: {cursor.rowcount}")
        
        # Insertar clientes de ejemplo
        print("📊 Insertando clientes de ejemplo...")
        clientes = [
            ('Juan Pérez Construction', '12345678-9', '+57 300 123 4567', 'juan.perez@email.com', 'Calle 123 #45-67, Bogotá'),
            ('María García Desarrollos', '23456789-0', '+57 310 234 5678', 'maria.garcia@email.com', 'Carrera 78 #90-12, Medellín'),
            ('Carlos López Inversiones', '34567890-1', '+57 320 345 6789', 'carlos.lopez@email.com', 'Avenida 15 #34-56, Cali')
        ]
        
        for nombre, documento, telefono, email, direccion in clientes:
            try:
                cursor.execute("""
                    INSERT INTO CLIENTES (nombre_cliente, documento_cliente, telefono_cliente, email_cliente, direccion_cliente)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nombre, documento, telefono, email, direccion))
                print(f"✅ Cliente insertado: {nombre}")
            except psycopg2.IntegrityError:
                print(f"⚠️  Cliente ya existe: {nombre}")
        
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()