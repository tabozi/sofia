"""
Tests unitaires pour le décorateur de cache
"""
import pytest
from unittest.mock import patch, MagicMock
from src.ai.cache.decorators import cached_response
from src.ai.cache.cache_manager import AIResponseCache
from typing import Optional, Dict

class MockModel:
    """Classe de test pour simuler un modèle d'IA"""
    def __init__(self):
        self.model_name = "test-model"
        self.call_count = 0
    
    @cached_response(ttl_hours=1)
    async def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Méthode de test avec cache"""
        self.call_count += 1
        return f"Response {self.call_count}"

@pytest.fixture
def mock_model():
    """Fixture pour créer une instance de test du modèle"""
    return MockModel()

@pytest.fixture
def mock_cache():
    """Fixture pour créer un mock du cache"""
    with patch('src.ai.cache.decorators.AIResponseCache') as mock:
        cache_instance = MagicMock()
        mock.return_value = cache_instance
        yield cache_instance

@pytest.mark.asyncio
async def test_cached_response_hit(mock_model, mock_cache):
    """Test quand la réponse est dans le cache"""
    # Configure le mock pour simuler un hit dans le cache
    mock_cache.get.return_value = "Cached response"
    
    # Premier appel
    response = await mock_model.generate_response("test prompt")
    assert response == "Cached response"
    assert mock_model.call_count == 0  # La méthode originale n'est pas appelée
    
    # Vérifie que le cache a été consulté
    mock_cache.get.assert_called_once_with(
        "test-model",
        "test prompt",
        None
    )

@pytest.mark.asyncio
async def test_cached_response_miss(mock_model, mock_cache):
    """Test quand la réponse n'est pas dans le cache"""
    # Configure le mock pour simuler un miss dans le cache
    mock_cache.get.return_value = None
    
    # Premier appel
    response = await mock_model.generate_response("test prompt")
    assert response == "Response 1"
    assert mock_model.call_count == 1  # La méthode originale est appelée
    
    # Vérifie que la réponse a été mise en cache
    mock_cache.set.assert_called_once_with(
        "test-model",
        "test prompt",
        "Response 1",
        None,
        1  # ttl_hours
    )

@pytest.mark.asyncio
async def test_cached_response_with_context(mock_model, mock_cache):
    """Test le cache avec un contexte"""
    context = {"test": "value"}
    mock_cache.get.return_value = None
    
    await mock_model.generate_response("test prompt", context)
    
    # Vérifie que le contexte est utilisé pour la clé de cache
    mock_cache.get.assert_called_once_with(
        "test-model",
        "test prompt",
        context
    )

@pytest.mark.asyncio
async def test_cached_response_error_handling(mock_model, mock_cache):
    """Test la gestion des erreurs du cache"""
    # Simule une erreur lors de l'accès au cache
    mock_cache.get.side_effect = Exception("Cache error")
    
    # La méthode devrait quand même fonctionner
    response = await mock_model.generate_response("test prompt")
    assert response == "Response 1"
    assert mock_model.call_count == 1

@pytest.mark.asyncio
async def test_different_ttl(mock_model, mock_cache):
    """Test différentes durées de vie du cache"""
    
    @cached_response(ttl_hours=48)
    async def long_cached_method(self, prompt: str, context: Optional[Dict] = None) -> str:
        return "Long cached response"
    
    # Ajoute la méthode à l'instance
    mock_model.long_cached_method = long_cached_method.__get__(mock_model)
    
    await mock_model.long_cached_method("test prompt")
    
    # Vérifie que le TTL correct est utilisé
    mock_cache.set.assert_called_once_with(
        "test-model",
        "test prompt",
        "Long cached response",
        None,
        48  # ttl_hours
    ) 