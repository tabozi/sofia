"""
Tests unitaires pour le modèle OpenAI
"""
import pytest
from unittest.mock import patch, MagicMock
from src.ai.models.openai_model import OpenAIModel

@pytest.fixture
def openai_model():
    """Fixture pour créer une instance du modèle OpenAI"""
    config = {"model_name": "gpt-4"}
    with patch('openai.api_key'):  # Mock l'API key pour les tests
        model = OpenAIModel(config)
        return model

@pytest.mark.asyncio
async def test_generate_response(openai_model):
    """Test la génération de réponse"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test response"))]
    
    with patch('openai.ChatCompletion.acreate', return_value=mock_response):
        response = await openai_model.generate_response("Test prompt")
        assert response == "Test response"

@pytest.mark.asyncio
async def test_generate_response_with_context(openai_model):
    """Test la génération de réponse avec contexte"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test response with context"))]
    
    context = {
        "conversation_history": [
            {"role": "user", "content": "Previous message"}
        ]
    }
    
    with patch('openai.ChatCompletion.acreate', return_value=mock_response):
        response = await openai_model.generate_response("Test prompt", context)
        assert response == "Test response with context"

@pytest.mark.asyncio
async def test_generate_post(openai_model):
    """Test la génération de post LinkedIn"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Test LinkedIn post"))]
    
    with patch('openai.ChatCompletion.acreate', return_value=mock_response):
        response = await openai_model.generate_post("AI Technology")
        assert response == "Test LinkedIn post"

@pytest.mark.asyncio
async def test_analyze_message(openai_model):
    """Test l'analyse de message"""
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content='{"intention": "test"}'))]
    
    with patch('openai.ChatCompletion.acreate', return_value=mock_response):
        response = await openai_model.analyze_message("Test message")
        assert "raw_analysis" in response

@pytest.mark.asyncio
async def test_error_handling(openai_model):
    """Test la gestion des erreurs"""
    with patch('openai.ChatCompletion.acreate', side_effect=Exception("API Error")):
        response = await openai_model.generate_response("Test prompt")
        assert response == "" 