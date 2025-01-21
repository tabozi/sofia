"""Gestionnaire de base de données SQLAlchemy."""

from contextlib import contextmanager
from typing import Generator
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from .models import Base
from ..config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class DatabaseManager:
    """Gestionnaire de base de données."""

    def __init__(self):
        """Initialise la connexion à la base de données."""
        settings = get_settings()
        
        # Création du moteur SQLAlchemy
        self.engine = create_engine(
            settings.database_url,  # Utilisation de database_url au lieu de DATABASE_URL
            echo=False,
            pool_size=5,
            max_overflow=10
        )
        
        # Configuration de la session
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def create_database(self) -> None:
        """Crée toutes les tables dans la base de données."""
        Base.metadata.create_all(bind=self.engine)

    def drop_database(self) -> None:
        """Supprime toutes les tables de la base de données."""
        Base.metadata.drop_all(bind=self.engine)

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Fournit une session de base de données dans un contexte.
        
        Yields:
            Session: Session SQLAlchemy
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Erreur de base de données : {str(e)}")
            raise
        finally:
            session.close()

    def check_connection(self) -> bool:
        """Vérifie la connexion à la base de données.
        
        Returns:
            bool: True si la connexion est établie, False sinon
        """
        try:
            with self.get_session() as session:
                session.execute("SELECT 1")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Erreur de connexion à la base de données : {str(e)}")
            return False

# Instance globale du gestionnaire de base de données
db = DatabaseManager() 