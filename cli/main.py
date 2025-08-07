from typer import Typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

app = Typer()
console = Console()

@app.callback()
def main():
    show_welcome()

def show_welcome():
    console.clear()
    
    title_text = Text("🚀 Welcome to Flick", style="bold magenta")
    subtitle = Text("A Serverless File Transfer Tool", style="italic cyan")
    
    panel = Panel.fit(
        title_text + "\n" + subtitle,
        border_style="bright_blue",
        padding=(1, 4),
    )
    
    console.print(panel)
    console.print("\n[bold green]Initializing Flick...[/bold green]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Starting services...", total=None)
        time.sleep(1.5)  # simulate loading
        progress.update(task, description="Loading modules...")
        time.sleep(1.5)
        progress.update(task, description="Ready to use Flick!")
        time.sleep(1)

    console.print("[bold yellow]Type [green]flick --help[/green] to see available commands.[/bold yellow]\n")

# Example command
@app.command()
def ping():
    """Simple ping test"""
    console.print("[cyan]Pong![/cyan]")

if __name__ == "__main__":
    app()
