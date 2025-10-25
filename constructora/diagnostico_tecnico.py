#!/usr/bin/env python3
"""
Análisis específico de secuencias SERIAL
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from database import get_connection
import logging

def verificar_secuencias_detallado():
    """Verificar estado de todas las secuencias SERIAL con método alternativo"""
    print("\n" + "="*80)
    print("🔢 ANÁLISIS DETALLADO DE SECUENCIAS SERIAL")
    print("="*80)
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Método alternativo para obtener secuencias
                cursor.execute("""
                    SELECT 
                        schemaname, 
                        sequencename,
                        last_value,
                        start_value,
                        increment_by,
                        max_value,
                        min_value,
                        log_cnt,
                        is_cycled,
                        is_called
                    FROM pg_sequences
                    WHERE schemaname = 'public'
                    ORDER BY sequencename;
                """)
                
                secuencias = cursor.fetchall()
                
                if not secuencias:
                    # Método alternativo si pg_sequences no está disponible
                    cursor.execute("""
                        SELECT sequence_name 
                        FROM information_schema.sequences 
                        WHERE sequence_schema = 'public'
                    """)
                    seq_names = cursor.fetchall()
                    
                    print(f"\n📊 SECUENCIAS ENCONTRADAS: {len(seq_names)}")
                    print("-" * 100)
                    print(f"{'SECUENCIA':<35} {'ÚLTIMO VALOR':<12} {'TABLA MAX ID':<12} {'ESTADO':<15}")
                    print("-" * 100)
                    
                    problemas_secuencia = []
                    
                    for (seq_name,) in seq_names:
                        try:
                            # Obtener valor actual de la secuencia
                            cursor.execute(f"SELECT last_value, is_called FROM {seq_name}")
                            last_val, is_called = cursor.fetchone()
                            
                            # Determinar tabla y columna asociada
                            if '_id_' in seq_name:
                                tabla_name = seq_name.split('_id_')[0]
                                col_parts = seq_name.replace(tabla_name + '_', '').replace('_seq', '')
                                id_column = col_parts
                                
                                # Verificar máximo ID actual en la tabla
                                cursor.execute(f"SELECT MAX({id_column}) FROM {tabla_name}")
                                max_id_result = cursor.fetchone()[0]
                                max_id = max_id_result if max_id_result is not None else 0
                                
                                # Determinar estado
                                if max_id > last_val:
                                    estado = "❌ DESINCRONIZADA"
                                    problemas_secuencia.append({
                                        'secuencia': seq_name,
                                        'tabla': tabla_name,
                                        'columna': id_column,
                                        'ultimo_secuencia': last_val,
                                        'maximo_tabla': max_id,
                                        'diferencia': max_id - last_val,
                                        'is_called': is_called
                                    })
                                elif max_id == 0 and last_val == 1 and not is_called:
                                    estado = "⚠️  NUEVA/VACÍA"
                                else:
                                    estado = "✅ OK"
                                
                                print(f"{seq_name:<35} {last_val:<12} {max_id:<12} {estado:<15}")
                                
                            else:
                                print(f"{seq_name:<35} {'N/A':<12} {'N/A':<12} {'ℹ️  OTRA':<15}")
                                
                        except Exception as e:
                            estado = f"❌ ERROR"
                            print(f"{seq_name:<35} {'N/A':<12} {'N/A':<12} {estado:<15}")
                            print(f"    Error: {e}")
                            problemas_secuencia.append({
                                'secuencia': seq_name,
                                'error': str(e)
                            })
                else:
                    # Usar datos de pg_sequences si está disponible
                    print(f"\n📊 SECUENCIAS ENCONTRADAS: {len(secuencias)}")
                    print("-" * 100)
                    print(f"{'SECUENCIA':<35} {'ÚLTIMO VALOR':<12} {'CALLED':<8} {'TABLA MAX ID':<12} {'ESTADO':<15}")
                    print("-" * 100)
                    
                    problemas_secuencia = []
                    
                    for seq in secuencias:
                        schema, seq_name, last_val, start_val, incr, max_val, min_val, log_cnt, cycled, called = seq
                        
                        # Similar lógica que arriba...
                        if '_id_' in seq_name:
                            tabla_name = seq_name.split('_id_')[0]
                            col_parts = seq_name.replace(tabla_name + '_', '').replace('_seq', '')
                            id_column = col_parts
                            
                            try:
                                cursor.execute(f"SELECT MAX({id_column}) FROM {tabla_name}")
                                max_id_result = cursor.fetchone()[0]
                                max_id = max_id_result if max_id_result is not None else 0
                                
                                if max_id > last_val:
                                    estado = "❌ DESINCRONIZADA"
                                    problemas_secuencia.append({
                                        'secuencia': seq_name,
                                        'tabla': tabla_name,
                                        'columna': id_column,
                                        'ultimo_secuencia': last_val,
                                        'maximo_tabla': max_id,
                                        'diferencia': max_id - last_val,
                                        'is_called': called
                                    })
                                elif max_id == 0 and last_val == 1 and not called:
                                    estado = "⚠️  NUEVA"
                                else:
                                    estado = "✅ OK"
                                
                                print(f"{seq_name:<35} {last_val:<12} {called!s:<8} {max_id:<12} {estado:<15}")
                                
                            except Exception as e:
                                estado = f"❌ ERROR"
                                print(f"{seq_name:<35} {last_val:<12} {called!s:<8} {'N/A':<12} {estado:<15}")
                                print(f"    Error: {e}")
                
                # Mostrar problemas encontrados
                if problemas_secuencia:
                    print(f"\n🚨 PROBLEMAS DE SECUENCIAS DETECTADOS ({len(problemas_secuencia)}):")
                    for i, prob in enumerate(problemas_secuencia, 1):
                        if 'diferencia' in prob:
                            print(f"\n  {i}. ❌ SECUENCIA DESINCRONIZADA: {prob['secuencia']}")
                            print(f"     📊 Tabla: {prob['tabla']}.{prob['columna']}")
                            print(f"     🔢 Último valor secuencia: {prob['ultimo_secuencia']}")
                            print(f"     📈 Máximo ID en tabla: {prob['maximo_tabla']}")
                            print(f"     ⚠️  Diferencia: +{prob['diferencia']}")
                            print(f"     🔧 FIX COMANDO:")
                            print(f"        SELECT setval('{prob['secuencia']}', {prob['maximo_tabla'] + 1}, false);")
                        else:
                            print(f"\n  {i}. ❌ ERROR EN SECUENCIA: {prob['secuencia']}")
                            print(f"     💥 Error: {prob['error']}")
                else:
                    print("\n✅ Todas las secuencias están correctamente sincronizadas")
                
                return problemas_secuencia
                
    except Exception as e:
        print(f"❌ Error analizando secuencias: {e}")
        import traceback
        traceback.print_exc()
        return []

def verificar_funciones_aplicacion():
    """Verificar funciones específicas de la aplicación"""
    print("\n" + "="*80)
    print("🔧 ANÁLISIS DE FUNCIONES DE APLICACIÓN")
    print("="*80)
    
    try:
        # Verificar imports críticos
        from database import (
            get_clientes_safe, get_obras_safe, get_empleados_safe,
            get_materiales_safe, get_vehiculos_safe, get_equipos_safe,
            insert_cliente_safe, insert_obra_safe
        )
        
        print("✅ Imports de database.py OK")
        
        # Probar funciones GET
        funciones_get = [
            ('get_clientes_safe', get_clientes_safe),
            ('get_obras_safe', get_obras_safe),
            ('get_empleados_safe', get_empleados_safe),
            ('get_materiales_safe', get_materiales_safe),
            ('get_vehiculos_safe', get_vehiculos_safe),
            ('get_equipos_safe', get_equipos_safe)
        ]
        
        print(f"\n📊 PROBANDO FUNCIONES GET:")
        print("-" * 60)
        print(f"{'FUNCIÓN':<25} {'REGISTROS':<10} {'ESTADO':<15}")
        print("-" * 60)
        
        problemas_funciones = []
        
        for nombre, funcion in funciones_get:
            try:
                result = funcion()
                count = len(result) if result else 0
                estado = "✅ OK" if count >= 0 else "⚠️  VACÍO"
                print(f"{nombre:<25} {count:<10} {estado:<15}")
                
                if count == 0:
                    problemas_funciones.append({
                        'funcion': nombre,
                        'problema': 'Sin datos',
                        'severidad': 'BAJO'
                    })
                    
            except Exception as e:
                print(f"{nombre:<25} {'ERROR':<10} {'❌ FALLA':<15}")
                print(f"  Error: {e}")
                problemas_funciones.append({
                    'funcion': nombre,
                    'problema': str(e),
                    'severidad': 'ALTO'
                })
        
        # Probar una función INSERT básica
        print(f"\n🧪 PROBANDO FUNCIÓN INSERT (cliente de prueba):")
        try:
            cliente_id = insert_cliente_safe(
                nombre="Cliente Prueba Diagnostico",
                documento="TEST-123",
                telefono="555-0123",
                email="test@diagnostico.com"
            )
            
            if cliente_id:
                print(f"✅ INSERT OK - Cliente creado con ID: {cliente_id}")
                
                # Limpiar datos de prueba
                with get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (cliente_id,))
                        conn.commit()
                print("🧹 Datos de prueba eliminados")
            else:
                print("❌ INSERT FALLÓ - No se retornó ID")
                problemas_funciones.append({
                    'funcion': 'insert_cliente_safe',
                    'problema': 'No retorna ID',
                    'severidad': 'ALTO'
                })
                
        except Exception as e:
            print(f"❌ INSERT ERROR: {e}")
            problemas_funciones.append({
                'funcion': 'insert_cliente_safe',
                'problema': str(e),
                'severidad': 'CRÍTICO'
            })
        
        return problemas_funciones
        
    except ImportError as e:
        print(f"❌ Error importando funciones: {e}")
        return [{'funcion': 'import', 'problema': str(e), 'severidad': 'CRÍTICO'}]

def main():
    """Ejecutar análisis específico de problemas técnicos"""
    print("🔧 DIAGNÓSTICO TÉCNICO ESPECÍFICO")
    print("="*80)
    
    # 1. Análisis de secuencias
    problemas_seq = verificar_secuencias_detallado()
    
    # 2. Análisis de funciones de aplicación
    problemas_func = verificar_funciones_aplicacion()
    
    # Resumen final
    print("\n" + "="*80)
    print("📋 RESUMEN DE PROBLEMAS TÉCNICOS")
    print("="*80)
    
    total_problemas = len(problemas_seq) + len(problemas_func)
    
    print(f"\n🔢 SECUENCIAS:")
    if problemas_seq:
        print(f"  ❌ Problemas encontrados: {len(problemas_seq)}")
        for prob in problemas_seq:
            if 'diferencia' in prob:
                print(f"    - {prob['secuencia']}: +{prob['diferencia']} registros desincronizados")
    else:
        print(f"  ✅ Todas las secuencias OK")
    
    print(f"\n🔧 FUNCIONES DE APLICACIÓN:")
    if problemas_func:
        print(f"  ❌ Problemas encontrados: {len(problemas_func)}")
        criticos = [p for p in problemas_func if p['severidad'] == 'CRÍTICO']
        altos = [p for p in problemas_func if p['severidad'] == 'ALTO']
        bajos = [p for p in problemas_func if p['severidad'] == 'BAJO']
        
        if criticos:
            print(f"    🚨 CRÍTICOS: {len(criticos)}")
            for p in criticos:
                print(f"      - {p['funcion']}: {p['problema']}")
        
        if altos:
            print(f"    ⚠️  ALTOS: {len(altos)}")
            for p in altos:
                print(f"      - {p['funcion']}: {p['problema']}")
        
        if bajos:
            print(f"    ℹ️  BAJOS: {len(bajos)}")
            for p in bajos:
                print(f"      - {p['funcion']}: {p['problema']}")
    else:
        print(f"  ✅ Todas las funciones OK")
    
    print(f"\n🎯 ESTADO GENERAL:")
    if total_problemas == 0:
        print("  ✅ EXCELENTE: Sistema técnicamente sólido")
    elif total_problemas <= 3:
        print("  ⚠️  BUENO: Problemas menores detectados")
    elif total_problemas <= 10:
        print("  🟡 REGULAR: Varios problemas requieren atención")
    else:
        print("  🔴 MALO: Problemas críticos requieren corrección inmediata")

if __name__ == "__main__":
    main()