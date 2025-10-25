#!/usr/bin/env python3
"""
Diagnóstico completo del sistema - Análisis detallado de todas las inconsistencias
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from database import get_connection
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analizar_estructura_tablas():
    """Analizar estructura completa de tablas"""
    print("\n" + "="*80)
    print("🔍 ANÁLISIS DE ESTRUCTURA DE TABLAS")
    print("="*80)
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # 1. Obtener todas las tablas
                cursor.execute("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public' 
                    ORDER BY tablename
                """)
                tablas = cursor.fetchall()
                
                print(f"\n📊 TABLAS ENCONTRADAS: {len(tablas)}")
                print("-" * 50)
                
                tablas_con_problemas = []
                tablas_sin_datos = []
                tablas_ok = []
                
                for tabla in tablas:
                    nombre_tabla = tabla[0]
                    try:
                        # Verificar si tiene datos
                        cursor.execute(f"SELECT COUNT(*) FROM {nombre_tabla}")
                        count = cursor.fetchone()[0]
                        
                        # Verificar estructura
                        cursor.execute(f"""
                            SELECT column_name, data_type, is_nullable, column_default
                            FROM information_schema.columns 
                            WHERE table_name = '{nombre_tabla}'
                            ORDER BY ordinal_position
                        """)
                        columnas = cursor.fetchall()
                        
                        if count == 0:
                            tablas_sin_datos.append({
                                'nombre': nombre_tabla,
                                'columnas': len(columnas),
                                'estructura': columnas
                            })
                            print(f"  ⚠️  {nombre_tabla:25} - {count:6} registros - {len(columnas)} columnas - SIN DATOS")
                        else:
                            tablas_ok.append({
                                'nombre': nombre_tabla,
                                'registros': count,
                                'columnas': len(columnas)
                            })
                            print(f"  ✅ {nombre_tabla:25} - {count:6} registros - {len(columnas)} columnas")
                            
                    except Exception as e:
                        tablas_con_problemas.append({
                            'nombre': nombre_tabla,
                            'error': str(e)
                        })
                        print(f"  ❌ {nombre_tabla:25} - ERROR: {str(e)}")
                
                print(f"\n📈 RESUMEN:")
                print(f"  ✅ Tablas OK: {len(tablas_ok)}")
                print(f"  ⚠️  Tablas vacías: {len(tablas_sin_datos)}")
                print(f"  ❌ Tablas con errores: {len(tablas_con_problemas)}")
                
                return {
                    'total_tablas': len(tablas),
                    'tablas_ok': tablas_ok,
                    'tablas_sin_datos': tablas_sin_datos,
                    'tablas_con_problemas': tablas_con_problemas
                }
                
    except Exception as e:
        print(f"❌ Error analizando estructura: {e}")
        traceback.print_exc()
        return None

def verificar_foreign_keys():
    """Verificar integridad de foreign keys"""
    print("\n" + "="*80)
    print("🔗 ANÁLISIS DE FOREIGN KEYS E INTEGRIDAD REFERENCIAL")
    print("="*80)
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Obtener todas las foreign keys
                cursor.execute("""
                    SELECT 
                        tc.table_name, 
                        kcu.column_name, 
                        ccu.table_name AS foreign_table_name,
                        ccu.column_name AS foreign_column_name,
                        rc.delete_rule,
                        rc.update_rule
                    FROM information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                        AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                        AND ccu.table_schema = tc.table_schema
                    JOIN information_schema.referential_constraints AS rc
                        ON tc.constraint_name = rc.constraint_name
                        AND tc.table_schema = rc.constraint_schema
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                    ORDER BY tc.table_name, kcu.column_name;
                """)
                
                foreign_keys = cursor.fetchall()
                
                print(f"\n📊 FOREIGN KEYS ENCONTRADAS: {len(foreign_keys)}")
                print("-" * 100)
                print(f"{'TABLA':<20} {'COLUMNA':<20} {'REFERENCIA':<25} {'ON DELETE':<12} {'ON UPDATE':<12}")
                print("-" * 100)
                
                fk_problems = []
                
                for fk in foreign_keys:
                    tabla, columna, ref_tabla, ref_columna, del_rule, up_rule = fk
                    print(f"{tabla:<20} {columna:<20} {ref_tabla}.{ref_columna:<20} {del_rule:<12} {up_rule:<12}")
                    
                    # Verificar integridad referencial
                    try:
                        cursor.execute(f"""
                            SELECT COUNT(*) FROM {tabla} t1
                            LEFT JOIN {ref_tabla} t2 ON t1.{columna} = t2.{ref_columna}
                            WHERE t1.{columna} IS NOT NULL AND t2.{ref_columna} IS NULL
                        """)
                        huerfanos = cursor.fetchone()[0]
                        
                        if huerfanos > 0:
                            fk_problems.append({
                                'tabla': tabla,
                                'columna': columna,
                                'referencia': f"{ref_tabla}.{ref_columna}",
                                'huerfanos': huerfanos
                            })
                            print(f"    ❌ {huerfanos} registros huérfanos encontrados")
                            
                    except Exception as e:
                        fk_problems.append({
                            'tabla': tabla,
                            'columna': columna,
                            'error': str(e)
                        })
                        print(f"    ❌ Error verificando integridad: {e}")
                
                if fk_problems:
                    print(f"\n🚨 PROBLEMAS DE INTEGRIDAD REFERENCIAL:")
                    for problem in fk_problems:
                        if 'huerfanos' in problem:
                            print(f"  ❌ {problem['tabla']}.{problem['columna']} → {problem['referencia']}: {problem['huerfanos']} registros huérfanos")
                        else:
                            print(f"  ❌ {problem['tabla']}.{problem['columna']}: {problem['error']}")
                else:
                    print("\n✅ Integridad referencial OK - No se encontraron registros huérfanos")
                
                return foreign_keys, fk_problems
                
    except Exception as e:
        print(f"❌ Error analizando foreign keys: {e}")
        traceback.print_exc()
        return [], []

def verificar_secuencias():
    """Verificar estado de todas las secuencias SERIAL"""
    print("\n" + "="*80)
    print("🔢 ANÁLISIS DE SECUENCIAS SERIAL")
    print("="*80)
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Obtener todas las secuencias
                cursor.execute("""
                    SELECT schemaname, sequencename, last_value, start_value, increment_by, 
                           max_value, min_value, cache_value, log_cnt, is_cycled, is_called
                    FROM pg_sequences
                    WHERE schemaname = 'public'
                    ORDER BY sequencename;
                """)
                
                secuencias = cursor.fetchall()
                
                print(f"\n📊 SECUENCIAS ENCONTRADAS: {len(secuencias)}")
                print("-" * 100)
                print(f"{'SECUENCIA':<35} {'ÚLTIMO VALOR':<12} {'CALLED':<8} {'TABLA MAX ID':<12} {'ESTADO':<10}")
                print("-" * 100)
                
                problemas_secuencia = []
                
                for seq in secuencias:
                    schema, seq_name, last_val, start_val, incr, max_val, min_val, cache, log_cnt, cycled, called = seq
                    
                    # Extraer nombre de tabla de la secuencia
                    if '_id_' in seq_name:
                        tabla_name = seq_name.split('_id_')[0]
                        id_column = seq_name.split('_')[-2] + '_' + seq_name.split('_')[-1].replace('seq', '').replace('_', '')
                        if not id_column.startswith('id_'):
                            id_column = 'id_' + id_column
                        
                        try:
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
                                    'diferencia': max_id - last_val
                                })
                            elif max_id == 0 and last_val == 1 and not called:
                                estado = "⚠️  NUEVA"
                            else:
                                estado = "✅ OK"
                            
                            print(f"{seq_name:<35} {last_val:<12} {called!s:<8} {max_id:<12} {estado:<10}")
                            
                        except Exception as e:
                            estado = f"❌ ERROR: {e}"
                            print(f"{seq_name:<35} {last_val:<12} {called!s:<8} {'N/A':<12} {estado:<10}")
                            problemas_secuencia.append({
                                'secuencia': seq_name,
                                'error': str(e)
                            })
                    else:
                        print(f"{seq_name:<35} {last_val:<12} {called!s:<8} {'N/A':<12} {'ℹ️  OTRO':<10}")
                
                if problemas_secuencia:
                    print(f"\n🚨 PROBLEMAS DE SECUENCIAS DETECTADOS:")
                    for prob in problemas_secuencia:
                        if 'diferencia' in prob:
                            print(f"  ❌ {prob['secuencia']}:")
                            print(f"     Tabla: {prob['tabla']}.{prob['columna']}")
                            print(f"     Último valor secuencia: {prob['ultimo_secuencia']}")
                            print(f"     Máximo ID en tabla: {prob['maximo_tabla']}")
                            print(f"     Diferencia: +{prob['diferencia']}")
                            print(f"     FIX: SELECT setval('{prob['secuencia']}', {prob['maximo_tabla'] + 1}, false);")
                            print()
                        else:
                            print(f"  ❌ {prob['secuencia']}: {prob['error']}")
                else:
                    print("\n✅ Todas las secuencias están sincronizadas")
                
                return secuencias, problemas_secuencia
                
    except Exception as e:
        print(f"❌ Error analizando secuencias: {e}")
        traceback.print_exc()
        return [], []

def verificar_indices():
    """Verificar índices de base de datos"""
    print("\n" + "="*80)
    print("📇 ANÁLISIS DE ÍNDICES")
    print("="*80)
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                # Obtener todos los índices
                cursor.execute("""
                    SELECT 
                        schemaname, 
                        tablename, 
                        indexname, 
                        indexdef
                    FROM pg_indexes 
                    WHERE schemaname = 'public'
                    ORDER BY tablename, indexname;
                """)
                
                indices = cursor.fetchall()
                
                print(f"\n📊 ÍNDICES ENCONTRADOS: {len(indices)}")
                print("-" * 100)
                
                indices_pk = []
                indices_fk = []
                indices_custom = []
                
                for idx in indices:
                    schema, tabla, nombre_idx, definicion = idx
                    
                    if '_pkey' in nombre_idx:
                        indices_pk.append((tabla, nombre_idx))
                    elif any(fk_word in nombre_idx.lower() for fk_word in ['fk_', 'foreign', 'ref_']):
                        indices_fk.append((tabla, nombre_idx))
                    else:
                        indices_custom.append((tabla, nombre_idx, definicion))
                    
                    print(f"  {tabla:<25} {nombre_idx:<40}")
                
                print(f"\n📈 RESUMEN DE ÍNDICES:")
                print(f"  🔑 Claves primarias (PKs): {len(indices_pk)}")
                print(f"  🔗 Foreign keys: {len(indices_fk)}")
                print(f"  ⚡ Índices personalizados: {len(indices_custom)}")
                
                # Sugerencias de índices faltantes
                print(f"\n💡 RECOMENDACIONES DE ÍNDICES FALTANTES:")
                
                # Verificar si hay índices en foreign keys
                cursor.execute("""
                    SELECT DISTINCT 
                        tc.table_name, 
                        kcu.column_name
                    FROM information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                    AND tc.table_schema = 'public'
                """)
                
                fk_columns = cursor.fetchall()
                
                indices_recomendados = []
                for tabla, columna in fk_columns:
                    # Verificar si ya existe índice para esta columna
                    cursor.execute(f"""
                        SELECT COUNT(*) FROM pg_indexes 
                        WHERE tablename = '{tabla}' 
                        AND indexdef ILIKE '%{columna}%'
                    """)
                    
                    tiene_indice = cursor.fetchone()[0] > 0
                    
                    if not tiene_indice:
                        indices_recomendados.append((tabla, columna))
                        print(f"  ⚡ CREATE INDEX idx_{tabla}_{columna} ON {tabla}({columna});")
                
                if not indices_recomendados:
                    print("  ✅ Todos los foreign keys tienen índices apropiados")
                
                return indices, indices_recomendados
                
    except Exception as e:
        print(f"❌ Error analizando índices: {e}")
        traceback.print_exc()
        return [], []

def verificar_datos_inconsistentes():
    """Verificar datos inconsistentes en el sistema"""
    print("\n" + "="*80)
    print("🔍 ANÁLISIS DE INCONSISTENCIAS EN DATOS")
    print("="*80)
    
    inconsistencias = []
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                
                # 1. Verificar obras sin cliente (si la tabla existe)
                try:
                    cursor.execute("""
                        SELECT COUNT(*) FROM obras WHERE id_cliente IS NULL
                    """)
                    obras_sin_cliente = cursor.fetchone()[0]
                    if obras_sin_cliente > 0:
                        inconsistencias.append(f"❌ {obras_sin_cliente} obras sin cliente asignado")
                    else:
                        print("✅ Todas las obras tienen cliente asignado")
                except:
                    print("⚠️  Tabla OBRAS no encontrada o no accesible")
                
                # 2. Verificar empleados sin datos básicos
                try:
                    cursor.execute("""
                        SELECT COUNT(*) FROM empleados 
                        WHERE nombre_empleado IS NULL OR TRIM(nombre_empleado) = ''
                    """)
                    empleados_sin_nombre = cursor.fetchone()[0]
                    if empleados_sin_nombre > 0:
                        inconsistencias.append(f"❌ {empleados_sin_nombre} empleados sin nombre")
                    else:
                        print("✅ Todos los empleados tienen nombre")
                except:
                    print("⚠️  Tabla EMPLEADOS no encontrada")
                
                # 3. Verificar materiales con precios negativos o cero
                try:
                    cursor.execute("""
                        SELECT COUNT(*) FROM materiales 
                        WHERE precio_unitario_material <= 0
                    """)
                    materiales_precio_invalido = cursor.fetchone()[0]
                    if materiales_precio_invalido > 0:
                        inconsistencias.append(f"❌ {materiales_precio_invalido} materiales con precio inválido (≤0)")
                    else:
                        print("✅ Todos los materiales tienen precios válidos")
                except:
                    print("⚠️  Tabla MATERIALES no encontrada")
                
                # 4. Verificar facturas con totales inconsistentes
                try:
                    cursor.execute("""
                        SELECT COUNT(*) FROM facturas 
                        WHERE total < 0 OR (subtotal + impuestos - descuento) != total
                    """)
                    facturas_inconsistentes = cursor.fetchone()[0]
                    if facturas_inconsistentes > 0:
                        inconsistencias.append(f"❌ {facturas_inconsistentes} facturas con cálculos incorrectos")
                    else:
                        print("✅ Todas las facturas tienen cálculos correctos")
                except:
                    print("⚠️  Tabla FACTURAS no encontrada")
                
                # 5. Verificar usuarios duplicados
                try:
                    cursor.execute("""
                        SELECT nombre_usuario, COUNT(*) 
                        FROM usuarios_sistema 
                        GROUP BY nombre_usuario 
                        HAVING COUNT(*) > 1
                    """)
                    usuarios_duplicados = cursor.fetchall()
                    if usuarios_duplicados:
                        for usuario, count in usuarios_duplicados:
                            inconsistencias.append(f"❌ Usuario '{usuario}' duplicado {count} veces")
                    else:
                        print("✅ No hay usuarios duplicados")
                except:
                    print("⚠️  Tabla USUARIOS_SISTEMA no encontrada")
                
                # 6. Verificar vehículos con placas duplicadas
                try:
                    cursor.execute("""
                        SELECT placa_vehiculo, COUNT(*) 
                        FROM vehiculos 
                        WHERE placa_vehiculo IS NOT NULL
                        GROUP BY placa_vehiculo 
                        HAVING COUNT(*) > 1
                    """)
                    placas_duplicadas = cursor.fetchall()
                    if placas_duplicadas:
                        for placa, count in placas_duplicadas:
                            inconsistencias.append(f"❌ Placa '{placa}' duplicada {count} veces")
                    else:
                        print("✅ No hay placas de vehículos duplicadas")
                except:
                    print("⚠️  Tabla VEHICULOS no encontrada")
                
                # Resumen de inconsistencias
                if inconsistencias:
                    print(f"\n🚨 INCONSISTENCIAS ENCONTRADAS ({len(inconsistencias)}):")
                    for inc in inconsistencias:
                        print(f"  {inc}")
                else:
                    print("\n✅ No se encontraron inconsistencias en los datos")
                
                return inconsistencias
                
    except Exception as e:
        print(f"❌ Error verificando inconsistencias: {e}")
        traceback.print_exc()
        return []

def main():
    """Ejecutar diagnóstico completo"""
    print("🏗️  SISTEMA ERP CONSTRUCTORA - DIAGNÓSTICO COMPLETO")
    print("=" * 80)
    print("📅 Fecha:", "24 de octubre de 2025")
    print("🔧 Analizando base de datos PostgreSQL...")
    
    # 1. Estructura de tablas
    resultado_tablas = analizar_estructura_tablas()
    
    # 2. Foreign keys e integridad
    fks, fk_problems = verificar_foreign_keys()
    
    # 3. Secuencias SERIAL
    secuencias, seq_problems = verificar_secuencias()
    
    # 4. Índices
    indices, indices_recomendados = verificar_indices()
    
    # 5. Inconsistencias en datos
    inconsistencias = verificar_datos_inconsistentes()
    
    # Generar resumen final
    print("\n" + "="*80)
    print("📋 RESUMEN FINAL DEL DIAGNÓSTICO")
    print("="*80)
    
    if resultado_tablas:
        print(f"\n🗄️  TABLAS:")
        print(f"  ✅ Total: {resultado_tablas['total_tablas']}")
        print(f"  ✅ Con datos: {len(resultado_tablas['tablas_ok'])}")
        print(f"  ⚠️  Vacías: {len(resultado_tablas['tablas_sin_datos'])}")
        print(f"  ❌ Con errores: {len(resultado_tablas['tablas_con_problemas'])}")
    
    print(f"\n🔗 FOREIGN KEYS:")
    print(f"  ✅ Total: {len(fks)}")
    print(f"  ❌ Con problemas: {len(fk_problems)}")
    
    print(f"\n🔢 SECUENCIAS:")
    print(f"  ✅ Total: {len(secuencias)}")
    print(f"  ❌ Desincronizadas: {len(seq_problems)}")
    
    print(f"\n📇 ÍNDICES:")
    print(f"  ✅ Existentes: {len(indices)}")
    print(f"  💡 Recomendados: {len(indices_recomendados)}")
    
    print(f"\n🔍 INCONSISTENCIAS:")
    print(f"  ❌ Encontradas: {len(inconsistencias)}")
    
    # Prioridades de corrección
    print(f"\n🎯 PRIORIDADES DE CORRECCIÓN:")
    
    if seq_problems:
        print("  🔥 CRÍTICO: Corregir secuencias desincronizadas")
        for prob in seq_problems:
            if 'diferencia' in prob:
                print(f"     python -c \"from database import get_connection; conn=get_connection(); cursor=conn.cursor(); cursor.execute(\\\"SELECT setval('{prob['secuencia']}', {prob['maximo_tabla'] + 1}, false)\\\"); conn.commit(); conn.close(); print('Secuencia {prob['secuencia']} corregida')\"")
    
    if fk_problems:
        print("  🔴 ALTO: Resolver problemas de integridad referencial")
    
    if indices_recomendados:
        print("  🟡 MEDIO: Agregar índices recomendados para performance")
    
    if inconsistencias:
        print("  🟠 BAJO: Limpiar inconsistencias en datos")
    
    if not any([seq_problems, fk_problems, len(indices_recomendados) > 5, len(inconsistencias) > 5]):
        print("  ✅ EXCELENTE: La base de datos está en buen estado")
    
    print("\n" + "="*80)
    print("✨ DIAGNÓSTICO COMPLETADO")
    print("="*80)

if __name__ == "__main__":
    main()