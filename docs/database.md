# Documentation de la Base de Données

## Structure

La base de données utilise PostgreSQL avec SQLAlchemy comme ORM. Elle est composée de cinq modèles principaux :

### 1. User
Stocke les informations des utilisateurs LinkedIn.
```python
- id : Identifiant unique
- linkedin_id : ID LinkedIn de l'utilisateur
- name : Nom de l'utilisateur
- profile_url : URL du profil LinkedIn
- created_at : Date de création
- updated_at : Date de mise à jour
```

### 2. Conversation
Gère les conversations avec les contacts.
```python
- id : Identifiant unique
- user_id : Référence vers l'utilisateur
- linkedin_conversation_id : ID de la conversation LinkedIn
- status : État (active, archived, blocked)
- created_at : Date de création
- updated_at : Date de mise à jour
- last_message_at : Date du dernier message
- metadata : Données supplémentaires (JSON)
```

### 3. Message
Stocke les messages individuels.
```python
- id : Identifiant unique
- conversation_id : Référence vers la conversation
- linkedin_message_id : ID du message LinkedIn
- content : Contenu du message
- is_from_bot : Indique si le message vient du bot
- sent_at : Date d'envoi
- delivered_at : Date de livraison
- read_at : Date de lecture
- metadata : Données supplémentaires (JSON)
```

### 4. Post
Gère les publications LinkedIn.
```python
- id : Identifiant unique
- user_id : Référence vers l'utilisateur
- linkedin_post_id : ID du post LinkedIn
- content : Contenu du post
- status : État (draft, scheduled, published, failed)
- scheduled_for : Date de publication programmée
- published_at : Date de publication effective
- created_at : Date de création
- updated_at : Date de mise à jour
- metadata : Données supplémentaires (JSON)
```

### 5. AIInteraction
Trace les interactions avec les modèles d'IA.
```python
- id : Identifiant unique
- message_id : Référence vers le message (optionnel)
- post_id : Référence vers le post (optionnel)
- model_name : Nom du modèle utilisé
- prompt : Prompt envoyé
- response : Réponse reçue
- tokens_used : Nombre de tokens utilisés
- duration_ms : Durée de l'interaction
- cost : Coût en millièmes de centime
- success : Succès de l'interaction
- error : Message d'erreur éventuel
- metadata : Données supplémentaires (JSON)
```

## Utilisation

### Initialisation
```python
from database.manager import db

# Création des tables
db.create_database()

# Vérification de la connexion
if db.check_connection():
    print("Connexion établie")
```

### Exemples d'utilisation

1. Création d'un utilisateur :
```python
from database.crud import create_user

with db.get_session() as session:
    user = create_user(
        session,
        linkedin_id="123456",
        name="John Doe",
        profile_url="https://linkedin.com/in/johndoe"
    )
```

2. Création d'une conversation :
```python
from database.crud import create_conversation

with db.get_session() as session:
    conversation = create_conversation(
        session,
        user_id=user.id,
        linkedin_conversation_id="conv123",
        metadata={"topic": "business"}
    )
```

3. Ajout d'un message :
```python
from database.crud import create_message

with db.get_session() as session:
    message = create_message(
        session,
        conversation_id=conversation.id,
        content="Bonjour !",
        linkedin_message_id="msg123",
        is_from_bot=True
    )
```

4. Création d'un post :
```python
from database.crud import create_post
from datetime import datetime, timedelta

with db.get_session() as session:
    post = create_post(
        session,
        user_id=user.id,
        content="Mon post LinkedIn",
        scheduled_for=datetime.utcnow() + timedelta(days=1)
    )
```

5. Tracking des interactions IA :
```python
from database.crud import create_ai_interaction

with db.get_session() as session:
    interaction = create_ai_interaction(
        session,
        model_name="gpt-4",
        prompt="Générer une réponse",
        response="Réponse générée",
        message_id=message.id,
        tokens_used=150,
        duration_ms=1200,
        cost=50  # 0.05€
    )
```

## Sauvegardes

Les sauvegardes sont gérées automatiquement par le script `backup.sh` qui :
- Sauvegarde la base de données quotidiennement
- Conserve un historique de 7 jours
- Stocke les sauvegardes dans le répertoire `backups/`

Pour restaurer une sauvegarde :
```bash
# 1. Arrêter les services
docker-compose down

# 2. Restaurer la base de données
cat backups/db_backup_YYYYMMDD_HHMMSS.sql | docker exec -i linkedin-bot-db-1 psql -U postgres -d linkedin_bot

# 3. Redémarrer les services
docker-compose up -d
``` 