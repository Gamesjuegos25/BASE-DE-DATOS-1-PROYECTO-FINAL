# 🏗️ Sistema ERP Constructora

Sistema integral de gestión para constructoras desarrollado con **Python Flask + PostgreSQL**
Incluye sistema completo de autenticación, gestión de usuarios y control de permisos.

## 🚀 Características Principales

- ✅ **Sistema de Login Completo** - Autenticación segura con roles y permisos
- ✅ **Gestión de Usuarios** - CRUD de usuarios del sistema con roles
- ✅ **Dashboard Ejecutivo** - Panel de control con estadísticas en tiempo real
- ✅ **Gestión de Obras** - CRUD completo de proyectos y obras
- ✅ **Control de Empleados** - Administración de personal y asignaciones
- ✅ **Inventario de Materiales** - Control de stock y gestión de materiales
- ✅ **Gestión de Proveedores** - Base de datos de proveedores y contratistas
- ✅ **Parque Vehicular** - Control de vehículos y equipos de la empresa
- ✅ **Reportes Académicos** - Reportes integrados y estadísticas
- ✅ **Auditoría de Sistema** - Log completo de acciones de usuarios

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.8+ con Flask
- **Base de Datos**: PostgreSQL 12+ con psycopg2
- **Frontend**: HTML5 + CSS3 + JavaScript (mínimo)
- **Templating**: Jinja2
- **Seguridad**: bcrypt para hash de contraseñas
- **Variables de Entorno**: python-dotenv

## 📁 Estructura del Proyecto

```
constructora/
├── app.py                  # Aplicación Flask principal con rutas
├── database.py             # Funciones de base de datos y autenticación
├── setup_admin.py          # Script para crear usuario administrador
├── migrar_db.py           # Script de migración de base de datos
├── requirements.txt        # Dependencias del proyecto
├── .env                   # Variables de entorno (crear basado en .env.example)
├── 
├── templates/             # Plantillas HTML
│   ├── base.html          # Template base con navegación y auth
│   ├── dashboard.html     # Dashboard principal personalizado
│   ├── auth/
│   │   ├── login.html     # Página de inicio de sesión
│   │   └── cambiar_password.html  # Cambio de contraseña
│   ├── usuarios/
│   │   └── listar.html    # Gestión de usuarios del sistema
│   ├── obras/
│   │   ├── listar.html    # Lista de obras
│   │   └── crear.html     # Crear nueva obra
│   ├── empleados/         # Gestión de empleados
│   ├── materiales/        # Gestión de inventario
│   ├── proveedores/       # Gestión de proveedores
│   ├── vehiculos/         # Gestión de vehículos
│   └── reportes/
│       └── academicos.html # Reportes del sistema
│
└── static/               # Archivos estáticos
    ├── css/
    │   └── styles.css    # Estilos CSS con diseño moderno
    └── js/
        ├── app.js        # JavaScript principal con funciones auth
        └── utils.js      # Utilidades JavaScript
```

## ⚡ Instalación y Configuración

### 1. Requisitos Previos
- Python 3.8 o superior
- PostgreSQL 12+ instalado y funcionando
- pip (gestor de paquetes Python)

### 2. Configurar el Proyecto
```bash
# Clonar o descargar el proyecto
cd constructora

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Base de Datos
```bash
# 1. Crear base de datos en PostgreSQL
createdb PROYECTO_FINAL_BD1

# 2. Crear archivo .env con tu configuración
DB_HOST=localhost
DB_PORT=5432
DB_NAME=PROYECTO_FINAL_BD1
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_password_postgres

# 3. Ejecutar migración de base de datos
python migrar_db.py
```

### 4. Configurar Usuario Administrador
```bash
# Ejecutar script de configuración inicial
python setup_admin.py

# Seguir las instrucciones para crear el usuario administrador
# Datos sugeridos:
# Usuario: admin
# Contraseña: admin123 (cambiar después del primer login)
# Email: admin@constructora.com
```

### 5. Ejecutar la Aplicación
```bash
# Iniciar el servidor Flask
python app.py

# La aplicación estará disponible en:
# http://localhost:5000
```

## 🔐 Primer Acceso al Sistema

### Credenciales por Defecto
Después de ejecutar `setup_admin.py`, podrás acceder con:
- **URL**: `http://localhost:5000`
- **Usuario**: admin (o el que hayas configurado)
- **Contraseña**: La que definiste durante el setup

### Funciones del Usuario Administrador
- ✅ Acceso completo a todas las secciones
- ✅ Gestión de usuarios y permisos
- ✅ Creación y administración de obras
- ✅ Visualización de reportes y auditoría
- ✅ Configuración del sistema

## 👥 Sistema de Usuarios y Permisos

### Roles Disponibles
- **ADMINISTRADOR**: Acceso completo al sistema
- **SUPERVISOR**: Gestión de obras y empleados
- **OPERADOR**: Acceso limitado a consultas
- **CONTADOR**: Acceso a reportes y finanzas

### Permisos Granulares
- `ADMIN_USUARIOS`: Gestión de usuarios del sistema
- `VER_REPORTES`: Visualización de reportes
- `CREAR_OBRAS`: Creación de nuevas obras
- `EDITAR_OBRAS`: Modificación de obras existentes
- `ELIMINAR_OBRAS`: Eliminación de obras
- `GESTIONAR_EMPLEADOS`: Administración de personal
- `GESTIONAR_MATERIALES`: Control de inventario
- `GESTIONAR_PROVEEDORES`: Administración de proveedores
- `GESTIONAR_VEHICULOS`: Control de vehículos
- `VER_AUDITORIA`: Acceso a logs del sistema

## 📋 Funcionalidades Principales

### 🏠 Dashboard
- Vista general del sistema con estadísticas
- Bienvenida personalizada por usuario
- Métricas de obras, empleados y materiales
- Gráficos de rendimiento (próximamente)

### 🏗️ Gestión de Obras
- **Crear Obra**: Formulario completo con validaciones
- **Listar Obras**: Tabla paginada con filtros
- **Editar Obra**: Modificación de datos existentes
- **Estados**: En planificación, En ejecución, Completada, Suspendida

### 👥 Gestión de Empleados  
- **Registro de Personal**: Datos completos de empleados
- **Asignación a Obras**: Control de personal por proyecto
- **Roles y Especialidades**: Clasificación del personal
- **Historial Laboral**: Seguimiento de asignaciones

### 📦 Gestión de Materiales
- **Inventario**: Control de stock en tiempo real
- **Proveedores**: Gestión de relaciones comerciales
- **Compras**: Registro de adquisiciones
- **Consumo por Obra**: Tracking de materiales utilizados

### 🚗 Gestión de Vehículos
- **Parque Vehicular**: Registro completo de vehículos
- **Mantenimientos**: Programación y seguimiento
- **Asignaciones**: Control de uso por obra/empleado
- **Documentación**: Seguros, permisos, certificaciones

## 🛡️ Características de Seguridad

### Autenticación
- Hash de contraseñas con bcrypt
- Gestión de sesiones Flask
- Límite de intentos de login
- Bloqueo automático de cuentas

### Autorización
- Control de acceso basado en roles (RBAC)
- Permisos granulares por función
- Decoradores de autorización en rutas
- Verificación de permisos en templates

### Auditoría
- Log completo de acciones de usuarios
- Registro de cambios en datos críticos  
- Seguimiento de accesos al sistema
- Reportes de actividad por usuario

## 🔧 Administración del Sistema

### Gestión de Usuarios
```bash
# Acceder a: http://localhost:5000/usuarios
# Funciones disponibles:
# - Crear nuevos usuarios
# - Asignar roles y permisos
# - Bloquear/desbloquear cuentas
# - Resetear contraseñas
# - Ver auditoría de accesos
```

### Cambio de Contraseñas
```bash
# Los usuarios pueden cambiar su contraseña en:
# http://localhost:5000/cambiar-password
# 
# Incluye validación de fortaleza:
# - Mínimo 8 caracteres
# - Al menos una mayúscula
# - Al menos una minúscula  
# - Al menos un número
```

### Reportes del Sistema
```bash
# Acceso a reportes académicos:
# http://localhost:5000/reportes/academicos
#
# Incluye:
# - Estadísticas de uso del sistema
# - Reportes de obras por estado
# - Análisis de empleados y productividad
# - Reportes de materiales y costos
```

## 🚀 Comandos de Desarrollo

### Configuración Inicial
```bash
# Configurar entorno completo
python setup_admin.py

# Migrar base de datos
python migrar_db.py

# Ejecutar en desarrollo
python app.py
```

### Gestión de Base de Datos
```bash
# Backup de base de datos
pg_dump PROYECTO_FINAL_BD1 > backup.sql

# Restaurar base de datos  
psql PROYECTO_FINAL_BD1 < backup.sql

# Ver logs de PostgreSQL
tail -f /var/log/postgresql/postgresql-*.log
```

### Limpieza y Mantenimiento
```bash
# Limpiar archivos Python compilados
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Actualizar dependencias
pip freeze > requirements.txt

# Verificar estilo de código
flake8 *.py
```

## 🌐 Despliegue en Producción

### Con Gunicorn
```bash
# Instalar Gunicorn
pip install gunicorn

# Ejecutar con múltiples workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Con configuración de timeout
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app
```

### Variables de Entorno para Producción
```bash
# .env para producción
DB_HOST=tu_servidor_postgres
DB_PORT=5432
DB_NAME=constructora_prod
DB_USER=usuario_prod
DB_PASSWORD=password_seguro
FLASK_ENV=production
SECRET_KEY=clave_secreta_muy_larga_y_segura
```

## 🐛 Solución de Problemas

### Problemas Comunes

**Error de Conexión a Base de Datos**
```bash
# Verificar que PostgreSQL esté ejecutándose
sudo systemctl status postgresql

# Verificar credenciales en .env
cat .env

# Probar conexión manualmente
psql -h localhost -U tu_usuario PROYECTO_FINAL_BD1
```

**Error de Importación de Módulos**
```bash
# Verificar entorno virtual activo
which python

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

**Problemas de Permisos**
```bash
# Verificar que el usuario tenga permisos asignados
# Acceder como administrador y revisar usuarios
# http://localhost:5000/usuarios
```

## 📞 Soporte

### Documentación Técnica
- Arquitectura basada en Flask con autenticación robusta
- Base de datos PostgreSQL con esquema normalizado
- Frontend responsive con HTML5/CSS3
- Sistema de permisos granular RBAC

### Contacto y Contribuciones
- Sistema desarrollado para uso académico y profesional
- Código limpio y bien documentado
- Arquitectura escalable y mantenible
- Compatible con estándares web modernos

---
**🎯 Sistema ERP Constructora - Versión 2.0 con Autenticación Completa**