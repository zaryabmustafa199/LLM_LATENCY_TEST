import asyncio
import time
import sys
from rich.console import Console
from rich.table import Table
from app.models.llama import LlamaHandler
from app.models.qwen import QwenHandler
from app.models.gemma import GemmaHandler

# Force Windows console encoding
sys.stdout.reconfigure(encoding='utf-8')

# Initialize Rich Console
console = Console()

async def compare_models():
    console.print("\n[bold cyan]============================================================[/bold cyan]")
    console.print("[bold cyan]🚀 LLM LATENCY COMPARISON: Llama 3 vs Qwen 2.5 vs Gemma 2[/bold cyan]")
    console.print("[bold cyan]============================================================[/bold cyan]\n")
    
    prompt = "Explain Machine Learning in one sentence."
    console.print(f"[bold]Prompt:[/bold] [italic]\"{prompt}\"[/italic]\n")
    
    handlers = [
        ("Llama 3 (8B)", LlamaHandler()),
        ("Qwen 2.5 (7B)", QwenHandler()),
        ("Gemma 2 (9B)", GemmaHandler())
    ]
    
    # Initialize Rich Table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Model", style="cyan", width=20)
    table.add_column("Status", justify="center", width=15)
    table.add_column("Latency (ms)", justify="right", style="green", width=15)
    
    with console.status("[bold green]Testing models... Please wait...[/bold green]"):
        for name, handler in handlers:
            start_time = time.time()
            try:
                await handler.generate(prompt)
                latency = (time.time() - start_time) * 1000
                table.add_row(name, "[bold green]SUCCESS[/bold green]", f"{latency:.2f}")
            except Exception as e:
                table.add_row(name, "[bold red]FAILED[/bold red]", "ERROR")
    
    console.print(table)
    console.print("\n[bold cyan]Benchmark Complete![/bold cyan]\n")

if __name__ == "__main__":
    asyncio.run(compare_models())

