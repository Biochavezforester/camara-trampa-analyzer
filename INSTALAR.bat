@echo off
REM ========================================
REM  INSTALADOR AUTOMATICO
REM  Plataforma de Camaras Trampa con IA
REM ========================================

color 0A
title Instalador - Plataforma de Camaras Trampa

echo.
echo ========================================
echo   INSTALADOR AUTOMATICO
echo   Plataforma de Camaras Trampa con IA
echo ========================================
echo.
echo Este instalador hara TODO automaticamente:
echo  - Verificar Python
echo  - Crear entorno virtual
echo  - Detectar tu GPU
echo  - Instalar dependencias
echo  - Crear acceso directo en el Escritorio
echo.
echo Presiona cualquier tecla para comenzar...
pause >nul

REM Verificar Python
echo.
echo [1/5] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo ERROR: Python no esta instalado
    echo.
    echo Por favor instala Python 3.8 o superior desde:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANTE: Durante la instalacion, marca la casilla
    echo "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
echo OK - Python encontrado
timeout /t 1 >nul

REM Crear entorno virtual
echo.
echo [2/5] Creando entorno virtual...
if exist venv (
    echo Entorno virtual ya existe, omitiendo...
) else (
    python -m venv venv
    echo OK - Entorno virtual creado
)
timeout /t 1 >nul

REM Activar entorno
echo.
echo [3/5] Activando entorno virtual...
call venv\Scripts\activate.bat
echo OK - Entorno activado
timeout /t 1 >nul

REM Detectar GPU
echo.
echo [4/5] Detectando GPU NVIDIA...
nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo.
    echo No se detecto GPU NVIDIA
    echo Instalando version CPU (modo manual)...
    echo.
    set GPU_MODE=0
) else (
    echo.
    echo GPU NVIDIA detectada!
    echo Instalando version con soporte GPU...
    echo.
    set GPU_MODE=1
)
timeout /t 2 >nul

REM Instalar dependencias
echo.
echo [5/5] Instalando dependencias...
echo Esto puede tomar varios minutos...
echo.

if %GPU_MODE%==1 (
    echo Instalando PyTorch con CUDA...
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118 --quiet
    if errorlevel 1 (
        echo Error instalando PyTorch, intentando version CPU...
        pip install torch torchvision --quiet
    )
)

echo Instalando dependencias principales...
pip install streamlit pandas openpyxl Pillow numpy scipy scikit-learn opencv-python tqdm requests matplotlib plotly --quiet

if errorlevel 1 (
    color 0C
    echo.
    echo ERROR: Fallo la instalacion de dependencias
    echo.
    pause
    exit /b 1
)

echo OK - Dependencias instaladas
timeout /t 1 >nul

REM Crear acceso directo en el escritorio
echo.
echo Creando acceso directo en el Escritorio...

set SCRIPT_DIR=%~dp0
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT=%DESKTOP%\Plataforma Camaras Trampa.lnk

REM Crear script VBS para crear el acceso directo
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%SHORTCUT%" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%INICIAR_PLATAFORMA.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "Plataforma de Analisis de Camaras Trampa con IA" >> CreateShortcut.vbs
echo oLink.IconLocation = "%SystemRoot%\System32\imageres.dll,190" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript CreateShortcut.vbs >nul
del CreateShortcut.vbs

echo OK - Acceso directo creado en el Escritorio

REM Resumen final
cls
color 0A
echo.
echo ========================================
echo   INSTALACION COMPLETADA!
echo ========================================
echo.
if %GPU_MODE%==1 (
    echo GPU: Detectada - Clasificacion automatica disponible
) else (
    echo GPU: No detectada - Modo manual asistido
)
echo.
echo Se ha creado un acceso directo en tu Escritorio:
echo   "Plataforma Camaras Trampa"
echo.
echo ========================================
echo   COMO USAR:
echo ========================================
echo.
echo 1. Haz DOBLE CLICK en el icono del Escritorio
echo 2. La aplicacion se abrira en tu navegador
echo 3. Listo para usar!
echo.
echo ========================================
echo.
echo Presiona cualquier tecla para iniciar la aplicacion ahora...
pause >nul

REM Iniciar aplicacion
call INICIAR_PLATAFORMA.bat
