@echo off
echo ============================================================
echo 🏗️ CONFIGURACION AUTOMATICA - SISTEMA CONSTRUCTORA
echo ============================================================
echo.

:: Verificar si Node.js está instalado
echo 1️⃣ Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js no está instalado
    echo 💡 Descarga e instala Node.js desde: https://nodejs.org/
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Node.js está instalado
)

echo.
echo 2️⃣ Verificando LocalDB...
sqllocaldb info MSSQLLocalDB >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ LocalDB MSSQLLocalDB no existe
    echo 💡 Creando LocalDB...
    sqllocaldb create MSSQLLocalDB
    if %errorlevel% neq 0 (
        echo ❌ Error creando LocalDB
        pause
        exit /b 1
    )
) else (
    echo ✅ LocalDB existe
)

echo.
echo 3️⃣ Iniciando LocalDB...
sqllocaldb start MSSQLLocalDB
if %errorlevel% neq 0 (
    echo ❌ Error iniciando LocalDB
    pause
    exit /b 1
) else (
    echo ✅ LocalDB iniciado correctamente
)

echo.
echo 4️⃣ Verificando si package.json existe...
if not exist package.json (
    echo 📦 Inicializando proyecto Node.js...
    echo {"name": "sistema-constructora", "version": "1.0.0", "description": "Sistema de consultas para constructora", "main": "backend.js", "scripts": {"start": "node backend.js", "test": "node test_conexion.js"}} > package.json
)

echo.
echo 5️⃣ Instalando dependencias de Node.js...
call npm install express mssql cors dotenv
if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
) else (
    echo ✅ Dependencias instaladas correctamente
)

echo.
echo 6️⃣ Probando conexión a la base de datos...
call node test_conexion.js

echo.
echo ============================================================
echo ✨ CONFIGURACION COMPLETADA
echo ============================================================
echo.
echo 📋 Próximos pasos:
echo.
echo 1. Si la base de datos no existe:
echo    - Ejecuta: crear_base_datos_y_tablas.sql en SQL Server
echo    - Ejecuta: insertar_datos.sql para poblar datos
echo.
echo 2. Para iniciar el sistema:
echo    - Ejecuta: iniciar_sistema.bat
echo    - O manualmente: node backend.js
echo.
echo 3. Para usar el sistema web:
echo    - Abre index.html en tu navegador
echo    - El sistema estará disponible en http://localhost:3000
echo.

pause