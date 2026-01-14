# Script de Instalación Rápida
# Plataforma de Cámaras Trampa con IA

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Instalación de Plataforma de Cámaras" -ForegroundColor Green
Write-Host "  Trampa con IA - Versión 2.0" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Verificar Python
Write-Host "Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python no encontrado. Por favor instala Python 3.8 o superior." -ForegroundColor Red
    Write-Host "Descarga desde: https://www.python.org/downloads/" -ForegroundColor Cyan
    pause
    exit 1
}
Write-Host "✓ Python encontrado: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Preguntar sobre GPU
Write-Host "¿Tienes una GPU NVIDIA RTX con CUDA?" -ForegroundColor Yellow
Write-Host "1. Sí (instalar soporte para IA)" -ForegroundColor Cyan
Write-Host "2. No (modo manual asistido)" -ForegroundColor Cyan
$gpuChoice = Read-Host "Selecciona opción (1 o 2)"

Write-Host ""
Write-Host "Creando entorno virtual..." -ForegroundColor Yellow
python -m venv venv

Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Instalando dependencias..." -ForegroundColor Yellow

if ($gpuChoice -eq "1") {
    Write-Host "Instalando PyTorch con soporte CUDA..." -ForegroundColor Cyan
    pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Fallo la instalación de PyTorch" -ForegroundColor Red
        pause
        exit 1
    }
}

Write-Host "Instalando dependencias principales..." -ForegroundColor Cyan
pip install streamlit pandas openpyxl Pillow numpy scipy scikit-learn opencv-python tqdm requests matplotlib plotly

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Fallo la instalación de dependencias" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✓ Instalación Completada" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para ejecutar la aplicación:" -ForegroundColor Yellow
Write-Host "1. Activa el entorno: .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "2. Ejecuta: streamlit run app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Presiona Enter para ejecutar ahora..." -ForegroundColor Yellow
pause

Write-Host ""
Write-Host "Iniciando aplicación..." -ForegroundColor Green
streamlit run app.py
