"""
Point d'entrée principal de l'application
"""
import asyncio
from typing import Optional
from src.config import settings
from src.linkedin.client import LinkedInClient
from src.ai.models.base import BaseAIModel
from src.ai.models.factory import AIModelFactory

class SofiaBot:
    """Classe principale du bot Sofia"""
    
    def __init__(self, model_type: Optional[str] = None):
        self.linkedin_client = LinkedInClient()
        self.model_type = model_type or settings.DEFAULT_AI_MODEL
        self.ai_model: Optional[BaseAIModel] = None
        
    async def initialize(self):
        """Initialise les composants du bot"""
        # Authentification LinkedIn
        if not await self.linkedin_client.authenticate():
            raise Exception("Échec de l'authentification LinkedIn")
            
        # Initialisation du modèle d'IA
        try:
            self.ai_model = AIModelFactory.create_model(self.model_type)
        except Exception as e:
            raise Exception(f"Échec de l'initialisation du modèle d'IA: {str(e)}")
        
    async def process_message(self, message: str) -> str:
        """Traite un message et génère une réponse"""
        if not self.ai_model:
            raise Exception("Modèle d'IA non initialisé")
            
        # Analyse du message
        analysis = await self.ai_model.analyze_message(message)
        
        # Génération de la réponse
        context = {"message_analysis": analysis}
        response = await self.ai_model.generate_response(message, context)
        
        return response
        
    async def create_post(self, topic: str) -> str:
        """Crée et publie un post sur LinkedIn"""
        if not self.ai_model:
            raise Exception("Modèle d'IA non initialisé")
            
        # Génération du contenu
        content = await self.ai_model.generate_post(topic)
        
        # Publication sur LinkedIn
        if content:
            await self.linkedin_client.create_post(content)
            
        return content
        
    async def run(self):
        """Lance le bot"""
        await self.initialize()
        
        # TODO: Implémenter la boucle principale du bot
        print(f"Bot initialisé avec le modèle : {self.model_type}")
        
async def main():
    """Fonction principale"""
    bot = SofiaBot()
    try:
        await bot.run()
    except Exception as e:
        print(f"Erreur lors de l'exécution du bot: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 