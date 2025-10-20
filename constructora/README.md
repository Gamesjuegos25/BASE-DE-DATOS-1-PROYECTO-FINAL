# Sistema de Constructora - LIMPIO# README.md - Sistema de Gestión de Constructora Python



Sistema simplificado de gestión de obras usando **SOLO Python + HTML + CSS**.## Descripción

Sistema de gestión para constructora desarrollado completamente en **Python + HTML + CSS** (sin JavaScript).

## ✅ Características

### Tecnologías Utilizadas

- **Backend**: Flask (Python)- **Backend**: Python 3.8+ con Flask

- **Frontend**: HTML + CSS (Sin JavaScript)- **Base de datos**: PostgreSQL con psycopg2

- **Base de Datos**: PostgreSQL con manejo UTF-8- **Frontend**: HTML5 + CSS3 puro (sin JavaScript)

- **Funcionalidad**: Dashboard + CRUD de Obras- **Templating**: Jinja2 (incluido en Flask)



## 📁 Estructura Limpia## Estructura del Proyecto

```

```constructora/

constructora/├── app.py                  # Aplicación Flask principal

├── app.py              # Aplicación Flask principal├── database.py             # Gestión de base de datos

├── database.py         # Conexión PostgreSQL + consultas seguras├── requirements.txt        # Dependencias Python

├── .env               # Configuración de base de datos├── .env                   # Variables de entorno

├── requirements.txt   # Dependencias Python├── README.md              # Este archivo

├── templates/├── templates/             # Plantillas HTML

│   ├── base.html      # Template base│   ├── base.html         # Template base

│   ├── dashboard.html # Dashboard principal│   ├── dashboard.html    # Dashboard principal

│   └── obras/│   └── obras/           

│       ├── crear.html # Formulario nueva obra│       ├── listar.html   # Lista de obras

│       └── listar.html # Lista de obras│       └── crear.html    # Crear nueva obra

└── static/└── static/

    └── css/    └── css/

        └── styles.css # Estilos CSS        └── styles.css    # Estilos CSS

```

```

## 🚀 Ejecutar

## Instalación y Configuración

1. **Configurar base de datos** en `.env`:

```### 1. Requisitos Previos

DB_HOST=localhost- Python 3.8 o superior

DB_PORT=5432- PostgreSQL instalado y funcionando

DB_USER=postgres- pip (gestor de paquetes Python)

DB_PASSWORD=123

DB_NAME=PROYECTO_FINAL_BD1### 2. Clonar e Instalar Dependencias

``````bash

# Navegar al directorio del proyecto

2. **Instalar dependencias**:cd constructora

```bash

pip install -r requirements.txt# Crear entorno virtual (recomendado)

```python -m venv venv



3. **Ejecutar aplicación**:# Activar entorno virtual

```bash# En Windows:

python app.pyvenv\Scripts\activate

```# En Linux/Mac:

source venv/bin/activate

4. **Acceder**: http://127.0.0.1:5000

# Instalar dependencias

## 🎯 Funcionalidadespip install -r requirements.txt

```

- **Dashboard**: Estadísticas de obras

- **Crear Obra**: Formulario completo### 3. Configurar Base de Datos

- **Listar Obras**: Tabla con filtros1. Crear base de datos PostgreSQL llamada `constructora`

- **Manejo UTF-8**: Caracteres especiales seguros2. Editar archivo `.env` con tus credenciales de base de datos:

```env

## 💡 TecnologíasDB_HOST=localhost

DB_PORT=5432

- ✅ Python 3.12 + FlaskDB_NAME=constructora

- ✅ PostgreSQL con psycopg2DB_USER=tu_usuario

- ✅ HTML5 + CSS3DB_PASSWORD=tu_password

- ✅ Font Awesome (iconos)```

- ❌ JavaScript (eliminado completamente)

3. Ejecutar scripts SQL del proyecto original para crear tablas:

---```sql

*Sistema limpio y funcional - Solo lo esencial*-- Usar los archivos SQL existentes:
-- - crear base de datos y tablas.sql
-- - insertar_datos.sql
```

### 4. Ejecutar la Aplicación
```bash
# Activar entorno virtual si no está activo
venv\Scripts\activate

# Ejecutar la aplicación
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Funcionalidades

### ✅ Implementado
- **Dashboard Principal**: Estadísticas y navegación
- **Gestión de Obras**: Listar, crear, editar obras
- **Sistema de Templates**: Layout base con navegación
- **Estilos CSS**: Diseño responsive sin JavaScript

### 🚧 Por Implementar
- **Gestión de Empleados**: CRUD completo
- **Gestión de Materiales**: Inventario y control
- **Gestión de Proveedores**: Administración de proveedores
- **Reportes**: Generación de reportes PDF/Excel
- **Sistema de Usuarios**: Login y permisos

## Características del Sistema

### Sin JavaScript
- **Navegación**: Mediante enlaces HTML y formularios POST
- **Interactividad**: CSS puro con :hover, :focus, :active
- **Formularios**: Envío tradicional con validación server-side
- **Feedback**: Mensajes flash de Flask para notificaciones

### Arquitectura Flask
- **Rutas RESTful**: Organización clara de URLs
- **Templates Jinja2**: Herencia de plantillas y componentes
- **Gestión de Estado**: Sesiones Flask para datos temporales
- **Configuración**: Variables de entorno con python-dotenv

### Base de Datos
- **ORM**: Conexiones directas con psycopg2 (sin SQLAlchemy)
- **Transacciones**: Manejo automático de commits/rollbacks
- **Conexiones**: Pool de conexiones para rendimiento

## Comandos Útiles

### Desarrollo
```bash
# Ejecutar en modo desarrollo
python app.py

# Ver logs de base de datos
# Los errores se muestran en consola Flask

# Limpiar cache Python
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} +
```

### Producción
```bash
# Ejecutar con gunicorn (instalar primero)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Personalización

### Agregar Nuevas Secciones
1. Crear ruta en `app.py`
2. Crear template en `templates/`
3. Agregar estilos en `static/css/styles.css`
4. Actualizar navegación en `templates/base.html`

### Modificar Estilos
- Todos los estilos están en `static/css/styles.css`
- Sistema basado en CSS Grid y Flexbox
- Variables CSS para colores y tamaños

## Soporte y Contacto
Sistema desarrollado completamente en Python + HTML + CSS como fue solicitado.
Sin dependencias de JavaScript ni frameworks frontend.

---
**Nota**: Este sistema utiliza exclusivamente las 3 tecnologías solicitadas: Python, HTML y CSS.