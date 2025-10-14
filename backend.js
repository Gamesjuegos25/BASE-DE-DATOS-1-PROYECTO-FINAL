// =================================================================
// EJEMPLO DE BACKEND EN NODE.JS PARA EL SISTEMA DE CONSTRUCTORA
// =================================================================
// Este archivo muestra cómo crear un backend que conecte con SQL Server
// y proporcione los endpoints necesarios para el sistema web
// =================================================================

const express = require('express');
const sql = require('mssql');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Configuración de la base de datos para LocalDB con Windows Authentication
const dbConfig = {
    server: process.env.DB_SERVER || '(LocalDb)\\MSSQLLocalDB',
    database: process.env.DB_DATABASE || 'BASEdeDATOSpf',
    options: {
        encrypt: false,
        trustServerCertificate: true,
        trustedConnection: true, // Usar Windows Authentication
        enableArithAbort: true,
        instanceName: 'MSSQLLocalDB'
    }
};

// Conectar a la base de datos
sql.connect(dbConfig).then(() => {
    console.log('Conectado a SQL Server');
}).catch(err => {
    console.error('Error conectando a la base de datos:', err);
});

// =================================================================
// ENDPOINTS PARA EL DASHBOARD
// =================================================================

app.get('/api/dashboard/estadisticas', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                (SELECT COUNT(*) FROM Obra WHERE estado = 'En Proceso') AS obras_activas,
                (SELECT COUNT(*) FROM Empleado WHERE estado = 'Activo') AS empleados_activos,
                (SELECT COUNT(*) FROM Material) AS total_materiales,
                (SELECT COUNT(*) FROM Proveedor) AS total_proveedores,
                (SELECT ISNULL(SUM(monto), 0) FROM FacturaProveedor) AS gastos_totales,
                (SELECT ISNULL(SUM(monto), 0) FROM PagoEmpleado WHERE estado = 'Pagado') AS pagos_realizados
        `);
        
        res.json(result.recordset[0]);
    } catch (error) {
        console.error('Error obteniendo estadísticas:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

app.get('/api/dashboard/obras-recientes', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT TOP 3 
                o.id_obra,
                o.nombre,
                o.ubicacion,
                o.estado,
                c.nombre AS cliente_nombre
            FROM Obra o
            LEFT JOIN Cliente c ON o.id_cliente = c.id_cliente
            ORDER BY o.id_obra DESC
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo obras recientes:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// =================================================================
// ENDPOINTS PARA OBRAS
// =================================================================

app.get('/api/obras', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                o.id_obra,
                o.nombre,
                o.ubicacion,
                o.tipo,
                o.estado,
                c.nombre AS cliente_nombre,
                c.contacto AS cliente_contacto,
                p.monto_estimado AS presupuesto,
                a.porcentaje_fisico,
                a.porcentaje_financiero,
                o.id_cliente
            FROM Obra o
            LEFT JOIN Cliente c ON o.id_cliente = c.id_cliente
            LEFT JOIN PresupuestoObra p ON o.id_obra = p.id_obra
            LEFT JOIN AvanceObra a ON o.id_obra = a.id_obra
            ORDER BY o.id_obra
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo obras:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

app.get('/api/obras/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const request = new sql.Request();
        request.input('id', sql.Int, id);
        
        const result = await request.query(`
            SELECT 
                o.id_obra,
                o.nombre,
                o.ubicacion,
                o.tipo,
                o.estado,
                c.nombre AS cliente_nombre,
                c.contacto AS cliente_contacto,
                c.tipo_cliente,
                p.monto_estimado,
                p.fecha AS fecha_presupuesto,
                a.porcentaje_fisico,
                a.porcentaje_financiero,
                a.fecha AS fecha_ultimo_avance
            FROM Obra o
            LEFT JOIN Cliente c ON o.id_cliente = c.id_cliente
            LEFT JOIN PresupuestoObra p ON o.id_obra = p.id_obra
            LEFT JOIN AvanceObra a ON o.id_obra = a.id_obra
            WHERE o.id_obra = @id
        `);
        
        if (result.recordset.length === 0) {
            return res.status(404).json({ error: 'Obra no encontrada' });
        }
        
        res.json(result.recordset[0]);
    } catch (error) {
        console.error('Error obteniendo detalle de obra:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// =================================================================
// ENDPOINTS PARA EMPLEADOS
// =================================================================

app.get('/api/empleados', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                e.id_empleado,
                e.nombre,
                e.tipo,
                e.salario_fijo,
                e.estado,
                COUNT(DISTINCT c.id_contrato) AS proyectos_asignados,
                (SELECT TOP 1 fecha FROM PagoEmpleado WHERE id_empleado = e.id_empleado ORDER BY fecha DESC) AS ultimo_pago,
                (SELECT TOP 1 monto FROM PagoEmpleado WHERE id_empleado = e.id_empleado ORDER BY fecha DESC) AS ultimo_monto
            FROM Empleado e
            LEFT JOIN Contrato c ON e.id_empleado = c.id_empleado AND c.estado = 'Activo'
            GROUP BY e.id_empleado, e.nombre, e.tipo, e.salario_fijo, e.estado
            ORDER BY e.id_empleado
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo empleados:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

app.get('/api/empleados/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const request = new sql.Request();
        request.input('id', sql.Int, id);
        
        const result = await request.query(`
            SELECT 
                e.id_empleado,
                e.nombre,
                e.tipo,
                e.salario_fijo,
                e.estado,
                COUNT(DISTINCT c.id_contrato) AS proyectos_asignados,
                (SELECT TOP 1 fecha FROM PagoEmpleado WHERE id_empleado = e.id_empleado ORDER BY fecha DESC) AS ultimo_pago,
                (SELECT TOP 1 monto FROM PagoEmpleado WHERE id_empleado = e.id_empleado ORDER BY fecha DESC) AS ultimo_monto
            FROM Empleado e
            LEFT JOIN Contrato c ON e.id_empleado = c.id_empleado AND c.estado = 'Activo'
            WHERE e.id_empleado = @id
            GROUP BY e.id_empleado, e.nombre, e.tipo, e.salario_fijo, e.estado
        `);
        
        if (result.recordset.length === 0) {
            return res.status(404).json({ error: 'Empleado no encontrado' });
        }
        
        res.json(result.recordset[0]);
    } catch (error) {
        console.error('Error obteniendo detalle de empleado:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// =================================================================
// ENDPOINTS PARA MATERIALES
// =================================================================

app.get('/api/materiales', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                m.id_material,
                m.nombre,
                m.unidad,
                m.precio_unitario,
                m.tipo_material,
                m.estado,
                p.nombre AS proveedor_nombre,
                p.contacto AS proveedor_contacto,
                ISNULL(SUM(i.cantidad), 0) AS stock_total
            FROM Material m
            LEFT JOIN Proveedor p ON m.id_proveedor = p.id_proveedor
            LEFT JOIN Inventario i ON m.id_material = i.id_material
            GROUP BY m.id_material, m.nombre, m.unidad, m.precio_unitario, m.tipo_material, m.estado, p.nombre, p.contacto
            ORDER BY m.id_material
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo materiales:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// =================================================================
// ENDPOINTS PARA PROVEEDORES
// =================================================================

app.get('/api/proveedores', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                p.id_proveedor,
                p.nombre,
                p.contacto,
                COUNT(DISTINCT m.id_material) AS materiales_suministrados,
                ISNULL(SUM(f.monto), 0) AS total_facturas,
                'Activo' AS estado
            FROM Proveedor p
            LEFT JOIN Material m ON p.id_proveedor = m.id_proveedor
            LEFT JOIN FacturaProveedor f ON p.id_proveedor = f.id_proveedor
            GROUP BY p.id_proveedor, p.nombre, p.contacto
            ORDER BY p.id_proveedor
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo proveedores:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// =================================================================
// ENDPOINTS PARA INVENTARIO
// =================================================================

app.get('/api/inventario', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                i.id_inventario,
                b.id_bodega,
                o.nombre AS obra_nombre,
                m.nombre AS material_nombre,
                i.cantidad,
                m.unidad,
                m.precio_unitario,
                (i.cantidad * m.precio_unitario) AS valor_total,
                b.responsable,
                m.estado
            FROM Inventario i
            JOIN Bodega b ON i.id_bodega = b.id_bodega
            JOIN Obra o ON b.id_obra = o.id_obra
            JOIN Material m ON i.id_material = m.id_material
            ORDER BY b.id_bodega, m.nombre
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo inventario:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// =================================================================
// ENDPOINTS PARA REPORTES
// =================================================================

app.get('/api/reportes/semanales', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                r.id_reporte,
                r.semana,
                o.nombre AS obra_nombre,
                r.fecha,
                r.resumen
            FROM ReporteSemanal r
            JOIN Obra o ON r.id_obra = o.id_obra
            ORDER BY r.fecha DESC
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo reportes semanales:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

app.get('/api/reportes/gastos', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                f.id_factura,
                p.nombre AS proveedor_nombre,
                f.fecha,
                f.monto,
                f.estado,
                'F-' + RIGHT('000' + CAST(f.id_factura AS VARCHAR), 3) + '-2024' AS numero_factura
            FROM FacturaProveedor f
            JOIN Proveedor p ON f.id_proveedor = p.id_proveedor
            ORDER BY f.fecha DESC
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo reportes de gastos:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

app.get('/api/reportes/materiales', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                m.nombre AS material_nombre,
                mov.tipo,
                mov.cantidad,
                m.unidad,
                mov.origen,
                mov.destino,
                mov.fecha
            FROM MovimientoMaterial mov
            JOIN Material m ON mov.id_material = m.id_material
            ORDER BY mov.fecha DESC
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo reportes de materiales:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

app.get('/api/reportes/pagos', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                e.nombre AS empleado_nombre,
                CASE 
                    WHEN e.salario_fijo > 0 THEN 'Salario Fijo'
                    ELSE 'Por Trabajo'
                END AS tipo_pago,
                p.fecha,
                p.monto,
                p.estado
            FROM PagoEmpleado p
            JOIN Empleado e ON p.id_empleado = e.id_empleado
            ORDER BY p.fecha DESC
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo reportes de pagos:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// =================================================================
// ENDPOINTS PARA CATÁLOGOS (FILTROS)
// =================================================================

app.get('/api/catalogos/bodegas', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                b.id_bodega,
                'Bodega ' + CAST(b.id_bodega AS VARCHAR) + ' - ' + o.nombre AS bodega_descripcion
            FROM Bodega b
            JOIN Obra o ON b.id_obra = o.id_obra
            ORDER BY b.id_bodega
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo catálogo de bodegas:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

app.get('/api/catalogos/obras', async (req, res) => {
    try {
        const result = await sql.query(`
            SELECT 
                id_obra,
                nombre
            FROM Obra
            ORDER BY nombre
        `);
        
        res.json(result.recordset);
    } catch (error) {
        console.error('Error obteniendo catálogo de obras:', error);
        res.status(500).json({ error: 'Error interno del servidor' });
    }
});

// =================================================================
// MIDDLEWARE DE MANEJO DE ERRORES
// =================================================================

app.use((err, req, res, next) => {
    console.error('Error no manejado:', err);
    res.status(500).json({ 
        error: 'Error interno del servidor',
        message: process.env.NODE_ENV === 'development' ? err.message : 'Contacte al administrador'
    });
});

// =================================================================
// INICIAR SERVIDOR
// =================================================================

app.listen(PORT, () => {
    console.log(`Servidor ejecutándose en http://localhost:${PORT}`);
    console.log('Endpoints disponibles:');
    console.log('- GET /api/dashboard/estadisticas');
    console.log('- GET /api/dashboard/obras-recientes');
    console.log('- GET /api/obras');
    console.log('- GET /api/obras/:id');
    console.log('- GET /api/empleados');
    console.log('- GET /api/empleados/:id');
    console.log('- GET /api/materiales');
    console.log('- GET /api/proveedores');
    console.log('- GET /api/inventario');
    console.log('- GET /api/reportes/semanales');
    console.log('- GET /api/reportes/gastos');
    console.log('- GET /api/reportes/materiales');
    console.log('- GET /api/reportes/pagos');
    console.log('- GET /api/catalogos/bodegas');
    console.log('- GET /api/catalogos/obras');
});

// =================================================================
// INSTRUCCIONES DE INSTALACIÓN Y USO
// =================================================================

/*
PARA INSTALAR Y EJECUTAR ESTE BACKEND:

1. INSTALAR DEPENDENCIAS:
   npm init -y
   npm install express mssql cors dotenv

2. CREAR ARCHIVO .env:
   DB_SERVER=(LocalDb)\MSSQLLocalDB
   DB_DATABASE=BASEdeDATOSpf
   NODE_ENV=development
   PORT=3000
   # No necesitas DB_USER ni DB_PASSWORD con Windows Authentication

3. EJECUTAR:
   node backend.js

4. PROBAR ENDPOINTS:
   - Abrir http://localhost:3000/api/dashboard/estadisticas
   - Verificar que devuelve datos JSON

5. MODIFICAR EL FRONTEND:
   - Cambiar API_CONFIG.baseURL a 'http://localhost:3000/api'
   - Usar las funciones *DB en lugar de las originales

ESTRUCTURA DE ARCHIVOS SUGERIDA:
├── backend.js (este archivo)
├── package.json
├── .env
├── public/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   ├── data.js (mantener como fallback)
│   └── conexion_database.js

SEGURIDAD ADICIONAL (PARA PRODUCCIÓN):
- Implementar autenticación JWT
- Validar entrada de datos
- Usar helmet.js para headers de seguridad
- Implementar rate limiting
- Configurar HTTPS
- Usar variables de entorno para configuración sensible
*/