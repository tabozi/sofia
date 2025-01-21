"""Utilitaires pour l'application."""

from .logging import setup_logging, get_logger, metrics as log_metrics
from .monitoring import metrics as perf_metrics, monitor_performance

def init_monitoring():
    """Initialise le système de logging et monitoring."""
    # Configuration du logging
    setup_logging()
    logger = get_logger(__name__)
    logger.info("Monitoring system initialized")
    
    # Réinitialisation des métriques
    log_metrics.reset()
    perf_metrics.reset()
    
    return logger

__all__ = [
    'setup_logging',
    'get_logger',
    'log_metrics',
    'perf_metrics',
    'monitor_performance',
    'init_monitoring'
]
