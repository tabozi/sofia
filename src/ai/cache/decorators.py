"""
Décorateurs pour la gestion du cache
"""
from functools import wraps
from typing import Optional, Dict, Any, Callable
from src.ai.cache.cache_manager import AIResponseCache

def cached_response(ttl_hours: int = 24):
    """
    Décorateur pour mettre en cache les réponses des modèles d'IA
    
    Args:
        ttl_hours: Durée de vie du cache en heures
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(self, prompt: str, context: Optional[Dict] = None, *args, **kwargs):
            cache = AIResponseCache()
            
            # Tente de récupérer depuis le cache
            cached_response = cache.get(self.model_name, prompt, context)
            if cached_response is not None:
                return cached_response
            
            # Si pas en cache, exécute la fonction
            response = await func(self, prompt, context, *args, **kwargs)
            
            # Stocke dans le cache
            if response:
                cache.set(self.model_name, prompt, response, context, ttl_hours)
            
            return response
        return wrapper
    return decorator 