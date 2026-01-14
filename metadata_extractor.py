"""
Extractor avanzado de metadatos EXIF y gestor de coordenadas UTM.
"""

from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Dict
import streamlit as st
from database_manager import get_database
from config_manager import get_config


class AdvancedMetadataExtractor:
    """Extractor de metadatos EXIF avanzado."""
    
    @staticmethod
    def extract_datetime(image_path: Path) -> Tuple[Optional[str], Optional[str]]:
        """
        Extrae fecha y hora de captura de EXIF.
        
        Returns:
            Tupla (fecha, hora) en formato (YYYY-MM-DD, HH:MM:SS)
        """
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "DateTimeOriginal":
                        dt = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
                        return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M:%S")
            
            return None, None
        except Exception:
            return None, None
    
    @staticmethod
    def extract_camera_model(image_path: Path) -> Optional[str]:
        """Extrae modelo de cámara de EXIF."""
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            
            if exif_data:
                make = None
                model = None
                
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == "Make":
                        make = value
                    elif tag == "Model":
                        model = value
                
                if make and model:
                    return f"{make} {model}"
                elif model:
                    return model
            
            return None
        except Exception:
            return None
    
    @staticmethod
    def extract_temperature(image_path: Path) -> Optional[float]:
        """Extrae temperatura de EXIF si está disponible."""
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            
            if exif_data:
                # Algunos modelos de cámaras trampa guardan temperatura
                # en tags personalizados (varía por fabricante)
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if "Temperature" in str(tag) or "Temp" in str(tag):
                        try:
                            return float(value)
                        except:
                            pass
            
            return None
        except Exception:
            return None
    
    @staticmethod
    def extract_all_metadata(image_path: Path) -> Dict:
        """Extrae todos los metadatos relevantes."""
        fecha, hora = AdvancedMetadataExtractor.extract_datetime(image_path)
        camera = AdvancedMetadataExtractor.extract_camera_model(image_path)
        temp = AdvancedMetadataExtractor.extract_temperature(image_path)
        
        return {
            'fecha': fecha,
            'hora': hora,
            'camera_model': camera,
            'temperature': temp,
            'has_exif': fecha is not None
        }


class UTMCoordinateManager:
    """Gestor de coordenadas UTM para cámaras."""
    
    VALID_UTM_ZONES_MEXICO = [
        "11Q", "11R",
        "12Q", "12R",
        "13Q", "13R",
        "14Q", "14R",
        "15Q", "15P",
        "16Q", "16P"
    ]
    
    @staticmethod
    def validate_utm_zone(zone: str) -> bool:
        """Valida que la zona UTM sea válida para México."""
        return zone.upper() in UTMCoordinateManager.VALID_UTM_ZONES_MEXICO
    
    @staticmethod
    def validate_utm_coordinates(zone: str, easting: float, northing: float) -> Tuple[bool, str]:
        """
        Valida coordenadas UTM.
        
        Returns:
            Tupla (válido, mensaje)
        """
        # Validar zona
        if not UTMCoordinateManager.validate_utm_zone(zone):
            return False, f"Zona UTM '{zone}' no válida para México. Zonas válidas: {', '.join(UTMCoordinateManager.VALID_UTM_ZONES_MEXICO)}"
        
        # Validar rango de Este (Easting)
        if not (100000 <= easting <= 900000):
            return False, f"Este (Easting) fuera de rango. Debe estar entre 100,000 y 900,000 m. Valor: {easting:,.0f}"
        
        # Validar rango de Norte (Northing) para México
        if not (900000 <= northing <= 3700000):
            return False, f"Norte (Northing) fuera de rango. Debe estar entre 900,000 y 3,700,000 m. Valor: {northing:,.0f}"
        
        return True, "Coordenadas válidas"
    
    @staticmethod
    def request_camera_coordinates_ui(project_id: int, site_name: str, camera_name: str) -> Optional[Dict]:
        """
        Muestra interfaz de Streamlit para ingresar coordenadas UTM.
        
        Returns:
            Dict con coordenadas o None si se cancela
        """
        db = get_database()
        config = get_config()
        
        # Verificar si ya existen coordenadas guardadas
        existing = db.get_camera_coordinates(project_id, site_name, camera_name)
        
        st.subheader(f"📍 Coordenadas UTM: {site_name} > {camera_name}")
        
        if existing:
            st.info(f"✓ Coordenadas guardadas previamente: {existing['utm_zone']} {existing['easting']:,.0f}E {existing['northing']:,.0f}N")
            
            if st.checkbox("Editar coordenadas existentes", key=f"edit_{site_name}_{camera_name}"):
                return UTMCoordinateManager._show_coordinate_form(
                    project_id, site_name, camera_name,
                    default_zone=existing['utm_zone'],
                    default_easting=existing['easting'],
                    default_northing=existing['northing'],
                    default_datum=existing['datum']
                )
            else:
                return existing
        else:
            st.warning("⚠️ No hay coordenadas guardadas para esta cámara")
            return UTMCoordinateManager._show_coordinate_form(project_id, site_name, camera_name)
    
    @staticmethod
    def _show_coordinate_form(project_id: int, site_name: str, camera_name: str,
                              default_zone: str = "13Q", default_easting: float = 0,
                              default_northing: float = 0, default_datum: str = "WGS84") -> Optional[Dict]:
        """Muestra formulario de ingreso de coordenadas."""
        config = get_config()
        
        col1, col2 = st.columns(2)
        
        with col1:
            utm_zone = st.selectbox(
                "Zona UTM",
                options=UTMCoordinateManager.VALID_UTM_ZONES_MEXICO,
                index=UTMCoordinateManager.VALID_UTM_ZONES_MEXICO.index(default_zone) if default_zone in UTMCoordinateManager.VALID_UTM_ZONES_MEXICO else 4,
                key=f"zone_{site_name}_{camera_name}",
                help="Zona UTM para México. Ejemplo: 13Q para Durango/Jalisco"
            )
            
            easting = st.number_input(
                "Este (Easting) en metros",
                min_value=100000.0,
                max_value=900000.0,
                value=float(default_easting) if default_easting > 0 else 500000.0,
                step=1.0,
                key=f"east_{site_name}_{camera_name}",
                help="Coordenada Este en metros. Ejemplo: 462728"
            )
        
        with col2:
            northing = st.number_input(
                "Norte (Northing) en metros",
                min_value=900000.0,
                max_value=3700000.0,
                value=float(default_northing) if default_northing > 0 else 2000000.0,
                step=1.0,
                key=f"north_{site_name}_{camera_name}",
                help="Coordenada Norte en metros. Ejemplo: 2630653"
            )
            
            datum = st.selectbox(
                "Datum",
                options=["WGS84", "NAD27", "NAD83"],
                index=0,
                key=f"datum_{site_name}_{camera_name}",
                help="Sistema de referencia geodésico (WGS84 recomendado)"
            )
        
        # Validar coordenadas
        valid, message = UTMCoordinateManager.validate_utm_coordinates(utm_zone, easting, northing)
        
        if valid:
            st.success(f"✓ {message}")
            st.info(f"📍 Coordenadas: **{utm_zone} {easting:,.0f}E {northing:,.0f}N** ({datum})")
            
            if st.button(f"💾 Guardar coordenadas", key=f"save_{site_name}_{camera_name}"):
                db = get_database()
                db.save_camera_coordinates(
                    project_id, site_name, camera_name,
                    utm_zone, easting, northing, datum
                )
                st.success("✓ Coordenadas guardadas exitosamente")
                
                return {
                    'utm_zone': utm_zone,
                    'easting': easting,
                    'northing': northing,
                    'datum': datum
                }
        else:
            st.error(f"❌ {message}")
        
        return None
    
    @staticmethod
    def get_all_coordinates_for_export(project_id: int) -> list:
        """Obtiene todas las coordenadas formateadas para exportación."""
        db = get_database()
        coords = db.get_all_camera_coordinates(project_id)
        
        export_data = []
        for coord in coords:
            export_data.append({
                'SITIO': coord['site_name'],
                'CAMARA': coord['camera_name'],
                'ZONA_UTM': coord['utm_zone'],
                'ESTE': coord['easting'],
                'NORTE': coord['northing'],
                'DATUM': coord['datum']
            })
        
        return export_data
