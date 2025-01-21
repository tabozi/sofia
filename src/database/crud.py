"""Opérations CRUD pour les modèles de base de données."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from .models import User, Conversation, Message, Post, AIInteraction

# Opérations User
def create_user(session: Session, linkedin_id: str, name: str, profile_url: str) -> User:
    """Crée un nouvel utilisateur."""
    user = User(
        linkedin_id=linkedin_id,
        name=name,
        profile_url=profile_url
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user(session: Session, user_id: int) -> Optional[User]:
    """Récupère un utilisateur par son ID."""
    return session.query(User).filter(User.id == user_id).first()

def get_user_by_linkedin_id(session: Session, linkedin_id: str) -> Optional[User]:
    """Récupère un utilisateur par son ID LinkedIn."""
    return session.query(User).filter(User.linkedin_id == linkedin_id).first()

# Opérations Conversation
def create_conversation(
    session: Session,
    user_id: int,
    linkedin_conversation_id: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Conversation:
    """Crée une nouvelle conversation."""
    conversation = Conversation(
        user_id=user_id,
        linkedin_conversation_id=linkedin_conversation_id,
        metadata=metadata or {}
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation

def get_active_conversations(session: Session) -> List[Conversation]:
    """Récupère les conversations actives."""
    return session.query(Conversation)\
        .filter(Conversation.status == 'active')\
        .order_by(Conversation.last_message_at.desc())\
        .all()

# Opérations Message
def create_message(
    session: Session,
    conversation_id: int,
    content: str,
    linkedin_message_id: str,
    is_from_bot: bool = False,
    metadata: Optional[Dict[str, Any]] = None
) -> Message:
    """Crée un nouveau message."""
    message = Message(
        conversation_id=conversation_id,
        content=content,
        linkedin_message_id=linkedin_message_id,
        is_from_bot=is_from_bot,
        metadata=metadata or {}
    )
    session.add(message)
    
    # Mise à jour du last_message_at de la conversation
    conversation = session.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()
    if conversation:
        conversation.last_message_at = datetime.utcnow()
    
    session.commit()
    session.refresh(message)
    return message

def get_conversation_messages(
    session: Session,
    conversation_id: int
) -> List[Message]:
    """Récupère les messages d'une conversation."""
    return session.query(Message)\
        .filter(Message.conversation_id == conversation_id)\
        .order_by(Message.sent_at)\
        .all()

# Opérations Post
def create_post(
    session: Session,
    user_id: int,
    content: str,
    scheduled_for: Optional[datetime] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Post:
    """Crée un nouveau post."""
    post = Post(
        user_id=user_id,
        content=content,
        scheduled_for=scheduled_for,
        metadata=metadata or {}
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

def get_scheduled_posts(session: Session) -> List[Post]:
    """Récupère les posts programmés."""
    return session.query(Post)\
        .filter(
            and_(
                Post.status == 'scheduled',
                Post.scheduled_for > datetime.utcnow()
            )
        )\
        .order_by(Post.scheduled_for)\
        .all()

# Opérations AIInteraction
def create_ai_interaction(
    session: Session,
    model_name: str,
    prompt: str,
    response: Optional[str] = None,
    message_id: Optional[int] = None,
    post_id: Optional[int] = None,
    tokens_used: Optional[int] = None,
    duration_ms: Optional[int] = None,
    cost: Optional[int] = None,
    success: bool = True,
    error: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> AIInteraction:
    """Crée une nouvelle interaction IA."""
    interaction = AIInteraction(
        model_name=model_name,
        prompt=prompt,
        response=response,
        message_id=message_id,
        post_id=post_id,
        tokens_used=tokens_used,
        duration_ms=duration_ms,
        cost=cost,
        success=success,
        error=error,
        metadata=metadata or {}
    )
    session.add(interaction)
    session.commit()
    session.refresh(interaction)
    return interaction

def get_recent_interactions(
    session: Session,
    start_date: datetime,
    end_date: datetime
) -> List[AIInteraction]:
    """Récupère les interactions récentes dans une période donnée."""
    return session.query(AIInteraction).filter(
        and_(
            AIInteraction.created_at >= start_date,
            AIInteraction.created_at <= end_date
        )
    ).all()

def get_ai_usage_stats(
    session: Session,
    start_date: datetime,
    end_date: datetime
) -> Dict:
    """Calcule les statistiques d'utilisation de l'IA."""
    interactions = get_recent_interactions(session, start_date, end_date)
    
    if not interactions:
        return {
            "total_interactions": 0,
            "success_rate": 0,
            "total_cost": 0,
            "average_duration": 0,
            "by_model": {}
        }
    
    # Calcul des statistiques
    total = len(interactions)
    success = sum(1 for i in interactions if i.success)
    total_cost = sum(i.cost for i in interactions)
    avg_duration = sum(i.duration_ms for i in interactions) / total
    
    # Répartition par modèle
    models = {}
    for interaction in interactions:
        models[interaction.model_name] = models.get(interaction.model_name, 0) + 1
    
    return {
        "total_interactions": total,
        "success_rate": success / total,
        "total_cost": total_cost,
        "average_duration": avg_duration,
        "by_model": models
    }

def get_ai_interactions_stats(
    session: Session,
    start_date: datetime,
    end_date: datetime
) -> Dict:
    """Alias pour get_ai_usage_stats pour la compatibilité."""
    return get_ai_usage_stats(session, start_date, end_date) 