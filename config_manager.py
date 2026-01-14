"""
Gestor de configuración para la plataforma de cámaras trampa.
Maneja archivo config.json con preferencias del usuario.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Gestor de configuración de la aplicación."""
    
    DEFAULT_CONFIG = {
        "processing": {
            "independent_event_minutes": 30,
            "image_extensions": [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"],
            "max_cameras_per_site": 10
        },
        "ai": {
            "enabled": True,
            "confidence_threshold": 0.80,
            "batch_size": 32,
            "auto_validate_high_confidence": False
        },
        "coordinates": {
            "default_datum": "WGS84",
            "utm_zones_mexico": ["11Q", "11R", "12Q", "12R", "13Q", "13R", "14Q", "14R", "15Q", "15P", "16Q", "16P"],
            "validate_ranges": True
        },
        "export": {
            "generate_basic_excel": True,
            "generate_complete_excel": True,
            "include_ai_predictions": True,
            "include_coordinates": True,
            "include_effort": True,
            "include_independent_events": True
        },
        "ui": {
            "language": "es",
            "theme": "light",
            "show_advanced_options": False
        }
    }
    
    def __init__(self, config_path: str = "config.json"):
        """
        Inicializa el gestor de configuración.
        
        Args:
            config_path: Ruta al archivo de configuración
        """
        self.config_path = Path(config_path)
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Carga configuración desde archivo o crea una nueva."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # Merge con configuración por defecto para agregar nuevas claves
                return self._merge_configs(self.DEFAULT_CONFIG, loaded_config)
            except Exception as e:
                print(f"Error cargando config: {e}. Usando configuración por defecto.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Crear archivo de configuración por defecto
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: Dict, loaded: Dict) -> Dict:
        """Merge recursivo de configuraciones."""
        result = default.copy()
        for key, value in loaded.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def save_config(self, config: Optional[Dict[str, Any]] = None):
        """Guarda configuración a archivo."""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando config: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Obtiene valor de configuración usando notación de punto.
        
        Args:
            key_path: Ruta a la clave (ej: "ai.confidence_threshold")
            default: Valor por defecto si no existe
            
        Returns:
            Valor de configuración
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any, save: bool = True):
        """
        Establece valor de configuración usando notación de punto.
        
        Args:
            key_path: Ruta a la clave (ej: "ai.confidence_threshold")
            value: Nuevo valor
            save: Si guardar automáticamente a archivo
        """
        keys = key_path.split('.')
        config = self.config
        
        # Navegar hasta el penúltimo nivel
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Establecer valor
        config[keys[-1]] = value
        
        if save:
            self.save_config()
    
    def reset_to_defaults(self):
        """Resetea configuración a valores por defecto."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()
    
    # Métodos de conveniencia para configuraciones comunes
    
    def get_independent_event_minutes(self) -> int:
        """Obtiene minutos para eventos independientes."""
        return self.get("processing.independent_event_minutes", 30)
    
    def set_independent_event_minutes(self, minutes: int):
        """Establece minutos para eventos independientes."""
        self.set("processing.independent_event_minutes", minutes)
    
    def get_confidence_threshold(self) -> float:
        """Obtiene umbral de confianza de IA."""
        return self.get("ai.confidence_threshold", 0.80)
    
    def set_confidence_threshold(self, threshold: float):
        """Establece umbral de confianza de IA."""
        if 0.0 <= threshold <= 1.0:
            self.set("ai.confidence_threshold", threshold)
    
    def is_ai_enabled(self) -> bool:
        """Verifica si IA está habilitada."""
        return self.get("ai.enabled", True)
    
    def set_ai_enabled(self, enabled: bool):
        """Habilita/deshabilita IA."""
        self.set("ai.enabled", enabled)
    
    def get_default_datum(self) -> str:
        """Obtiene datum por defecto para coordenadas."""
        return self.get("coordinates.default_datum", "WGS84")
    
    def get_utm_zones(self) -> list:
        """Obtiene lista de zonas UTM válidas para México."""
        return self.get("coordinates.utm_zones_mexico", [])
    
    def should_generate_basic_excel(self) -> bool:
        """Verifica si generar Excel básico (FORXIME/2)."""
        return self.get("export.generate_basic_excel", True)
    
    def should_generate_complete_excel(self) -> bool:
        """Verifica si generar Excel completo."""
        return self.get("export.generate_complete_excel", True)
    
    def get_language(self) -> str:
        """Obtiene idioma de la interfaz."""
        return self.get("ui.language", "es")
    
    def set_language(self, language: str):
        """Establece idioma de la interfaz."""
        if language in ["es", "en"]:
            self.set("ui.language", language)


# Instancia global del gestor de configuración
_global_config: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """
    Obtiene la instancia global del gestor de configuración.
    
    Returns:
        Instancia del ConfigManager
    """
    global _global_config
    if _global_config is None:
        _global_config = ConfigManager()
    return _global_config
