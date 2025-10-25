# Tema Warm Autumn Glow - ERP Constructora

## 📋 Descripción

El tema **Warm Autumn Glow** es un sistema de diseño completo para el ERP Constructora que utiliza una paleta de colores cálida y otoñal inspirada en tonos terrosos y acogedores. Combina las mejores prácticas de Tailwind CSS con un diseño personalizado que mejora la experiencia del usuario.

## 🎨 Paleta de Colores

### Colores Principales

| Color | Nombre | Hex | RGB | Uso Principal |
|-------|--------|-----|-----|---------------|
| ![#003049](https://via.placeholder.com/20/003049/FFFFFF?text=+) | **Prussian Blue** | `#003049` | `rgb(0, 48, 73)` | Elementos principales, textos importantes |
| ![#d62828](https://via.placeholder.com/20/d62828/FFFFFF?text=+) | **Fire Engine Red** | `#d62828` | `rgb(214, 40, 40)` | Alertas, botones de eliminación |
| ![#f77f00](https://via.placeholder.com/20/f77f00/FFFFFF?text=+) | **Orange Wheel** | `#f77f00` | `rgb(247, 127, 0)` | Botones secundarios, elementos de acento |
| ![#fcbf49](https://via.placeholder.com/20/fcbf49/000000?text=+) | **Xanthous** | `#fcbf49` | `rgb(252, 191, 73)` | Destacados importantes, métricas |
| ![#eae2b7](https://via.placeholder.com/20/eae2b7/000000?text=+) | **Vanilla** | `#eae2b7` | `rgb(234, 226, 183)` | Fondos suaves, elementos neutros |

### Variaciones de Color

Cada color principal tiene 9 variaciones (100-900) para diferentes niveles de intensidad:

```css
/* Ejemplo: Prussian Blue */
--prussian-blue-100: #00090e;  /* Más oscuro */
--prussian-blue-500: #003049;  /* Color base */
--prussian-blue-900: #a7e0ff;  /* Más claro */
```

## 📁 Estructura de Archivos

```
constructora/
├── static/
│   ├── css/
│   │   ├── warm-autumn-theme.css      # Tema principal
│   │   ├── tailwind-warm-autumn.css   # Utilidades tipo Tailwind
│   │   └── styles.css                 # Estilos originales (fallback)
│   └── js/
│       └── warm-autumn-theme.js       # Efectos dinámicos
├── templates/
│   ├── base.html                      # Template base actualizado
│   ├── dashboard_warm_autumn.html     # Dashboard de demostración
│   └── ...                           # Otros templates
└── apply_warm_autumn_theme.py         # Script de aplicación automática
```

## 🚀 Instalación y Configuración

### 1. Archivos Requeridos

Asegúrate de que los siguientes archivos estén en su lugar:

- `static/css/warm-autumn-theme.css`
- `static/css/tailwind-warm-autumn.css` 
- `static/js/warm-autumn-theme.js`

### 2. Actualizar Template Base

El template `base.html` debe incluir los archivos CSS y JS del tema:

```html
<!-- CSS del tema -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/warm-autumn-theme.css') }}">
<link rel="stylesheet" href="{{ url_for('static', filename='css/tailwind-warm-autumn.css') }}">

<!-- JavaScript del tema -->
<script src="{{ url_for('static', filename='js/warm-autumn-theme.js') }}"></script>
```

### 3. Aplicar Tema Automáticamente

Ejecuta el script de aplicación automática:

```bash
python apply_warm_autumn_theme.py
```

Este script:
- ✅ Crea backups de los archivos originales
- ✅ Convierte clases Bootstrap a Warm Autumn
- ✅ Aplica la nueva paleta de colores
- ✅ Actualiza iconos y elementos visuales

## 🎯 Componentes Principales

### Botones

```html
<!-- Botón principal -->
<button class="btn btn-primary">
    <i class="fas fa-save"></i> Guardar
</button>

<!-- Botón secundario -->
<button class="btn btn-secondary">
    <i class="fas fa-edit"></i> Editar
</button>

<!-- Botón de acento -->
<button class="btn btn-accent">
    <i class="fas fa-star"></i> Destacar
</button>

<!-- Botón de peligro -->
<button class="btn btn-danger">
    <i class="fas fa-trash"></i> Eliminar
</button>
```

### Tarjetas (Cards)

```html
<!-- Tarjeta de estadística -->
<div class="stat-card">
    <div class="stat-header">
        <div class="stat-title">Obras Activas</div>
        <div class="stat-icon primary">
            <i class="fas fa-building"></i>
        </div>
    </div>
    <div class="stat-value">24</div>
    <div class="stat-change positive">
        <i class="fas fa-arrow-up"></i>
        <span>+12% este mes</span>
    </div>
</div>

<!-- Tarjeta de módulo -->
<div class="module-card">
    <div class="module-header">
        <div class="module-icon">
            <i class="fas fa-users"></i>
        </div>
        <div class="module-title">Recursos Humanos</div>
        <div class="module-description">
            Gestión completa de empleados y nóminas
        </div>
    </div>
    <div class="module-content">
        <!-- Contenido del módulo -->
    </div>
</div>
```

### Tablas

```html
<div class="table-container">
    <div class="table-header">
        <h3 class="table-title">Lista de Empleados</h3>
        <div class="table-tools">
            <div class="table-search">
                <i class="fas fa-search search-icon"></i>
                <input type="text" class="form-control" placeholder="Buscar...">
            </div>
            <button class="btn btn-primary btn-sm">
                <i class="fas fa-plus"></i> Agregar
            </button>
        </div>
    </div>
    <table class="table">
        <thead>
            <tr>
                <th>Nombre</th>
                <th>Cargo</th>
                <th>Estado</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Juan Pérez</td>
                <td>Ingeniero</td>
                <td><span class="badge badge-success">Activo</span></td>
                <td class="actions-cell">
                    <div class="table-actions">
                        <a href="#" class="btn-action btn-view" title="Ver">
                            <i class="fas fa-eye"></i>
                        </a>
                        <a href="#" class="btn-action btn-edit" title="Editar">
                            <i class="fas fa-edit"></i>
                        </a>
                        <a href="#" class="btn-action btn-delete" title="Eliminar">
                            <i class="fas fa-trash"></i>
                        </a>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

### Formularios

```html
<div class="form-container">
    <div class="form-group">
        <label class="form-label required" for="nombre">Nombre</label>
        <input type="text" id="nombre" class="form-control" placeholder="Ingrese el nombre">
    </div>
    
    <div class="form-group">
        <label class="form-label" for="descripcion">Descripción</label>
        <textarea id="descripcion" class="form-control form-textarea" placeholder="Descripción detallada"></textarea>
    </div>
    
    <div class="form-actions">
        <button type="button" class="btn btn-secondary">
            <i class="fas fa-times"></i> Cancelar
        </button>
        <button type="submit" class="btn btn-primary">
            <i class="fas fa-save"></i> Guardar
        </button>
    </div>
</div>
```

### Alertas y Badges

```html
<!-- Alertas -->
<div class="alert alert-success">
    <i class="fas fa-check-circle alert-icon"></i>
    <div>Operación completada exitosamente</div>
</div>

<div class="alert alert-danger">
    <i class="fas fa-exclamation-triangle alert-icon"></i>
    <div>Error al procesar la solicitud</div>
</div>

<!-- Badges -->
<span class="badge badge-success">Activo</span>
<span class="badge badge-warning">Pendiente</span>
<span class="badge badge-danger">Suspendido</span>
```

## 🎨 Utilidades Tailwind-like

El tema incluye utilidades similares a Tailwind CSS:

### Colores

```html
<!-- Texto -->
<p class="text-prussian-blue">Texto azul principal</p>
<p class="text-orange-wheel">Texto naranja</p>
<p class="text-xanthous">Texto amarillo dorado</p>

<!-- Fondos -->
<div class="bg-prussian-blue text-white">Fondo azul</div>
<div class="bg-gradient-warm-autumn">Gradiente otoñal</div>

<!-- Bordes -->
<div class="border border-xanthous">Borde dorado</div>
```

### Espaciado

```html
<!-- Padding -->
<div class="p-4">Padding estándar</div>
<div class="px-6 py-4">Padding horizontal y vertical</div>

<!-- Margin -->
<div class="m-4">Margin estándar</div>
<div class="mb-6">Margin bottom</div>
```

### Flexbox y Grid

```html
<!-- Flexbox -->
<div class="flex items-center justify-between">
    <span>Izquierda</span>
    <span>Derecha</span>
</div>

<!-- Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>
```

## ⚡ Efectos JavaScript

El archivo `warm-autumn-theme.js` proporciona efectos interactivos:

### Notificaciones Toast

```javascript
// Mostrar notificación
WarmAutumnTheme.showToast('Operación completada', 'success');
WarmAutumnTheme.showToast('Error al procesar', 'error');
WarmAutumnTheme.showToast('Advertencia importante', 'warning');
```

### Sistema de Loading

```javascript
// Mostrar loading
const loadingOverlay = WarmAutumnTheme.showLoading('#mi-contenedor', 'Procesando...');

// Ocultar loading
WarmAutumnTheme.hideLoading('#mi-contenedor');
```

### Animaciones Automáticas

El sistema aplica automáticamente:

- ✨ Animaciones de entrada para cards y elementos
- 🎯 Efectos hover mejorados para botones y enlaces
- 📊 Pulso periódico en métricas importantes
- 🌊 Efectos ripple en botones al hacer click
- 📱 Scroll effects y parallax suave

## 📱 Responsive Design

El tema es completamente responsive con breakpoints:

- **Mobile**: < 640px
- **Tablet**: 640px - 1024px  
- **Desktop**: > 1024px

```html
<!-- Clases responsive -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
    <!-- Se adapta automáticamente -->
</div>
```

## 🔧 Personalización

### Modificar Colores

Edita las variables CSS en `warm-autumn-theme.css`:

```css
:root {
    --prussian-blue: #003049;        /* Cambiar color principal */
    --orange-wheel: #f77f00;         /* Cambiar color secundario */
    --xanthous: #fcbf49;             /* Cambiar color de acento */
    /* ... */
}
```

### Agregar Nuevos Componentes

1. Define el CSS en `warm-autumn-theme.css`
2. Agrega utilidades en `tailwind-warm-autumn.css`
3. Incluye efectos JavaScript en `warm-autumn-theme.js`

### Crear Variaciones de Color

```css
/* Nuevo color personalizado */
.bg-custom-gradient {
    background: linear-gradient(135deg, var(--prussian-blue), var(--your-color));
}

.text-custom {
    color: var(--your-color);
}
```

## 🐛 Resolución de Problemas

### Estilos no se Aplican

1. Verifica que los archivos CSS estén enlazados correctamente
2. Asegúrate de que la ruta de archivos estáticos sea correcta
3. Limpia la caché del navegador (Ctrl+F5)

### JavaScript no Funciona

1. Verifica que `warm-autumn-theme.js` esté cargado
2. Abre la consola del navegador para ver errores
3. Asegúrate de que jQuery esté cargado si es necesario

### Responsividad Rota

1. Revisa las clases de breakpoints (sm:, md:, lg:)
2. Verifica el viewport meta tag en el HTML
3. Prueba en diferentes dispositivos

## 📊 Rendimiento

- **CSS minificado**: Para producción, minifica los archivos CSS
- **Lazy loading**: Las animaciones se cargan cuando son necesarias
- **Optimización de imágenes**: Usa formatos modernos (WebP, AVIF)
- **Cache**: Configura headers de cache para archivos estáticos

## 🔄 Actualizaciones

Para actualizar el tema:

1. Respalda tus personalizaciones
2. Reemplaza los archivos del tema
3. Ejecuta el script de aplicación automática
4. Prueba en diferentes navegadores
5. Valida que todas las funcionalidades trabajen correctamente

## 📞 Soporte

Si encuentras problemas:

1. Revisa esta documentación
2. Verifica la consola del navegador
3. Consulta los backups creados automáticamente
4. Restaura archivos originales si es necesario

---

**¡Disfruta del nuevo tema Warm Autumn Glow!** 🍂✨