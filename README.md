# 📷 Plataforma Profesional de Análisis de Datos de Cámaras Trampa

**Desarrollado por: Biólogo Erick Elio Chavez Gurrola**

## 📋 Descripción

Plataforma local diseñada para facilitar el análisis de datos de cámaras trampa. Extrae automáticamente la información de fecha y hora de captura de fotografías y organiza los datos en un formato estructurado para análisis posterior.

### ✨ Características Principales

- ✅ **Extracción automática de metadatos EXIF** - Lee la fecha de captura original de las fotografías
- ✅ **Generación de reportes Excel** - Crea archivos `.xlsx` con columnas organizadas
- ✅ **Funcionamiento 100% offline** - No requiere conexión a internet
- ✅ **Procesamiento selectivo** - Solo procesa fotografías, ignora videos automáticamente
- ✅ **Interfaz profesional** - Diseño intuitivo y fácil de usar
- ✅ **Validación de estructura** - Verifica que las carpetas estén organizadas correctamente

## 🔗 Complemento de FORXIME/2

Esta plataforma es un **complemento perfecto** para [FORXIME/2](https://forxime2-udpq6cmnacvdn4ai9qdj9g.streamlit.app/), una herramienta especializada en análisis estadístico avanzado de datos de fauna silvestre.

**Flujo de trabajo recomendado:**

1. Usa esta plataforma para organizar y extraer datos de tus cámaras trampa
2. Genera el archivo Excel con los datos estructurados
3. Importa el Excel en FORXIME/2 para análisis estadístico avanzado

## 📁 Estructura de Carpetas Requerida

Para que la plataforma funcione correctamente, organiza tus carpetas de la siguiente manera:

```
NOMBRE_DEL_PROYECTO/
├── SITIO_1/
│   ├── CAMARA_1/
│   │   ├── ESPECIE_A/
│   │   │   ├── foto001.jpg
│   │   │   ├── foto002.jpg
│   │   │   └── ...
│   │   ├── HUMANO/
│   │   │   └── foto003.jpg
│   │   └── VACIO/
│   │       └── foto004.jpg
│   ├── CAMARA_2/
│   │   └── ...
│   └── CAMARA_3/
│       └── ...
└── SITIO_2/
    └── ...
```

### 📝 Reglas Importantes

- Cada **sitio** puede tener hasta **3 cámaras**
- Las categorías de observación pueden ser: especies, **HUMANO**, **VACIO**, **GANADO**, etc.
- Solo se procesarán archivos de imagen: **JPG**, **JPEG**, **PNG**
- Los **videos serán ignorados** automáticamente
- Las fotografías deben tener metadatos EXIF de fecha de captura

## 🚀 Instalación Local (Sin Internet)

### Requisitos Previos

- **Python 3.8 o superior** instalado en tu computadora
- **Conexión a internet** (solo para la instalación inicial)

### Paso 1: Instalar Python

Si no tienes Python instalado:

1. Descarga Python desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, **marca la casilla** "Add Python to PATH"
3. Completa la instalación

### Paso 2: Descargar el Proyecto

1. Descarga este proyecto desde GitHub
2. Extrae el archivo ZIP en una carpeta de tu preferencia
3. Abre la carpeta del proyecto

### Paso 3: Instalar Dependencias

Abre una terminal (PowerShell o CMD) en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

Este comando instalará todas las bibliotecas necesarias:

- `streamlit` - Framework de la aplicación web
- `pandas` - Procesamiento de datos
- `openpyxl` - Generación de archivos Excel
- `Pillow` - Lectura de metadatos EXIF

### Paso 4: Ejecutar la Aplicación

En la misma terminal, ejecuta:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado en `http://localhost:8501`

## 📖 Guía de Uso

### 1. Preparar tus Datos

Organiza tus fotografías siguiendo la estructura de carpetas requerida:

- Carpeta principal con el nombre del proyecto
- Subcarpetas para cada sitio
- Subcarpetas para cada cámara (máximo 3 por sitio)
- Subcarpetas para cada especie o categoría
- Fotografías dentro de las carpetas de especies

### 2. Ejecutar la Aplicación

```bash
streamlit run app.py
```

### 3. Seleccionar Proyecto

En la interfaz de la aplicación:

1. Ingresa la ruta completa de tu carpeta de proyecto
   - Ejemplo: `C:\Users\Usuario\Documents\MiProyectoCamaras`
2. La aplicación validará automáticamente la estructura

### 4. Procesar Datos

1. Haz clic en el botón **"Procesar Datos y Generar Excel"**
2. Espera mientras la aplicación:
   - Recorre todas las carpetas
   - Lee los metadatos EXIF de cada fotografía
   - Extrae la fecha y hora de captura
   - Organiza los datos

### 5. Revisar Resultados

La aplicación mostrará:

- **Vista previa** de los datos procesados
- **Estadísticas** (número de sitios, cámaras, especies)
- **Ubicación** del archivo Excel generado

### 6. Descargar Excel

- El archivo Excel se guardará automáticamente en la carpeta del proyecto
- También puedes descargarlo directamente desde la interfaz
- El archivo incluirá las columnas: **SITIO**, **CAMARA**, **ESPECIE**, **FECHA**, **HORA**

## 📊 Formato del Excel Generado

El archivo Excel contendrá las siguientes columnas:

| SITIO | CAMARA | ESPECIE | FECHA | HORA |
|-------|--------|---------|-------|------|
| SITIO_1 | CAMARA_1 | Venado | 2024-01-15 | 14:30:25 |
| SITIO_1 | CAMARA_1 | HUMANO | 2024-01-15 | 16:45:10 |
| SITIO_2 | CAMARA_1 | VACIO | 2024-01-16 | 08:20:00 |

## ❓ Solución de Problemas

### La aplicación no encuentra imágenes

- Verifica que la estructura de carpetas sea correcta
- Asegúrate de que las fotografías tengan extensión `.jpg`, `.jpeg` o `.png`
- Confirma que las imágenes tengan metadatos EXIF de fecha de captura

### Error al leer metadatos

- Algunas cámaras no guardan metadatos EXIF correctamente
- Verifica las propiedades de la imagen en tu sistema operativo
- Busca la propiedad "Fecha de captura" o "Date Taken"

### La aplicación no inicia

- Verifica que Python esté instalado correctamente
- Asegúrate de haber instalado todas las dependencias
- Ejecuta `pip install -r requirements.txt` nuevamente

### Problemas con la ruta del proyecto

- Usa rutas absolutas completas
- En Windows, usa barras invertidas `\` o dobles barras `/`
- Ejemplo correcto: `C:\Users\Usuario\Documents\Proyecto`

## 🔧 Requisitos del Sistema

- **Sistema Operativo:** Windows, macOS, Linux
- **Python:** 3.8 o superior
- **RAM:** Mínimo 2 GB
- **Espacio en Disco:** 100 MB para la aplicación + espacio para tus datos

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso académico y científico.

## 👨‍🔬 Autor

**Biólogo Erick Elio Chavez Gurrola**

Para análisis estadístico avanzado, visita [FORXIME/2](https://forxime2-udpq6cmnacvdn4ai9qdj9g.streamlit.app/)

---

**Versión:** 1.0  
**Última actualización:** Enero 2026
