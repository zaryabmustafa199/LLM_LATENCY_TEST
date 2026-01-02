import asyncio
import time
import sys
from app.models.llama import LlamaHandler
from app.models.qwen import QwenHandler
from app.models.gemma import GemmaHandler

# Force Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

async def compare_models():
    print("="*60)
    print("LLM LATENCY COMPARISON: Llama 3 vs Qwen 2.5 vs Gemma 2")
    print("="*60)
    
    prompt = "Explain Machine Learning in one sentence."
    print(f"Prompt: \"{prompt}\"\n")
    
    handlers = [
        ("Llama 3", LlamaHandler()),
        ("Qwen 2.5", QwenHandler()),
        ("Gemma 2", GemmaHandler())
    ]
    
    results = []
    
    print(f"{'Model':<15} | {'Status':<10} | {'Latency (ms)':<15}")
    print("-" * 45)
    
    for name, handler in handlers:
        start_time = time.time()
        try:
            # We bypass api_key check here since we use handlers directly
            await handler.generate(prompt)
            latency = (time.time() - start_time) * 1000
            status = "SUCCESS"
            print(f"{name:<15} | {status:<10} | {latency:.2f}")
        except Exception as e:
            latency = 0
            status = "FAILED"
            print(f"{name:<15} | {status:<10} | {str(e)[:50]}...")
            
if __name__ == "__main__":
    asyncio.run(compare_models())
