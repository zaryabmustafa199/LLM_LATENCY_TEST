import time
import logging
from fastapi import FastAPI, HTTPException, Depends, Security, Request
from fastapi.security import APIKeyHeader
from app.models.llama import LlamaHandler
from app.models.qwen import QwenHandler
from app.models.gemma import GemmaHandler
from app.schemas import GenerationRequest, GenerationResponse, HealthResponse
from app.utils.timing import Timer
from app.config import settings

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI LLM Benchmark", version="2.0.0")

# Security Dependency
API_KEY_NAME = "x-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.api_key:
        logger.warning("Failed authentication attempt.")
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return api_key

# Global Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # Add custom header for total request time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request: {request.method} {request.url.path} - Completed in {process_time:.4f}s")
    return response

# Initialize handlers
llama_handler = LlamaHandler()
qwen_handler = QwenHandler()
gemma_handler = GemmaHandler()

@app.get("/", tags=["Status"])
async def root():
    return {
        "service": "FastAPI LLM Benchmark",
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
async def generate_text(request: GenerationRequest, api_key: str = Depends(get_api_key)):
    """
    Generates text using the specified LLM. 
    Secured via Dependency Injection (x-api-key header).
    """
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
        logger.error(f"Inference error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
