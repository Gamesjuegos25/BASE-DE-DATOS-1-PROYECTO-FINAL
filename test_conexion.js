// =================================================================
// SCRIPT DE PRUEBA DE CONEXIÓN PARA SQL SERVER LOCALDB
// =================================================================
// Este script verifica que la conexión con LocalDB funcione correctamente

const sql = require('mssql');

// Configuración específica para LocalDB
const dbConfig = {
    server: '(LocalDb)\\MSSQLLocalDB',
    database: 'BASEdeDATOSpf',
    options: {
        encrypt: false,
        trustServerCertificate: true,
        trustedConnection: true, // Windows Authentication
        enableArithAbort: true,
        instanceName: 'MSSQLLocalDB'
    }
};

async function probarConexion() {
    try {
        console.log('🔄 Intentando conectar a LocalDB...');
        console.log('Servidor:', dbConfig.server);
        console.log('Base de datos:', dbConfig.database);
        console.log('Autenticación: Windows Authentication');
        console.log('');

        // Conectar a la base de datos
        await sql.connect(dbConfig);
        console.log('✅ ¡Conexión exitosa a SQL Server LocalDB!');
        
        // Probar una consulta simple
        console.log('\n🔍 Probando consulta de prueba...');
        const result = await sql.query('SELECT COUNT(*) as total_tablas FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\'');
        console.log(`✅ Consulta exitosa: Se encontraron ${result.recordset[0].total_tablas} tablas en la base de datos`);
        
        // Verificar algunas tablas específicas
        console.log('\n📋 Verificando tablas principales...');
        const tablas = await sql.query(`
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE' 
            AND TABLE_NAME IN ('Cliente', 'Obra', 'Empleado', 'Material', 'Proveedor')
            ORDER BY TABLE_NAME
        `);
        
        if (tablas.recordset.length > 0) {
            console.log('✅ Tablas principales encontradas:');
            tablas.recordset.forEach(tabla => {
                console.log(`   - ${tabla.TABLE_NAME}`);
            });
        } else {
            console.log('⚠️ No se encontraron las tablas principales. Asegúrate de haber ejecutado el script de creación.');
        }
        
        // Verificar si hay datos
        console.log('\n📊 Verificando datos...');
        try {
            const obras = await sql.query('SELECT COUNT(*) as total FROM Obra');
            const empleados = await sql.query('SELECT COUNT(*) as total FROM Empleado');
            const materiales = await sql.query('SELECT COUNT(*) as total FROM Material');
            
            console.log(`✅ Datos encontrados:`);
            console.log(`   - Obras: ${obras.recordset[0].total}`);
            console.log(`   - Empleados: ${empleados.recordset[0].total}`);
            console.log(`   - Materiales: ${materiales.recordset[0].total}`);
            
            if (obras.recordset[0].total === 0) {
                console.log('\n💡 Sugerencia: Ejecuta el script "insertar_datos.sql" para poblar la base de datos');
            }
        } catch (error) {
            console.log('⚠️ Las tablas existen pero no hay datos o hay un error en la estructura');
            console.log('💡 Ejecuta primero "crear base de datos y tablas.sql" y luego "insertar_datos.sql"');
        }
        
    } catch (error) {
        console.log('❌ Error de conexión:');
        console.log('Error:', error.message);
        
        if (error.message.includes('Login failed')) {
            console.log('\n💡 Soluciones posibles:');
            console.log('1. Verifica que SQL Server LocalDB esté ejecutándose');
            console.log('2. Ejecuta: sqllocaldb start MSSQLLocalDB');
            console.log('3. Verifica que tengas permisos de Windows para acceder');
        } else if (error.message.includes('database') && error.message.includes('does not exist')) {
            console.log('\n💡 La base de datos no existe. Para crearla:');
            console.log('1. Ejecuta el script "crear base de datos y tablas.sql"');
            console.log('2. Luego ejecuta "insertar_datos.sql"');
        } else if (error.message.includes('server was not found')) {
            console.log('\n💡 No se puede conectar al servidor. Verifica:');
            console.log('1. Que SQL Server LocalDB esté instalado');
            console.log('2. Ejecuta: sqllocaldb info');
            console.log('3. Si no está creado: sqllocaldb create MSSQLLocalDB');
            console.log('4. Para iniciarlo: sqllocaldb start MSSQLLocalDB');
        }
    } finally {
        // Cerrar la conexión
        try {
            await sql.close();
            console.log('\n🔌 Conexión cerrada correctamente');
        } catch (closeError) {
            console.log('⚠️ Error cerrando conexión:', closeError.message);
        }
    }
}

// Función para verificar el estado de LocalDB
async function verificarLocalDB() {
    const { exec } = require('child_process');
    
    return new Promise((resolve) => {
        exec('sqllocaldb info MSSQLLocalDB', (error, stdout, stderr) => {
            if (error) {
                console.log('⚠️ LocalDB no está disponible o no está creado');
                console.log('💡 Para crear LocalDB ejecuta: sqllocaldb create MSSQLLocalDB');
                resolve(false);
            } else {
                console.log('✅ LocalDB está disponible');
                if (stdout.includes('Running')) {
                    console.log('✅ LocalDB está ejecutándose');
                } else {
                    console.log('⚠️ LocalDB no está ejecutándose');
                    console.log('💡 Para iniciarlo ejecuta: sqllocaldb start MSSQLLocalDB');
                }
                resolve(true);
            }
        });
    });
}

// Ejecutar las verificaciones
async function main() {
    console.log('='.repeat(60));
    console.log('🏗️ PRUEBA DE CONEXIÓN - SISTEMA CONSTRUCTORA');
    console.log('='.repeat(60));
    
    console.log('\n1️⃣ Verificando LocalDB...');
    await verificarLocalDB();
    
    console.log('\n2️⃣ Probando conexión a la base de datos...');
    await probarConexion();
    
    console.log('\n' + '='.repeat(60));
    console.log('✨ Prueba de conexión completada');
    console.log('='.repeat(60));
}

// Solo ejecutar si este archivo se ejecuta directamente
if (require.main === module) {
    main().catch(console.error);
}

module.exports = { probarConexion, verificarLocalDB };