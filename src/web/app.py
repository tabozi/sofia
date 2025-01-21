"""Application Streamlit pour l'interface utilisateur."""

import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from src.database.manager import db
from src.database.models import User, Conversation, Message, Post, AIInteraction
from src.database.crud import (
    get_recent_interactions,
    get_active_conversations,
    get_conversation_messages,
    get_scheduled_posts,
    get_ai_usage_stats,
    get_ai_interactions_stats
)
from src.utils import log_metrics, perf_metrics

# Configuration de la page
st.set_page_config(
    page_title="LinkedIn Bot Dashboard",
    page_icon="🤖",
    layout="wide"
)

# Menu de navigation statique
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "",
    ["Dashboard", "Conversations", "Publications", "Configuration", "Statistiques", "Monitoring"],
    key="nav"
)

# Pages
if page == "Dashboard":
    st.title("🤖 Dashboard LinkedIn Bot")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with db.get_session() as session:
        # Statistiques IA sur les dernières 24h
        stats = get_ai_interactions_stats(
            session,
            datetime.utcnow() - timedelta(days=1),
            datetime.utcnow()
        )
        
        col1.metric(
            "Interactions IA (24h)",
            stats['total_interactions']
        )
        col2.metric(
            "Taux de succès IA",
            f"{stats['success_rate']*100:.1f}%"
        )
        col3.metric(
            "Coût total",
            f"{stats['total_cost']/1000:.2f}€"
        )
        col4.metric(
            "Temps moyen",
            f"{stats['average_duration']:.0f}ms"
        )
    
    # Graphiques
    st.subheader("Activité récente")
    
    # Graphique des interactions par modèle
    fig = px.pie(
        values=list(stats['by_model'].values()),
        names=list(stats['by_model'].keys()),
        title="Répartition des modèles d'IA"
    )
    st.plotly_chart(fig)

elif page == "Conversations":
    st.title("💬 Gestion des Conversations")
    
    with db.get_session() as session:
        # Liste des conversations actives
        conversations = get_active_conversations(session, user_id=1)  # TODO: user_id dynamique
        
        for conv in conversations:
            with st.expander(f"Conversation {conv.linkedin_conversation_id}"):
                messages = get_conversation_messages(session, conv.id)
                for msg in messages:
                    if msg.is_from_bot:
                        st.info(msg.content)
                    else:
                        st.text(msg.content)
                
                # Formulaire de réponse
                with st.form(f"reply_form_{conv.id}"):
                    response = st.text_area("Réponse")
                    if st.form_submit_button("Envoyer"):
                        st.success("Message envoyé !")  # TODO: Implémenter l'envoi

elif page == "Publications":
    st.title("📝 Gestion des Publications")
    
    # Nouvelle publication
    with st.form("new_post"):
        content = st.text_area("Contenu du post")
        scheduled_time = st.datetime_input(
            "Date de publication",
            value=datetime.now() + timedelta(hours=1)
        )
        
        if st.form_submit_button("Programmer"):
            st.success("Post programmé !")  # TODO: Implémenter la programmation
    
    # Posts programmés
    st.subheader("Publications programmées")
    with db.get_session() as session:
        posts = get_scheduled_posts(session)
        for post in posts:
            st.text(f"📅 {post.scheduled_for}: {post.content[:100]}...")

elif page == "Configuration":
    st.title("⚙️ Configuration")
    
    # Configuration LinkedIn
    st.subheader("LinkedIn API")
    with st.form("linkedin_config"):
        client_id = st.text_input("Client ID")
        client_secret = st.text_input("Client Secret", type="password")
        if st.form_submit_button("Sauvegarder"):
            st.success("Configuration sauvegardée !")  # TODO: Implémenter la sauvegarde
    
    # Configuration IA
    st.subheader("Intelligence Artificielle")
    with st.form("ai_config"):
        default_model = st.selectbox(
            "Modèle par défaut",
            ["gpt-4", "claude-2", "llama2"]
        )
        temperature = st.slider("Température", 0.0, 1.0, 0.7)
        if st.form_submit_button("Sauvegarder"):
            st.success("Configuration sauvegardée !")  # TODO: Implémenter la sauvegarde

elif page == "Statistiques":
    st.title("📊 Statistiques")
    
    # Période
    period = st.selectbox(
        "Période",
        ["24 heures", "7 jours", "30 jours"]
    )
    
    # Statistiques IA
    with db.get_session() as session:
        if period == "24 heures":
            delta = timedelta(days=1)
        elif period == "7 jours":
            delta = timedelta(days=7)
        else:
            delta = timedelta(days=30)
            
        stats = get_ai_interactions_stats(
            session,
            datetime.utcnow() - delta,
            datetime.utcnow()
        )
    
    # Affichage des statistiques
    st.subheader("Utilisation de l'IA")
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=stats['success_rate'] * 100,
            title={'text': "Taux de succès"},
            gauge={'axis': {'range': [0, 100]}}
        ))
        st.plotly_chart(fig)
    
    with col2:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=stats['total_cost'] / 1000,
            title={'text': "Coût total (€)"},
            gauge={'axis': {'range': [0, 10]}}
        ))
        st.plotly_chart(fig)

elif page == "Monitoring":
    st.title("🔍 Monitoring Système")
    
    # Métriques de performance
    st.header("Performance")
    col1, col2, col3 = st.columns(3)
    
    metrics = perf_metrics.get_metrics()
    system_metrics = perf_metrics.get_system_metrics()
    
    with col1:
        st.metric("Uptime", f"{metrics['uptime_seconds']:.0f}s")
        st.metric("Appels API", metrics['api_calls'])
    
    with col2:
        st.metric("Taux d'erreur", f"{metrics['error_rate']*100:.1f}%")
        st.metric("Temps moyen", f"{metrics['avg_response_time']*1000:.0f}ms")
    
    with col3:
        st.metric("CPU", f"{system_metrics['cpu_percent']}%")
        st.metric("Mémoire", f"{system_metrics['memory_percent']}%")
    
    # Graphique d'utilisation système
    st.subheader("Utilisation Système")
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = system_metrics['cpu_percent'],
        title = {'text': "CPU"},
        domain = {'x': [0, 0.3], 'y': [0, 1]},
        gauge = {'axis': {'range': [0, 100]}}
    ))
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = system_metrics['memory_percent'],
        title = {'text': "Mémoire"},
        domain = {'x': [0.35, 0.65], 'y': [0, 1]},
        gauge = {'axis': {'range': [0, 100]}}
    ))
    fig.add_trace(go.Indicator(
        mode = "gauge+number",
        value = system_metrics['disk_percent'],
        title = {'text': "Disque"},
        domain = {'x': [0.7, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [0, 100]}}
    ))
    fig.update_layout(height=250)
    st.plotly_chart(fig, use_container_width=True)
    
    # Métriques de logging
    st.header("Logs")
    log_data = log_metrics.get_metrics()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Erreurs", log_data['error_count'])
        st.metric("Warnings", log_data['warning_count'])
    with col2:
        st.metric("Info", log_data['info_count'])
        st.metric("Debug", log_data['debug_count'])
    
    if log_data['last_error']:
        st.error(f"Dernière erreur ({log_data['last_error_time']}): {log_data['last_error']}")
    
    # Affichage des derniers logs
    st.subheader("Derniers logs")
    try:
        with open("logs/linkedin_bot.log", "r") as f:
            logs = f.readlines()[-10:]  # Afficher les 10 dernières lignes
            for log in logs:
                st.text(log.strip())
    except Exception as e:
        st.warning(f"Impossible de lire les logs: {str(e)}") 