@echo off
echo ============================================================
echo 🚀 INICIANDO SISTEMA DE CONSTRUCTORA
echo ============================================================
echo.

:: Verificar que LocalDB esté ejecutándose
echo 1️⃣ Verificando LocalDB...
sqllocaldb info MSSQLLocalDB | find "Running" >nul
if %errorlevel% neq 0 (
    echo ⚠️ LocalDB no está ejecutándose. Iniciando...
    sqllocaldb start MSSQLLocalDB
    if %errorlevel% neq 0 (
        echo ❌ Error iniciando LocalDB
        pause
        exit /b 1
    ) else (
        echo ✅ LocalDB iniciado
    )
) else (
    echo ✅ LocalDB ya está ejecutándose
)

echo.
echo 2️⃣ Verificando dependencias de Node.js...
if not exist node_modules (
    echo 📦 Instalando dependencias...
    call npm install
)

echo.
echo 3️⃣ Probando conexión rápida...
call node test_conexion.js

echo.
echo 4️⃣ Iniciando servidor backend...
echo.
echo 🌐 El servidor estará disponible en: http://localhost:3000
echo 📱 Abre index.html en tu navegador para usar el sistema
echo.
echo ⏹️ Presiona Ctrl+C para detener el servidor
echo.

node backend.js