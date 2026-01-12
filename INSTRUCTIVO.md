# 📖 Instructivo Detallado - Plataforma de Análisis de Cámaras Trampa

**Guía paso a paso para usuarios sin conocimientos técnicos**

---

## 🎯 Objetivo

Este instructivo te guiará en la instalación y uso de la Plataforma de Análisis de Cámaras Trampa en tu computadora, **sin necesidad de conexión a internet** una vez instalada.

---

## 📋 Tabla de Contenidos

1. [Instalación de Python](#1-instalación-de-python)
2. [Descarga del Proyecto](#2-descarga-del-proyecto)
3. [Instalación de Dependencias](#3-instalación-de-dependencias)
4. [Preparación de tus Datos](#4-preparación-de-tus-datos)
5. [Ejecución de la Aplicación](#5-ejecución-de-la-aplicación)
6. [Uso de la Plataforma](#6-uso-de-la-plataforma)
7. [Análisis Avanzado con FORXIME/2](#7-análisis-avanzado-con-forxime2)
8. [Preguntas Frecuentes](#8-preguntas-frecuentes)

---

## 1. Instalación de Python

Python es el lenguaje de programación necesario para ejecutar la plataforma.

### Paso 1.1: Descargar Python

1. Abre tu navegador web
2. Ve a la página oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/)
3. Haz clic en el botón amarillo **"Download Python 3.x.x"** (la versión más reciente)
4. Espera a que se descargue el instalador

### Paso 1.2: Instalar Python

1. Abre el archivo descargado (doble clic)
2. **MUY IMPORTANTE:** Marca la casilla **"Add Python to PATH"** en la parte inferior
3. Haz clic en **"Install Now"**
4. Espera a que termine la instalación
5. Haz clic en **"Close"** cuando termine

### Paso 1.3: Verificar la Instalación

1. Abre el **Símbolo del sistema** (CMD) o **PowerShell**:
   - Presiona `Windows + R`
   - Escribe `cmd` y presiona Enter
2. Escribe el siguiente comando y presiona Enter:

   ```bash
   python --version
   ```

3. Deberías ver algo como: `Python 3.11.x`
4. Si ves este mensaje, ¡Python está instalado correctamente! ✅

---

## 2. Descarga del Proyecto

### Opción A: Descargar desde GitHub (Recomendado)

1. Ve al repositorio de GitHub del proyecto
2. Haz clic en el botón verde **"Code"**
3. Selecciona **"Download ZIP"**
4. Guarda el archivo en una ubicación fácil de recordar (por ejemplo, `Documentos`)
5. Extrae el archivo ZIP:
   - Haz clic derecho en el archivo ZIP
   - Selecciona **"Extraer todo..."**
   - Elige la ubicación de destino
   - Haz clic en **"Extraer"**

### Opción B: Clonar con Git (Avanzado)

Si tienes Git instalado:

```bash
git clone [URL-del-repositorio]
```

---

## 3. Instalación de Dependencias

Las dependencias son bibliotecas adicionales que la plataforma necesita para funcionar.

### Paso 3.1: Abrir la Terminal en la Carpeta del Proyecto

**Método 1 (Windows 10/11):**

1. Abre el Explorador de Archivos
2. Navega hasta la carpeta del proyecto extraída
3. Haz clic en la barra de direcciones (donde dice la ruta)
4. Escribe `cmd` y presiona Enter
5. Se abrirá una ventana de comandos en esa carpeta

**Método 2 (Cualquier Windows):**

1. Abre el Explorador de Archivos
2. Navega hasta la carpeta del proyecto
3. Mantén presionada la tecla `Shift`
4. Haz clic derecho en un espacio vacío
5. Selecciona **"Abrir ventana de PowerShell aquí"** o **"Abrir en Terminal"**

### Paso 3.2: Instalar las Bibliotecas

1. En la ventana de comandos que acabas de abrir, escribe:

   ```bash
   pip install -r requirements.txt
   ```

2. Presiona Enter
3. Espera a que se descarguen e instalen todas las bibliotecas
4. Verás mensajes de instalación en pantalla
5. Cuando termine, verás el cursor parpadeando de nuevo

**Nota:** Este paso **requiere conexión a internet**, pero solo se hace una vez.

---

## 4. Preparación de tus Datos

Antes de usar la plataforma, debes organizar tus fotografías de cámaras trampa.

### Paso 4.1: Crear la Estructura de Carpetas

Crea una carpeta principal con el nombre de tu proyecto, por ejemplo:

```
MiProyectoCamaras
```

### Paso 4.2: Organizar por Sitios

Dentro de la carpeta del proyecto, crea una carpeta para cada sitio de muestreo:

```
MiProyectoCamaras/
├── SITIO_NORTE/
├── SITIO_SUR/
└── SITIO_ESTE/
```

### Paso 4.3: Organizar por Cámaras

Dentro de cada sitio, crea carpetas para cada cámara (máximo 3 por sitio):

```
MiProyectoCamaras/
└── SITIO_NORTE/
    ├── CAMARA_1/
    ├── CAMARA_2/
    └── CAMARA_3/
```

### Paso 4.4: Organizar por Especies/Categorías

Dentro de cada cámara, crea carpetas para cada especie o categoría observada:

```
MiProyectoCamaras/
└── SITIO_NORTE/
    └── CAMARA_1/
        ├── Venado/
        ├── Puma/
        ├── HUMANO/
        ├── VACIO/
        └── GANADO/
```

### Paso 4.5: Colocar las Fotografías

Coloca las fotografías correspondientes en cada carpeta de especie:

```
MiProyectoCamaras/
└── SITIO_NORTE/
    └── CAMARA_1/
        └── Venado/
            ├── IMG_001.jpg
            ├── IMG_002.jpg
            └── IMG_003.jpg
```

### ⚠️ Importante

- Solo se procesarán archivos **JPG**, **JPEG** y **PNG**
- Los **videos serán ignorados** automáticamente
- Las fotografías deben tener **metadatos EXIF** de fecha de captura
- La mayoría de las cámaras trampa guardan estos metadatos automáticamente

---

## 5. Ejecución de la Aplicación

Una vez instalado todo, puedes ejecutar la aplicación **sin necesidad de internet**.

### Paso 5.1: Abrir la Terminal

1. Abre la terminal en la carpeta del proyecto (ver Paso 3.1)

### Paso 5.2: Ejecutar el Comando

1. Escribe el siguiente comando:

   ```bash
   streamlit run app.py
   ```

2. Presiona Enter
3. Espera unos segundos

### Paso 5.3: Acceder a la Aplicación

1. La aplicación se abrirá automáticamente en tu navegador
2. Si no se abre automáticamente, abre tu navegador y ve a:

   ```
   http://localhost:8501
   ```

3. Verás la pantalla de bienvenida de la plataforma

### 🎉 ¡Listo! La aplicación está funcionando

---

## 6. Uso de la Plataforma

### Paso 6.1: Pantalla de Bienvenida

Al abrir la aplicación verás:

- Título de la plataforma
- Créditos del desarrollador
- Descripción de características
- Instrucciones de estructura de carpetas

### Paso 6.2: Seleccionar tu Proyecto

1. Busca la sección **"Seleccionar Proyecto"**
2. En el campo de texto, ingresa la ruta completa de tu carpeta de proyecto

   **Ejemplo en Windows:**

   ```
   C:\Users\TuNombre\Documents\MiProyectoCamaras
   ```

   **Cómo obtener la ruta:**
   - Abre el Explorador de Archivos
   - Navega hasta tu carpeta de proyecto
   - Haz clic en la barra de direcciones
   - Copia la ruta completa (Ctrl + C)
   - Pégala en el campo de texto de la aplicación (Ctrl + V)

3. La aplicación validará automáticamente la estructura

### Paso 6.3: Validación

Si la estructura es correcta, verás:

- ✅ Mensaje de éxito en verde
- Número de sitios encontrados

Si hay un error, verás:

- ❌ Mensaje de error en rojo
- Descripción del problema

### Paso 6.4: Procesar Datos

1. Haz clic en el botón **"🚀 Procesar Datos y Generar Excel"**
2. Espera mientras la aplicación:
   - Recorre todas las carpetas
   - Lee cada fotografía
   - Extrae los metadatos EXIF
   - Organiza los datos

### Paso 6.5: Revisar Resultados

Una vez completado el procesamiento, verás:

1. **Mensaje de éxito** con el número de fotografías procesadas
2. **Vista previa de los datos** en formato de tabla
3. **Estadísticas:**
   - Total de sitios
   - Total de cámaras
   - Total de especies/categorías
4. **Ubicación del archivo Excel** generado

### Paso 6.6: Descargar el Excel

Tienes dos opciones:

**Opción 1: Descarga directa**

- Haz clic en el botón **"⬇️ Descargar Excel"**
- El archivo se descargará a tu carpeta de Descargas

**Opción 2: Ubicación en el proyecto**

- El archivo Excel se guardó automáticamente en tu carpeta de proyecto
- Nombre del archivo: `datos_camaras_trampa_YYYYMMDD_HHMMSS.xlsx`

### Paso 6.7: Abrir el Excel

1. Abre Microsoft Excel, LibreOffice Calc, o Google Sheets
2. Abre el archivo generado
3. Verás las columnas:
   - **SITIO:** Nombre del sitio
   - **CAMARA:** Nombre de la cámara
   - **ESPECIE:** Especie o categoría observada
   - **FECHA:** Fecha de captura (YYYY-MM-DD)
   - **HORA:** Hora de captura (HH:MM:SS)

---

## 7. Análisis Avanzado con FORXIME/2

Una vez que tengas tu archivo Excel, puedes realizar análisis estadísticos avanzados.

### ¿Qué es FORXIME/2?

FORXIME/2 es una plataforma web especializada en análisis estadístico de datos de fauna silvestre que incluye:

- Análisis de diversidad (índices de Shannon y Simpson)
- Análisis de ocupación
- Comparaciones entre sitios
- Dendrogramas de similitud
- Visualizaciones interactivas

### Cómo usar FORXIME/2

1. **Asegúrate de tener conexión a internet**
2. Abre tu navegador web
3. Ve a: [https://forxime2-udpq6cmnacvdn4ai9qdj9g.streamlit.app/](https://forxime2-udpq6cmnacvdn4ai9qdj9g.streamlit.app/)
4. Sigue las instrucciones en la plataforma
5. Sube el archivo Excel generado por esta plataforma
6. Explora los análisis estadísticos disponibles

### Flujo de Trabajo Completo

```
1. Organizar fotografías
   ↓
2. Usar esta plataforma (offline)
   ↓
3. Generar Excel
   ↓
4. Importar a FORXIME/2 (online)
   ↓
5. Análisis estadístico avanzado
```

---

## 8. Preguntas Frecuentes

### ❓ ¿Necesito internet para usar la plataforma?

**No.** Solo necesitas internet para:

- Descargar Python (una sola vez)
- Descargar el proyecto (una sola vez)
- Instalar las dependencias (una sola vez)

Una vez instalado todo, la plataforma funciona **completamente offline**.

### ❓ ¿Qué pasa si mis fotos no tienen metadatos EXIF?

La plataforma solo procesará fotografías con metadatos EXIF de fecha de captura. Si tus fotos no los tienen, no aparecerán en el Excel. La mayoría de las cámaras trampa modernas guardan estos metadatos automáticamente.

### ❓ ¿Puedo procesar videos?

**No.** La plataforma está diseñada exclusivamente para fotografías. Los videos serán ignorados automáticamente.

### ❓ ¿Cuántas cámaras puedo tener por sitio?

Puedes tener **hasta 3 cámaras por sitio**, aunque técnicamente la plataforma procesará más si las tienes.

### ❓ ¿Qué categorías puedo usar?

Puedes usar cualquier nombre para las categorías, pero se recomiendan:

- Nombres de especies (Venado, Puma, Jaguar, etc.)
- **HUMANO** - para registros de personas
- **VACIO** - para fotos sin animales
- **GANADO** - para ganado doméstico

### ❓ ¿Cómo cierro la aplicación?

1. Cierra la pestaña del navegador
2. En la terminal donde ejecutaste el comando, presiona `Ctrl + C`
3. Cierra la ventana de la terminal

### ❓ ¿Puedo usar la plataforma en Mac o Linux?

**Sí.** La plataforma funciona en Windows, macOS y Linux. Los pasos de instalación son similares.

### ❓ ¿Qué hago si encuentro un error?

1. Verifica que la estructura de carpetas sea correcta
2. Asegúrate de que las fotografías tengan metadatos EXIF
3. Revisa que todas las dependencias estén instaladas
4. Consulta la sección de "Solución de Problemas" en el README.md

### ❓ ¿Puedo modificar el código?

**Sí.** El proyecto es de código abierto. Puedes modificarlo según tus necesidades.

### ❓ ¿Dónde se guardan los archivos Excel?

Los archivos Excel se guardan automáticamente en la **carpeta de tu proyecto** (la misma que seleccionaste en la aplicación).

---

## 📞 Soporte

Para preguntas, sugerencias o reportar problemas, consulta el repositorio de GitHub del proyecto.

---

## ✅ Checklist de Instalación

Usa esta lista para verificar que completaste todos los pasos:

- [ ] Python instalado y verificado
- [ ] Proyecto descargado y extraído
- [ ] Dependencias instaladas con `pip install -r requirements.txt`
- [ ] Fotografías organizadas según la estructura requerida
- [ ] Aplicación ejecutada con `streamlit run app.py`
- [ ] Proyecto procesado y Excel generado exitosamente

---

**¡Felicidades! Ahora estás listo para usar la Plataforma de Análisis de Cámaras Trampa** 🎉

---

**Desarrollado por: Biólogo Erick Elio Chavez Gurrola**  
**Versión: 1.0 | Enero 2026**
