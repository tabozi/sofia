"""Module de monitoring des performances."""

import time
import psutil
from datetime import datetime
from typing import Dict, Optional
from contextlib import contextmanager

from .logging import get_logger

logger = get_logger(__name__)

class PerformanceMetrics:
    """Classe pour collecter et suivre les métriques de performance."""
    
    def __init__(self):
        """Initialise les métriques."""
        self.reset()
    
    def reset(self) -> None:
        """Réinitialise les métriques."""
        self.api_calls = 0
        self.api_errors = 0
        self.total_response_time = 0
        self.max_response_time = 0
        self.min_response_time = float('inf')
        self.last_error = None
        self.last_error_time = None
        self.start_time = datetime.utcnow()
    
    def record_api_call(self, response_time: float, success: bool = True) -> None:
        """Enregistre un appel API.
        
        Args:
            response_time: Temps de réponse en secondes
            success: Si l'appel a réussi
        """
        self.api_calls += 1
        if not success:
            self.api_errors += 1
        
        self.total_response_time += response_time
        self.max_response_time = max(self.max_response_time, response_time)
        self.min_response_time = min(self.min_response_time, response_time)
    
    def record_error(self, error: str) -> None:
        """Enregistre une erreur.
        
        Args:
            error: Message d'erreur
        """
        self.last_error = error
        self.last_error_time = datetime.utcnow()
        logger.error("API error", error=error)
    
    def get_metrics(self) -> Dict:
        """Retourne les métriques actuelles.
        
        Returns:
            Dict contenant les métriques
        """
        uptime = (datetime.utcnow() - self.start_time).total_seconds()
        avg_response_time = (
            self.total_response_time / self.api_calls 
            if self.api_calls > 0 else 0
        )
        
        return {
            "uptime_seconds": uptime,
            "api_calls": self.api_calls,
            "api_errors": self.api_errors,
            "error_rate": self.api_errors / self.api_calls if self.api_calls > 0 else 0,
            "avg_response_time": avg_response_time,
            "max_response_time": self.max_response_time,
            "min_response_time": self.min_response_time if self.min_response_time != float('inf') else 0,
            "last_error": self.last_error,
            "last_error_time": self.last_error_time
        }
    
    def get_system_metrics(self) -> Dict:
        """Retourne les métriques système.
        
        Returns:
            Dict contenant les métriques système
        """
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent
        }

@contextmanager
def monitor_performance(operation: str, logger: Optional[object] = None) -> None:
    """Context manager pour monitorer la performance d'une opération.
    
    Args:
        operation: Nom de l'opération
        logger: Logger à utiliser (utilise le logger par défaut si None)
    """
    start_time = time.time()
    try:
        yield
    finally:
        duration = time.time() - start_time
        if logger:
            logger.info(
                "Operation completed",
                operation=operation,
                duration=duration
            )
        else:
            get_logger(__name__).info(
                "Operation completed",
                operation=operation,
                duration=duration
            )
        metrics.record_api_call(duration)

# Instance globale pour les métriques
metrics = PerformanceMetrics() 