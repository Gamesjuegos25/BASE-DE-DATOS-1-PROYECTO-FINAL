#!/usr/bin/env python3
"""
🔍 VERIFICADOR DE FUNCIONES DE DETALLE
Verifica que todas las funciones get_*_by_id_safe estén actualizadas y funcionen correctamente
"""

import sys
import os
from datetime import datetime

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database import (
        get_empleado_by_id_safe,
        get_material_by_id_safe,
        get_obra_by_id_safe,
        get_proveedor_by_id_safe,
        get_equipo_by_id_safe,
        get_vehiculo_by_id_safe,
        get_contrato_by_id_safe,
        get_bitacora_by_id_safe,
        get_factura_by_id_safe,
        get_cliente_by_id_safe
    )
    print("✅ Todas las funciones importadas correctamente")
except ImportError as e:
    print(f"❌ Error importando funciones: {e}")
    sys.exit(1)

def verificar_funcion(nombre_funcion, funcion, test_id=1):
    """Verifica una función específica"""
    print(f"\n🔍 Probando {nombre_funcion}(id={test_id})...")
    
    try:
        resultado = funcion(test_id)
        
        if resultado is None:
            print(f"   ⚠️  No se encontraron datos con ID {test_id}")
            return False
        
        if isinstance(resultado, dict):
            campos = list(resultado.keys())
            print(f"   ✅ Función OK - {len(campos)} campos retornados")
            print(f"   📋 Campos: {', '.join(campos[:5])}{'...' if len(campos) > 5 else ''}")
            
            # Verificar campos importantes
            if 'id' in str(campos).lower():
                print("   ✅ Contiene campo ID")
            
            return True
        else:
            print(f"   ❌ Tipo de retorno inesperado: {type(resultado)}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error en función: {str(e)[:100]}...")
        return False

def main():
    print("=" * 60)
    print("🧪 VERIFICACIÓN DE FUNCIONES DE DETALLE")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Lista de funciones a verificar
    funciones_a_verificar = [
        ("get_empleado_by_id_safe", get_empleado_by_id_safe),
        ("get_material_by_id_safe", get_material_by_id_safe),
        ("get_obra_by_id_safe", get_obra_by_id_safe),
        ("get_proveedor_by_id_safe", get_proveedor_by_id_safe),
        ("get_equipo_by_id_safe", get_equipo_by_id_safe),
        ("get_vehiculo_by_id_safe", get_vehiculo_by_id_safe),
        ("get_contrato_by_id_safe", get_contrato_by_id_safe),
        ("get_bitacora_by_id_safe", get_bitacora_by_id_safe),
        ("get_factura_by_id_safe", get_factura_by_id_safe),
        ("get_cliente_by_id_safe", get_cliente_by_id_safe),
    ]
    
    resultados = []
    
    # Verificar cada función con IDs específicos
    ids_especificos = {
        "get_obra_by_id_safe": 9,  # Usamos un ID que existe
    }
    
    for nombre, funcion in funciones_a_verificar:
        test_id = ids_especificos.get(nombre, 1)
        exito = verificar_funcion(nombre, funcion, test_id)
        resultados.append((nombre, exito))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    exitosas = sum(1 for _, exito in resultados if exito)
    total = len(resultados)
    
    for nombre, exito in resultados:
        estado = "✅ OK" if exito else "❌ ERROR"
        print(f"{estado} {nombre}")
    
    print(f"\n🎯 RESULTADO: {exitosas}/{total} funciones funcionando correctamente")
    
    if exitosas == total:
        print("🎉 ¡TODAS LAS FUNCIONES ESTÁN FUNCIONANDO!")
        return True
    else:
        print(f"⚠️  {total - exitosas} funciones necesitan atención")
        return False

if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)