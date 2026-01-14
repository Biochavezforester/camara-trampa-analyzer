"""
Validador de datos de cámaras trampa.
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Tuple
from collections import Counter
import re


class ExifValidator:
    """Validador de metadatos EXIF."""
    
    @staticmethod
    def validate_date_range(fecha: str, min_year: int = 2010, max_year: int = 2030) -> Tuple[bool, str]:
        """Valida que una fecha esté en un rango razonable."""
        try:
            date = datetime.strptime(fecha, "%Y-%m-%d")
            if min_year <= date.year <= max_year:
                return True, "Fecha válida"
            else:
                return False, f"Fecha fuera de rango ({min_year}-{max_year}): {fecha}"
        except:
            return False, f"Formato de fecha inválido: {fecha}"
    
    @staticmethod
    def find_photos_without_exif(df: pd.DataFrame) -> List[str]:
        """Encuentra fotos sin metadatos EXIF."""
        # Fotos sin fecha o hora son consideradas sin EXIF
        missing_exif = df[(df['FECHA'].isna()) | (df['HORA'].isna())]
        return missing_exif.index.tolist() if len(missing_exif) > 0 else []


class NomenclatureValidator:
    """Validador de nomenclatura de especies."""
    
    @staticmethod
    def detect_duplicates(df: pd.DataFrame) -> Dict[str, List[str]]:
        """Detecta nombres duplicados de cámaras."""
        duplicates = {}
        
        # Agrupar por sitio
        for sitio, group in df.groupby('SITIO'):
            camera_counts = Counter(group['CAMARA'])
            # Cámaras que aparecen más de una vez (normal)
            # Pero verificar si hay inconsistencias en nombres
            cameras = group['CAMARA'].unique()
            
            # Buscar nombres similares que podrían ser errores
            for i, cam1 in enumerate(cameras):
                for cam2 in cameras[i+1:]:
                    if NomenclatureValidator._are_similar(cam1, cam2):
                        if sitio not in duplicates:
                            duplicates[sitio] = []
                        duplicates[sitio].append(f"{cam1} ≈ {cam2}")
        
        return duplicates
    
    @staticmethod
    def _are_similar(name1: str, name2: str, threshold: float = 0.8) -> bool:
        """Verifica si dos nombres son similares (posible error de tipeo)."""
        # Normalizar
        n1 = name1.upper().strip()
        n2 = name2.upper().strip()
        
        if n1 == n2:
            return False  # Exactamente iguales, no es error
        
        # Verificar si uno contiene al otro
        if n1 in n2 or n2 in n1:
            return True
        
        # Verificar similitud de Levenshtein simple
        if len(n1) == len(n2):
            diff_count = sum(c1 != c2 for c1, c2 in zip(n1, n2))
            similarity = 1 - (diff_count / len(n1))
            return similarity >= threshold
        
        return False
    
    @staticmethod
    def suggest_species_standardization(df: pd.DataFrame) -> Dict[str, str]:
        """Sugiere estandarización de nombres de especies."""
        from utils import suggest_species_correction, clean_species_name
        
        suggestions = {}
        
        for especie in df['ESPECIE'].unique():
            cleaned = clean_species_name(especie)
            suggestion = suggest_species_correction(cleaned)
            
            if suggestion and suggestion != cleaned:
                suggestions[especie] = suggestion
        
        return suggestions
    
    @staticmethod
    def detect_inconsistent_species_names(df: pd.DataFrame) -> List[Tuple[str, str]]:
        """Detecta nombres de especies inconsistentes."""
        inconsistencies = []
        species_list = df['ESPECIE'].unique()
        
        for i, sp1 in enumerate(species_list):
            for sp2 in species_list[i+1:]:
                # Normalizar y comparar
                sp1_norm = sp1.upper().strip()
                sp2_norm = sp2.upper().strip()
                
                # Detectar variaciones comunes
                if sp1_norm != sp2_norm:
                    # Remover espacios y comparar
                    sp1_no_space = sp1_norm.replace(' ', '')
                    sp2_no_space = sp2_norm.replace(' ', '')
                    
                    if sp1_no_space == sp2_no_space:
                        inconsistencies.append((sp1, sp2))
                    # Detectar singular/plural
                    elif sp1_norm.rstrip('S') == sp2_norm or sp2_norm.rstrip('S') == sp1_norm:
                        inconsistencies.append((sp1, sp2))
        
        return inconsistencies


class QualityReporter:
    """Generador de reportes de calidad de datos."""
    
    @staticmethod
    def generate_quality_report(df: pd.DataFrame) -> Dict:
        """
        Genera reporte completo de calidad de datos.
        
        Returns:
            Dict con métricas de calidad
        """
        report = {
            'total_records': len(df),
            'date_issues': [],
            'exif_issues': [],
            'nomenclature_issues': [],
            'duplicate_cameras': {},
            'species_suggestions': {},
            'quality_score': 100.0
        }
        
        # Validar fechas
        for idx, row in df.iterrows():
            valid, msg = ExifValidator.validate_date_range(row['FECHA'])
            if not valid:
                report['date_issues'].append(msg)
                report['quality_score'] -= 1
        
        # Detectar fotos sin EXIF
        missing_exif = ExifValidator.find_photos_without_exif(df)
        if missing_exif:
            report['exif_issues'] = missing_exif
            report['quality_score'] -= len(missing_exif) * 0.5
        
        # Detectar duplicados de cámaras
        duplicates = NomenclatureValidator.detect_duplicates(df)
        if duplicates:
            report['duplicate_cameras'] = duplicates
            report['quality_score'] -= len(duplicates) * 2
        
        # Sugerencias de especies
        suggestions = NomenclatureValidator.suggest_species_standardization(df)
        if suggestions:
            report['species_suggestions'] = suggestions
            report['quality_score'] -= len(suggestions) * 1
        
        # Detectar inconsistencias en nombres de especies
        inconsistencies = NomenclatureValidator.detect_inconsistent_species_names(df)
        if inconsistencies:
            report['nomenclature_issues'] = inconsistencies
            report['quality_score'] -= len(inconsistencies) * 3
        
        # Asegurar que el score no sea negativo
        report['quality_score'] = max(0, report['quality_score'])
        
        return report
    
    @staticmethod
    def format_quality_report_text(report: Dict) -> str:
        """Formatea reporte de calidad como texto."""
        lines = []
        lines.append("=" * 60)
        lines.append("REPORTE DE CALIDAD DE DATOS")
        lines.append("=" * 60)
        lines.append(f"\nTotal de registros: {report['total_records']}")
        lines.append(f"Puntuación de calidad: {report['quality_score']:.1f}/100")
        lines.append("")
        
        if report['date_issues']:
            lines.append("⚠️ PROBLEMAS DE FECHAS:")
            for issue in report['date_issues'][:10]:  # Mostrar solo primeros 10
                lines.append(f"  - {issue}")
            if len(report['date_issues']) > 10:
                lines.append(f"  ... y {len(report['date_issues']) - 10} más")
            lines.append("")
        
        if report['exif_issues']:
            lines.append(f"⚠️ FOTOS SIN METADATOS EXIF: {len(report['exif_issues'])}")
            lines.append("")
        
        if report['duplicate_cameras']:
            lines.append("⚠️ POSIBLES DUPLICADOS DE CÁMARAS:")
            for sitio, dups in report['duplicate_cameras'].items():
                lines.append(f"  Sitio {sitio}:")
                for dup in dups:
                    lines.append(f"    - {dup}")
            lines.append("")
        
        if report['species_suggestions']:
            lines.append("💡 SUGERENCIAS DE ESTANDARIZACIÓN:")
            for original, suggestion in list(report['species_suggestions'].items())[:10]:
                lines.append(f"  '{original}' → '{suggestion}'")
            if len(report['species_suggestions']) > 10:
                lines.append(f"  ... y {len(report['species_suggestions']) - 10} más")
            lines.append("")
        
        if report['nomenclature_issues']:
            lines.append("⚠️ INCONSISTENCIAS EN NOMBRES:")
            for sp1, sp2 in report['nomenclature_issues'][:10]:
                lines.append(f"  '{sp1}' vs '{sp2}'")
            if len(report['nomenclature_issues']) > 10:
                lines.append(f"  ... y {len(report['nomenclature_issues']) - 10} más")
            lines.append("")
        
        if report['quality_score'] >= 90:
            lines.append("✅ CALIDAD EXCELENTE - Datos listos para análisis")
        elif report['quality_score'] >= 70:
            lines.append("⚠️ CALIDAD BUENA - Revisar advertencias menores")
        elif report['quality_score'] >= 50:
            lines.append("⚠️ CALIDAD ACEPTABLE - Se recomienda corregir problemas")
        else:
            lines.append("❌ CALIDAD BAJA - Correcciones necesarias antes de análisis")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
