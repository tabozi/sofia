#!/bin/bash

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "Docker n'est pas installé. Installation..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose n'est pas installé. Installation..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Créer les répertoires nécessaires
mkdir -p data prometheus grafana

# Copier le fichier d'exemple .env s'il n'existe pas
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Veuillez configurer le fichier .env avec vos paramètres"
    exit 1
fi

# Créer la configuration Prometheus
cat > prometheus/prometheus.yml << EOL
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'linkedin-bot'
    static_configs:
      - targets: ['app:8501']
EOL

# Arrêter les conteneurs existants
docker-compose down

# Construire et démarrer les conteneurs
docker-compose up -d --build

# Vérifier l'état des conteneurs
docker-compose ps

echo "Déploiement terminé !"
echo "Application : http://localhost:8501"
echo "Grafana : http://localhost:3000"
echo "Prometheus : http://localhost:9090" 