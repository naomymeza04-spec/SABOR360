@echo off
chcp 65001 >nul
cd /d "%~dp0"
title SABOR 360 - Iniciar proyecto

echo ============================================
echo   SABOR 360 - Iniciador
echo ============================================
echo.

if not exist "frontend\node_modules" (
    echo Instalando dependencias del frontend...
    cd frontend
    call npm install
    cd ..
)

echo Cargando base de datos...
".venv\Scripts\python.exe" cli\crear_bd.py

echo.
echo Iniciando BACKEND (API)...
start "SABOR360 - Backend" cmd /k "cd /d "%~dp0" && .venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --port 8000"

echo Iniciando FRONTEND...
start "SABOR360 - Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo Esperando a que los servicios arranquen...
timeout /t 4 /nobreak >nul
start "" "http://127.0.0.1:8000/docs"
timeout /t 3 /nobreak >nul
start "" "http://localhost:5173"

echo.
echo Proyecto iniciado. Cierra las dos ventanas para detener el servidor.