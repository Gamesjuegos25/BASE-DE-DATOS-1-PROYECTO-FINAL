#!/usr/bin/env python3
"""
Script de Implementación del Sistema ERP Constructora Completo
86 Tablas - 8 Módulos Integrados

Este script ejecuta la implementación completa del sistema extendido.
"""

import subprocess
import sys
import os
import time

def ejecutar_comando(comando, descripcion):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n{'='*60}")
    print(f"🔄 {descripcion}")
    print(f"{'='*60}")
    
    try:
        if isinstance(comando, list):
            resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
        else:
            resultado = subprocess.run(comando, capture_output=True, text=True, shell=True)
        
        if resultado.returncode == 0:
            print(f"✅ {descripcion} - EXITOSO")
            if resultado.stdout:
                print("Salida:", resultado.stdout[:500])
        else:
            print(f"❌ {descripcion} - ERROR")
            print("Error:", resultado.stderr)
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def verificar_postgres():
    """Verifica si PostgreSQL está ejecutándose"""
    print("\n🔍 Verificando PostgreSQL...")
    comando = 'psql -U postgres -d PROYECTO_FINAL_BD1 -c "SELECT version();"'
    return ejecutar_comando(comando, "Verificación de PostgreSQL")

def crear_tablas_extendidas():
    """Crea las 30 nuevas tablas"""
    print("\n📊 Creando 30 nuevas tablas...")
    comando = 'psql -U postgres -d PROYECTO_FINAL_BD1 -f "EXTENSION_TABLAS_COMPLETA.sql"'
    return ejecutar_comando(comando, "Creación de tablas extendidas")

def insertar_datos_ejemplo():
    """Inserta datos de ejemplo en las nuevas tablas"""
    print("\n💾 Insertando datos de ejemplo...")
    comando = 'psql -U postgres -d PROYECTO_FINAL_BD1 -f "DATOS_EXTENSION_COMPLETA.sql"'
    return ejecutar_comando(comando, "Inserción de datos de ejemplo")

def instalar_dependencias():
    """Instala las dependencias de Python necesarias"""
    print("\n📦 Verificando dependencias de Python...")
    
    dependencias = [
        "flask==3.0.0",
        "psycopg2-binary==2.9.9",
        "python-dotenv==1.0.0"
    ]
    
    for dep in dependencias:
        comando = f"pip install {dep}"
        if not ejecutar_comando(comando, f"Instalando {dep}"):
            return False
    
    return True

def integrar_codigo_extendido():
    """Integra el código extendido al sistema existente"""
    print("\n🔧 Integrando código extendido...")
    
    try:
        # Leer el archivo de extensión de database.py
        with open('database_extension.py', 'r', encoding='utf-8') as f:
            extension_code = f.read()
        
        # Leer el archivo database.py existente
        with open('database.py', 'r', encoding='utf-8') as f:
            existing_code = f.read()
        
        # Verificar si ya está integrado
        if "# FUNCIONES EXTENDIDAS PARA 30 NUEVAS TABLAS" in existing_code:
            print("✅ El código extendido ya está integrado en database.py")
        else:
            # Agregar el código de extensión
            with open('database.py', 'a', encoding='utf-8') as f:
                f.write('\n\n' + extension_code)
            print("✅ Código extendido agregado a database.py")
        
        return True
    
    except Exception as e:
        print(f"❌ Error integrando código: {e}")
        return False

def crear_rutas_extendidas():
    """Crea las rutas extendidas en app.py"""
    print("\n🛠️ Configurando rutas extendidas...")
    
    try:
        # Leer el archivo de extensión de app.py
        with open('app_extension.py', 'r', encoding='utf-8') as f:
            extension_routes = f.read()
        
        # Leer el archivo app.py existente
        with open('app.py', 'r', encoding='utf-8') as f:
            existing_app = f.read()
        
        # Verificar si ya está integrado
        if "# RUTAS MÓDULO FACTURACIÓN Y PAGOS" in existing_app:
            print("✅ Las rutas extendidas ya están integradas en app.py")
        else:
            # Buscar el punto de inserción (antes del if __name__ == '__main__':)
            insertion_point = existing_app.find("if __name__ == '__main__':")
            if insertion_point != -1:
                new_app_content = (existing_app[:insertion_point] + 
                                 '\n\n' + extension_routes + '\n\n' + 
                                 existing_app[insertion_point:])
                
                with open('app.py', 'w', encoding='utf-8') as f:
                    f.write(new_app_content)
                print("✅ Rutas extendidas agregadas a app.py")
            else:
                print("❌ No se pudo encontrar el punto de inserción en app.py")
                return False
        
        return True
    
    except Exception as e:
        print(f"❌ Error configurando rutas: {e}")
        return False

def verificar_sistema():
    """Verifica que el sistema está funcionando correctamente"""
    print("\n🔍 Verificando sistema completo...")
    
    # Verificar tablas creadas
    comando = '''psql -U postgres -d PROYECTO_FINAL_BD1 -c "
    SELECT 'Total de tablas: ' || COUNT(*) as resultado
    FROM information_schema.tables 
    WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    "'''
    
    if not ejecutar_comando(comando, "Verificación de tablas"):
        return False
    
    # Verificar datos insertados
    comando = '''psql -U postgres -d PROYECTO_FINAL_BD1 -c "
    SELECT 'Facturas: ' || COUNT(*) FROM FACTURAS
    UNION ALL
    SELECT 'Repuestos: ' || COUNT(*) FROM REPUESTOS
    UNION ALL
    SELECT 'Métricas KPI: ' || COUNT(*) FROM METRICAS_KPI;
    "'''
    
    return ejecutar_comando(comando, "Verificación de datos")

def mostrar_resumen():
    """Muestra un resumen del sistema implementado"""
    print(f"\n{'='*80}")
    print("🎉 SISTEMA ERP CONSTRUCTORA COMPLETO IMPLEMENTADO")
    print(f"{'='*80}")
    print("""
📊 ESTADÍSTICAS DEL SISTEMA:
   • Total de Tablas: 86 (56 originales + 30 nuevas)
   • Módulos Funcionales: 8
   • Archivos de Configuración: 5
   • Plantillas HTML: 15+
   • Funciones de Base de Datos: 150+

🏗️ MÓDULOS IMPLEMENTADOS:
   1. Comercial (Clientes, Obras, Contratos)
   2. Facturación (Facturas, Pagos, Cobranzas)
   3. Contabilidad (Cuentas, Movimientos, Flujo de Caja)
   4. Recursos Humanos (Empleados, Nómina, Capacitaciones)
   5. Activos (Equipos, Vehículos, Mantenimiento)
   6. Inventarios (Materiales, Bodegas, Compras)
   7. Reportes (KPIs, Dashboards, Alertas)
   8. Seguridad (Auditoría, Control de Acceso)

🚀 PARA EJECUTAR EL SISTEMA:
   1. cd constructora
   2. python app.py
   3. Abrir navegador en: http://127.0.0.1:5000
   4. Acceder a: http://127.0.0.1:5000/sistema-completo

🔧 FUNCIONALIDADES DISPONIBLES:
   • Dashboard unificado con métricas en tiempo real
   • Gestión completa de facturación y cobranzas
   • Control contable y flujo de caja
   • Mantenimiento preventivo y correctivo
   • Gestión de nómina y asistencia
   • Reportes avanzados y KPIs
   • Búsqueda global en todo el sistema
   • Alertas automáticas del sistema

📝 ARCHIVOS PRINCIPALES:
   • app.py - Aplicación Flask principal
   • database.py - Funciones de base de datos
   • EXTENSION_TABLAS_COMPLETA.sql - 30 nuevas tablas
   • DATOS_EXTENSION_COMPLETA.sql - Datos de ejemplo
   • templates/sistema_completo.html - Dashboard principal
   """)
    print(f"{'='*80}")

def main():
    """Función principal de implementación"""
    print("🏗️ IMPLEMENTACIÓN SISTEMA ERP CONSTRUCTORA COMPLETO")
    print("86 Tablas - 8 Módulos Integrados")
    print(f"{'='*60}")
    
    # Cambiar al directorio de trabajo
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    pasos = [
        (verificar_postgres, "Verificación de PostgreSQL"),
        (instalar_dependencias, "Instalación de dependencias"),
        (crear_tablas_extendidas, "Creación de 30 nuevas tablas"),
        (insertar_datos_ejemplo, "Inserción de datos de ejemplo"),
        (integrar_codigo_extendido, "Integración de código extendido"),
        (crear_rutas_extendidas, "Configuración de rutas extendidas"),
        (verificar_sistema, "Verificación del sistema completo")
    ]
    
    pasos_exitosos = 0
    
    for paso_func, descripcion in pasos:
        if paso_func():
            pasos_exitosos += 1
            time.sleep(1)  # Pausa breve entre pasos
        else:
            print(f"\n❌ FALLO EN: {descripcion}")
            print("🔧 Revise los errores anteriores y vuelva a intentar")
            return False
    
    if pasos_exitosos == len(pasos):
        mostrar_resumen()
        print("\n🎉 ¡IMPLEMENTACIÓN COMPLETADA EXITOSAMENTE!")
        print("🚀 El sistema está listo para usar")
        return True
    else:
        print(f"\n⚠️ Implementación parcial: {pasos_exitosos}/{len(pasos)} pasos completados")
        return False

if __name__ == "__main__":
    try:
        exito = main()
        sys.exit(0 if exito else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Implementación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")
        sys.exit(1)