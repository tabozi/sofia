#!/bin/bash

echo "Nettoyage de l'environnement de test..."

# Arrêter Streamlit si en cours d'exécution
if pgrep -f streamlit > /dev/null; then
    echo "Arrêt de Streamlit..."
    pkill -f streamlit
fi

# Supprimer la base de données de test
if [ -f "test.db" ]; then
    echo "Suppression de la base de données de test..."
    rm -f test.db
fi

# Nettoyer le cache Streamlit
if [ -d ~/.streamlit ]; then
    echo "Nettoyage du cache Streamlit..."
    rm -rf ~/.streamlit/
fi

# Supprimer l'environnement virtuel
if [ -d "venv" ]; then
    echo "Suppression de l'environnement virtuel..."
    rm -rf venv
fi

# Supprimer les fichiers Python compilés
echo "Suppression des fichiers Python compilés..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -r {} +

echo "Environnement de test nettoyé !" 