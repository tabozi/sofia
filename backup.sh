#!/bin/bash

# Configuration
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_CONTAINER="linkedin-bot-db-1"
DB_NAME="linkedin_bot"
DB_USER="postgres"

# Créer le répertoire de sauvegarde s'il n'existe pas
mkdir -p "$BACKUP_DIR"

# Sauvegarde de la base de données
echo "Sauvegarde de la base de données..."
docker exec $DB_CONTAINER pg_dump -U $DB_USER $DB_NAME > "$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# Sauvegarde des données de l'application
echo "Sauvegarde des données de l'application..."
tar -czf "$BACKUP_DIR/data_backup_$TIMESTAMP.tar.gz" ./data

# Sauvegarde des configurations
echo "Sauvegarde des configurations..."
tar -czf "$BACKUP_DIR/config_backup_$TIMESTAMP.tar.gz" .env prometheus/prometheus.yml

# Nettoyage des anciennes sauvegardes (garde les 7 derniers jours)
find "$BACKUP_DIR" -type f -mtime +7 -delete

echo "Sauvegarde terminée !"
echo "Fichiers sauvegardés dans $BACKUP_DIR :"
ls -lh "$BACKUP_DIR" 