"""
Pydantic schemas for request and response validation

Defines the API contract for the /generate endpoint.
"""

from pydantic import BaseModel, Field, ConfigDict

class GenerationRequest(BaseModel):
    """Request schema for LLM generation endpoint"""
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=4000,
        description="User prompt to send to the LLM",
        examples=["What is the capital of France?"]
    )
    
    model: str = Field(
        ...,
        pattern="^(llama|qwen|gemma|mistral)$",
        description="Model name to use for generation (llama, qwen, gemma, or mistral)",
        examples=["mistral"]
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "Explain quantum computing in simple terms",
                "model": "qwen"
            }
        }
    )



class GenerationResponse(BaseModel):
    """Response schema for LLM generation endpoint"""
    
    model_used: str = Field(
        ...,
        description="Model that was used for generation"
    )
    
    response: str = Field(
        ...,
        description="Raw output from the LLM"
    )
    
    latency_ms: float = Field(
        ...,
        description="Measured latency in milliseconds",
        ge=0.0
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "model_used": "qwen",
                "response": "Quantum computing is a type of computing that uses quantum bits...",
                "latency_ms": 1247.83
            }
        }
    )

class HealthResponse(BaseModel):
    """Response schema for health check"""
    status: str
    models: dict
