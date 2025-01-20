"""
Implémentation du modèle OpenAI
"""
from typing import Dict, Any, Optional
import openai
from src.ai.models.base import BaseAIModel
from src.config import settings

class OpenAIModel(BaseAIModel):
    """Modèle utilisant l'API OpenAI"""
    
    def __init__(self, config: Dict[str, Any]):
        self.model_name = "gpt-4"  # ou "gpt-3.5-turbo" selon la config
        super().__init__(config)
    
    def initialize(self) -> None:
        """Initialise le client OpenAI"""
        openai.api_key = settings.OPENAI_API_KEY
        
    async def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Génère une réponse via OpenAI"""
        messages = []
        
        if context and context.get('conversation_history'):
            messages.extend(context['conversation_history'])
            
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model_name,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Erreur OpenAI: {str(e)}")
            return ""
            
    async def generate_post(self, topic: str, context: Optional[Dict] = None) -> str:
        """Génère un post LinkedIn via OpenAI"""
        prompt = f"""
        Crée un post LinkedIn professionnel sur le sujet suivant : {topic}
        Le post doit être :
        - Engageant et informatif
        - Entre 100 et 200 mots
        - Inclure des hashtags pertinents
        - Avoir un ton professionnel mais accessible
        """
        return await self.generate_response(prompt, context)
        
    async def analyze_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Analyse un message pour en extraire les intentions et le contexte"""
        prompt = f"""
        Analyse ce message LinkedIn et fournis les informations suivantes au format JSON :
        Message : {message}
        
        Extrais :
        - L'intention principale
        - Le ton du message
        - Les points clés
        - Les actions requises
        """
        response = await self.generate_response(prompt, context)
        # TODO: Parser la réponse JSON
        return {"raw_analysis": response} 