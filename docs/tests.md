# Documentation des Tests

## Structure des Tests

```
src/tests/
├── unit/                     # Tests unitaires
│   ├── ai/
│   │   └── models/          # Tests des modèles d'IA
│   │       ├── test_factory.py
│   │       ├── test_openai_model.py
│   │       ├── test_anthropic_model.py
│   │       └── test_ollama_model.py
│   ├── linkedin/            # Tests LinkedIn (à venir)
│   └── config/              # Tests de configuration (à venir)
├── integration/             # Tests d'intégration (à venir)
└── conftest.py             # Fixtures partagées
```

## Types de Tests

### Tests Unitaires
Tests qui vérifient le comportement individuel des composants :
- Factory des modèles d'IA
- Modèles d'IA (OpenAI, Anthropic, Ollama)
- Système de cache
- Décorateurs

### Tests de Performance
Tests qui mesurent les performances et l'utilisation des ressources :
- Temps de réponse
- Utilisation mémoire
- Scalabilité
- Comportement sous charge
- Gestion de la concurrence

### Tests d'Intégration (à venir)
Tests qui vérifient l'interaction entre les composants.

## Configuration

Le projet utilise `pytest` comme framework de test. La configuration se trouve dans `pytest.ini` :

```ini
[pytest]
testpaths = src/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v -ra -q
markers =
    unit: Tests unitaires
    integration: Tests d'intégration
    slow: Tests lents
    asyncio: Tests asynchrones
    performance: Tests de performance
```

## Exécution des Tests

### Tous les tests
```bash
pytest
```

### Tests par catégorie
```bash
pytest -m unit          # Tests unitaires
pytest -m integration   # Tests d'intégration
pytest -m performance   # Tests de performance
```

### Tests spécifiques
```bash
# Tests des modèles d'IA
pytest src/tests/unit/ai/models/

# Tests du cache
pytest src/tests/unit/ai/cache/
pytest src/tests/performance/test_cache_performance.py
```

## Tests de Performance

### Configuration Requise
- psutil : Pour mesurer l'utilisation mémoire
- Base de données de test dédiée
- Environnement isolé

### Métriques Mesurées
1. **Temps de Réponse**
   - Temps moyen par opération
   - Latence sous charge
   - Distribution des temps de réponse

2. **Utilisation des Ressources**
   - Consommation mémoire
   - Utilisation CPU
   - Taille du cache

3. **Scalabilité**
   - Impact de la taille du cache
   - Performance avec différentes charges
   - Limites du système

4. **Concurrence**
   - Accès simultanés
   - Contentions
   - Cohérence des données

### Seuils de Performance
- Écriture : < 10ms par opération
- Lecture : < 5ms par opération
- Concurrence : < 2s pour 100 opérations simultanées
- Nettoyage : < 1s pour 1000 entrées

### Rapports de Performance
Les tests génèrent des rapports détaillés incluant :
```
Performance d'écriture:
- Temps total: X.XX secondes
- Temps moyen par entrée: X.XX ms
- Mémoire utilisée: X.XX MB

Performance de lecture:
- Temps total: X.XX secondes
- Temps moyen par lecture: X.XX ms
- Taux de hits: XX.X%

Impact de la taille du cache:
- Taille: XXXX entrées
- Temps de lecture moyen: X.XX ms
- Temps d'écriture moyen: X.XX ms
```

## Fixtures Disponibles

Les fixtures sont définies dans `src/tests/conftest.py` :

### `mock_config`
Configuration de base pour les tests des modèles d'IA :
```python
{
    "openai": {
        "model_name": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 500
    },
    # ... autres configurations
}
```

### `mock_conversation_history`
Historique de conversation pour les tests :
```python
{
    "conversation_history": [
        {"role": "user", "content": "Bonjour"},
        {"role": "assistant", "content": "Bonjour ! Comment puis-je vous aider ?"},
        {"role": "user", "content": "J'ai une question"}
    ]
}
```

### `mock_message_analysis`
Analyse de message type pour les tests :
```python
{
    "intention": "question",
    "ton": "professionnel",
    "points_cles": ["point 1", "point 2"],
    "actions": ["action 1"],
    "priorite": 3
}
```

## Ajout de Nouveaux Tests

1. Créer un nouveau fichier de test dans le dossier approprié
2. Nommer le fichier `test_*.py`
3. Utiliser les fixtures existantes ou en créer de nouvelles dans `conftest.py`
4. Décorer les tests asynchrones avec `@pytest.mark.asyncio`
5. Utiliser les marqueurs appropriés pour catégoriser les tests

### Exemple de Structure de Test
```python
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def my_fixture():
    # Configuration du fixture
    return something

@pytest.mark.asyncio
async def test_my_async_function(my_fixture):
    # Corps du test
    assert something == expected

def test_my_sync_function(my_fixture):
    # Corps du test
    assert something == expected
```

## Bonnes Pratiques

### Tests Unitaires
1. **Isolation** : Chaque test doit être indépendant
2. **Mocking** : Simuler les dépendances externes
3. **Nommage** : Noms descriptifs et clairs
4. **Documentation** : Docstring pour chaque test
5. **Assertions** : Précises et explicites
6. **Fixtures** : Réutiliser quand possible

### Tests de Performance
1. **Environnement Contrôlé** : Tests dans un environnement stable
2. **Données Représentatives** : Utiliser des volumes de données réalistes
3. **Métriques Claires** : Définir des seuils de performance explicites
4. **Reproductibilité** : Tests reproductibles et stables
5. **Monitoring** : Collecter toutes les métriques pertinentes
6. **Nettoyage** : Nettoyer l'environnement après les tests

## Maintenance des Tests

1. **Exécution Régulière**
   - Avant chaque commit
   - Dans l'intégration continue
   - Après les modifications majeures

2. **Maintenance**
   - Mettre à jour les seuils de performance
   - Adapter aux nouvelles fonctionnalités
   - Nettoyer les tests obsolètes

3. **Monitoring**
   - Suivre les tendances de performance
   - Identifier les régressions
   - Optimiser selon les résultats 