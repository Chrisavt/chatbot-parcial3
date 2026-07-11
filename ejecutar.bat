@echo off
REM Lanzador del Chatbot de IA (no requiere PowerShell ni permisos)
title Mapache Bot - Chatbot de IA
cd /d "%~dp0"

echo ============================================
echo   Chatbot de IA - Parcial 3 (Mapache Bot)
echo ============================================

if not exist ".venv\Scripts\python.exe" (
    echo [1/3] Creando entorno virtual (.venv)...
    python -m venv .venv
) else (
    echo [1/3] Entorno virtual ya presente.
)

echo [2/3] Verificando dependencias (openai es opcional)...
call .venv\Scripts\pip install -r requirements.txt >nul 2>&1 || echo [AVISO] No se pudieron instalar dependencias; el bot funciona en modo local.

echo [3/3] Iniciando el chatbot...
echo --------------------------------------------
call .venv\Scripts\python.exe src/bot.py
echo --------------------------------------------
echo [FIN] Sesion terminada.
pause
