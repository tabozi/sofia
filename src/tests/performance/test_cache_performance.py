"""
Tests de performance pour le système de cache
"""
import pytest
import time
import asyncio
import psutil
import random
import string
from typing import List, Dict
from pathlib import Path
from src.ai.cache.cache_manager import AIResponseCache

def generate_random_string(length: int) -> str:
    """Génère une chaîne aléatoire de longueur donnée"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def measure_memory_usage() -> float:
    """Mesure l'utilisation mémoire du processus actuel"""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024  # En MB

@pytest.fixture
def perf_cache():
    """Fixture pour créer une instance de test du cache"""
    db_path = "perf_test_cache.db"
    cache = AIResponseCache(db_path)
    yield cache
    Path(db_path).unlink(missing_ok=True)

@pytest.mark.performance
def test_write_performance(perf_cache):
    """Test les performances en écriture"""
    num_entries = 1000
    start_memory = measure_memory_usage()
    start_time = time.time()
    
    # Écrit un grand nombre d'entrées
    for i in range(num_entries):
        prompt = generate_random_string(50)
        response = generate_random_string(200)
        perf_cache.set("test-model", prompt, response)
    
    end_time = time.time()
    end_memory = measure_memory_usage()
    
    write_time = end_time - start_time
    memory_used = end_memory - start_memory
    
    print(f"\nPerformance d'écriture:")
    print(f"Temps total: {write_time:.2f} secondes")
    print(f"Temps moyen par entrée: {(write_time/num_entries)*1000:.2f} ms")
    print(f"Mémoire utilisée: {memory_used:.2f} MB")
    
    assert write_time/num_entries < 0.01  # Max 10ms par écriture

@pytest.mark.performance
def test_read_performance(perf_cache):
    """Test les performances en lecture"""
    # Prépare les données
    prompts = []
    for i in range(1000):
        prompt = generate_random_string(50)
        prompts.append(prompt)
        perf_cache.set("test-model", prompt, generate_random_string(200))
    
    # Test de lecture
    start_time = time.time()
    hits = 0
    
    for prompt in prompts:
        result = perf_cache.get("test-model", prompt)
        if result:
            hits += 1
    
    end_time = time.time()
    read_time = end_time - start_time
    
    print(f"\nPerformance de lecture:")
    print(f"Temps total: {read_time:.2f} secondes")
    print(f"Temps moyen par lecture: {(read_time/len(prompts))*1000:.2f} ms")
    print(f"Taux de hits: {(hits/len(prompts))*100:.1f}%")
    
    assert read_time/len(prompts) < 0.005  # Max 5ms par lecture

@pytest.mark.performance
def test_concurrent_access(perf_cache):
    """Test les accès concurrents"""
    async def concurrent_operation(operation: str, prompt: str):
        if operation == "write":
            perf_cache.set("test-model", prompt, generate_random_string(200))
        else:
            perf_cache.get("test-model", prompt)
    
    async def run_concurrent_operations():
        num_operations = 100
        operations = []
        
        # Mélange de lectures et écritures
        for i in range(num_operations):
            op = "write" if random.random() < 0.3 else "read"
            prompt = generate_random_string(50)
            operations.append(concurrent_operation(op, prompt))
        
        start_time = time.time()
        await asyncio.gather(*operations)
        end_time = time.time()
        
        return end_time - start_time
    
    total_time = asyncio.run(run_concurrent_operations())
    
    print(f"\nPerformance des accès concurrents:")
    print(f"Temps total: {total_time:.2f} secondes")
    
    assert total_time < 2.0  # Max 2 secondes pour 100 opérations concurrentes

@pytest.mark.performance
def test_cache_size_impact(perf_cache):
    """Test l'impact de la taille du cache sur les performances"""
    sizes = [100, 1000, 10000]
    results: Dict[int, Dict[str, float]] = {}
    
    for size in sizes:
        # Remplit le cache
        for i in range(size):
            prompt = generate_random_string(50)
            response = generate_random_string(200)
            perf_cache.set("test-model", prompt, response)
        
        # Mesure le temps de lecture
        start_time = time.time()
        for _ in range(100):
            perf_cache.get("test-model", generate_random_string(50))
        read_time = time.time() - start_time
        
        # Mesure le temps d'écriture
        start_time = time.time()
        for _ in range(100):
            perf_cache.set("test-model", generate_random_string(50), generate_random_string(200))
        write_time = time.time() - start_time
        
        results[size] = {
            "read_time": read_time,
            "write_time": write_time
        }
    
    print("\nImpact de la taille du cache:")
    for size, times in results.items():
        print(f"\nTaille du cache: {size} entrées")
        print(f"Temps de lecture moyen: {(times['read_time']/100)*1000:.2f} ms")
        print(f"Temps d'écriture moyen: {(times['write_time']/100)*1000:.2f} ms")
        
        # Les performances ne devraient pas se dégrader de manière significative
        assert times['read_time']/100 < 0.01  # Max 10ms par lecture
        assert times['write_time']/100 < 0.02  # Max 20ms par écriture

@pytest.mark.performance
def test_memory_cleanup(perf_cache):
    """Test l'efficacité du nettoyage de la mémoire"""
    # Remplit le cache avec des entrées expirées
    num_entries = 1000
    for i in range(num_entries):
        perf_cache.set("test-model", f"prompt{i}", generate_random_string(200), ttl_hours=0)
    
    time.sleep(1)  # Attend que les entrées expirent
    
    start_memory = measure_memory_usage()
    start_time = time.time()
    
    # Nettoie les entrées expirées
    deleted = perf_cache.clear_expired()
    
    end_time = time.time()
    end_memory = measure_memory_usage()
    
    cleanup_time = end_time - start_time
    memory_freed = start_memory - end_memory
    
    print(f"\nPerformance du nettoyage:")
    print(f"Temps de nettoyage: {cleanup_time:.2f} secondes")
    print(f"Mémoire libérée: {memory_freed:.2f} MB")
    print(f"Entrées supprimées: {deleted}")
    
    assert cleanup_time < 1.0  # Max 1 seconde pour le nettoyage
    assert deleted == num_entries  # Toutes les entrées doivent être supprimées 