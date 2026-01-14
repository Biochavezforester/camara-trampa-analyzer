@echo off
REM ========================================
REM  INICIADOR DE PLATAFORMA
REM  Plataforma de Camaras Trampa con IA
REM ========================================

title Plataforma de Camaras Trampa con IA

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar que existe el entorno virtual
if not exist venv (
    color 0C
    echo.
    echo ERROR: No se encuentra el entorno virtual
    echo.
    echo Por favor ejecuta primero: INSTALAR.bat
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Limpiar pantalla y mostrar banner
cls
color 0A
echo.
echo ========================================
echo   Plataforma de Camaras Trampa con IA
echo   Version 2.0
echo ========================================
echo.
echo Iniciando aplicacion...
echo.

REM Verificar GPU
python -c "import torch; gpu=torch.cuda.is_available(); print(f'GPU: {\"Detectada - Modo IA\" if gpu else \"No detectada - Modo Manual\"}'); print(f'Dispositivo: {torch.cuda.get_device_name(0) if gpu else \"CPU\"}' if gpu else '')" 2>nul

echo.
echo La aplicacion se abrira en tu navegador
echo en: http://localhost:8501
echo.
echo ========================================
echo   INSTRUCCIONES:
echo ========================================
echo.
echo 1. Selecciona la carpeta de tu proyecto
echo 2. Click en "Procesar Proyecto"
echo 3. Ingresa coordenadas UTM
echo 4. Genera reportes Excel
echo.
echo Para CERRAR la aplicacion:
echo   - Cierra esta ventana
echo   - O presiona Ctrl+C
echo.
echo ========================================
echo.

REM Iniciar Streamlit
streamlit run app.py

REM Si Streamlit se cierra, pausar
echo.
echo La aplicacion se ha cerrado.
pause
