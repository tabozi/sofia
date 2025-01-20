"""
Factory pour la création des modèles d'IA
"""
from typing import Dict, Any, Optional
from src.ai.models.base import BaseAIModel
from src.ai.models.openai_model import OpenAIModel
from src.ai.models.anthropic_model import AnthropicModel
from src.ai.models.ollama_model import OllamaModel
from src.config import settings

class AIModelFactory:
    """Factory pour créer les instances de modèles d'IA"""
    
    @staticmethod
    def create_model(model_type: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> BaseAIModel:
        """
        Crée une instance du modèle d'IA spécifié
        
        Args:
            model_type: Type de modèle ('openai', 'anthropic', 'ollama')
            config: Configuration spécifique au modèle
            
        Returns:
            Instance de BaseAIModel
        """
        if config is None:
            config = {}
            
        model_type = model_type or settings.DEFAULT_AI_MODEL
        
        if model_type == "openai":
            return OpenAIModel(config)
        elif model_type == "anthropic":
            return AnthropicModel(config)
        elif model_type == "ollama":
            return OllamaModel(config)
        else:
            raise ValueError(f"Type de modèle non supporté : {model_type}") 