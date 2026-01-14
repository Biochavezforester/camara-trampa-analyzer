@echo off
echo ========================================
echo   Plataforma de Camaras Trampa con IA
echo   Iniciando con GPU Local
echo ========================================
echo.

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar GPU
echo.
echo Verificando GPU NVIDIA...
python -c "import torch; print(f'CUDA disponible: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"No detectada - Modo manual activado\"}')"
echo.

REM Ejecutar aplicación
echo Iniciando aplicacion Streamlit...
echo La aplicacion se abrira en tu navegador en http://localhost:8501
echo.
echo Presiona Ctrl+C para detener la aplicacion
echo.
streamlit run app.py

pause
