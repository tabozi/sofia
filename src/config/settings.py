"""
Configuration principale de l'application
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

# Chargement des variables d'environnement
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

# Configuration LinkedIn
LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
LINKEDIN_ACCESS_TOKEN = os.getenv('LINKEDIN_ACCESS_TOKEN')
LINKEDIN_REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI')

# Configuration IA
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
LLAMA_MODEL_PATH = os.getenv('LLAMA_MODEL_PATH')
DEFAULT_AI_MODEL = os.getenv('DEFAULT_AI_MODEL', 'openai')

# Configuration Base de données
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./linkedin_bot.db')
DATABASE_ECHO = False
DATABASE_POOL_SIZE = 5
DATABASE_MAX_OVERFLOW = 10

# Configuration Application
DEBUG = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class Settings(BaseSettings):
    """Configuration de l'application."""
    
    # Mode debug et logging
    debug_mode: bool = Field(default=False, description="Mode debug de l'application")
    log_level: str = Field(default="INFO", description="Niveau de logging")
    
    # Base de données
    database_url: str = Field(
        default="sqlite:///./app.db",
        description="URL de connexion à la base de données"
    )
    
    # LinkedIn API
    linkedin_client_id: str = Field(default="test_id", description="Client ID LinkedIn")
    linkedin_client_secret: str = Field(default="test_secret", description="Client Secret LinkedIn")
    linkedin_access_token: str = Field(default="test_token", description="Token d'accès LinkedIn")
    
    # OpenAI
    openai_api_key: Optional[str] = Field(default=None, description="Clé API OpenAI")
    
    # Anthropic
    anthropic_api_key: Optional[str] = Field(default=None, description="Clé API Anthropic")
    
    # Ollama
    ollama_api_url: str = Field(
        default="http://localhost:11434",
        description="URL de l'API Ollama"
    )
    
    # Configuration par défaut
    default_ai_model: str = Field(default="openai", description="Modèle IA par défaut")
    
    class Config:
        """Configuration de Pydantic."""
        env_file = ".env"
        case_sensitive = False
        extra = "allow"  # Permet les champs supplémentaires

@lru_cache()
def get_settings() -> Settings:
    """Retourne une instance singleton des paramètres."""
    return Settings() 