#!/usr/bin/env python3
"""
ANÁLISIS COMPLETO DE MÓDULOS - SISTEMA ERP CONSTRUCTORA
=======================================================
Script para identificar errores, completar funcionalidades y unificar estilos
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Lista completa de módulos del sistema
MODULOS_SISTEMA = [
    'obras', 'clientes', 'empleados', 'proveedores', 'materiales', 
    'vehiculos', 'equipos', 'proyectos', 'areas', 'contratos',
    'trabajos', 'actividades', 'bitacoras', 'incidentes', 'auditorias',
    'bodegas', 'requisiciones', 'movimientos', 'avances', 'presupuestos',
    'facturas', 'usuarios', 'permisos', 'inventarios', 'herramientas',
    'compras', 'ventas', 'pagos', 'nomina'
]

class AnalizadorModulos:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.templates_dir = self.base_dir / 'templates'
        self.static_dir = self.base_dir / 'static'
        self.app_file = self.base_dir / 'app.py'
        
        self.errores_encontrados = []
        self.modulos_incompletos = []
        self.problemas_estilo = []
        
    def analizar_app_py(self):
        """Analiza app.py para verificar rutas CRUD"""
        print("🔍 ANALIZANDO APP.PY...")
        print("=" * 50)
        
        if not self.app_file.exists():
            self.errores_encontrados.append("❌ Archivo app.py no encontrado")
            return {}
        
        with open(self.app_file, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        rutas_por_modulo = defaultdict(list)
        
        # Buscar rutas para cada módulo
        for modulo in MODULOS_SISTEMA:
            # Patrones de rutas CRUD
            patrones = [
                f"@app.route.*/{modulo}.*methods.*GET.*POST",  # Crear
                f"@app.route.*/{modulo}",  # Listar
                f"@app.route.*/{modulo}.*<int:id>.*GET",  # Ver detalle
                f"@app.route.*/{modulo}.*<int:id>.*editar",  # Editar
                f"@app.route.*/{modulo}.*<int:id>.*eliminar"  # Eliminar
            ]
            
            rutas_encontradas = []
            for patron in patrones:
                matches = re.findall(patron, contenido, re.IGNORECASE)
                rutas_encontradas.extend(matches)
            
            if rutas_encontradas:
                rutas_por_modulo[modulo] = rutas_encontradas
                
        return rutas_por_modulo
    
    def analizar_templates(self):
        """Analiza templates para verificar completitud"""
        print("\n🎨 ANALIZANDO TEMPLATES...")
        print("=" * 50)
        
        templates_por_modulo = {}
        
        for modulo in MODULOS_SISTEMA:
            modulo_dir = self.templates_dir / modulo
            templates_info = {
                'listar': False,
                'crear': False,
                'detalle': False,
                'editar': False,
                'archivos': []
            }
            
            if modulo_dir.exists():
                archivos = list(modulo_dir.glob('*.html'))
                templates_info['archivos'] = [a.name for a in archivos]
                
                for archivo in archivos:
                    nombre = archivo.stem.lower()
                    if 'listar' in nombre or 'index' in nombre:
                        templates_info['listar'] = True
                    if 'crear' in nombre or 'nuevo' in nombre:
                        templates_info['crear'] = True
                    if 'detalle' in nombre or 'ver' in nombre:
                        templates_info['detalle'] = True
                    if 'editar' in nombre:
                        templates_info['editar'] = True
            
            templates_por_modulo[modulo] = templates_info
            
            # Verificar completitud
            esperados = ['listar', 'crear', 'detalle', 'editar']
            faltantes = [t for t in esperados if not templates_info[t]]
            
            if faltantes:
                self.modulos_incompletos.append({
                    'modulo': modulo,
                    'faltantes': faltantes,
                    'existentes': templates_info['archivos']
                })
                
        return templates_por_modulo
    
    def analizar_estilos_css(self):
        """Analiza archivos CSS existentes"""
        print("\n🎨 ANALIZANDO ESTILOS CSS...")
        print("=" * 50)
        
        css_dir = self.static_dir / 'css'
        archivos_css = []
        
        if css_dir.exists():
            archivos_css = list(css_dir.glob('*.css'))
        
        # Verificar archivos CSS críticos
        css_criticos = [
            'form-pages.css',
            'list-pages.css', 
            'detail-page.css',
            'create-forms.css'
        ]
        
        css_existentes = [f.name for f in archivos_css]
        css_faltantes = [c for c in css_criticos if c not in css_existentes]
        
        if css_faltantes:
            self.problemas_estilo.extend(css_faltantes)
            
        return {
            'existentes': css_existentes,
            'faltantes': css_faltantes,
            'total': len(archivos_css)
        }
    
    def verificar_consistencia_templates(self):
        """Verifica consistencia visual entre templates"""
        print("\n🔍 VERIFICANDO CONSISTENCIA VISUAL...")
        print("=" * 50)
        
        inconsistencias = []
        
        for modulo in MODULOS_SISTEMA:
            modulo_dir = self.templates_dir / modulo
            if not modulo_dir.exists():
                continue
                
            archivos = list(modulo_dir.glob('*.html'))
            
            for archivo in archivos:
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                    
                    # Verificar que extienda base.html
                    if '{% extends "base.html" %}' not in contenido:
                        inconsistencias.append(f"❌ {modulo}/{archivo.name}: No extiende base.html")
                    
                    # Verificar enlaces CSS
                    if 'form-pages.css' not in contenido and 'crear' in archivo.name:
                        inconsistencias.append(f"⚠️  {modulo}/{archivo.name}: Falta form-pages.css")
                    
                    if 'list-pages.css' not in contenido and 'listar' in archivo.name:
                        inconsistencias.append(f"⚠️  {modulo}/{archivo.name}: Falta list-pages.css")
                    
                    if 'detail-page.css' not in contenido and 'detalle' in archivo.name:
                        inconsistencias.append(f"⚠️  {modulo}/{archivo.name}: Falta detail-page.css")
                        
                except Exception as e:
                    inconsistencias.append(f"❌ Error leyendo {modulo}/{archivo.name}: {str(e)}")
        
        return inconsistencias
    
    def generar_reporte_completo(self):
        """Genera un reporte completo del análisis"""
        print("\n📊 GENERANDO REPORTE COMPLETO...")
        print("=" * 60)
        
        # Ejecutar todos los análisis
        rutas = self.analizar_app_py()
        templates = self.analizar_templates()
        css_info = self.analizar_estilos_css()
        inconsistencias = self.verificar_consistencia_templates()
        
        # Generar reporte
        reporte = f"""
# 📋 REPORTE COMPLETO DE ANÁLISIS - SISTEMA ERP CONSTRUCTORA
=========================================================

## 📊 RESUMEN EJECUTIVO
- **Total módulos analizados**: {len(MODULOS_SISTEMA)}
- **Módulos con rutas en app.py**: {len(rutas)}
- **Módulos con templates**: {len([m for m, t in templates.items() if t['archivos']])}
- **Archivos CSS existentes**: {css_info['total']}
- **Inconsistencias encontradas**: {len(inconsistencias)}

## ❌ PROBLEMAS CRÍTICOS ENCONTRADOS

### 1. MÓDULOS INCOMPLETOS
"""
        
        if self.modulos_incompletos:
            reporte += "\n```\n"
            for modulo_info in self.modulos_incompletos:
                reporte += f"❌ {modulo_info['modulo']}: Faltan {', '.join(modulo_info['faltantes'])}\n"
                if modulo_info['existentes']:
                    reporte += f"   ✅ Tiene: {', '.join(modulo_info['existentes'])}\n"
            reporte += "```\n"
        else:
            reporte += "\n✅ Todos los módulos están completos\n"
        
        reporte += f"""
### 2. ARCHIVOS CSS FALTANTES
"""
        if css_info['faltantes']:
            reporte += "\n```\n"
            for css in css_info['faltantes']:
                reporte += f"❌ {css}\n"
            reporte += "```\n"
        else:
            reporte += "\n✅ Todos los archivos CSS críticos están presentes\n"
        
        reporte += f"""
### 3. INCONSISTENCIAS VISUALES
"""
        if inconsistencias:
            reporte += "\n```\n"
            for inc in inconsistencias[:20]:  # Mostrar solo las primeras 20
                reporte += f"{inc}\n"
            if len(inconsistencias) > 20:
                reporte += f"... y {len(inconsistencias) - 20} más\n"
            reporte += "```\n"
        else:
            reporte += "\n✅ No se encontraron inconsistencias visuales\n"
        
        reporte += f"""
## 📈 ESTADÍSTICAS DETALLADAS

### MÓDULOS POR ESTADO
"""
        
        # Calcular estadísticas
        modulos_completos = []
        modulos_parciales = []
        modulos_sin_templates = []
        
        for modulo, info in templates.items():
            if not info['archivos']:
                modulos_sin_templates.append(modulo)
            elif all(info[t] for t in ['listar', 'crear', 'detalle', 'editar']):
                modulos_completos.append(modulo)
            else:
                modulos_parciales.append(modulo)
        
        reporte += f"""
- **Completos (100%)**: {len(modulos_completos)} módulos
- **Parciales**: {len(modulos_parciales)} módulos  
- **Sin templates**: {len(modulos_sin_templates)} módulos

### MÓDULOS COMPLETOS
```
{', '.join(modulos_completos) if modulos_completos else 'Ninguno'}
```

### MÓDULOS PARCIALES
```
{', '.join(modulos_parciales) if modulos_parciales else 'Ninguno'}
```

### MÓDULOS SIN TEMPLATES
```
{', '.join(modulos_sin_templates) if modulos_sin_templates else 'Ninguno'}
```

## 🎯 RECOMENDACIONES DE ACCIÓN

### PRIORIDAD ALTA
1. **Completar módulos parciales**: {len(modulos_parciales)} módulos necesitan templates
2. **Crear templates faltantes**: {len(modulos_sin_templates)} módulos sin implementar
3. **Unificar estilos CSS**: {len(css_info['faltantes'])} archivos CSS faltantes
4. **Corregir inconsistencias**: {len(inconsistencias)} problemas visuales

### PRIORIDAD MEDIA
- Optimizar rendimiento de templates existentes
- Implementar validaciones adicionales en formularios
- Mejorar responsive design en módulos antiguos

### PRIORIDAD BAJA
- Agregar animaciones y micro-interacciones
- Implementar modo oscuro
- Optimizar SEO de templates

## 📞 SIGUIENTE PASO
Ejecutar script de corrección automática para resolver problemas identificados.

---
*Reporte generado automáticamente - {len(MODULOS_SISTEMA)} módulos analizados*
"""
        
        return reporte
    
    def guardar_reporte(self, reporte):
        """Guarda el reporte en un archivo"""
        archivo_reporte = self.base_dir / 'REPORTE_ANALISIS_COMPLETO.md'
        
        with open(archivo_reporte, 'w', encoding='utf-8') as f:
            f.write(reporte)
        
        print(f"\n📄 Reporte guardado en: {archivo_reporte}")
        
    def ejecutar_analisis(self):
        """Ejecuta el análisis completo"""
        print("🚀 INICIANDO ANÁLISIS COMPLETO DEL SISTEMA")
        print("=" * 60)
        print(f"📂 Directorio base: {self.base_dir}")
        print(f"🎨 Templates: {self.templates_dir}")
        print(f"💅 Estilos: {self.static_dir}")
        print()
        
        reporte = self.generar_reporte_completo()
        self.guardar_reporte(reporte)
        
        # Mostrar resumen en consola
        print("\n📊 RESUMEN DEL ANÁLISIS")
        print("=" * 40)
        print(f"✅ Módulos analizados: {len(MODULOS_SISTEMA)}")
        print(f"❌ Errores encontrados: {len(self.errores_encontrados)}")
        print(f"⚠️  Módulos incompletos: {len(self.modulos_incompletos)}")
        print(f"🎨 Problemas de estilo: {len(self.problemas_estilo)}")
        
        if self.errores_encontrados or self.modulos_incompletos or self.problemas_estilo:
            print(f"\n🔧 ACCIÓN REQUERIDA: Ejecutar script de corrección")
        else:
            print(f"\n🎉 ¡PERFECTO! Sistema completamente funcional")

def main():
    """Función principal"""
    analizador = AnalizadorModulos()
    analizador.ejecutar_analisis()

if __name__ == "__main__":
    main()