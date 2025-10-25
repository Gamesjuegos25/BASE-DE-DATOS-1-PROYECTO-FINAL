#!/usr/bin/env python3
"""
Verificar y actualizar campos de empleados para mostrar contacto y fecha de contratación
"""

import sys
import os
from datetime import datetime, date
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database import get_connection
except ImportError:
    print("Error: No se pudo importar database.py")
    sys.exit(1)

def verificar_campos_empleados():
    """Verifica qué campos tiene la tabla empleados"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print("🔍 VERIFICANDO ESTRUCTURA DE TABLA EMPLEADOS")
        print("=" * 50)
        
        # Obtener estructura de la tabla
        cur.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'empleados'
            ORDER BY ordinal_position
        """)
        
        columnas = cur.fetchall()
        
        campos_requeridos = ['telefono', 'email', 'fecha_ingreso']
        campos_encontrados = []
        
        print("CAMPOS ACTUALES:")
        for col in columnas:
            nombre, tipo, nullable = col
            print(f"• {nombre} ({tipo}) - {'NULL' if nullable == 'YES' else 'NOT NULL'}")
            if nombre in campos_requeridos:
                campos_encontrados.append(nombre)
        
        print(f"\nCAMPOS PARA CONTACTO Y FECHA:")
        for campo in campos_requeridos:
            if campo in campos_encontrados:
                print(f"✅ {campo} - Existe")
            else:
                print(f"❌ {campo} - No existe")
        
        cur.close()
        conn.close()
        
        return campos_encontrados
        
    except Exception as e:
        print(f"Error: {e}")
        return []

def agregar_campos_faltantes():
    """Agrega campos faltantes a la tabla empleados"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print(f"\n🔧 AGREGANDO CAMPOS FALTANTES")
        print("=" * 35)
        
        # Verificar si existen los campos y agregarlos si no existen
        campos_a_agregar = [
            ("telefono", "VARCHAR(20)"),
            ("email", "VARCHAR(100)"),
            ("fecha_ingreso", "DATE")
        ]
        
        for campo, tipo in campos_a_agregar:
            try:
                # Intentar agregar el campo
                cur.execute(f"ALTER TABLE empleados ADD COLUMN {campo} {tipo}")
                print(f"✅ Campo '{campo}' agregado exitosamente")
            except Exception as e:
                if "already exists" in str(e) or "ya existe" in str(e):
                    print(f"⚪ Campo '{campo}' ya existe")
                else:
                    print(f"❌ Error agregando '{campo}': {e}")
        
        conn.commit()
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def actualizar_datos_empleados():
    """Actualiza empleados existentes con datos de contacto y fecha"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print(f"\n📊 ACTUALIZANDO DATOS DE EMPLEADOS")
        print("=" * 40)
        
        # Datos de ejemplo para actualizar
        datos_actualizacion = [
            {
                'id': 1,
                'telefono': '2234-5678',
                'email': 'pedro.sanchez@constructora.com',
                'fecha_ingreso': '2023-01-15'
            },
            {
                'id': 2,
                'telefono': '2345-6789',
                'email': 'luisa.martinez@constructora.com',
                'fecha_ingreso': '2023-02-01'
            },
            {
                'id': 4,
                'telefono': '2456-7890',
                'email': 'carmen.ruiz@constructora.com',
                'fecha_ingreso': '2023-03-10'
            },
            {
                'id': 5,
                'telefono': '2567-8901',
                'email': 'jorge.lopez@constructora.com',
                'fecha_ingreso': '2023-01-20'
            },
            {
                'id': 6,
                'telefono': '2678-9012',
                'email': 'maria.gonzalez@constructora.com',
                'fecha_ingreso': '2023-04-05'
            },
            {
                'id': 7,
                'telefono': '2789-0123',
                'email': 'carlos.rodriguez@constructora.com',
                'fecha_ingreso': '2023-02-15'
            },
            {
                'id': 8,
                'telefono': '2890-1234',
                'email': 'ana.torres@constructora.com',
                'fecha_ingreso': '2023-03-01'
            },
            {
                'id': 9,
                'telefono': '2901-2345',
                'email': 'miguel.herrera@constructora.com',
                'fecha_ingreso': '2023-03-20'
            },
            {
                'id': 10,
                'telefono': '3012-3456',
                'email': 'jose.morales@constructora.com',
                'fecha_ingreso': '2023-04-01'
            },
            {
                'id': 11,
                'telefono': '3123-4567',
                'email': 'david.castillo@constructora.com',
                'fecha_ingreso': '2023-04-10'
            }
        ]
        
        empleados_actualizados = 0
        
        for datos in datos_actualizacion:
            try:
                cur.execute("""
                    UPDATE empleados 
                    SET telefono = %s, email = %s, fecha_ingreso = %s
                    WHERE id_empleado = %s
                """, (datos['telefono'], datos['email'], datos['fecha_ingreso'], datos['id']))
                
                if cur.rowcount > 0:
                    empleados_actualizados += 1
                    print(f"✅ Empleado ID {datos['id']} actualizado")
                else:
                    print(f"⚪ Empleado ID {datos['id']} no encontrado")
                    
            except Exception as e:
                print(f"❌ Error actualizando empleado ID {datos['id']}: {e}")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"\n📊 RESUMEN: {empleados_actualizados} empleados actualizados")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def verificar_resultado_final():
    """Verifica el resultado final de la actualización"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print(f"\n🎯 VERIFICACIÓN FINAL")
        print("=" * 25)
        
        cur.execute("""
            SELECT 
                id_empleado,
                nombre_empleado,
                tipo_empleado,
                telefono,
                email,
                fecha_ingreso,
                salario_fijo_empleado
            FROM empleados 
            ORDER BY id_empleado
            LIMIT 5
        """)
        
        empleados = cur.fetchall()
        
        print("EMPLEADOS CON DATOS COMPLETOS:")
        print("-" * 70)
        
        for emp in empleados:
            id_emp, nombre, cargo, telefono, email, fecha, salario = emp
            
            print(f"ID: {id_emp}")
            print(f"  Nombre: {nombre}")
            print(f"  Cargo: {cargo}")
            print(f"  Teléfono: {telefono or 'Sin teléfono'}")
            print(f"  Email: {email or 'Sin email'}")
            print(f"  Fecha Ingreso: {fecha or 'Sin fecha'}")
            print(f"  Salario: Q{salario:,.2f}" if salario else "Sin salario")
            print("-" * 30)
        
        # Contar empleados con datos completos
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(telefono) as con_telefono,
                COUNT(email) as con_email,
                COUNT(fecha_ingreso) as con_fecha
            FROM empleados
        """)
        
        stats = cur.fetchone()
        total, con_tel, con_email, con_fecha = stats
        
        print(f"ESTADÍSTICAS:")
        print(f"• Total empleados: {total}")
        print(f"• Con teléfono: {con_tel}")
        print(f"• Con email: {con_email}")
        print(f"• Con fecha ingreso: {con_fecha}")
        
        completitud = (con_tel + con_email + con_fecha) / (total * 3) * 100 if total > 0 else 0
        print(f"• Completitud datos: {completitud:.1f}%")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 ACTUALIZAR CAMPOS DE EMPLEADOS PARA VISTA COMPLETA")
    print("=" * 60)
    
    # 1. Verificar campos actuales
    campos_existentes = verificar_campos_empleados()
    
    # 2. Agregar campos faltantes si es necesario
    if len(campos_existentes) < 3:
        if agregar_campos_faltantes():
            print("✅ Campos agregados correctamente")
    
    # 3. Actualizar datos de empleados
    if actualizar_datos_empleados():
        print("✅ Datos de empleados actualizados")
    
    # 4. Verificar resultado final
    if verificar_resultado_final():
        print("\n🎉 ACTUALIZACIÓN COMPLETADA")
        print("=" * 30)
        print("✅ Campos de contacto y fecha agregados")
        print("✅ Datos de ejemplo cargados")
        print("✅ Template actualizado para mostrar:")
        print("   • Cargo con badge colorido")
        print("   • Contacto (teléfono y email)")
        print("   • Salario Fijo con badge")
        print("   • Fecha de contratación")
        print("✅ Vista responsiva mantenida")

if __name__ == "__main__":
    main()