"""
Sistema de logging para la plataforma de cámaras trampa.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class CameraTrapLogger:
    """Gestor de logging para la aplicación."""
    
    def __init__(self, log_dir: str = "logs", app_name: str = "camara_trampa"):
        """
        Inicializa el sistema de logging.
        
        Args:
            log_dir: Directorio donde guardar los logs
            app_name: Nombre de la aplicación para los archivos de log
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.app_name = app_name
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Configura el logger con handlers para archivo y consola."""
        logger = logging.getLogger(self.app_name)
        logger.setLevel(logging.DEBUG)
        
        # Evitar duplicar handlers si ya existen
        if logger.handlers:
            return logger
        
        # Formato de log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para archivo (log diario)
        log_filename = self.log_dir / f"{self.app_name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Handler para consola (solo INFO y superior)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def debug(self, message: str):
        """Log nivel DEBUG."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log nivel INFO."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log nivel WARNING."""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info: bool = False):
        """Log nivel ERROR."""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message: str, exc_info: bool = False):
        """Log nivel CRITICAL."""
        self.logger.critical(message, exc_info=exc_info)
    
    def log_processing_start(self, project_path: str, total_files: int):
        """Log inicio de procesamiento."""
        self.info(f"=== INICIO DE PROCESAMIENTO ===")
        self.info(f"Proyecto: {project_path}")
        self.info(f"Total de archivos a procesar: {total_files}")
    
    def log_processing_end(self, processed: int, successful: int, errors: int, duration: float):
        """Log fin de procesamiento."""
        self.info(f"=== FIN DE PROCESAMIENTO ===")
        self.info(f"Archivos procesados: {processed}")
        self.info(f"Exitosos: {successful}")
        self.info(f"Errores: {errors}")
        self.info(f"Duración: {duration:.2f} segundos")
    
    def log_file_error(self, file_path: str, error: str):
        """Log error en archivo específico."""
        self.error(f"Error procesando {file_path}: {error}")
    
    def log_gpu_detection(self, gpu_available: bool, gpu_name: Optional[str] = None, cuda_version: Optional[str] = None):
        """Log detección de GPU."""
        if gpu_available:
            self.info(f"✓ GPU detectada: {gpu_name}")
            self.info(f"✓ CUDA versión: {cuda_version}")
        else:
            self.warning("⚠ GPU no detectada - usando CPU")
    
    def log_model_download(self, model_name: str, size_mb: float):
        """Log descarga de modelo."""
        self.info(f"Descargando modelo: {model_name} ({size_mb:.1f} MB)")
    
    def log_ai_prediction(self, image_path: str, prediction: str, confidence: float):
        """Log predicción de IA."""
        self.debug(f"Predicción IA - {image_path}: {prediction} (confianza: {confidence:.2%})")
    
    def log_validation_issue(self, issue_type: str, details: str):
        """Log problema de validación."""
        self.warning(f"Validación - {issue_type}: {details}")
    
    def get_log_file_path(self) -> Path:
        """Retorna la ruta del archivo de log actual."""
        return self.log_dir / f"{self.app_name}_{datetime.now().strftime('%Y%m%d')}.log"


# Instancia global del logger
_global_logger: Optional[CameraTrapLogger] = None


def get_logger() -> CameraTrapLogger:
    """
    Obtiene la instancia global del logger.
    
    Returns:
        Instancia del logger
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = CameraTrapLogger()
    return _global_logger
