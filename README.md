# Sistema de Consultas para Constructora

## Descripción del Proyecto

Este sistema web permite consultar y gestionar todos los datos relacionados con una constructora, incluyendo obras, empleados, materiales, proveedores, inventario, proyectos, reportes, vehículos y equipos. Está diseñado para cumplir con los requerimientos del proyecto final de Base de Datos.

## Características Principales

### 📊 Dashboard Interactivo
- Resumen general de estadísticas clave
- Obras activas, empleados, materiales y proveedores
- Visualización de actividad reciente
- Métricas financieras y de avance

### 🏗️ Gestión de Obras
- **Consulta completa de obras**: Casas habitacionales, edificios de oficina, edificios habitacionales, bodegas
- **Información detallada**: Ubicación, tipo, estado, cliente asignado
- **Seguimiento de avance**: Porcentaje físico y financiero
- **Presupuestos**: Montos estimados por obra

### 👷 Administración de Personal
- **Empleados por tipo**: Ingenieros, arquitectos, albañiles, personal administrativo
- **Gestión de contratos**: Salarios fijos y pagos por trabajo realizado
- **Seguimiento de pagos**: Historial de pagos y estados
- **Asignación de proyectos**: Control de empleados por área de trabajo

### 📦 Control de Materiales e Inventario
- **Catálogo completo**: Cemento, acero, ladrillos, herramientas, agregados
- **Gestión de proveedores**: Contactos, materiales suministrados, facturas
- **Control de inventario**: Stock por bodega y obra
- **Movimientos de material**: Ingresos, salidas y transferencias

### 🚚 Gestión de Recursos
- **Vehículos**: Pickups, camiones, maquinaria con ubicación actual
- **Equipos**: Herramientas, maquinaria, equipos de medición
- **Asignaciones**: Control de responsables y fechas

### 📈 Reportes y Análisis
- **Reportes semanales**: Avances por obra y semana
- **Control de gastos**: Por obra y área de trabajo
- **Uso de materiales**: Consumo por área y proyecto
- **Pagos a empleados**: Historial y montos por tipo de pago

## Estructura del Sistema

### Archivos Principales

1. **`index.html`** - Página principal con navegación y todas las secciones
2. **`styles.css`** - Estilos CSS responsivos y modernos
3. **`script.js`** - Funcionalidad JavaScript e interactividad
4. **`data.js`** - Datos de ejemplo y funciones auxiliares
5. **`crear base de datos y tablas.sql`** - Script de base de datos original

### Módulos del Sistema

#### 1. Dashboard
- Estadísticas generales
- Resumen de actividad reciente
- Métricas clave del negocio

#### 2. Obras
- Lista completa de obras
- Filtros por estado (En Proceso, Completada, Suspendida)
- Búsqueda por nombre o ubicación
- Detalles de presupuesto y avance

#### 3. Empleados
- Gestión de personal por tipo
- Información salarial y estado
- Proyectos asignados
- Historial de pagos

#### 4. Materiales
- Catálogo de materiales disponibles
- Precios unitarios actualizados
- Stock total por tipo
- Información de proveedores

#### 5. Proveedores
- Directorio de proveedores
- Materiales suministrados
- Total de facturas procesadas
- Estado de relación comercial

#### 6. Inventario
- Stock por bodega y obra
- Valor total de inventario
- Responsables de cada bodega
- Estado de disponibilidad

#### 7. Proyectos
- Proyectos por obra
- Fechas de inicio y finalización
- Porcentaje de avance
- Número de actividades

#### 8. Reportes
- **Semanales**: Avances y observaciones por semana
- **Gastos**: Control financiero por obra
- **Materiales**: Uso y consumo por área
- **Pagos**: Histórico de pagos a empleados

#### 9. Vehículos
- Flota de vehículos por tipo
- Ubicación actual
- Obra asignada
- Estado operativo

#### 10. Equipos
- Inventario de equipos y herramientas
- Asignaciones a empleados
- Fechas de préstamo
- Estado de disponibilidad

## Funcionalidades Técnicas

### 🔍 Sistema de Búsqueda
- Búsqueda en tiempo real en todas las tablas
- Filtros específicos por categoría
- Resultados instantáneos sin recarga

### 📱 Diseño Responsivo
- Compatible con dispositivos móviles
- Sidebar colapsable en pantallas pequeñas
- Tablas con scroll horizontal en móvil
- Optimización para tablets

### 🎨 Interfaz Moderna
- Diseño Material Design inspirado
- Iconos de Font Awesome
- Animaciones suaves y transiciones
- Esquema de colores profesional

### ⚡ Rendimiento
- Carga rápida de datos
- Navegación sin recarga de página
- Datos simulados para demostración
- Interfaz reactiva y fluida

## Instalación y Uso

### Requisitos
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Conexión a internet (para cargar iconos de Font Awesome)

### Instalación
1. Descargar todos los archivos del proyecto
2. Colocar en una carpeta accesible
3. Abrir `index.html` en un navegador web

### Uso del Sistema
1. **Navegación**: Usar el menú lateral para acceder a diferentes módulos
2. **Búsqueda**: Utilizar las cajas de búsqueda para filtrar información
3. **Filtros**: Aplicar filtros específicos usando los selectores
4. **Detalles**: Hacer clic en el botón "Ver" para información detallada
5. **Responsive**: El sistema se adapta automáticamente al tamaño de pantalla

## Datos de Ejemplo

El sistema incluye datos de ejemplo que representan:

- **5 obras** de diferentes tipos y estados
- **6 empleados** de diversas especialidades
- **6 materiales** con precios y proveedores
- **5 proveedores** con información de contacto
- **5 bodegas** distribuidas por obras
- **Inventario completo** por bodega
- **Reportes semanales** de avance
- **Vehículos y equipos** asignados

## Estructura de Base de Datos

El sistema está basado en el script SQL proporcionado que incluye:

### Tablas Principales
- `Cliente`, `Obra`, `Empleado`, `Material`, `Proveedor`
- `Area`, `Proyecto`, `Actividad`, `Bodega`, `Inventario`
- `Vehiculo`, `Equipo`, `UsuarioSistema`

### Tablas de Control
- `PresupuestoObra`, `AvanceObra`, `ReporteSemanal`
- `Contrato`, `DetalleTrabajo`, `PagoEmpleado`
- `Requisicion`, `DetalleRequisicion`
- `MovimientoMaterial`, `FacturaProveedor`

### Tablas de Auditoría
- `Auditoria`, `Bitacora`, `Incidente`
- `ArchivoAdjunto`, `PermisoAcceso`

## Características del Diseño

### Colores Principales
- **Azul Primario**: #3498db (Navegación y elementos principales)
- **Azul Oscuro**: #2c3e50 (Textos y headers)
- **Gris Claro**: #ecf0f1 (Fondos y separadores)
- **Verde**: #27ae60 (Estados positivos)
- **Naranja**: #f39c12 (Estados en proceso)
- **Rojo**: #e74c3c (Estados negativos)

### Tipografía
- **Fuente Principal**: Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Tamaños Responsivos**: Ajustados automáticamente según dispositivo

### Iconografía
- **Font Awesome 6.0.0**: Iconos modernos y consistentes
- **Iconos específicos**: Cada módulo tiene su icono representativo

## Navegación y UX

### Sidebar Navegación
- **Fija en desktop**: Siempre visible en pantallas grandes
- **Colapsable en móvil**: Se oculta/muestra con botón hamburguesa
- **Estados activos**: Indicación visual de sección actual

### Tablas de Datos
- **Headers fijos**: Títulos siempre visibles
- **Hover effects**: Resaltado de filas al pasar el mouse
- **Acciones rápidas**: Botones de ver/editar en cada fila
- **Scroll horizontal**: En móvil para mantener legibilidad

### Modales Informativos
- **Detalles completos**: Información expandida en ventanas emergentes
- **Diseño elegante**: Animaciones suaves de entrada/salida
- **Responsive**: Adaptados al tamaño de pantalla

## Beneficios del Sistema

### Para la Constructora
1. **Control Total**: Visibilidad completa de todas las operaciones
2. **Eficiencia Operativa**: Acceso rápido a información crítica
3. **Seguimiento en Tiempo Real**: Monitoreo constante de avances
4. **Gestión Financiera**: Control de gastos y presupuestos

### Para los Usuarios
1. **Interfaz Intuitiva**: Fácil de usar sin entrenamiento extensivo
2. **Acceso Móvil**: Consultas desde cualquier dispositivo
3. **Búsqueda Rápida**: Encontrar información específica al instante
4. **Información Centralizada**: Todo en un solo lugar

### Para el Negocio
1. **Toma de Decisiones**: Datos claros para decisiones informadas
2. **Productividad**: Reducción de tiempo en consultas manuales
3. **Transparencia**: Información accesible para todos los niveles
4. **Escalabilidad**: Fácil expansión para futuras necesidades

## Futuras Mejoras Sugeridas

### Funcionalidades Adicionales
- **Autenticación de usuarios**: Sistema de login por roles
- **Edición en línea**: Modificar datos directamente desde las tablas
- **Exportación de reportes**: PDF, Excel, CSV
- **Gráficos interactivos**: Visualización de datos con charts

### Integración con Base de Datos
- **Conexión real**: Integrar con base de datos SQL Server/MySQL
- **API REST**: Desarrollo de servicios web para datos dinámicos
- **Sincronización**: Actualizaciones en tiempo real
- **Backup automático**: Respaldo de información crítica

### Mejoras Técnicas
- **PWA**: Aplicación web progresiva para uso offline
- **Notificaciones**: Alertas de eventos importantes
- **Cache inteligente**: Mejor rendimiento con datos frecuentes
- **Multi-idioma**: Soporte para diferentes idiomas

## Tecnologías Utilizadas

- **HTML5**: Estructura semántica y accesible
- **CSS3**: Estilos modernos y responsivos
- **JavaScript (Vanilla)**: Interactividad sin dependencias externas
- **Font Awesome**: Iconografía profesional
- **Responsive Design**: Mobile-first approach

## Contacto y Soporte

Este sistema fue desarrollado como parte del proyecto final de Base de Datos para una constructora, cumpliendo con todos los requerimientos establecidos en las fases del proyecto académico.

---

**Nota**: Este sistema utiliza datos simulados para fines de demostración. Para implementación en producción, se requiere integración con una base de datos real y sistema de autenticación apropiado.