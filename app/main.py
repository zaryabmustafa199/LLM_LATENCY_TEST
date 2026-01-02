from fastapi import FastAPI, HTTPException, Depends
from app.models.llama import LlamaHandler
from app.models.qwen import QwenHandler
from app.models.gemma import GemmaHandler
from app.schemas import GenerationRequest, GenerationResponse, HealthResponse
from app.utils.timing import Timer
import time
from typing import Dict

app = FastAPI(title="LLM Microservice", version="1.0.0")

# Initialize handlers
llama_handler = LlamaHandler()
qwen_handler = QwenHandler()
gemma_handler = GemmaHandler()

@app.get("/", tags=["Status"])
async def root():
    return {
        "service": "LLM Microservice",
        "status": "healthy",
        "models": ["llama", "qwen", "gemma"]
    }

@app.get("/health", response_model=HealthResponse, tags=["Status"])
async def health_check():
    return {
        "status": "healthy",
        "models": {
            "llama": "ready",
            "qwen": "ready",
            "gemma": "ready"
        }
    }

@app.post("/generate", response_model=GenerationResponse, tags=["Inference"])
async def generate_text(request: GenerationRequest):
    # Validate API Key (Simple check)
    from app.config import settings
    if request.api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    timer = Timer()
    timer.start()
    
    try:
        model_name = request.model.lower()
        
        if "llama" in model_name:
            response_text = await llama_handler.generate(request.query)
            used_model = "llama"
        elif "qwen" in model_name:
            response_text = await qwen_handler.generate(request.query)
            used_model = "qwen"
        elif "gemma" in model_name:
            response_text = await gemma_handler.generate(request.query)
            used_model = "gemma"
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Unknown model: {request.model}. Available: llama, qwen, gemma"
            )
            
        latency = timer.stop()
        
        return {
            "response": response_text,
            "latency_ms": latency,
            "model_used": used_model
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
