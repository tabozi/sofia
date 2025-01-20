"""
Configuration principale de l'application
"""
import os
from pathlib import Path
from dotenv import load_dotenv

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

# Configuration Application
DEBUG = os.getenv('DEBUG_MODE', 'False').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO') 