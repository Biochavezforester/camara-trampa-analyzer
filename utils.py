"""
Utilidades y funciones auxiliares para la plataforma de cámaras trampa.
"""

import re
from datetime import datetime, timedelta
from typing import Optional, Tuple, List
from pathlib import Path


def clean_species_name(name: str) -> str:
    """
    Limpia y estandariza nombres de especies.
    
    Args:
        name: Nombre de especie a limpiar
        
    Returns:
        Nombre limpio y estandarizado
    """
    if not name:
        return ""
    
    # Convertir a mayúsculas
    name = name.upper().strip()
    
    # Eliminar caracteres especiales excepto espacios y guiones
    name = re.sub(r'[^A-ZÁÉÍÓÚÑ\s\-]', '', name)
    
    # Eliminar espacios múltiples
    name = re.sub(r'\s+', ' ', name)
    
    return name


def standardize_category(category: str) -> str:
    """
    Estandariza categorías comunes (VACIO, HUMANO, etc).
    
    Args:
        category: Categoría a estandarizar
        
    Returns:
        Categoría estandarizada
    """
    category = clean_species_name(category)
    
    # Mapeo de variaciones comunes
    mappings = {
        'VACIA': 'VACIO',
        'VACIAS': 'VACIO',
        'EMPTY': 'VACIO',
        'BLANK': 'VACIO',
        'SIN ANIMAL': 'VACIO',
        'PERSONA': 'HUMANO',
        'PERSONAS': 'HUMANO',
        'HUMAN': 'HUMANO',
        'GENTE': 'HUMANO',
        'GANADO BOVINO': 'GANADO',
        'VACA': 'GANADO',
        'VACAS': 'GANADO',
        'CATTLE': 'GANADO',
        'PERRO': 'DOMESTICO',
        'GATO': 'DOMESTICO',
        'DOG': 'DOMESTICO',
        'CAT': 'DOMESTICO',
    }
    
    return mappings.get(category, category)


def format_time_24h(time_str: str) -> str:
    """
    Formatea hora a formato 24h legible.
    
    Args:
        time_str: Hora en formato HH:MM:SS
        
    Returns:
        Hora formateada
    """
    try:
        dt = datetime.strptime(time_str, "%H:%M:%S")
        return dt.strftime("%H:%M:%S")
    except:
        return time_str


def get_time_period(time_str: str) -> str:
    """
    Clasifica hora en período del día.
    
    Args:
        time_str: Hora en formato HH:MM:SS
        
    Returns:
        Período: DIURNO, NOCTURNO, CREPUSCULAR_MATUTINO, CREPUSCULAR_VESPERTINO
    """
    try:
        hour = int(time_str.split(':')[0])
        
        if 6 <= hour < 8:
            return "CREPUSCULAR_MATUTINO"
        elif 8 <= hour < 18:
            return "DIURNO"
        elif 18 <= hour < 20:
            return "CREPUSCULAR_VESPERTINO"
        else:
            return "NOCTURNO"
    except:
        return "DESCONOCIDO"


def calculate_days_between(date1: str, date2: str) -> int:
    """
    Calcula días entre dos fechas.
    
    Args:
        date1: Fecha en formato YYYY-MM-DD
        date2: Fecha en formato YYYY-MM-DD
        
    Returns:
        Número de días
    """
    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")
        return abs((d2 - d1).days)
    except:
        return 0


def validate_date_range(date_str: str, min_year: int = 2010, max_year: int = 2030) -> bool:
    """
    Valida que una fecha esté en un rango razonable.
    
    Args:
        date_str: Fecha en formato YYYY-MM-DD
        min_year: Año mínimo válido
        max_year: Año máximo válido
        
    Returns:
        True si la fecha es válida
    """
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return min_year <= date.year <= max_year
    except:
        return False


def parse_gps_coordinate(coord_tuple: Tuple) -> Optional[float]:
    """
    Convierte coordenadas GPS de EXIF a decimal.
    
    Args:
        coord_tuple: Tupla de coordenadas EXIF ((degrees, 1), (minutes, 1), (seconds, 100))
        
    Returns:
        Coordenada en formato decimal o None
    """
    try:
        degrees = coord_tuple[0][0] / coord_tuple[0][1]
        minutes = coord_tuple[1][0] / coord_tuple[1][1]
        seconds = coord_tuple[2][0] / coord_tuple[2][1]
        
        return degrees + (minutes / 60.0) + (seconds / 3600.0)
    except:
        return None


def format_file_size(size_bytes: int) -> str:
    """
    Formatea tamaño de archivo a formato legible.
    
    Args:
        size_bytes: Tamaño en bytes
        
    Returns:
        Tamaño formateado (ej: "1.5 GB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def get_common_species_mexico() -> List[str]:
    """
    Retorna lista de especies comunes en México para autocompletado.
    
    Returns:
        Lista de nombres de especies
    """
    return [
        # Mamíferos grandes
        "VENADO COLA BLANCA",
        "PECARI DE COLLAR",
        "JAGUAR",
        "PUMA",
        "OCELOTE",
        "TIGRILLO",
        
        # Carnívoros medianos
        "COYOTE",
        "ZORRO GRIS",
        "MAPACHE",
        "COATI",
        "TEJON",
        "CACOMIXTLE",
        
        # Mamíferos pequeños
        "ARMADILLO",
        "CONEJO",
        "LIEBRE",
        "ARDILLA",
        "TLACUACHE",
        "ZORRILLO",
        
        # Aves
        "PAVO OCELADO",
        "HOCOFAISAN",
        "CHACHALACA",
        "CODORNIZ",
        "PALOMA",
        
        # Categorías especiales
        "HUMANO",
        "VACIO",
        "GANADO",
        "DOMESTICO",
    ]


def suggest_species_correction(species: str) -> Optional[str]:
    """
    Sugiere corrección para nombres de especies mal escritos.
    
    Args:
        species: Nombre de especie posiblemente mal escrito
        
    Returns:
        Sugerencia de corrección o None
    """
    species = clean_species_name(species)
    common_species = get_common_species_mexico()
    
    # Mapeo de errores comunes
    corrections = {
        'BENADO': 'VENADO COLA BLANCA',
        'VENADO': 'VENADO COLA BLANCA',
        'PECARI': 'PECARI DE COLLAR',
        'JABALI': 'PECARI DE COLLAR',
        'TIGRE': 'JAGUAR',
        'LEON': 'PUMA',
        'LEON DE MONTAÑA': 'PUMA',
        'GATO MONTES': 'OCELOTE',
        'MAPACHIN': 'MAPACHE',
        'TEJON DE COLA BLANCA': 'COATI',
        'ZARIGUEYA': 'TLACUACHE',
        'VACIO': 'VACIO',
        'VACIA': 'VACIO',
        'PERSONA': 'HUMANO',
    }
    
    return corrections.get(species)


def create_folder_structure_template(base_path: Path) -> None:
    """
    Crea estructura de carpetas de ejemplo para proyecto de cámaras trampa.
    
    Args:
        base_path: Ruta base donde crear la estructura
    """
    # Estructura de ejemplo
    structure = {
        'SITIO_1': {
            'CAMARA_1': ['VENADO COLA BLANCA', 'PECARI DE COLLAR', 'VACIO'],
            'CAMARA_2': ['JAGUAR', 'PUMA', 'HUMANO'],
            'CAMARA_3': ['COYOTE', 'MAPACHE', 'VACIO'],
        },
        'SITIO_2': {
            'CAMARA_1': ['OCELOTE', 'ARMADILLO', 'VACIO'],
            'CAMARA_2': ['TEJON', 'COATI', 'GANADO'],
        }
    }
    
    for sitio, camaras in structure.items():
        for camara, especies in camaras.items():
            for especie in especies:
                folder = base_path / sitio / camara / especie
                folder.mkdir(parents=True, exist_ok=True)
                
                # Crear archivo README en cada carpeta de especie
                readme = folder / 'README.txt'
                readme.write_text(
                    f"Coloca aquí las fotografías de {especie}\n"
                    f"capturadas en {camara} del {sitio}.\n\n"
                    f"Solo archivos JPG, JPEG o PNG.\n"
                    f"Los videos serán ignorados automáticamente."
                )
