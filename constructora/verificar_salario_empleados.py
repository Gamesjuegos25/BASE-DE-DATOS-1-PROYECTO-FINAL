#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificar implementación de salario fijo en empleados
"""
from database import get_connection, insert_empleado_safe

def verificar_estructura_empleados():
    """Verificar que la tabla empleados tenga la estructura correcta"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # Verificar estructura de la tabla empleados
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'empleados' 
            ORDER BY ordinal_position
        """)
        columnas = cur.fetchall()
        
        print("🔍 Estructura tabla empleados:")
        for col in columnas:
            print(f"   {col[0]}: {col[1]}")
        
        # Verificar si existe la columna salario_fijo_empleado
        columnas_dict = {col[0]: col[1] for col in columnas}
        
        if 'salario_fijo_empleado' in columnas_dict:
            print("✅ Campo salario_fijo_empleado encontrado")
            print(f"   Tipo: {columnas_dict['salario_fijo_empleado']}")
        else:
            print("❌ Campo salario_fijo_empleado NO encontrado")
            return False
            
        # Verificar algunos empleados existentes
        cur.execute("""
            SELECT id_empleado, nombre_empleado, apellido_empleado, 
                   tipo_empleado, salario_fijo_empleado
            FROM empleados 
            WHERE salario_fijo_empleado IS NOT NULL
            LIMIT 5
        """)
        empleados_con_salario = cur.fetchall()
        
        print(f"\n📊 Empleados con salario definido ({len(empleados_con_salario)}):")
        for emp in empleados_con_salario:
            print(f"   ID {emp[0]}: {emp[1]} {emp[2]} ({emp[3]}) - ${emp[4]:,.0f}")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estructura: {str(e)}")
        return False

def probar_crear_empleado_con_salario():
    """Probar crear un empleado con salario fijo"""
    try:
        nombre = "Carlos"
        apellido = "Prueba"
        tipo = "OBRERO"
        salario = 1200000.0
        telefono = "3001234567"
        email = "carlos.prueba@test.com"
        fecha_ingreso = "2024-01-15"
        
        print(f"\n🧪 Probando crear empleado:")
        print(f"   Nombre: {nombre} {apellido}")
        print(f"   Tipo: {tipo}")
        print(f"   Salario: ${salario:,.0f}")
        
        empleado_id = insert_empleado_safe(
            nombre=nombre,
            apellido=apellido, 
            tipo=tipo,
            salario=salario,
            telefono=telefono,
            email=email,
            fecha_ingreso=fecha_ingreso
        )
        
        if empleado_id:
            print(f"✅ Empleado creado exitosamente con ID: {empleado_id}")
            
            # Verificar que se guardó correctamente
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT nombre_empleado, apellido_empleado, salario_fijo_empleado
                FROM empleados WHERE id_empleado = %s
            """, (empleado_id,))
            resultado = cur.fetchone()
            
            if resultado:
                print(f"✅ Verificación: {resultado[0]} {resultado[1]} - ${resultado[2]:,.0f}")
            else:
                print("❌ No se pudo verificar el empleado creado")
                
            cur.close()
            conn.close()
            return True
        else:
            print("❌ Error al crear empleado")
            return False
            
    except Exception as e:
        print(f"❌ Error creando empleado: {str(e)}")
        return False

def main():
    print("🚀 VERIFICACIÓN DE SALARIO FIJO EN EMPLEADOS")
    print("=" * 50)
    
    # Verificar estructura
    if not verificar_estructura_empleados():
        return
    
    # Probar funcionalidad
    probar_crear_empleado_con_salario()
    
    print("\n" + "=" * 50)
    print("✅ Verificación completada")

if __name__ == "__main__":
    main()