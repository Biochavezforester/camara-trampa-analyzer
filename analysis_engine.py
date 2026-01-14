"""
Motor de análisis de datos de cámaras trampa.
Calcula trampas-día, eventos independientes, y análisis temporal.
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict


class TrapEffortCalculator:
    """Calculador de esfuerzo de muestreo (trampas-día)."""
    
    @staticmethod
    def calculate_trap_days(df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula trampas-día por cámara.
        
        Args:
            df: DataFrame con columnas SITIO, CAMARA, FECHA
            
        Returns:
            DataFrame con esfuerzo por cámara
        """
        effort_data = []
        
        # Agrupar por sitio y cámara
        for (sitio, camara), group in df.groupby(['SITIO', 'CAMARA']):
            # Convertir fechas a datetime
            fechas = pd.to_datetime(group['FECHA'])
            
            primera_captura = fechas.min()
            ultima_captura = fechas.max()
            
            # Calcular días activos
            dias_activos = (ultima_captura - primera_captura).days + 1
            
            effort_data.append({
                'SITIO': sitio,
                'CAMARA': camara,
                'PRIMERA_CAPTURA': primera_captura.strftime('%Y-%m-%d'),
                'ULTIMA_CAPTURA': ultima_captura.strftime('%Y-%m-%d'),
                'TRAMPAS_DIA': dias_activos,
                'TOTAL_CAPTURAS': len(group)
            })
        
        return pd.DataFrame(effort_data)


class IndependentEventDetector:
    """Detector de eventos independientes."""
    
    def __init__(self, time_threshold_minutes: int = 30):
        """
        Inicializa detector.
        
        Args:
            time_threshold_minutes: Minutos entre eventos para considerarlos independientes
        """
        self.time_threshold = timedelta(minutes=time_threshold_minutes)
    
    def detect_independent_events(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detecta eventos independientes agrupando fotos consecutivas.
        
        Args:
            df: DataFrame con columnas SITIO, CAMARA, ESPECIE, FECHA, HORA
            
        Returns:
            DataFrame con eventos independientes por especie
        """
        # Crear columna datetime combinando fecha y hora
        df['DATETIME'] = pd.to_datetime(df['FECHA'] + ' ' + df['HORA'])
        
        # Ordenar por sitio, cámara, especie y datetime
        df_sorted = df.sort_values(['SITIO', 'CAMARA', 'ESPECIE', 'DATETIME'])
        
        events_data = []
        
        # Agrupar por sitio, cámara y especie
        for (sitio, camara, especie), group in df_sorted.groupby(['SITIO', 'CAMARA', 'ESPECIE']):
            total_capturas = len(group)
            eventos_independientes = 1  # Primera captura siempre es un evento
            
            # Comparar tiempos entre capturas consecutivas
            prev_time = None
            for current_time in group['DATETIME']:
                if prev_time is not None:
                    time_diff = current_time - prev_time
                    if time_diff >= self.time_threshold:
                        eventos_independientes += 1
                prev_time = current_time
            
            events_data.append({
                'SITIO': sitio,
                'CAMARA': camara,
                'ESPECIE': especie,
                'CAPTURAS_TOTALES': total_capturas,
                'EVENTOS_INDEPENDIENTES': eventos_independientes
            })
        
        return pd.DataFrame(events_data)
    
    def calculate_rai(self, events_df: pd.DataFrame, effort_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula RAI (Relative Abundance Index) por especie.
        
        RAI = (Eventos independientes / Trampas-día) * 100
        
        Args:
            events_df: DataFrame de eventos independientes
            effort_df: DataFrame de esfuerzo de muestreo
            
        Returns:
            DataFrame con RAI por especie y sitio
        """
        # Calcular trampas-día totales por sitio
        effort_by_site = effort_df.groupby('SITIO')['TRAMPAS_DIA'].sum().to_dict()
        
        rai_data = []
        
        # Agrupar eventos por sitio y especie
        for (sitio, especie), group in events_df.groupby(['SITIO', 'ESPECIE']):
            total_eventos = group['EVENTOS_INDEPENDIENTES'].sum()
            trampas_dia = effort_by_site.get(sitio, 1)  # Evitar división por cero
            
            rai = (total_eventos / trampas_dia) * 100
            
            rai_data.append({
                'SITIO': sitio,
                'ESPECIE': especie,
                'EVENTOS_INDEPENDIENTES': total_eventos,
                'TRAMPAS_DIA': trampas_dia,
                'RAI': round(rai, 2)
            })
        
        return pd.DataFrame(rai_data)


class TemporalAnalyzer:
    """Analizador de patrones temporales."""
    
    PERIODS = {
        'CREPUSCULAR_MATUTINO': (6, 8),
        'DIURNO': (8, 18),
        'CREPUSCULAR_VESPERTINO': (18, 20),
        'NOCTURNO': (20, 24, 0, 6)  # 20:00-23:59 y 00:00-05:59
    }
    
    @staticmethod
    def classify_time_period(hora: str) -> str:
        """
        Clasifica hora en período del día.
        
        Args:
            hora: Hora en formato HH:MM:SS
            
        Returns:
            Período del día
        """
        try:
            hour = int(hora.split(':')[0])
            
            if 6 <= hour < 8:
                return 'CREPUSCULAR_MATUTINO'
            elif 8 <= hour < 18:
                return 'DIURNO'
            elif 18 <= hour < 20:
                return 'CREPUSCULAR_VESPERTINO'
            else:
                return 'NOCTURNO'
        except:
            return 'DESCONOCIDO'
    
    @staticmethod
    def analyze_temporal_patterns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Analiza patrones temporales por especie.
        
        Args:
            df: DataFrame con columnas ESPECIE, HORA
            
        Returns:
            DataFrame con distribución temporal por especie
        """
        # Clasificar cada captura por período
        df['PERIODO'] = df['HORA'].apply(TemporalAnalyzer.classify_time_period)
        
        # Contar capturas por especie y período
        temporal_data = []
        
        for especie, group in df.groupby('ESPECIE'):
            period_counts = group['PERIODO'].value_counts().to_dict()
            total = len(group)
            
            temporal_data.append({
                'ESPECIE': especie,
                'TOTAL_CAPTURAS': total,
                'CREPUSCULAR_MATUTINO': period_counts.get('CREPUSCULAR_MATUTINO', 0),
                'DIURNO': period_counts.get('DIURNO', 0),
                'CREPUSCULAR_VESPERTINO': period_counts.get('CREPUSCULAR_VESPERTINO', 0),
                'NOCTURNO': period_counts.get('NOCTURNO', 0),
                'PATRON_DOMINANTE': max(period_counts, key=period_counts.get) if period_counts else 'DESCONOCIDO'
            })
        
        return pd.DataFrame(temporal_data)
    
    @staticmethod
    def get_peak_hours(df: pd.DataFrame, especie: str = None) -> Dict:
        """
        Identifica horas pico de actividad.
        
        Args:
            df: DataFrame con columnas ESPECIE, HORA
            especie: Especie específica (None para todas)
            
        Returns:
            Dict con horas pico
        """
        if especie:
            df = df[df['ESPECIE'] == especie]
        
        # Extraer hora (0-23)
        df['HOUR'] = df['HORA'].apply(lambda x: int(x.split(':')[0]))
        
        # Contar capturas por hora
        hour_counts = df['HOUR'].value_counts().sort_index()
        
        if len(hour_counts) == 0:
            return {'peak_hour': None, 'peak_count': 0}
        
        peak_hour = hour_counts.idxmax()
        peak_count = hour_counts.max()
        
        return {
            'peak_hour': f"{peak_hour:02d}:00",
            'peak_count': int(peak_count),
            'hourly_distribution': hour_counts.to_dict()
        }


class VisitFrequencyCalculator:
    """Calculador de frecuencia de visitas."""
    
    @staticmethod
    def calculate_visit_frequency(df: pd.DataFrame, effort_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula frecuencia de visitas por especie.
        
        Args:
            df: DataFrame con capturas
            effort_df: DataFrame con esfuerzo de muestreo
            
        Returns:
            DataFrame con frecuencia de visitas
        """
        # Calcular trampas-día totales
        total_trap_days = effort_df['TRAMPAS_DIA'].sum()
        
        frequency_data = []
        
        for especie, group in df.groupby('ESPECIE'):
            total_capturas = len(group)
            sitios_detectado = group['SITIO'].nunique()
            camaras_detectado = group['CAMARA'].nunique()
            
            # Frecuencia = capturas / trampas-día
            frecuencia = total_capturas / total_trap_days if total_trap_days > 0 else 0
            
            frequency_data.append({
                'ESPECIE': especie,
                'TOTAL_CAPTURAS': total_capturas,
                'SITIOS_DETECTADO': sitios_detectado,
                'CAMARAS_DETECTADO': camaras_detectado,
                'FRECUENCIA_VISITAS': round(frecuencia, 4),
                'CAPTURAS_POR_100_TRAMPAS_DIA': round(frecuencia * 100, 2)
            })
        
        return pd.DataFrame(frequency_data).sort_values('TOTAL_CAPTURAS', ascending=False)


class GapDetector:
    """Detector de períodos sin capturas (gaps)."""
    
    @staticmethod
    def detect_gaps(df: pd.DataFrame, min_gap_days: int = 7) -> List[Dict]:
        """
        Detecta períodos sin capturas por cámara.
        
        Args:
            df: DataFrame con columnas SITIO, CAMARA, FECHA
            min_gap_days: Mínimo de días para considerar un gap
            
        Returns:
            Lista de gaps detectados
        """
        gaps = []
        
        # Convertir fechas
        df['FECHA_DT'] = pd.to_datetime(df['FECHA'])
        
        for (sitio, camara), group in df.groupby(['SITIO', 'CAMARA']):
            # Ordenar por fecha
            fechas_sorted = sorted(group['FECHA_DT'])
            
            # Buscar gaps entre fechas consecutivas
            for i in range(len(fechas_sorted) - 1):
                fecha_actual = fechas_sorted[i]
                fecha_siguiente = fechas_sorted[i + 1]
                
                gap_days = (fecha_siguiente - fecha_actual).days
                
                if gap_days >= min_gap_days:
                    gaps.append({
                        'SITIO': sitio,
                        'CAMARA': camara,
                        'FECHA_INICIO_GAP': fecha_actual.strftime('%Y-%m-%d'),
                        'FECHA_FIN_GAP': fecha_siguiente.strftime('%Y-%m-%d'),
                        'DIAS_SIN_CAPTURAS': gap_days
                    })
        
        return gaps
