# Documentation de l'Interface Utilisateur

## Vue d'ensemble

L'interface utilisateur est construite avec Streamlit et offre un dashboard complet pour gérer le chatbot LinkedIn. Elle est composée de cinq sections principales :

1. Dashboard
2. Conversations
3. Publications
4. Configuration
5. Statistiques

## Fonctionnalités

### Dashboard

Le dashboard principal affiche :
- Métriques clés des dernières 24 heures
  - Nombre total d'interactions IA
  - Taux de succès des interactions
  - Coût total des appels API
  - Temps de réponse moyen
- Graphiques d'activité
  - Répartition des modèles d'IA utilisés

### Conversations

La section conversations permet de :
- Voir toutes les conversations actives
- Lire l'historique des messages
- Répondre aux messages
- Voir le statut des messages (envoyé, livré, lu)

### Publications

Gestion des publications LinkedIn :
- Création de nouveaux posts
- Programmation des publications
- Vue d'ensemble des posts programmés
- Statut des publications

### Configuration

Paramètres du système :
- Configuration de l'API LinkedIn
  - Client ID
  - Client Secret
- Paramètres IA
  - Choix du modèle par défaut
  - Réglage de la température
  - Limites d'utilisation

### Statistiques

Analyses détaillées :
- Statistiques d'utilisation de l'IA
- Métriques de performance
- Coûts d'utilisation
- Filtrage par période (24h, 7j, 30j)

## Installation

1. Installer les dépendances :
```bash
pip install streamlit plotly
```

2. Lancer l'application :
```bash
streamlit run src/web/app.py
```

## Utilisation

### Navigation

- Utilisez la barre latérale pour naviguer entre les sections
- Chaque section est organisée de manière intuitive avec des formulaires et des visualisations

### Gestion des conversations

1. Ouvrez la section "Conversations"
2. Cliquez sur une conversation pour l'expandre
3. Lisez l'historique des messages
4. Utilisez le formulaire en bas pour répondre

### Création de publications

1. Allez dans la section "Publications"
2. Remplissez le formulaire de nouvelle publication
3. Choisissez une date de publication
4. Cliquez sur "Programmer"

### Configuration

1. Accédez à la section "Configuration"
2. Remplissez les informations d'API LinkedIn
3. Ajustez les paramètres d'IA selon vos besoins
4. Sauvegardez les modifications

### Analyse des statistiques

1. Ouvrez la section "Statistiques"
2. Sélectionnez la période d'analyse
3. Consultez les graphiques et indicateurs
4. Exportez les données si nécessaire

## Sécurité

- Les secrets (API keys, tokens) sont masqués dans l'interface
- Les sessions sont gérées de manière sécurisée
- Les données sensibles ne sont jamais affichées en clair

## Personnalisation

L'interface peut être personnalisée en modifiant :
- Les couleurs et le thème
- Les métriques affichées
- Les types de graphiques
- La disposition des éléments

## Dépannage

### Problèmes courants

1. Page blanche
   - Vérifiez que Streamlit est bien installé
   - Vérifiez la connexion à la base de données

2. Graphiques non affichés
   - Vérifiez l'installation de Plotly
   - Vérifiez que les données sont disponibles

3. Erreurs de configuration
   - Vérifiez les variables d'environnement
   - Vérifiez les permissions de la base de données 