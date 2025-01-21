#!/bin/bash

# Nettoyer l'environnement existant
if [ -d "venv" ]; then
    echo "Suppression de l'ancien environnement virtuel..."
    rm -rf venv
fi

# Vérifier si l'environnement virtuel existe
echo "Création de l'environnement virtuel..."
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Mettre à jour pip
echo "Mise à jour de pip..."
python3 -m pip install --upgrade pip

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

# Vérifier les installations critiques
python3 -c "import plotly" || {
    echo "Erreur: plotly n'a pas été installé correctement"
    exit 1
}
python3 -c "import sqlalchemy" || {
    echo "Erreur: sqlalchemy n'a pas été installé correctement"
    exit 1
}
python3 -c "import streamlit" || {
    echo "Erreur: streamlit n'a pas été installé correctement"
    exit 1
}

# Créer le dossier logs s'il n'existe pas
if [ ! -d "logs" ]; then
    echo "Création du dossier logs..."
    mkdir logs
fi

# Créer le dossier .streamlit dans le home si nécessaire
if [ ! -d ~/.streamlit ]; then
    echo "Création du dossier .streamlit dans le home..."
    mkdir -p ~/.streamlit
fi

# Copier la configuration Streamlit dans le home
echo "Configuration de Streamlit..."
cat > ~/.streamlit/config.toml << EOL
[browser]
gatherUsageStats = false

[theme]
primaryColor = "#0077B5"  # Couleur LinkedIn
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#262626"
font = "sans serif"
EOL

# Créer le dossier .streamlit local pour le projet
if [ ! -d .streamlit ]; then
    echo "Création du dossier .streamlit local..."
    mkdir .streamlit
fi

# Copier la configuration locale
cp ~/.streamlit/config.toml .streamlit/

# Vérifier si le fichier .env existe
if [ ! -f ".env" ]; then
    echo "Création du fichier .env de test..."
    cp .env.example .env
    # Ajouter des données de test
    cat >> .env << EOL

# Configuration de test
DEBUG_MODE=true
LOG_LEVEL=DEBUG

# Base de données de test
DATABASE_URL=sqlite:///./test.db

# Clés API de test
LINKEDIN_CLIENT_ID=test_client_id
LINKEDIN_CLIENT_SECRET=test_secret
LINKEDIN_ACCESS_TOKEN=test_token

# Configuration IA de test
OPENAI_API_KEY=test_openai_key
ANTHROPIC_API_KEY=test_anthropic_key
OLLAMA_API_URL=http://localhost:11434
EOL
fi

# Nettoyer l'ancienne base de données de test si elle existe
if [ -f "test.db" ]; then
    echo "Suppression de l'ancienne base de données de test..."
    rm test.db
fi

# Créer la base de données de test avec quelques données
echo "Initialisation de la base de données de test..."
python << EOL
from src.utils import init_monitoring
from src.database.manager import db
from src.database.crud import create_user, create_conversation, create_message, create_post, create_ai_interaction
from datetime import datetime, timedelta

# Initialiser le monitoring
logger = init_monitoring()
logger.info("Starting test environment setup")

# Créer les tables
db.create_database()

# Créer un utilisateur de test
with db.get_session() as session:
    # Utilisateur
    user = create_user(
        session,
        linkedin_id="test123",
        name="Test User",
        profile_url="https://linkedin.com/in/testuser"
    )
    
    # Conversation
    conv = create_conversation(
        session,
        user_id=user.id,
        linkedin_conversation_id="conv123",
        conversation_metadata={"topic": "test"}
    )
    
    # Messages
    create_message(
        session,
        conversation_id=conv.id,
        content="Bonjour, comment puis-je vous aider ?",
        linkedin_message_id="msg1",
        is_from_bot=True,
        message_metadata={"intent": "greeting"}
    )
    
    create_message(
        session,
        conversation_id=conv.id,
        content="J'ai une question sur vos services",
        linkedin_message_id="msg2",
        is_from_bot=False,
        message_metadata={"intent": "question"}
    )
    
    # Posts
    create_post(
        session,
        user_id=user.id,
        content="Post de test programmé",
        scheduled_for=datetime.utcnow() + timedelta(hours=2),
        post_metadata={"type": "article"}
    )
    
    # Interactions IA
    for model in ["gpt-4", "claude-2", "llama2"]:
        create_ai_interaction(
            session,
            model_name=model,
            prompt="Test prompt",
            response="Test response",
            tokens_used=100,
            duration_ms=500,
            cost=10,
            interaction_metadata={"version": "1.0"}
        )

logger.info("Test environment setup completed")
EOL

echo "Lancement de l'interface..."
export PYTHONPATH=$PWD
streamlit run src/web/app.py 