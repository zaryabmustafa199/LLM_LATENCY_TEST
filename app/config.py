from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # API Security
    api_key: str = Field(
        ...,
        min_length=16,
        description="Shared secret for API authentication"
    )
    
    # HuggingFace Configuration
    huggingface_token: str = Field(
        ...,
        description="HuggingFace API token for fetching models"
    )
    
    # Model Identifiers
    llama_model_id: str = Field(
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        description="HuggingFace model ID for Llama 3"
    )
    qwen_model_id: str = Field(
        default="Qwen/Qwen2.5-7B-Instruct",
        description="HuggingFace model ID for Qwen 2.5"
    )
    gemma_model_id: str = Field(
        default="google/gemma-2-9b-it",
        description="HuggingFace model ID for Gemma 2"
    )
    mistral_model_id: str = Field(
        default="mistralai/Mistral-7B-Instruct-v0.3",
        description="HuggingFace model ID for Mistral 7B Instruct"
    )
    
    # Generation Parameters
    max_new_tokens: int = Field(default=512, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
