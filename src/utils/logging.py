"""Configuration et utilitaires de logging."""

import os
import sys
import logging
import structlog
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import Optional

from ..config.settings import get_settings

settings = get_settings()

# Configuration des logs
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "linkedin_bot.log")
MAX_BYTES = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5

def setup_logging(
    log_level: Optional[str] = None,
    log_file: Optional[str] = None
) -> None:
    """Configure le système de logging.
    
    Args:
        log_level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Chemin vers le fichier de log
    """
    # Création du dossier de logs si nécessaire
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # Configuration du niveau de log
    level = getattr(logging, (log_level or settings.log_level).upper())
    
    # Configuration du handler de fichier avec rotation
    file_handler = RotatingFileHandler(
        log_file or LOG_FILE,
        maxBytes=MAX_BYTES,
        backupCount=BACKUP_COUNT
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # Configuration du handler de console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    
    # Configuration du logger racine
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Configuration de structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.render_to_log_kwargs,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def get_logger(name: str) -> structlog.BoundLogger:
    """Retourne un logger configuré pour le module spécifié.
    
    Args:
        name: Nom du module/logger
        
    Returns:
        Logger configuré
    """
    return structlog.get_logger(name)

class LogMetrics:
    """Classe pour collecter et suivre les métriques de logging."""
    
    def __init__(self):
        """Initialise les métriques."""
        self.reset()
    
    def reset(self) -> None:
        """Réinitialise les métriques."""
        self.error_count = 0
        self.warning_count = 0
        self.info_count = 0
        self.debug_count = 0
        self.last_error = None
        self.last_error_time = None
    
    def increment_error(self, error: str) -> None:
        """Incrémente le compteur d'erreurs."""
        self.error_count += 1
        self.last_error = error
        self.last_error_time = datetime.utcnow()
    
    def increment_warning(self) -> None:
        """Incrémente le compteur d'avertissements."""
        self.warning_count += 1
    
    def increment_info(self) -> None:
        """Incrémente le compteur d'infos."""
        self.info_count += 1
    
    def increment_debug(self) -> None:
        """Incrémente le compteur de debug."""
        self.debug_count += 1
    
    def get_metrics(self) -> dict:
        """Retourne les métriques actuelles.
        
        Returns:
            Dict contenant les métriques
        """
        return {
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "info_count": self.info_count,
            "debug_count": self.debug_count,
            "last_error": self.last_error,
            "last_error_time": self.last_error_time
        }

# Instance globale pour les métriques
metrics = LogMetrics() 