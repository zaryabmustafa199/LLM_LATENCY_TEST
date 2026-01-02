from huggingface_hub import AsyncInferenceClient
from fastapi import HTTPException, status
from app.config import settings

class GemmaHandler:
    def __init__(self):
        """Initialize the Gemma handler with HuggingFace client"""
        self.client = AsyncInferenceClient(
            token=settings.huggingface_token
        )
        self.model_id = settings.gemma_model_id
        print(f"Initialized GemmaHandler with model: {self.model_id}")

    async def generate(self, query: str) -> str:
        """
        Generate response from Gemma 2
        """
        try:
            messages = [{"role": "user", "content": query}]
            
            response = await self.client.chat_completion(
                messages=messages,
                model=self.model_id,
                max_tokens=settings.max_new_tokens,
                temperature=settings.temperature,
                seed=42
            )
            
            if not response or not response.choices:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Gemma model returned empty response"
                )
            
            return response.choices[0].message.content
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Gemma Inference Error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Gemma inference failed: {str(e)}"
            )
