# 📷 Plataforma Profesional de Análisis de Datos de Cámaras Trampa con IA

## Versión 2.0 - Con Clasificación Automática y Análisis Avanzado

**Desarrollado por:** Biólogo Erick Elio Chavez Gurrola

---

## 🎯 Características Principales

### ✨ Funcionalidades Core

- ✅ **Extracción automática de metadatos EXIF** (fecha, hora, modelo de cámara, temperatura)
- ✅ **Clasificación con IA** (si GPU NVIDIA RTX disponible) o modo asistido manual
- ✅ **Cálculo de esfuerzo de muestreo** (trampas-día por cámara)
- ✅ **Detección de eventos independientes** con criterio temporal configurable
- ✅ **Análisis temporal completo** (diurno, nocturno, crepuscular, horas pico)
- ✅ **Índice de Abundancia Relativa (RAI)** por especie
- ✅ **Gestión de coordenadas UTM** con validación para zonas de México
- ✅ **Exportación dual de Excel**: Básico (FORXIME/2) + Completo (análisis)
- ✅ **Validación de calidad de datos** con scoring automático
- ✅ **Base de datos local** (SQLite) para historial de proyectos
- ✅ **100% offline** (después de instalación inicial)

### 🤖 Sistema de IA (Opcional - Requiere GPU)

- **Detección automática de GPU CUDA**
- **Modo dual**: IA automática (GPU) o asistido manual (CPU)
- **Clasificación de especies** optimizada para fauna mexicana
- **Niveles de confianza** en predicciones
- **Validación obligatoria** de predicciones por el usuario

### 📊 Análisis Avanzado

- Cálculo de trampas-día por cámara y sitio
- Eventos independientes con RAI
- Patrones temporales (24 horas)
- Frecuencia de visitas por especie
- Detección de períodos sin capturas (gaps)
- Reporte de calidad de datos

### 📍 Coordenadas UTM

- Soporte para zonas UTM de México (11Q-16P)
- Validación de rangos para territorio mexicano
- Datum WGS84 por defecto
- Almacenamiento en base de datos para reutilización
- Exportación a Excel con coordenadas

---

## 🚀 Instalación

### Requisitos Mínimos

- **Python:** 3.8 o superior
- **RAM:** 4 GB
- **Espacio en disco:** 2 GB

### Requisitos Recomendados (para IA)

- **GPU:** NVIDIA RTX 3060+ (6GB VRAM)
- **CUDA:** 11.8 o superior
- **RAM:** 16 GB
- **Espacio en disco:** 10 GB (modelos de IA)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**

```bash
git clone https://github.com/tu-usuario/camara-trampa-analyzer.git
cd camara-trampa-analyzer
```

1. **Crear entorno virtual** (recomendado)

```bash
python -m venv venv
```

1. **Activar entorno virtual**

- Windows:

```bash
venv\Scripts\activate
```

- Linux/Mac:

```bash
source venv/bin/activate
```

1. **Instalar dependencias**

**Sin GPU (modo manual):**

```bash
pip install streamlit pandas openpyxl Pillow numpy scipy scikit-learn opencv-python tqdm requests matplotlib plotly
```

**Con GPU NVIDIA (modo IA):**

```bash
# Primero instalar PyTorch con CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Luego el resto de dependencias
pip install -r requirements.txt
```

1. **Ejecutar la aplicación**

```bash
streamlit run app.py
```

---

## 📁 Estructura de Carpetas Requerida

```
PROYECTO/
├── SITIO_1/
│   ├── CAMARA_1/
│   │   ├── VENADO_COLA_BLANCA/
│   │   │   ├── IMG_0001.JPG
│   │   │   ├── IMG_0002.JPG
│   │   │   └── ...
│   │   ├── PECARI_DE_COLLAR/
│   │   │   └── ...
│   │   └── VACIO/
│   │       └── ...
│   └── CAMARA_2/
│       └── ...
└── SITIO_2/
    └── ...
```

### Reglas Importantes

- ✅ Jerarquía: **Proyecto > Sitio > Cámara > Especie > Fotos**
- ✅ Formatos soportados: **JPG, JPEG, PNG** (mayúsculas o minúsculas)
- ✅ Videos se ignoran automáticamente
- ✅ Máximo 10 cámaras por sitio
- ✅ Nombres de especies en MAYÚSCULAS recomendado

---

## 🎮 Uso de la Plataforma

### 1. Procesamiento Inicial

1. Abrir la aplicación
2. Ir a tab "📁 Procesamiento"
3. Ingresar ruta del proyecto
4. Click en "🚀 Procesar Proyecto"
5. Esperar a que termine el procesamiento

### 2. Ingreso de Coordenadas UTM

1. Ir a tab "📍 Coordenadas UTM"
2. Para cada cámara, ingresar:
   - Zona UTM (ej: 13Q, 14R)
   - Este (Easting) en metros
   - Norte (Northing) en metros
   - Datum (WGS84 por defecto)
3. Click en "💾 Guardar coordenadas"

### 3. Análisis y Exportación

1. Ir a tab "📊 Análisis y Reportes"
2. Revisar análisis estadísticos
3. Click en "💾 Generar Excel (Básico + Completo)"
4. Descargar ambos archivos:
   - **Básico**: Para importar en FORXIME/2
   - **Completo**: Con todos los análisis

---

## 📄 Formatos de Exportación

### Excel Básico (FORXIME/2)

**Columnas:**

- SITIO
- CAMARA
- ESPECIE
- FECHA (YYYY-MM-DD)
- HORA (HH:MM:SS)

**Uso:** Importación directa en FORXIME/2 para análisis estadístico avanzado

### Excel Completo

**Hojas:**

1. **Datos**: Todos los registros con metadatos completos
2. **Coordenadas**: Ubicación UTM de cada cámara
3. **Esfuerzo**: Trampas-día por cámara
4. **Eventos_Independientes**: Análisis de eventos únicos con RAI
5. **Analisis_Temporal**: Patrones de actividad por especie
6. **Resumen**: Estadísticas generales del proyecto

---

## 🗺️ Zonas UTM en México

### Zonas Comunes

- **11Q, 11R**: Baja California
- **12Q, 12R**: Sonora, Sinaloa
- **13Q, 13R**: Durango, Jalisco, Zacatecas
- **14Q, 14R**: Coahuila, Nuevo León, Guanajuato
- **15Q, 15P**: Veracruz, Oaxaca, Chiapas
- **16Q, 16P**: Yucatán, Quintana Roo, Campeche

### Bandas de Latitud

- **P** (8-16°N): Extremo sur
- **Q** (16-24°N): Sur y centro - **MÁS COMÚN**
- **R** (24-32°N): Norte

**Ejemplo:** El Salto, Durango = **13Q 462728E 2630653N**

---

## 🔧 Configuración

### Parámetros Ajustables

- **Minutos entre eventos independientes**: 5-120 minutos (default: 30)
- **Zonas UTM válidas**: Configuradas para México
- **Datum por defecto**: WGS84
- **Formatos de exportación**: Ambos activados por defecto

### Archivo de Configuración

La plataforma genera automáticamente `config.json` con todas las configuraciones.

---

## 🤝 Integración con FORXIME/2

Esta plataforma está diseñada para trabajar en conjunto con [FORXIME/2](https://forxime2-udpq6cmnacvdn4ai9qdj9g.streamlit.app/):

1. **Procesar fotos** con esta plataforma
2. **Exportar Excel básico**
3. **Importar en FORXIME/2** para:
   - Índices de diversidad (Shannon, Simpson)
   - Curvas de rarefacción
   - Dendrogramas de similitud
   - Análisis de ocupación
   - Comparaciones entre sitios

---

## 📊 Base de Datos Local

La plataforma mantiene una base de datos SQLite (`database/projects.db`) con:

- Historial de proyectos procesados
- Coordenadas UTM guardadas por cámara
- Historial de procesamiento
- Catálogo de especies por proyecto

**Ventaja:** Las coordenadas se guardan automáticamente y se reutilizan en futuros procesamientos del mismo proyecto.

---

## 🐛 Solución de Problemas

### GPU no detectada

- Verificar drivers NVIDIA actualizados
- Verificar instalación de CUDA
- La plataforma funcionará en modo manual automáticamente

### Fotos sin metadatos EXIF

- Verificar que las fotos tengan fecha de captura
- Usar cámaras que graben metadatos EXIF
- Revisar reporte de calidad de datos

### Error en estructura de carpetas

- Verificar jerarquía: Proyecto > Sitio > Cámara > Especie > Fotos
- Máximo 10 cámaras por sitio
- Solo imágenes (JPG, JPEG, PNG)

---

## 📝 Registro de Cambios

### Versión 2.0 (2026)

- ✨ Sistema de clasificación con IA
- ✨ Detección automática de GPU CUDA
- ✨ Modo dual (IA/Manual)
- ✨ Gestión de coordenadas UTM
- ✨ Exportación dual de Excel
- ✨ Base de datos local
- ✨ Análisis temporal avanzado
- ✨ Validación de calidad de datos
- ✨ Interfaz completamente renovada

### Versión 1.0

- Extracción básica de metadatos EXIF
- Generación de Excel simple
- Validación de estructura de carpetas

---

## 👨‍🔬 Autor

**Biólogo Erick Elio Chavez Gurrola**

---

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para más detalles.

---

## 🙏 Agradecimientos

- Microsoft CameraTraps (MegaDetector)
- Comunidad de PyTorch
- FORXIME/2 platform

---

## 📧 Soporte

Para reportar problemas o sugerencias, crear un issue en el repositorio de GitHub.
