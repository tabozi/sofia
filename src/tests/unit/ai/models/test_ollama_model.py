"""
Tests unitaires pour le modèle Ollama
"""
import pytest
from unittest.mock import patch, MagicMock
import aiohttp
from src.ai.models.ollama_model import OllamaModel

@pytest.fixture
def ollama_model():
    """Fixture pour créer une instance du modèle Ollama"""
    config = {
        "model_name": "llama2",
        "temperature": 0.7,
        "max_tokens": 500
    }
    model = OllamaModel(config)
    return model

@pytest.mark.asyncio
async def test_make_request(ollama_model):
    """Test la requête à l'API Ollama"""
    mock_response = MagicMock()
    mock_response.status = 200
    mock_response.json = MagicMock(return_value={"response": "Test response"})
    
    mock_session = MagicMock()
    mock_session.post = MagicMock(return_value=MagicMock(__aenter__=MagicMock(return_value=mock_response)))
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        response = await ollama_model._make_request("Test prompt")
        assert response == "Test response"

@pytest.mark.asyncio
async def test_make_request_error(ollama_model):
    """Test la gestion des erreurs de l'API Ollama"""
    mock_response = MagicMock()
    mock_response.status = 500
    
    mock_session = MagicMock()
    mock_session.post = MagicMock(return_value=MagicMock(__aenter__=MagicMock(return_value=mock_response)))
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        response = await ollama_model._make_request("Test prompt")
        assert response == ""

@pytest.mark.asyncio
async def test_generate_response(ollama_model):
    """Test la génération de réponse"""
    with patch.object(ollama_model, '_make_request', return_value="Test response"):
        response = await ollama_model.generate_response("Test prompt")
        assert response == "Test response"

@pytest.mark.asyncio
async def test_generate_response_with_context(ollama_model):
    """Test la génération de réponse avec contexte"""
    context = {
        "conversation_history": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"}
        ]
    }
    
    with patch.object(ollama_model, '_make_request', return_value="Test response with context"):
        response = await ollama_model.generate_response("Test prompt", context)
        assert response == "Test response with context"

@pytest.mark.asyncio
async def test_generate_post(ollama_model):
    """Test la génération de post LinkedIn"""
    with patch.object(ollama_model, '_make_request', return_value="Test LinkedIn post"):
        response = await ollama_model.generate_post("AI Technology")
        assert response == "Test LinkedIn post"

@pytest.mark.asyncio
async def test_analyze_message_valid_json(ollama_model):
    """Test l'analyse de message avec réponse JSON valide"""
    mock_json = '{"intention": "test", "ton": "professionnel", "points_cles": ["test"], "actions": [], "priorite": "3"}'
    
    with patch.object(ollama_model, '_make_request', return_value=mock_json):
        response = await ollama_model.analyze_message("Test message")
        assert "intention" in response
        assert response["intention"] == "test"

@pytest.mark.asyncio
async def test_analyze_message_invalid_json(ollama_model):
    """Test l'analyse de message avec réponse JSON invalide"""
    with patch.object(ollama_model, '_make_request', return_value="Invalid JSON"):
        response = await ollama_model.analyze_message("Test message")
        assert "raw_analysis" in response
        assert response["raw_analysis"] == "Invalid JSON"

def test_endpoint_configuration(ollama_model):
    """Test la configuration de l'endpoint"""
    assert ollama_model.generate_endpoint == f"{ollama_model.api_url}/api/generate" 