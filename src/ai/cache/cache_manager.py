"""
Gestionnaire de cache pour les réponses des modèles d'IA
"""
import json
import hashlib
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path
from src.config import settings

class AIResponseCache:
    """Gestionnaire de cache pour les réponses des modèles d'IA"""
    
    def __init__(self, db_path: Optional[str] = None):
        """Initialise le gestionnaire de cache"""
        if db_path is None:
            db_path = Path(settings.DATABASE_URL.replace('sqlite:///', ''))
            
        self.db_path = db_path
        self.init_db()
        
    def init_db(self) -> None:
        """Initialise la base de données SQLite"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ai_cache (
                    cache_key TEXT PRIMARY KEY,
                    model_name TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    context TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP,
                    usage_count INTEGER DEFAULT 1
                )
            """)
            
    def _generate_cache_key(self, model_name: str, prompt: str, context: Optional[Dict] = None) -> str:
        """Génère une clé de cache unique"""
        key_parts = [model_name, prompt]
        if context:
            key_parts.append(json.dumps(context, sort_keys=True))
            
        key_string = "|".join(key_parts)
        return hashlib.sha256(key_string.encode()).hexdigest()
        
    def get(self, model_name: str, prompt: str, context: Optional[Dict] = None) -> Optional[str]:
        """Récupère une réponse du cache"""
        cache_key = self._generate_cache_key(model_name, prompt, context)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT response, expires_at, usage_count 
                FROM ai_cache 
                WHERE cache_key = ?
            """, (cache_key,))
            
            result = cursor.fetchone()
            
            if result:
                response, expires_at, usage_count = result
                
                # Vérifie si le cache est expiré
                if expires_at and datetime.fromisoformat(expires_at) < datetime.now():
                    self.delete(cache_key)
                    return None
                
                # Incrémente le compteur d'utilisation
                conn.execute("""
                    UPDATE ai_cache 
                    SET usage_count = ? 
                    WHERE cache_key = ?
                """, (usage_count + 1, cache_key))
                
                return response
                
        return None
        
    def set(self, model_name: str, prompt: str, response: str, 
            context: Optional[Dict] = None, ttl_hours: int = 24) -> None:
        """Stocke une réponse dans le cache"""
        cache_key = self._generate_cache_key(model_name, prompt, context)
        expires_at = datetime.now() + timedelta(hours=ttl_hours)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO ai_cache 
                (cache_key, model_name, prompt, response, context, expires_at) 
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                cache_key,
                model_name,
                prompt,
                response,
                json.dumps(context) if context else None,
                expires_at.isoformat()
            ))
            
    def delete(self, cache_key: str) -> None:
        """Supprime une entrée du cache"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM ai_cache WHERE cache_key = ?", (cache_key,))
            
    def clear_expired(self) -> int:
        """Nettoie les entrées expirées du cache"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                DELETE FROM ai_cache 
                WHERE expires_at < datetime('now')
            """)
            return cursor.rowcount
            
    def get_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques du cache"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_entries,
                    SUM(usage_count) as total_hits,
                    AVG(usage_count) as avg_hits_per_entry,
                    COUNT(CASE WHEN expires_at < datetime('now') THEN 1 END) as expired_entries
                FROM ai_cache
            """)
            
            stats = dict(zip(['total_entries', 'total_hits', 'avg_hits_per_entry', 'expired_entries'], 
                           cursor.fetchone()))
                           
            # Calcul de la taille du cache
            cursor = conn.execute("SELECT SUM(LENGTH(response)) FROM ai_cache")
            stats['total_size_bytes'] = cursor.fetchone()[0] or 0
            
            return stats 

    def _get_connection(self) -> sqlite3.Connection:
        """Crée une connexion à la base de données"""
        return sqlite3.connect(self.db_path) 