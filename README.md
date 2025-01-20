# LinkedIn Chatbot Automatisé

Bot intelligent pour l'automatisation des publications et la gestion des messages sur LinkedIn.

## Installation

1. Cloner le repository
```bash
git clone [url_du_repository]
cd linkedin-chatbot
```

2. Créer et activer l'environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configuration
- Copier le fichier `.env.example` vers `.env`
- Remplir les variables d'environnement dans `.env`

## Configuration LinkedIn API

1. Créer une application sur [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Obtenir les identifiants API (Client ID et Client Secret)
3. Configurer les URLs de redirection
4. Ajouter les identifiants dans le fichier `.env`

## Utilisation

[Instructions à venir]

## Structure du Projet

```
linkedin-chatbot/
├── venv/
├── src/
├── tests/
├── .env
├── requirements.txt
└── README.md
``` 