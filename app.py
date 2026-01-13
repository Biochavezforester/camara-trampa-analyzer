import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Cámaras Trampa",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .developer {
        font-size: 1rem;
        color: #1976D2;
        text-align: center;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2E7D32;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #E8F5E9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
        margin-bottom: 1rem;
    }
    .warning-box {
        background-color: #FFF3E0;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #F57C00;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #E3F2FD;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1976D2;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

def extract_exif_datetime(image_path):
    """Extrae la fecha y hora de captura de los metadatos EXIF de una imagen."""
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        
        if exif_data is not None:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "DateTimeOriginal":
                    # Formato típico: "2024:01:15 14:30:25"
                    dt = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                    return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")
        
        return None, None
    except Exception as e:
        return None, None

def validate_folder_structure(project_path):
    """Valida que la estructura de carpetas sea correcta."""
    try:
        # Normalizar la ruta (eliminar espacios, convertir barras)
        project_path = Path(project_path.strip())
        
        if not project_path.exists():
            return False, f"❌ La carpeta no existe: `{project_path}`\n\n**Sugerencias:**\n- Verifica que el disco externo esté conectado\n- Comprueba la letra de unidad (D:, E:, F:, etc.)\n- Asegúrate de copiar la ruta completa desde el Explorador de Archivos"
        
        if not project_path.is_dir():
            return False, f"❌ La ruta no es una carpeta: `{project_path}`"
        
        # Verificar que existan subcarpetas (sitios)
        sitios = [d for d in project_path.iterdir() if d.is_dir()]
        if not sitios:
            return False, f"❌ No se encontraron carpetas de sitios en: `{project_path}`\n\n**La carpeta existe pero está vacía o no tiene la estructura correcta.**\nVerifica que contenga subcarpetas para cada sitio."
        
        return True, f"✅ Estructura válida. Se encontraron {len(sitios)} sitio(s)."
    except PermissionError:
        return False, f"❌ No tienes permisos para acceder a: `{project_path}`\n\nIntenta ejecutar la aplicación como administrador."
    except Exception as e:
        return False, f"❌ Error al validar la ruta: {str(e)}"

def process_camera_trap_data(project_path, progress_bar=None, status_text=None):
    """Procesa todas las imágenes en la estructura de carpetas y genera el DataFrame."""
    project_path = Path(project_path)
    data = []
    
    # Extensiones de imagen permitidas
    image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
    
    # Contar total de archivos primero para la barra de progreso
    total_files = 0
    all_files = []
    
    for sitio_dir in project_path.iterdir():
        if not sitio_dir.is_dir():
            continue
        for camara_dir in sitio_dir.iterdir():
            if not camara_dir.is_dir():
                continue
            for especie_dir in camara_dir.iterdir():
                if not especie_dir.is_dir():
                    continue
                for foto_path in especie_dir.iterdir():
                    if foto_path.is_file() and foto_path.suffix in image_extensions:
                        all_files.append((foto_path, sitio_dir.name, camara_dir.name, especie_dir.name))
                        total_files += 1
    
    if status_text:
        status_text.text(f"📊 Total de fotos encontradas: {total_files:,}")
    
    # Procesar archivos con barra de progreso
    processed = 0
    errors = 0
    
    for foto_path, sitio_nombre, camara_nombre, especie_nombre in all_files:
        try:
            fecha, hora = extract_exif_datetime(foto_path)
            
            if fecha and hora:
                data.append({
                    'SITIO': sitio_nombre,
                    'CAMARA': camara_nombre,
                    'ESPECIE': especie_nombre,
                    'FECHA': fecha,
                    'HORA': hora
                })
        except Exception as e:
            errors += 1
            # Continuar con la siguiente foto si hay error
            pass
        
        processed += 1
        
        # Actualizar progreso cada 100 fotos para no saturar la UI
        if progress_bar and processed % 100 == 0:
            progress_bar.progress(processed / total_files)
            if status_text:
                status_text.text(f"Procesando: {processed:,} / {total_files:,} fotos ({(processed/total_files)*100:.1f}%)")
    
    # Actualizar al 100%
    if progress_bar:
        progress_bar.progress(1.0)
    if status_text:
        status_text.text(f"✅ Completado: {processed:,} fotos procesadas, {len(data):,} con metadatos válidos")
        if errors > 0:
            status_text.text(f"⚠️ {errors} fotos con errores fueron omitidas")
    
    return pd.DataFrame(data)

# Título principal
st.markdown('<p class="main-title">📷 Plataforma Profesional de Análisis de Datos de Cámaras Trampa</p>', unsafe_allow_html=True)
st.markdown('<p class="developer">Desarrollado por: Biólogo Erick Elio Chavez Gurrola</p>', unsafe_allow_html=True)

# Sección de bienvenida
st.markdown('<div class="info-box">', unsafe_allow_html=True)
st.markdown("""
### 👋 ¡Bienvenido!

Esta plataforma está diseñada para facilitar el análisis de datos de cámaras trampa, extrayendo automáticamente 
la información de fecha y hora de captura de las fotografías y organizándola en un formato estructurado para su análisis.

**Características principales:**
- ✅ Extracción automática de metadatos EXIF (fecha de captura)
- ✅ Generación de reportes en formato Excel
- ✅ Funcionamiento 100% offline (sin necesidad de internet)
- ✅ Procesamiento exclusivo de fotografías (videos ignorados)
""")
st.markdown('</div>', unsafe_allow_html=True)

# Estructura de carpetas requerida
st.markdown('<p class="section-header">📁 Estructura de Carpetas Requerida</p>', unsafe_allow_html=True)
st.markdown('<div class="warning-box">', unsafe_allow_html=True)
st.markdown("""
Para que la plataforma funcione correctamente, tus carpetas deben seguir esta estructura jerárquica:

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

**Importante:**
- Cada sitio puede tener hasta **3 cámaras**
- Las categorías de observación pueden ser: **especies**, **HUMANO**, **VACIO**, **GANADO**, etc.
- Solo se procesarán archivos de imagen (JPG, JPEG, PNG)
- Los videos serán ignorados automáticamente
""")
st.markdown('</div>', unsafe_allow_html=True)

# Selector de carpeta
st.markdown('<p class="section-header">🔍 Seleccionar Proyecto</p>', unsafe_allow_html=True)

# Input para la ruta del proyecto
project_path = st.text_input(
    "Ingresa la ruta completa de la carpeta del proyecto:",
    placeholder="Ejemplo: C:\\Users\\Usuario\\Documents\\MiProyectoCamaras",
    help="Pega aquí la ruta completa de la carpeta que contiene tus sitios (sin comillas)"
)

# Limpiar comillas si el usuario las pegó accidentalmente
if project_path:
    project_path = project_path.strip().strip('"').strip("'")

if project_path:
    # Panel de depuración (temporal)
    with st.expander("🔧 Información de Depuración", expanded=False):
        st.code(f"Ruta ingresada: {repr(project_path)}")
        st.code(f"Tipo: {type(project_path)}")
        st.code(f"Longitud: {len(project_path)}")
        
        import os
        test_path = Path(project_path.strip())
        st.code(f"Path object: {test_path}")
        st.code(f"Path.exists(): {test_path.exists()}")
        st.code(f"Path.is_dir(): {test_path.is_dir()}")
        st.code(f"os.path.exists(): {os.path.exists(str(test_path))}")
        
        # Intentar listar D:\
        try:
            d_contents = list(Path("D:\\").iterdir())
            st.write(f"Contenido de D:\\ ({len(d_contents)} elementos):")
            for item in d_contents[:10]:  # Mostrar solo los primeros 10
                st.write(f"  - {item.name}")
        except Exception as e:
            st.error(f"Error al listar D:\\: {e}")
    
    # Validar estructura
    is_valid, message = validate_folder_structure(project_path)
    
    if is_valid:
        st.success(f"✅ {message}")
        
        # Botón para procesar
        if st.button("🚀 Procesar Datos y Generar Excel", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔍 Escaneando carpetas y contando archivos...")
            
            df = process_camera_trap_data(project_path, progress_bar, status_text)
            
            if len(df) > 0:
                st.markdown('<div class="success-box">', unsafe_allow_html=True)
                st.markdown(f"### ✅ Procesamiento Completado")
                st.markdown(f"Se procesaron **{len(df)} fotografías** exitosamente.")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Mostrar vista previa
                st.markdown("### 📊 Vista Previa de los Datos")
                st.dataframe(df, use_container_width=True)
                
                # Estadísticas
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Sitios", df['SITIO'].nunique())
                with col2:
                    st.metric("Total de Cámaras", df['CAMARA'].nunique())
                with col3:
                    st.metric("Total de Especies/Categorías", df['ESPECIE'].nunique())
                
                # Generar archivo Excel
                output_filename = f"datos_camaras_trampa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                output_path = Path(project_path) / output_filename
                
                df.to_excel(output_path, index=False, engine='openpyxl')
                
                st.success(f"📁 Archivo Excel generado: `{output_filename}`")
                st.info(f"📍 Ubicación: `{output_path}`")
                
                # Botón de descarga
                with open(output_path, 'rb') as f:
                    st.download_button(
                        label="⬇️ Descargar Excel",
                        data=f,
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.error("❌ No se encontraron imágenes con metadatos EXIF válidos en la estructura de carpetas.")
                st.warning("Verifica que las imágenes tengan metadatos de fecha de captura y que la estructura de carpetas sea correcta.")
    else:
        st.error(f"❌ {message}")
        st.info("Por favor, verifica que la ruta sea correcta y que la estructura de carpetas siga el formato requerido.")

# Sección de análisis estadístico avanzado
st.markdown("---")
st.markdown('<p class="section-header">📈 Análisis Estadístico Avanzado</p>', unsafe_allow_html=True)
st.markdown('<div class="success-box">', unsafe_allow_html=True)
st.markdown("""
### 🔗 Complemento FORXIME/2

Esta plataforma es un **complemento perfecto** para **FORXIME/2**, una herramienta especializada en análisis 
estadístico avanzado de datos de fauna silvestre.

Una vez que hayas generado tu archivo Excel con esta plataforma, puedes importarlo en FORXIME/2 para realizar:
- 📊 Análisis de diversidad (Shannon, Simpson)
- 🗺️ Análisis de ocupación
- 📉 Comparaciones entre sitios
- 🌳 Dendrogramas de similitud
- Y mucho más...

**Accede a FORXIME/2 aquí:**  
🔗 [https://forxime2-udpq6cmnacvdn4ai9qdj9g.streamlit.app/](https://forxime2-udpq6cmnacvdn4ai9qdj9g.streamlit.app/)

*Nota: FORXIME/2 requiere conexión a internet. Esta plataforma funciona completamente offline.*
""")
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>Plataforma de Análisis de Cámaras Trampa v1.0 | 2026</p>
    <p>Desarrollado por: Biólogo Erick Elio Chavez Gurrola</p>
</div>
""", unsafe_allow_html=True)
