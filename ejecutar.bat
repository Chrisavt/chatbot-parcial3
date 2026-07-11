@echo off
REM Lanzador del Chatbot de IA (no requiere PowerShell ni permisos)
cd /d "%~dp0"

REM Crear entorno virtual si no existe
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
)

REM Instalar dependencias (no detiene el bot si falla)
call .venv\Scripts\pip install -r requirements.txt >nul 2>&1 || echo [AVISO] No se pudieron instalar las dependencias.

REM Ejecutar el chatbot
call .venv\Scripts\python.exe -m src.bot
pause
