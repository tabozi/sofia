"""
Classe de base pour tous les modèles d'IA
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.ai.cache.decorators import cached_response

class BaseAIModel(ABC):
    """Classe abstraite définissant l'interface pour tous les modèles d'IA"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = "base"
        self.initialize()
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialise le modèle et ses ressources"""
        pass
    
    @cached_response(ttl_hours=24)
    @abstractmethod
    async def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Génère une réponse basée sur le prompt et le contexte"""
        pass
    
    @cached_response(ttl_hours=48)
    @abstractmethod
    async def generate_post(self, topic: str, context: Optional[Dict] = None) -> str:
        """Génère un post LinkedIn basé sur le sujet et le contexte"""
        pass
    
    @cached_response(ttl_hours=24)
    @abstractmethod
    async def analyze_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Analyse un message et retourne les informations pertinentes"""
        pass
    
    def cleanup(self) -> None:
        """Nettoie les ressources utilisées par le modèle"""
        pass 