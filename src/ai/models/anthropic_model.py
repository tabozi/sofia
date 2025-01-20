"""
Implémentation du modèle Anthropic Claude
"""
from typing import Dict, Any, Optional
import anthropic
from src.ai.models.base import BaseAIModel
from src.config import settings

class AnthropicModel(BaseAIModel):
    """Modèle utilisant l'API Anthropic Claude"""
    
    def __init__(self, config: Dict[str, Any]):
        self.model_name = "claude-2"
        super().__init__(config)
    
    def initialize(self) -> None:
        """Initialise le client Anthropic"""
        self.client = anthropic.Client(api_key=settings.ANTHROPIC_API_KEY)
        
    async def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Génère une réponse via Anthropic Claude"""
        try:
            # Formatage du prompt selon les recommandations Anthropic
            formatted_prompt = f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}"
            
            response = self.client.completion(
                prompt=formatted_prompt,
                model=self.model_name,
                max_tokens_to_sample=500,
                temperature=0.7
            )
            return response.completion
        except Exception as e:
            print(f"Erreur Anthropic: {str(e)}")
            return ""
            
    async def generate_post(self, topic: str, context: Optional[Dict] = None) -> str:
        """Génère un post LinkedIn via Anthropic Claude"""
        prompt = f"""
        En tant qu'expert en communication professionnelle, crée un post LinkedIn sur : {topic}
        
        Critères :
        - Longueur : 100-200 mots
        - Style : professionnel mais accessible
        - Structure : accroche + développement + conclusion
        - Inclure des hashtags pertinents
        
        Le post doit être directement publiable sur LinkedIn.
        """
        return await self.generate_response(prompt, context)
        
    async def analyze_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """Analyse un message pour en extraire les informations pertinentes"""
        prompt = f"""
        Analyse ce message LinkedIn de manière structurée :
        
        Message : {message}
        
        Fournis une analyse au format JSON avec :
        1. Intention principale du message
        2. Ton employé (formel, amical, etc.)
        3. Points clés abordés
        4. Actions attendues ou suggérées
        5. Niveau de priorité (1-5)
        """
        response = await self.generate_response(prompt, context)
        # TODO: Parser la réponse JSON
        return {"raw_analysis": response} 