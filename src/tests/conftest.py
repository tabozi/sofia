"""
Fixtures partagées pour les tests
"""
import pytest
from typing import Dict, Any

@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Configuration de base pour les tests"""
    return {
        "openai": {
            "model_name": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 500
        },
        "anthropic": {
            "model_name": "claude-2",
            "temperature": 0.7,
            "max_tokens": 500
        },
        "ollama": {
            "model_name": "llama2",
            "temperature": 0.7,
            "max_tokens": 500
        }
    }

@pytest.fixture
def mock_conversation_history() -> Dict[str, Any]:
    """Historique de conversation pour les tests"""
    return {
        "conversation_history": [
            {"role": "user", "content": "Bonjour"},
            {"role": "assistant", "content": "Bonjour ! Comment puis-je vous aider ?"},
            {"role": "user", "content": "J'ai une question"}
        ]
    }

@pytest.fixture
def mock_message_analysis() -> Dict[str, Any]:
    """Analyse de message pour les tests"""
    return {
        "intention": "question",
        "ton": "professionnel",
        "points_cles": ["point 1", "point 2"],
        "actions": ["action 1"],
        "priorite": 3
    } 