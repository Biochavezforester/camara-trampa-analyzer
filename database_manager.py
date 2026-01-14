"""
Gestor de base de datos SQLite para la plataforma de cámaras trampa.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json


class DatabaseManager:
    """Gestor de base de datos local SQLite."""
    
    def __init__(self, db_path: str = "database/projects.db"):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene conexión a la base de datos."""
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Inicializa tablas de la base de datos."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla de proyectos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_processed TIMESTAMP,
                total_photos INTEGER DEFAULT 0,
                total_species INTEGER DEFAULT 0
            )
        """)
        
        # Tabla de coordenadas de cámaras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS camera_coordinates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                site_name TEXT NOT NULL,
                camera_name TEXT NOT NULL,
                utm_zone TEXT NOT NULL,
                easting REAL NOT NULL,
                northing REAL NOT NULL,
                datum TEXT DEFAULT 'WGS84',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                UNIQUE(project_id, site_name, camera_name)
            )
        """)
        
        # Tabla de historial de procesamiento
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processing_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_photos INTEGER,
                ai_predictions INTEGER DEFAULT 0,
                validated_predictions INTEGER DEFAULT 0,
                processing_time_seconds REAL,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        """)
        
        # Tabla de catálogo de especies
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS species_catalog (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                species_name TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id),
                UNIQUE(project_id, species_name)
            )
        """)
        
        conn.commit()
        conn.close()
    
    # Métodos para proyectos
    
    def create_project(self, name: str, path: str) -> int:
        """Crea un nuevo proyecto."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO projects (name, path) VALUES (?, ?)",
                (name, path)
            )
            conn.commit()
            project_id = cursor.lastrowid
            return project_id
        except sqlite3.IntegrityError:
            # Proyecto ya existe, obtener ID
            cursor.execute("SELECT id FROM projects WHERE path = ?", (path,))
            row = cursor.fetchone()
            return row['id'] if row else None
        finally:
            conn.close()
    
    def get_project(self, project_path: str) -> Optional[Dict]:
        """Obtiene información de un proyecto."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM projects WHERE path = ?", (project_path,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def update_project_stats(self, project_id: int, total_photos: int, total_species: int):
        """Actualiza estadísticas del proyecto."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE projects 
            SET total_photos = ?, total_species = ?, last_processed = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (total_photos, total_species, project_id))
        
        conn.commit()
        conn.close()
    
    # Métodos para coordenadas de cámaras
    
    def save_camera_coordinates(self, project_id: int, site_name: str, camera_name: str,
                                utm_zone: str, easting: float, northing: float, datum: str = "WGS84"):
        """Guarda coordenadas de una cámara."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO camera_coordinates 
            (project_id, site_name, camera_name, utm_zone, easting, northing, datum)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (project_id, site_name, camera_name, utm_zone, easting, northing, datum))
        
        conn.commit()
        conn.close()
    
    def get_camera_coordinates(self, project_id: int, site_name: str, camera_name: str) -> Optional[Dict]:
        """Obtiene coordenadas de una cámara."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM camera_coordinates 
            WHERE project_id = ? AND site_name = ? AND camera_name = ?
        """, (project_id, site_name, camera_name))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_all_camera_coordinates(self, project_id: int) -> List[Dict]:
        """Obtiene todas las coordenadas de cámaras de un proyecto."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM camera_coordinates WHERE project_id = ?
            ORDER BY site_name, camera_name
        """, (project_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    # Métodos para historial de procesamiento
    
    def add_processing_record(self, project_id: int, total_photos: int, 
                            ai_predictions: int = 0, validated_predictions: int = 0,
                            processing_time: float = 0.0):
        """Agrega registro de procesamiento."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO processing_history 
            (project_id, total_photos, ai_predictions, validated_predictions, processing_time_seconds)
            VALUES (?, ?, ?, ?, ?)
        """, (project_id, total_photos, ai_predictions, validated_predictions, processing_time))
        
        conn.commit()
        conn.close()
    
    def get_processing_history(self, project_id: int, limit: int = 10) -> List[Dict]:
        """Obtiene historial de procesamiento."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM processing_history 
            WHERE project_id = ?
            ORDER BY processed_at DESC
            LIMIT ?
        """, (project_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    # Métodos para catálogo de especies
    
    def add_or_update_species(self, project_id: int, species_name: str):
        """Agrega o actualiza especie en el catálogo."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO species_catalog (project_id, species_name, count, last_seen)
            VALUES (?, ?, 1, CURRENT_TIMESTAMP)
            ON CONFLICT(project_id, species_name) DO UPDATE SET
                count = count + 1,
                last_seen = CURRENT_TIMESTAMP
        """, (project_id, species_name))
        
        conn.commit()
        conn.close()
    
    def get_species_catalog(self, project_id: int) -> List[Dict]:
        """Obtiene catálogo de especies del proyecto."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM species_catalog 
            WHERE project_id = ?
            ORDER BY count DESC, species_name
        """, (project_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]


# Instancia global del gestor de base de datos
_global_db: Optional[DatabaseManager] = None


def get_database() -> DatabaseManager:
    """
    Obtiene la instancia global del gestor de base de datos.
    
    Returns:
        Instancia del DatabaseManager
    """
    global _global_db
    if _global_db is None:
        _global_db = DatabaseManager()
    return _global_db
