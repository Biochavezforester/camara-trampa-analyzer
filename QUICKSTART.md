# 🚀 Guía de Inicio Rápido

## Instalación en 3 Pasos

### 1. Ejecutar Script de Instalación (Windows)

```powershell
.\install.ps1
```

El script automáticamente:

- ✅ Verifica Python
- ✅ Crea entorno virtual
- ✅ Pregunta si tienes GPU
- ✅ Instala dependencias correctas
- ✅ Ejecuta la aplicación

### 2. Instalación Manual

**Sin GPU:**

```bash
python -m venv venv
venv\Scripts\activate
pip install streamlit pandas openpyxl Pillow numpy scipy scikit-learn opencv-python tqdm requests matplotlib plotly
streamlit run app.py
```

**Con GPU NVIDIA:**

```bash
python -m venv venv
venv\Scripts\activate
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
streamlit run app.py
```

### 3. Primer Uso

1. La aplicación se abrirá en tu navegador
2. Ir a tab "📁 Procesamiento"
3. Ingresar ruta de tu proyecto
4. Click "🚀 Procesar Proyecto"
5. ¡Listo!

---

## 📁 Preparar tus Datos

Organiza tus fotos así:

```
MiProyecto/
├── SITIO_NORTE/
│   ├── CAM_01/
│   │   ├── VENADO_COLA_BLANCA/
│   │   │   └── *.JPG
│   │   └── VACIO/
│   │       └── *.JPG
│   └── CAM_02/
│       └── ...
└── SITIO_SUR/
    └── ...
```

---

## ⚡ Uso Rápido

1. **Procesar**: Selecciona carpeta → Procesar
2. **Coordenadas**: Ingresa UTM para cada cámara
3. **Exportar**: Genera Excel (Básico + Completo)
4. **FORXIME/2**: Importa Excel básico para análisis avanzado

---

## 🆘 Problemas Comunes

**"GPU no detectada"**
→ Normal si no tienes GPU NVIDIA. Usa modo manual.

**"No se encontraron fotos"**
→ Verifica estructura de carpetas.

**"Fotos sin EXIF"**
→ Tus fotos deben tener fecha de captura en metadatos.

---

## 📞 Soporte

Ver README.md completo para documentación detallada.
