"""
Sistema de clasificación con IA para fauna mexicana.
Incluye detección de GPU CUDA y modo fallback a CPU/manual.
"""

import torch
from typing import Optional, Dict, Tuple, List
from pathlib import Path
from logger import get_logger

logger = get_logger()


class CUDADetector:
    """Detector de GPU CUDA."""
    
    @staticmethod
    def detect_cuda() -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Detecta disponibilidad de GPU CUDA.
        
        Returns:
            Tupla (disponible, nombre_gpu, version_cuda)
        """
        try:
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name(0)
                cuda_version = torch.version.cuda
                logger.log_gpu_detection(True, gpu_name, cuda_version)
                return True, gpu_name, cuda_version
            else:
                logger.log_gpu_detection(False)
                return False, None, None
        except Exception as e:
            logger.error(f"Error detectando CUDA: {e}")
            return False, None, None
    
    @staticmethod
    def get_gpu_info() -> Dict:
        """Obtiene información detallada de la GPU."""
        if not torch.cuda.is_available():
            return {
                'available': False,
                'message': 'GPU CUDA no disponible. La plataforma funcionará en modo asistido manual.'
            }
        
        return {
            'available': True,
            'device_count': torch.cuda.device_count(),
            'device_name': torch.cuda.get_device_name(0),
            'cuda_version': torch.version.cuda,
            'memory_total': torch.cuda.get_device_properties(0).total_memory / 1024**3,  # GB
            'memory_allocated': torch.cuda.memory_allocated(0) / 1024**3,  # GB
        }


class AIClassifierStub:
    """
    Stub para clasificador de IA.
    
    NOTA: Este es un placeholder. La implementación completa de MegaDetector v5
    y el clasificador de especies mexicanas requiere:
    1. Descarga de modelos pre-entrenados (~2-3 GB)
    2. Integración con MegaDetector oficial
    3. Fine-tuning para fauna mexicana
    
    Por ahora, este módulo detecta GPU y prepara la infraestructura.
    """
    
    def __init__(self, use_gpu: bool = True):
        """
        Inicializa clasificador.
        
        Args:
            use_gpu: Si usar GPU (si está disponible)
        """
        self.gpu_available, self.gpu_name, self.cuda_version = CUDADetector.detect_cuda()
        self.use_gpu = use_gpu and self.gpu_available
        self.device = torch.device('cuda' if self.use_gpu else 'cpu')
        
        logger.info(f"Clasificador inicializado en: {self.device}")
    
    def classify_image(self, image_path: Path) -> Dict:
        """
        Clasifica una imagen (STUB - requiere modelos descargados).
        
        Args:
            image_path: Ruta a la imagen
            
        Returns:
            Dict con predicción y confianza
        """
        # STUB: En implementación completa, aquí iría:
        # 1. Cargar imagen
        # 2. Preprocesar para MegaDetector
        # 3. Detectar animal/humano/vehículo/vacío
        # 4. Si es animal, clasificar especie
        # 5. Retornar predicción con confianza
        
        return {
            'species': 'CLASIFICACION_PENDIENTE',
            'confidence': 0.0,
            'is_empty': False,
            'is_human': False,
            'is_vehicle': False,
            'requires_manual_classification': True,
            'message': 'Clasificación automática requiere descarga de modelos de IA'
        }
    
    def batch_classify(self, image_paths: List[Path], progress_callback=None) -> List[Dict]:
        """
        Clasifica múltiples imágenes en batch (STUB).
        
        Args:
            image_paths: Lista de rutas a imágenes
            progress_callback: Función callback para progreso
            
        Returns:
            Lista de predicciones
        """
        results = []
        
        for i, img_path in enumerate(image_paths):
            result = self.classify_image(img_path)
            result['image_path'] = str(img_path)
            results.append(result)
            
            if progress_callback:
                progress_callback(i + 1, len(image_paths))
        
        return results


class ManualClassificationAssistant:
    """
    Asistente para clasificación manual cuando no hay GPU/IA.
    Proporciona sugerencias inteligentes basadas en historial.
    """
    
    def __init__(self):
        """Inicializa asistente de clasificación manual."""
        from utils import get_common_species_mexico
        self.common_species = get_common_species_mexico()
        self.species_history = []
    
    def get_suggestions(self, site: str = None, camera: str = None, 
                       recent_species: List[str] = None) -> List[str]:
        """
        Obtiene sugerencias de especies para clasificación manual.
        
        Args:
            site: Nombre del sitio
            camera: Nombre de la cámara
            recent_species: Especies recientes en este sitio/cámara
            
        Returns:
            Lista de especies sugeridas (ordenadas por probabilidad)
        """
        suggestions = []
        
        # Agregar especies recientes primero
        if recent_species:
            suggestions.extend([s for s in recent_species if s not in suggestions])
        
        # Agregar especies comunes de México
        suggestions.extend([s for s in self.common_species if s not in suggestions])
        
        return suggestions[:20]  # Top 20 sugerencias
    
    def add_to_history(self, species: str):
        """Agrega especie al historial para mejorar sugerencias."""
        if species not in self.species_history:
            self.species_history.insert(0, species)
            # Mantener solo últimas 50
            self.species_history = self.species_history[:50]
    
    def suggest_correction(self, species_name: str) -> Optional[str]:
        """Sugiere corrección para nombre de especie."""
        from utils import suggest_species_correction
        return suggest_species_correction(species_name)


def get_classifier(use_gpu: bool = True) -> AIClassifierStub:
    """
    Obtiene instancia del clasificador de IA.
    
    Args:
        use_gpu: Si intentar usar GPU
        
    Returns:
        Instancia del clasificador
    """
    return AIClassifierStub(use_gpu=use_gpu)


def get_manual_assistant() -> ManualClassificationAssistant:
    """
    Obtiene instancia del asistente de clasificación manual.
    
    Returns:
        Instancia del asistente
    """
    return ManualClassificationAssistant()


# Información sobre implementación completa de IA
AI_IMPLEMENTATION_NOTES = """
NOTAS SOBRE IMPLEMENTACIÓN COMPLETA DE IA:

Para implementar clasificación automática completa, se requiere:

1. MEGADETECTOR v5:
   - Modelo: https://github.com/microsoft/CameraTraps
   - Peso del modelo: ~300 MB
   - Función: Detectar animales/humanos/vehículos/vacío
   - Precisión: ~95% en detección

2. CLASIFICADOR DE ESPECIES MÉXICO:
   - Opción A: Fine-tune de modelos existentes (iNaturalist, Wildlife Insights)
   - Opción B: Entrenar modelo personalizado con dataset mexicano
   - Peso estimado: 1-2 GB
   - Especies objetivo: 50-100 especies comunes de México
   - Precisión esperada: 85-95% en especies comunes

3. PIPELINE DE PROCESAMIENTO:
   - Carga de imagen
   - Preprocesamiento (resize, normalización)
   - Detección con MegaDetector
   - Si animal detectado: clasificación de especie
   - Cálculo de confianza
   - Post-procesamiento

4. OPTIMIZACIONES GPU:
   - Batch processing (32-64 imágenes simultáneas)
   - Mixed precision (FP16) para RTX
   - CUDA streams para paralelización
   - Caché de modelos en VRAM

5. INTEGRACIÓN:
   - Descargar modelos en primera ejecución
   - Validar checksums
   - Cargar modelos en GPU
   - Procesar imágenes en batches
   - Guardar predicciones con confianza
   - Interfaz de validación obligatoria

ESTIMACIÓN DE TIEMPO DE IMPLEMENTACIÓN:
- Integración MegaDetector: 4-6 horas
- Fine-tuning para México: 8-12 horas (requiere dataset)
- Optimización GPU: 2-4 horas
- Testing y validación: 4-6 horas
TOTAL: 18-28 horas de desarrollo

ALTERNATIVA RÁPIDA:
- Usar MegaDetector solo para filtrar vacías
- Clasificación manual asistida para especies
- Implementación: 2-4 horas
"""
