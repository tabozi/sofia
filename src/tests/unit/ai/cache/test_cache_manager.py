"""
Tests unitaires pour le gestionnaire de cache
"""
import pytest
import json
from datetime import datetime, timedelta
from pathlib import Path
from src.ai.cache.cache_manager import AIResponseCache

@pytest.fixture
def cache():
    """Fixture pour créer une instance de test du cache"""
    # Utilise une base de données temporaire pour les tests
    db_path = "test_cache.db"
    cache = AIResponseCache(db_path)
    yield cache
    # Nettoyage après les tests
    Path(db_path).unlink(missing_ok=True)

def test_cache_initialization(cache):
    """Test l'initialisation du cache"""
    assert cache.db_path == "test_cache.db"
    # Vérifie que la table a été créée
    with cache._get_connection() as conn:
        cursor = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='ai_cache'
        """)
        assert cursor.fetchone() is not None

def test_generate_cache_key(cache):
    """Test la génération des clés de cache"""
    # Test sans contexte
    key1 = cache._generate_cache_key("gpt-4", "test prompt")
    key2 = cache._generate_cache_key("gpt-4", "test prompt")
    assert key1 == key2  # Même clé pour mêmes paramètres
    
    # Test avec contexte
    context = {"test": "value"}
    key3 = cache._generate_cache_key("gpt-4", "test prompt", context)
    assert key1 != key3  # Clé différente avec contexte

def test_set_and_get(cache):
    """Test l'écriture et la lecture du cache"""
    model_name = "test-model"
    prompt = "test prompt"
    response = "test response"
    
    # Test écriture
    cache.set(model_name, prompt, response)
    
    # Test lecture
    cached = cache.get(model_name, prompt)
    assert cached == response

def test_cache_with_context(cache):
    """Test le cache avec contexte"""
    context = {"history": ["previous message"]}
    cache.set("test-model", "prompt", "response", context)
    
    # Même prompt, contexte différent
    assert cache.get("test-model", "prompt", {"history": ["different"]}) is None
    
    # Même prompt, même contexte
    assert cache.get("test-model", "prompt", context) == "response"

def test_cache_expiration(cache):
    """Test l'expiration du cache"""
    # Ajoute une entrée qui expire dans 1 heure
    cache.set("test-model", "prompt", "response", ttl_hours=1)
    assert cache.get("test-model", "prompt") == "response"
    
    # Modifie la date d'expiration pour la rendre expirée
    with cache._get_connection() as conn:
        conn.execute("""
            UPDATE ai_cache 
            SET expires_at = datetime('now', '-1 hour')
            WHERE model_name = 'test-model'
        """)
    
    # Vérifie que l'entrée expirée n'est pas retournée
    assert cache.get("test-model", "prompt") is None

def test_usage_count(cache):
    """Test le compteur d'utilisation"""
    cache.set("test-model", "prompt", "response")
    
    # Premier accès
    cache.get("test-model", "prompt")
    stats = cache.get_stats()
    assert stats["total_hits"] == 1
    
    # Deuxième accès
    cache.get("test-model", "prompt")
    stats = cache.get_stats()
    assert stats["total_hits"] == 2

def test_clear_expired(cache):
    """Test le nettoyage des entrées expirées"""
    # Ajoute une entrée expirée
    cache.set("test-model", "prompt1", "response1", ttl_hours=1)
    with cache._get_connection() as conn:
        conn.execute("""
            UPDATE ai_cache 
            SET expires_at = datetime('now', '-1 hour')
            WHERE model_name = 'test-model'
        """)
    
    # Ajoute une entrée valide
    cache.set("test-model", "prompt2", "response2", ttl_hours=24)
    
    # Nettoie les entrées expirées
    deleted = cache.clear_expired()
    assert deleted == 1  # Une entrée supprimée
    
    # Vérifie que seule l'entrée valide reste
    assert cache.get("test-model", "prompt1") is None
    assert cache.get("test-model", "prompt2") == "response2"

def test_get_stats(cache):
    """Test les statistiques du cache"""
    # Ajoute quelques entrées
    cache.set("model1", "prompt1", "response1")
    cache.set("model2", "prompt2", "response2")
    
    # Accède plusieurs fois
    cache.get("model1", "prompt1")
    cache.get("model1", "prompt1")
    cache.get("model2", "prompt2")
    
    stats = cache.get_stats()
    assert stats["total_entries"] == 2
    assert stats["total_hits"] == 3
    assert stats["avg_hits_per_entry"] == 1.5
    assert "total_size_bytes" in stats 