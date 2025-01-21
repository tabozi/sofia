# Guide de Test de l'Interface Utilisateur

## Vue d'ensemble

Ce guide explique comment tester l'interface utilisateur du chatbot LinkedIn en utilisant un environnement de test isolé.

## Scripts disponibles

### 1. Script de test (`scripts/test_ui.sh`)

Ce script configure et lance l'environnement de test complet.

```bash
./scripts/test_ui.sh
```

#### Fonctionnalités du script :

1. Configuration de l'environnement
   - Création d'un environnement virtuel Python
   - Installation des dépendances
   - Configuration du fichier `.env` avec des données de test

2. Initialisation de la base de données
   - Création d'une base SQLite de test
   - Génération de données d'exemple :
     - Un utilisateur test
     - Une conversation avec messages
     - Un post programmé
     - Des interactions IA pour différents modèles

3. Lancement de l'interface
   - Démarrage du serveur Streamlit
   - Ouverture automatique dans le navigateur

### 2. Script de nettoyage (`scripts/cleanup_test.sh`)

Ce script nettoie l'environnement de test.

```bash
./scripts/cleanup_test.sh
```

#### Actions de nettoyage :
- Arrêt du serveur Streamlit
- Suppression de la base de données de test
- Nettoyage du cache Streamlit

## Données de test

### Utilisateur test
- ID LinkedIn : "test123"
- Nom : "Test User"
- Profil : "https://linkedin.com/in/testuser"

### Conversation test
- ID : "conv123"
- Messages :
  1. Bot : "Bonjour, comment puis-je vous aider ?"
  2. Utilisateur : "J'ai une question sur vos services"

### Post test
- Contenu : "Post de test programmé"
- Programmé : 2 heures dans le futur

### Interactions IA
Pour chaque modèle (gpt-4, claude-2, llama2) :
- Prompt : "Test prompt"
- Réponse : "Test response"
- Tokens : 100
- Durée : 500ms
- Coût : 0.01€

## Configuration de test

```env
# Mode debug activé
DEBUG_MODE=true
LOG_LEVEL=DEBUG

# Base de données SQLite locale
DATABASE_URL=sqlite:///./test.db

# Clés API factices
LINKEDIN_CLIENT_ID=test_client_id
LINKEDIN_CLIENT_SECRET=test_secret
LINKEDIN_ACCESS_TOKEN=test_token

# Clés IA factices
OPENAI_API_KEY=test_openai_key
ANTHROPIC_API_KEY=test_anthropic_key
OLLAMA_API_URL=http://localhost:11434
```

## Procédure de test

1. Préparation
   ```bash
   # Rendre les scripts exécutables
   chmod +x scripts/test_ui.sh scripts/cleanup_test.sh
   ```

2. Lancement des tests
   ```bash
   ./scripts/test_ui.sh
   ```

3. Tests manuels
   - Vérifier le dashboard
   - Explorer les conversations
   - Tester la création de posts
   - Vérifier les configurations
   - Explorer les statistiques

4. Nettoyage
   ```bash
   ./scripts/cleanup_test.sh
   ```

## Points à tester

### Dashboard
- [ ] Affichage des métriques
- [ ] Graphiques d'activité
- [ ] Mise à jour des données

### Conversations
- [ ] Liste des conversations
- [ ] Affichage des messages
- [ ] Formulaire de réponse
- [ ] Statut des messages

### Publications
- [ ] Création de post
- [ ] Programmation
- [ ] Liste des posts programmés

### Configuration
- [ ] Formulaire LinkedIn
- [ ] Paramètres IA
- [ ] Sauvegarde des configurations

### Statistiques
- [ ] Sélection de période
- [ ] Graphiques de performance
- [ ] Calcul des coûts

## Résolution des problèmes

### Erreurs courantes

1. Erreur de base de données
   ```
   Solution : Supprimer test.db et relancer le script
   ```

2. Port Streamlit occupé
   ```
   Solution : ./scripts/cleanup_test.sh puis relancer
   ```

3. Dépendances manquantes
   ```
   Solution : pip install -r requirements.txt
   ```

### Vérification de l'état

Pour vérifier l'état de l'environnement de test :
```bash
# Vérifier le processus Streamlit
ps aux | grep streamlit

# Vérifier la base de données
ls -l test.db

# Vérifier les logs
tail -f ~/.streamlit/logs/
``` 