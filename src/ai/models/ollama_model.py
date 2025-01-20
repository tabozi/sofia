"""
Implémentation du modèle Ollama (local)
"""
from typing import Dict, Any, Optional
import json
import aiohttp
from src.ai.models.base import BaseAIModel
from src.config import settings

class OllamaModel(BaseAIModel):
    """Modèle utilisant Ollama en local"""
    
    def __init__(self, config: Dict[str, Any]):
        self.model_name = config.get('model_name', 'llama2')
        self.api_url = settings.OLLAMA_API_URL
        super().__init__(config)
    
    def initialize(self) -> None:
        """Initialise les paramètres Ollama"""
        self.generate_endpoint = f"{self.api_url}/api/generate"
        
    async def _make_request(self, prompt: str) -> str:
        """Effectue une requête à l'API Ollama"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    self.generate_endpoint,
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "num_predict": 500
                        }
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('response', '')
                    else:
                        print(f"Erreur Ollama: Status {response.status}")
                        return ""
            except Exception as e:
                print(f"Erreur de connexion Ollama: {str(e)}")
                return ""
    
    async def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Génère une réponse via Ollama"""
        if context and context.get('conversation_history'):
            # Ajoute l'historique au prompt
            history = "\n".join([f"{msg['role']}: {msg['content']}" 
                               for msg in context['conversation_history']])
            prompt = f"{history}\nUser: {prompt}"
            
        return await self._make_request(prompt)
            
    async def generate_post(self, topic: str, context: Optional[Dict] = None) -> str:
        """Génère un post LinkedIn via Ollama"""
        prompt = f"""
        Crée un post LinkedIn professionnel sur le sujet : {topic}
        
        Instructions :
        1. Le post doit faire entre 100 et 200 mots
        2. Utilise un ton professionnel mais accessible
        3. Structure : introduction, développement, conclusion
        4. Ajoute des hashtags pertinents
        5. Le contenu doit être engageant et informatif
        
        Format ta réponse pour qu'elle soit directement publiable sur LinkedIn.
        """
        return await self.generate_response(prompt, context)
        
    async def analyze_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Analyse un message pour en extraire les informations clés"""
        prompt = f"""
        Analyse ce message LinkedIn et fournis une réponse au format JSON :
        
        Message : {message}
        
        {{"
            "intention": "intention principale",
            "ton": "ton du message",
            "points_cles": ["point 1", "point 2", ...],
            "actions": ["action 1", "action 2", ...],
            "priorite": "1-5"
        }}
        
        Assure-toi que la réponse est un JSON valide.
        """
        response = await self.generate_response(prompt, context)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"raw_analysis": response} 