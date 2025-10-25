# Mejoras y problemas solucionados (bitácora de cambios)

Este documento resume, en español, todas las mejoras aplicadas, los problemas que se resolvieron y cómo usar las nuevas capacidades del sistema. Está orientado a Windows/PowerShell y al proyecto Flask + PostgreSQL en la carpeta `constructora/`.

## Resumen de mejoras

- Navegación/UI
  - Corregido el enlace a Bodegas desde el dashboard.
  - Añadido botón de Cerrar sesión (logout) visible en el encabezado.
  - Flujo de edición de usuarios: nueva ruta y plantilla para ver/editar un usuario.
- Autenticación y permisos
  - Arreglado error de “transacción abortada” en registro al separar validaciones/insert en conexiones y commits/rollbacks claros.
  - Permisos robustos con “doble modo”: usa esquema de permisos completo si existe; si no, cae a un mapeo por rol en `USUARIOS_SISTEMA` (con atajo para `ADMINISTRADOR`).
- Facturación desde contratos
  - Integración end-to-end para “Facturizar contrato”: botón en UI (lista y detalle), ruta Flask dedicada, y nueva función de BD.
  - SQL de soporte: tablas/vistas/funciones de facturación (archivo `queries/contratos_facturacion.sql`) y función `facturizar_contrato` (archivo `queries/facturizar_contrato.sql`).
  - Previsualización de líneas de factura (archivo `queries/previsualizar_factura_contrato.sql`).
  - Script utilitario para aplicar el SQL de facturación: `scripts/aplicar_sql_facturacion.py`.
  - Fallback Python: si la función SQL no está instalada/compatible, el backend genera la factura y sus detalles detectando columnas disponibles en `FACTURAS`.

## Problemas corregidos (antes / después)

- Registro de usuario fallaba con “transacción abortada”
  - Causa: uso de la misma conexión en estado abortado tras un error, sin rollback.
  - Solución: separar validación/escritura, manejo explícito de commit/rollback, y mensajes claros.

- “No tienes permisos suficientes para esta acción” aun con usuarios válidos
  - Causa: faltaba el esquema completo de permisos en algunas instalaciones.
  - Solución: funciones que validan permisos ahora prueban el esquema complejo y, si no existe, caen a un mapeo rol→permisos desde `USUARIOS_SISTEMA.rol_usuario`. `ADMINISTRADOR` tiene acceso total.

- Falta de ruta/plantilla para editar usuarios del sistema
  - Solución: nueva ruta GET/POST `/usuarios/<id>/editar` y plantilla `templates/usuarios/editar.html`.

- Botón de logout poco visible / inexistente
  - Solución: botón destacado en el header (`templates/base.html`) con estilo en `static/css/styles.css`.

- Enlace incorrecto a Bodegas en el dashboard
  - Solución: actualizado el enlace para apuntar a la ruta activa.

## Facturación de contratos: qué se agregó

- Ruta Flask para facturizar un contrato:
  - `GET/POST /contratos/<id>/facturizar`
  - Llama a `facturizar_contrato_safe(id)` y redirige a la factura creada.

- UI (Jinja)
  - `templates/contratos/detalle.html`: botón “Generar factura”.
  - `templates/contratos/listar.html`: acción “Facturar” en cada fila.

- Capa de datos (`database.py`)
  - `facturizar_contrato_safe(id_contrato)`: intenta usar la función SQL `facturizar_contrato`. Si no existe o falla por diferencias de esquema, hace un fallback en Python:
    - Detecta columnas reales de `FACTURAS` (ej. `fecha_emision` vs `fecha_factura`, `estado` vs `estado_factura`, etc.).
    - Inserta la factura con número autogenerado (`generar_numero_factura_safe()` o fallback temporal).
    - Toma líneas desde `CONTRATO_DETALLE_TRABAJO` + `DETALLES_TRABAJO`.
    - Calcula subtotal/IVA/total y actualiza la factura.

- SQL de soporte en `constructora/queries/`
  - `contratos_facturacion.sql`: crea `FACTURAS`, `DETALLES_FACTURA`, `PAGOS`, trigger y vista `CONTRATOS_FACTURABLES` (ajustada para el esquema base: `fecha_inicio_contrato/fecha_fin_contrato` y relación a `OBRAS` mediante `CONTRATO_OBRA`).
  - `facturizar_contrato.sql`: función `facturizar_contrato(p_id_contrato)` que inserta factura y detalles desde el contrato (usa fallbacks si faltan objetos opcionales).
  - `previsualizar_factura_contrato.sql`: consulta para revisar las líneas que se facturarían (reemplazar el `WHERE c.id_contrato = 1`).

## Cómo usar (rápido)

- Requisitos: Python 3.10+, PostgreSQL disponible, e instalar dependencias en el venv del proyecto `constructora/venv_constructora`.
- Iniciar app (PowerShell):

```powershell
cd "c:\Users\VICTUS\Videos\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\BASE-DE-DATOS-1-PROYECTO-FINAL-master\constructora"
python app.py
```

- Ingresar con tu usuario; si es `ADMINISTRADOR`, verás todas las opciones.
- Ir a Contratos > Ver o Listar y usar el botón “Generar factura”/“Facturar”.
- Si la función SQL está instalada y compatible, la usará; si no, el fallback Python generará la factura.

## Aplicar SQL de facturación (opcional pero recomendado)

Si deseas habilitar la función SQL y las vistas/trigger de facturación:

```powershell
cd "c:\Users\VICTUS\Videos\BASE-DE-DATOS-1-PROYECTO-FINAL-master (2)\BASE-DE-DATOS-1-PROYECTO-FINAL-master\constructora"
python scripts\aplicar_sql_facturacion.py
```

Notas:
- Si aparece error por columnas distintas (ej. `fecha_emision` vs `fecha_factura`), ya hay tablas previas con otro esquema. Puedes:
  1) Ajustar manualmente el SQL a tus columnas reales y volver a ejecutar, o
  2) Confiar en el fallback Python (no requiere cambios en DB y ya maneja nombres alternativos).

## Verificación rápida

- Ver facturas: menú Facturas > Lista o después de “Generar factura”, te redirige al detalle.
- Detalles y pagos: accesibles desde el detalle de la factura.

## Archivos tocados (principales)

- Backend
  - `constructora/app.py`: nuevas rutas de usuarios, facturación de contratos y wiring general.
  - `constructora/database.py`: registro robusto, permisos con fallback, funciones seguras CRUD y `facturizar_contrato_safe` con fallback Python.
- Plantillas
  - `templates/base.html`: botón de logout en el header.
  - `templates/dashboard.html`: enlace corregido a Bodegas.
  - `templates/usuarios/editar.html`: formulario de edición de usuario.
  - `templates/contratos/detalle.html` y `templates/contratos/listar.html`: botones para facturar.
- Estilos
  - `static/css/styles.css`: estilo del botón de logout y ajustes menores.
- SQL/Utilidades
  - `queries/contratos_facturacion.sql` y `queries/facturizar_contrato.sql` (función + vista + trigger).
  - `queries/previsualizar_factura_contrato.sql` (consulta de previsualización).
  - `scripts/aplicar_sql_facturacion.py` (aplicador de SQL, opcional).

## Limitaciones actuales y próximos pasos

- Si tu base ya tenía tablas `FACTURAS` con otros nombres de columnas, el aplicador SQL puede fallar. El fallback Python ya contempla estas diferencias y permite operar sin migrar de inmediato.
- Podríamos agregar permisos finos para facturación (p.ej. `FACTURAS_CREAR`) envolviendo la ruta `/contratos/<id>/facturizar` con `@permiso_requerido('FACTURAS_CREAR')`.
- Evitar facturas duplicadas por contrato: añadir chequeo previo en BD o en `facturizar_contrato_safe` (ej. buscar facturas existentes del contrato y solicitar confirmación).
- Reporte PDF de facturas (ruta de impresión): pendiente de implementar.

---

¿Dudas o quieres que automatice el chequeo de duplicidades y permisos en la ruta de facturación? Puedo dejarlo listo según tus reglas de negocio.