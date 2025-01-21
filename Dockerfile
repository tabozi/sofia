# Utiliser une image Python officielle comme base
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY src/ ./src/
COPY .env.example ./.env

# Exposer le port (à ajuster selon votre configuration)
EXPOSE 8501

# Commande par défaut pour démarrer l'application
CMD ["python", "src/main.py"] 