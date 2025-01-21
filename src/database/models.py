"""Modèles SQLAlchemy pour la base de données."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """Modèle pour les utilisateurs LinkedIn."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    linkedin_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(100))
    profile_url = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    conversations = relationship("Conversation", back_populates="user")
    posts = relationship("Post", back_populates="user")

class Conversation(Base):
    """Modèle pour les conversations."""
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    linkedin_conversation_id = Column(String, unique=True, nullable=False)
    conversation_metadata = Column(JSON)  # Renommé de metadata à conversation_metadata
    status = Column(String(20), default='active')  # active, archived, blocked
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_message_at = Column(DateTime)

    # Relations
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    """Modèle pour les messages individuels."""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    linkedin_message_id = Column(String(50), unique=True)
    content = Column(Text, nullable=False)
    is_from_bot = Column(Boolean, default=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    delivered_at = Column(DateTime)
    read_at = Column(DateTime)
    message_metadata = Column(JSON)  # Renommé de metadata à message_metadata

    # Relations
    conversation = relationship("Conversation", back_populates="messages")
    ai_interactions = relationship("AIInteraction", back_populates="message")

class Post(Base):
    """Modèle pour les publications LinkedIn."""
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    linkedin_post_id = Column(String(50), unique=True)
    content = Column(Text, nullable=False)
    status = Column(String(20), default='draft')  # draft, scheduled, published, failed
    scheduled_for = Column(DateTime)
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    post_metadata = Column(JSON)  # Renommé de metadata à post_metadata

    # Relations
    user = relationship("User", back_populates="posts")
    ai_interactions = relationship("AIInteraction", back_populates="post")

class AIInteraction(Base):
    """Modèle pour tracker les interactions avec l'IA."""
    __tablename__ = 'ai_interactions'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('messages.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    model_name = Column(String(50), nullable=False)  # openai, anthropic, ollama
    prompt = Column(Text, nullable=False)
    response = Column(Text)
    tokens_used = Column(Integer)
    duration_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    cost = Column(Integer)  # en millièmes de centime
    success = Column(Boolean, default=True)
    error = Column(Text)
    interaction_metadata = Column(JSON)  # Renommé de metadata à interaction_metadata

    # Relations
    message = relationship("Message", back_populates="ai_interactions")
    post = relationship("Post", back_populates="ai_interactions") 