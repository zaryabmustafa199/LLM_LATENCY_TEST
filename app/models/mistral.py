import logging
from httpx import AsyncClient, Timeout
from app.config import settings

logger = logging.getLogger(__name__)

class MistralHandler:
    """Handler for Mistral 7B API interactions via HuggingFace Serverless Inference."""
    
    def __init__(self):
        self.model_id = settings.mistral_model_id
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
        # We also support the router URL for chat completions
        self.chat_url = "https://router.huggingface.co/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {settings.huggingface_token}",
            "Content-Type": "application/json"
        }
        self.client = AsyncClient(timeout=Timeout(30.0))
        
    async def generate(self, prompt: str) -> str:
        """
        Sends a generation request to the Mistral model.
        Uses the standard chat completion format.
        """
        payload = {
            "model": self.model_id,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": settings.max_new_tokens,
            "temperature": settings.temperature
        }
        
        try:
            logger.info(f"Sending request to Mistral ({self.model_id})")
            response = await self.client.post(
                self.chat_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
            
        except Exception as e:
            logger.error(f"Mistral inference failed: {str(e)}")
            # Attach response text for debugging if available
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response details: {e.response.text}")
                raise Exception(f"Mistral inference failed: {str(e)}\n\nDetails:\n{e.response.text}")
            raise Exception(f"Mistral inference failed: {str(e)}")
