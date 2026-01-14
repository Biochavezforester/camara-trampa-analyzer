"""
Plataforma Profesional de Análisis de Datos de Cámaras Trampa con IA
Versión 2.0 - Con clasificación automática y análisis avanzado

Desarrollado por: Biólogo Erick Elio Chavez Gurrola
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import time

# Importar módulos propios
from logger import get_logger
from config_manager import get_config
from database_manager import get_database
from metadata_extractor import AdvancedMetadataExtractor, UTMCoordinateManager
from analysis_engine import (
    TrapEffortCalculator, IndependentEventDetector,
    TemporalAnalyzer, VisitFrequencyCalculator, GapDetector
)
from data_validator import QualityReporter
from report_generator import export_dual_excel
from ai_classifier import CUDADetector, get_manual_assistant
from utils import clean_species_name, standardize_category, get_common_species_mexico

# Inicializar
logger = get_logger()
config = get_config()
db = get_database()

# Configuración de página
st.set_page_config(
    page_title="Plataforma de Cámaras Trampa con IA",
    page_icon="📷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
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

# Inicializar estado de sesión
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'project_id' not in st.session_state:
    st.session_state.project_id = None
if 'gpu_info' not in st.session_state:
    # Detectar GPU al inicio
    gpu_available, gpu_name, cuda_version = CUDADetector.detect_cuda()
    st.session_state.gpu_info = {
        'available': gpu_available,
        'name': gpu_name,
        'cuda_version': cuda_version
    }

# Título principal
st.markdown('<p class="main-title">📷 Plataforma Profesional de Análisis de Datos de Cámaras Trampa</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Con Clasificación Automática mediante IA y Análisis Avanzado</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #1976D2; font-style: italic;">Desarrollado por: Biólogo Erick Elio Chavez Gurrola</p>', unsafe_allow_html=True)

# Barra lateral con información
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Mostrar estado de GPU
    st.subheader("🎮 Estado del Sistema")
    if st.session_state.gpu_info['available']:
        st.success(f"✓ GPU Detectada: {st.session_state.gpu_info['name']}")
        st.info(f"CUDA: {st.session_state.gpu_info['cuda_version']}")
        st.caption("Clasificación automática disponible")
    else:
        st.warning("⚠️ GPU no detectada")
        st.caption("Modo asistido manual activado")
    
    st.divider()
    
    # Configuraciones
    st.subheader("📋 Parámetros")
    
    independent_event_minutes = st.number_input(
        "Minutos entre eventos independientes",
        min_value=5,
        max_value=120,
        value=config.get_independent_event_minutes(),
        step=5,
        help="Tiempo mínimo entre fotos para considerarlas eventos separados"
    )
    
    if independent_event_minutes != config.get_independent_event_minutes():
        config.set_independent_event_minutes(independent_event_minutes)
    
    st.divider()
    
    # Enlace a FORXIME/2
    st.subheader("🔗 FORXIME/2")
    st.markdown("""
    Esta plataforma genera Excel compatible con **FORXIME/2** para análisis estadístico avanzado.
    
    [Abrir FORXIME/2](https://forxime2-udpq6cmnacvdn4ai9qdj9g.streamlit.app/)
    """)

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs([
    "📁 Procesamiento",
    "📊 Análisis y Reportes",
    "📍 Coordenadas UTM",
    "ℹ️ Información"
])

# TAB 1: PROCESAMIENTO
with tab1:
    st.header("📁 Procesamiento de Datos")
    
    # Información de estructura
    with st.expander("📋 Estructura de Carpetas Requerida", expanded=False):
        st.markdown("""
        ```
        PROYECTO/
        ├── SITIO_1/
        │   ├── CAMARA_1/
        │   │   ├── ESPECIE_A/
        │   │   │   └── fotos.jpg
        │   │   └── VACIO/
        │   │       └── fotos.jpg
        │   └── CAMARA_2/
        │       └── ...
        └── SITIO_2/
            └── ...
        ```
        
        **Reglas:**
        - Máximo 10 cámaras por sitio
        - Solo imágenes: JPG, JPEG, PNG
        - Videos se ignoran automáticamente
        """)
    
    # Selector de proyecto
    project_path = st.text_input(
        "📂 Ruta del Proyecto",
        placeholder="C:\\Users\\Usuario\\Documents\\MiProyecto",
        help="Ruta completa a la carpeta del proyecto"
    )
    
    if project_path:
        project_path = project_path.strip().strip('"').strip("'")
        project_path_obj = Path(project_path)
        
        if not project_path_obj.exists():
            st.error(f"❌ La carpeta no existe: {project_path}")
        elif not project_path_obj.is_dir():
            st.error(f"❌ La ruta no es una carpeta válida")
        else:
            st.success(f"✓ Carpeta válida: {project_path_obj.name}")
            
            # Botón de procesamiento
            if st.button("🚀 Procesar Proyecto", type="primary", use_container_width=True):
                process_project(project_path_obj)

# TAB 2: ANÁLISIS Y REPORTES
with tab2:
    st.header("📊 Análisis y Reportes")
    
    if st.session_state.processed_data is None:
        st.info("👈 Procesa un proyecto primero en la pestaña 'Procesamiento'")
    else:
        show_analysis_and_reports()

# TAB 3: COORDENADAS UTM
with tab3:
    st.header("📍 Coordenadas UTM por Cámara")
    
    if st.session_state.processed_data is None or st.session_state.project_id is None:
        st.info("👈 Procesa un proyecto primero")
    else:
        show_utm_coordinates_input()

# TAB 4: INFORMACIÓN
with tab4:
    st.header("ℹ️ Información de la Plataforma")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✨ Características")
        st.markdown("""
        - ✅ Extracción automática de metadatos EXIF
        - ✅ Clasificación con IA (si GPU disponible)
        - ✅ Cálculo de trampas-día
        - ✅ Detección de eventos independientes
        - ✅ Análisis temporal (diurno/nocturno)
        - ✅ Coordenadas UTM con validación
        - ✅ Exportación dual de Excel
        - ✅ Compatible con FORXIME/2
        - ✅ 100% offline (después de setup)
        """)
    
    with col2:
        st.subheader("📄 Formatos de Exportación")
        st.markdown("""
        **Excel Básico (FORXIME/2):**
        - SITIO, CAMARA, ESPECIE, FECHA, HORA
        - Listo para importar en FORXIME/2
        
        **Excel Completo:**
        - Todos los datos + análisis
        - Coordenadas UTM
        - Esfuerzo de muestreo
        - Eventos independientes
        - Análisis temporal
        - Resumen ejecutivo
        """)
    
    st.divider()
    
    st.subheader("🔧 Requisitos del Sistema")
    st.markdown("""
    **Mínimos:**
    - Python 3.8+
    - 4 GB RAM
    - 2 GB espacio en disco
    
    **Recomendados (para IA):**
    - GPU NVIDIA RTX 3060+ (6GB VRAM)
    - CUDA 11.8+
    - 16 GB RAM
    - 10 GB espacio (modelos de IA)
    """)


# FUNCIONES AUXILIARES

def process_project(project_path: Path):
    """Procesa un proyecto completo."""
    
    # Crear o obtener proyecto en BD
    project_name = project_path.name
    project_id = db.create_project(project_name, str(project_path))
    st.session_state.project_id = project_id
    
    logger.info(f"Procesando proyecto: {project_name}")
    
    # Barra de progreso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("🔍 Escaneando estructura de carpetas...")
    
    # Escanear archivos
    image_extensions = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'}
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
                        all_files.append({
                            'path': foto_path,
                            'sitio': sitio_dir.name,
                            'camara': camara_dir.name,
                            'especie': especie_dir.name
                        })
    
    total_files = len(all_files)
    
    if total_files == 0:
        st.error("❌ No se encontraron imágenes en la estructura de carpetas")
        return
    
    status_text.text(f"📊 Encontradas {total_files:,} fotos. Procesando...")
    
    # Procesar fotos
    data = []
    start_time = time.time()
    
    for i, file_info in enumerate(all_files):
        # Extraer metadatos
        metadata = AdvancedMetadataExtractor.extract_all_metadata(file_info['path'])
        
        if metadata['fecha'] and metadata['hora']:
            # Limpiar y estandarizar nombres
            especie_clean = standardize_category(file_info['especie'])
            
            data.append({
                'SITIO': file_info['sitio'],
                'CAMARA': file_info['camara'],
                'ESPECIE': especie_clean,
                'FECHA': metadata['fecha'],
                'HORA': metadata['hora'],
                'CAMERA_MODEL': metadata['camera_model'],
                'TEMPERATURE': metadata['temperature']
            })
        
        # Actualizar progreso
        if i % 50 == 0:
            progress = (i + 1) / total_files
            progress_bar.progress(progress)
            status_text.text(f"⚡ Procesando: {i+1:,} / {total_files:,} ({progress*100:.1f}%)")
    
    progress_bar.progress(1.0)
    processing_time = time.time() - start_time
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    if len(df) == 0:
        st.error("❌ No se encontraron fotos con metadatos EXIF válidos")
        return
    
    status_text.text(f"✅ Procesadas {len(df):,} fotos en {processing_time:.1f} segundos")
    
    # Guardar en sesión
    st.session_state.processed_data = df
    
    # Actualizar estadísticas del proyecto
    db.update_project_stats(project_id, len(df), df['ESPECIE'].nunique())
    db.add_processing_record(project_id, len(df), processing_time=processing_time)
    
    # Mostrar resultados
    st.success(f"✅ Proyecto procesado exitosamente")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Fotos", f"{len(df):,}")
    with col2:
        st.metric("Sitios", df['SITIO'].nunique())
    with col3:
        st.metric("Especies", df['ESPECIE'].nunique())
    
    # Vista previa
    st.subheader("📋 Vista Previa de Datos")
    st.dataframe(df.head(20), use_container_width=True)
    
    # Reporte de calidad
    with st.expander("📊 Reporte de Calidad de Datos"):
        quality_report = QualityReporter.generate_quality_report(df)
        report_text = QualityReporter.format_quality_report_text(quality_report)
        st.text(report_text)


def show_analysis_and_reports():
    """Muestra análisis y genera reportes."""
    df = st.session_state.processed_data
    
    st.subheader("📈 Análisis Estadístico")
    
    # Calcular análisis
    with st.spinner("Calculando análisis..."):
        # Esfuerzo de muestreo
        effort_df = TrapEffortCalculator.calculate_trap_days(df)
        
        # Eventos independientes
        event_detector = IndependentEventDetector(
            time_threshold_minutes=config.get_independent_event_minutes()
        )
        events_df = event_detector.detect_independent_events(df)
        rai_df = event_detector.calculate_rai(events_df, effort_df)
        
        # Análisis temporal
        temporal_df = TemporalAnalyzer.analyze_temporal_patterns(df)
    
    # Mostrar resultados en tabs
    analysis_tab1, analysis_tab2, analysis_tab3 = st.tabs([
        "Esfuerzo de Muestreo",
        "Eventos Independientes",
        "Patrones Temporales"
    ])
    
    with analysis_tab1:
        st.dataframe(effort_df, use_container_width=True)
        st.metric("Esfuerzo Total", f"{effort_df['TRAMPAS_DIA'].sum()} trampas-día")
    
    with analysis_tab2:
        st.dataframe(events_df, use_container_width=True)
        st.dataframe(rai_df, use_container_width=True)
    
    with analysis_tab3:
        st.dataframe(temporal_df, use_container_width=True)
    
    # Botón de exportación
    st.divider()
    st.subheader("📥 Exportar Resultados")
    
    if st.button("💾 Generar Excel (Básico + Completo)", type="primary", use_container_width=True):
        generate_excel_exports(df, effort_df, events_df, temporal_df)


def show_utm_coordinates_input():
    """Muestra interfaz para ingresar coordenadas UTM."""
    df = st.session_state.processed_data
    project_id = st.session_state.project_id
    
    st.info("Ingresa las coordenadas UTM para cada cámara detectada en el proyecto")
    
    # Obtener cámaras únicas
    cameras = df.groupby(['SITIO', 'CAMARA']).size().reset_index()[['SITIO', 'CAMARA']]
    
    for idx, row in cameras.iterrows():
        with st.expander(f"📍 {row['SITIO']} > {row['CAMARA']}", expanded=False):
            UTMCoordinateManager.request_camera_coordinates_ui(
                project_id, row['SITIO'], row['CAMARA']
            )


def generate_excel_exports(df, effort_df, events_df, temporal_df):
    """Genera archivos Excel de exportación."""
    project_id = st.session_state.project_id
    project = db.get_project(st.session_state.processed_data.iloc[0]['SITIO'])
    
    # Obtener coordenadas
    coordinates_data = UTMCoordinateManager.get_all_coordinates_for_export(project_id)
    coordinates_df = pd.DataFrame(coordinates_data) if coordinates_data else None
    
    # Generar Excel
    with st.spinner("Generando archivos Excel..."):
        project_path = Path(st.session_state.processed_data.iloc[0]['SITIO']).parent.parent
        
        basic_path, complete_path = export_dual_excel(
            df, project_path, "proyecto",
            effort_df, events_df, temporal_df, coordinates_df
        )
    
    st.success("✅ Archivos Excel generados exitosamente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"📄 **Excel Básico (FORXIME/2)**\n\n{basic_path.name}")
        with open(basic_path, 'rb') as f:
            st.download_button(
                "⬇️ Descargar Básico",
                f,
                file_name=basic_path.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col2:
        st.info(f"📄 **Excel Completo**\n\n{complete_path.name}")
        with open(complete_path, 'rb') as f:
            st.download_button(
                "⬇️ Descargar Completo",
                f,
                file_name=complete_path.name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>Plataforma de Análisis de Cámaras Trampa v2.0 | 2026</p>
    <p>Desarrollado por: Biólogo Erick Elio Chavez Gurrola</p>
    <p>Compatible con <a href="https://forxime2-udpq6cmnacvdn4ai9qdj9g.streamlit.app/" target="_blank">FORXIME/2</a></p>
</div>
""", unsafe_allow_html=True)
