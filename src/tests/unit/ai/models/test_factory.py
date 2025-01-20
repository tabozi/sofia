"""
Tests unitaires pour la factory des modèles d'IA
"""
import pytest
from src.ai.models.factory import AIModelFactory
from src.ai.models.openai_model import OpenAIModel
from src.ai.models.anthropic_model import AnthropicModel
from src.ai.models.ollama_model import OllamaModel

def test_create_openai_model():
    """Test la création d'un modèle OpenAI"""
    model = AIModelFactory.create_model("openai")
    assert isinstance(model, OpenAIModel)
    assert model.model_name == "gpt-4"

def test_create_anthropic_model():
    """Test la création d'un modèle Anthropic"""
    model = AIModelFactory.create_model("anthropic")
    assert isinstance(model, AnthropicModel)
    assert model.model_name == "claude-2"

def test_create_ollama_model():
    """Test la création d'un modèle Ollama"""
    config = {"model_name": "llama2"}
    model = AIModelFactory.create_model("ollama", config)
    assert isinstance(model, OllamaModel)
    assert model.model_name == "llama2"

def test_create_default_model():
    """Test la création du modèle par défaut"""
    model = AIModelFactory.create_model()
    # Le modèle par défaut est défini dans settings.DEFAULT_AI_MODEL
    assert isinstance(model, (OpenAIModel, AnthropicModel, OllamaModel))

def test_create_invalid_model():
    """Test la gestion des erreurs pour un type de modèle invalide"""
    with pytest.raises(ValueError) as exc_info:
        AIModelFactory.create_model("invalid_model")
    assert "Type de modèle non supporté" in str(exc_info.value) 