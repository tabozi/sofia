# Guide de Déploiement

Ce document décrit le processus de déploiement du chatbot LinkedIn automatisé.

## Prérequis

- Linux/Unix ou WSL2 sur Windows
- Accès root/sudo
- Connexion Internet

## Structure du Déploiement

Le déploiement utilise Docker et se compose de quatre services principaux :
1. Application principale (Python)
2. Base de données (PostgreSQL)
3. Monitoring (Prometheus)
4. Visualisation (Grafana)

## Configuration

1. Copier le fichier d'exemple `.env` :
```bash
cp .env.example .env
```

2. Configurer les variables d'environnement dans `.env` :
```env
# Base de données
DB_PASSWORD=votre_mot_de_passe_db

# Grafana
GRAFANA_PASSWORD=votre_mot_de_passe_grafana

# LinkedIn API
LINKEDIN_CLIENT_ID=votre_client_id
LINKEDIN_CLIENT_SECRET=votre_client_secret

# IA
OPENAI_API_KEY=votre_cle_api
ANTHROPIC_API_KEY=votre_cle_api
```

## Déploiement

1. Rendre les scripts exécutables :
```bash
chmod +x deploy.sh backup.sh
```

2. Lancer le déploiement :
```bash
./deploy.sh
```

Le script va :
- Vérifier/installer Docker et Docker Compose
- Créer les répertoires nécessaires
- Configurer Prometheus
- Démarrer tous les services

## Accès aux Services

- Application : http://localhost:8501
- Grafana : http://localhost:3000
- Prometheus : http://localhost:9090

## Sauvegardes

Les sauvegardes sont gérées par le script `backup.sh` qui :
- Sauvegarde la base de données
- Sauvegarde les données de l'application
- Sauvegarde les configurations
- Conserve 7 jours d'historique

Pour exécuter une sauvegarde manuelle :
```bash
./backup.sh
```

Pour automatiser les sauvegardes quotidiennes, ajouter au crontab :
```bash
0 2 * * * /chemin/vers/backup.sh
```

## Monitoring

### Prometheus
- Collecte les métriques de l'application
- Intervalle de scraping : 15 secondes
- Configuration dans `prometheus/prometheus.yml`

### Grafana
- Interface de visualisation des métriques
- Accès initial :
  - Utilisateur : admin
  - Mot de passe : défini dans `.env`

## Maintenance

### Mise à jour des conteneurs
```bash
docker-compose pull
docker-compose up -d
```

### Logs
```bash
# Tous les services
docker-compose logs

# Service spécifique
docker-compose logs app
```

### Arrêt des services
```bash
docker-compose down
```

## Restauration

Pour restaurer une sauvegarde :
1. Arrêter les services :
```bash
docker-compose down
```

2. Restaurer la base de données :
```bash
cat backups/db_backup_YYYYMMDD_HHMMSS.sql | docker exec -i linkedin-bot-db-1 psql -U postgres -d linkedin_bot
```

3. Restaurer les données :
```bash
tar -xzf backups/data_backup_YYYYMMDD_HHMMSS.tar.gz
```

4. Redémarrer les services :
```bash
docker-compose up -d
``` 