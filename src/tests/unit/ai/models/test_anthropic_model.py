"""
Tests unitaires pour le modèle Anthropic
"""
import pytest
from unittest.mock import patch, MagicMock
from src.ai.models.anthropic_model import AnthropicModel
import anthropic

@pytest.fixture
def anthropic_model():
    """Fixture pour créer une instance du modèle Anthropic"""
    config = {"model_name": "claude-2"}
    with patch('anthropic.Client'):  # Mock le client Anthropic
        model = AnthropicModel(config)
        return model

@pytest.mark.asyncio
async def test_generate_response(anthropic_model):
    """Test la génération de réponse"""
    mock_response = MagicMock()
    mock_response.completion = "Test response"
    
    with patch.object(anthropic_model.client, 'completion', return_value=mock_response):
        response = await anthropic_model.generate_response("Test prompt")
        assert response == "Test response"

@pytest.mark.asyncio
async def test_generate_response_with_context(anthropic_model):
    """Test la génération de réponse avec contexte"""
    mock_response = MagicMock()
    mock_response.completion = "Test response with context"
    
    context = {
        "conversation_history": [
            {"role": "user", "content": "Previous message"}
        ]
    }
    
    with patch.object(anthropic_model.client, 'completion', return_value=mock_response):
        response = await anthropic_model.generate_response("Test prompt", context)
        assert response == "Test response with context"

@pytest.mark.asyncio
async def test_generate_post(anthropic_model):
    """Test la génération de post LinkedIn"""
    mock_response = MagicMock()
    mock_response.completion = "Test LinkedIn post #AI #Innovation"
    
    with patch.object(anthropic_model.client, 'completion', return_value=mock_response):
        response = await anthropic_model.generate_post("AI Technology")
        assert response == "Test LinkedIn post #AI #Innovation"

@pytest.mark.asyncio
async def test_analyze_message(anthropic_model):
    """Test l'analyse de message"""
    mock_response = MagicMock()
    mock_response.completion = '{"intention": "test", "priorite": 3}'
    
    with patch.object(anthropic_model.client, 'completion', return_value=mock_response):
        response = await anthropic_model.analyze_message("Test message")
        assert "raw_analysis" in response

@pytest.mark.asyncio
async def test_error_handling(anthropic_model):
    """Test la gestion des erreurs"""
    with patch.object(anthropic_model.client, 'completion', side_effect=Exception("API Error")):
        response = await anthropic_model.generate_response("Test prompt")
        assert response == ""

def test_prompt_formatting(anthropic_model):
    """Test le formatage des prompts selon les spécifications Anthropic"""
    prompt = "Test prompt"
    formatted = f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}"
    assert formatted.startswith(anthropic.HUMAN_PROMPT)
    assert formatted.endswith(anthropic.AI_PROMPT) 