"""Command-line interface for KP Code Agent."""

import click
import os
from pathlib import Path
from rich.console import Console

from .agent import CodeAgent
from .ollama_client import OllamaClient
from .i18n import get_i18n

console = Console()


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="0.1.0")
@click.option('--lang', '-l', type=click.Choice(['en', 'es']), help='Language (en/es)')
def cli(ctx, lang):
    """KP Code Agent - Your local AI coding assistant for learning.

    KP Code Agent - Tu asistente de código local con IA para aprender.
    """
    # Set language if provided
    if lang:
        os.environ['KP_LANG'] = lang

    i18n = get_i18n(lang)

    if ctx.invoked_subcommand is None:
        console.print(f"[bold cyan]{i18n.t('app.name')}[/bold cyan] - {i18n.t('app.tagline')}")
        console.print(f"\n{i18n.t('cli.usage')}:")
        console.print("  kp-codeagent <task>          - Execute a coding task / Ejecutar tarea")
        console.print("  kp-codeagent --help          - Show help / Mostrar ayuda")
        console.print(f"\n{i18n.t('cli.commands')}:")
        console.print(f"  setup                        - {i18n.t('commands.setup.description')}")
        console.print(f"  check                        - {i18n.t('commands.check.description')}")
        console.print(f"\n{i18n.t('cli.examples')}:")
        if i18n.lang == 'es':
            console.print('  kp-codeagent --lang es "crea una función Python para calcular fibonacci"')
            console.print('  kp-codeagent --lang es "agrega manejo de errores a main.py"')
        else:
            console.print('  kp-codeagent "create a Python function to calculate fibonacci"')
            console.print('  kp-codeagent "add error handling to main.py"')


@cli.command()
@click.argument('task', required=True)
@click.option('--model', '-m', default='codellama:7b', help='Model to use (default: codellama:7b)')
@click.option('--temperature', '-t', default=0.7, help='Temperature for generation (default: 0.7)')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--force', '-f', is_flag=True, help='Skip confirmations (use with caution)')
@click.option('--lang', '-l', type=click.Choice(['en', 'es']), help='Language (en/es)')
def run(task: str, model: str, temperature: float, verbose: bool, force: bool, lang: str):
    """Execute a coding task."""
    if lang:
        os.environ['KP_LANG'] = lang
    agent = CodeAgent(model=model, temperature=temperature, verbose=verbose, lang=lang)
    success = agent.run(task)
    exit(0 if success else 1)


@cli.command()
@click.option('--model', '-m', default='codellama:7b', help='Model to download (default: codellama:7b)')
def setup(model: str):
    """Set up Ollama and download the required model."""
    console.print("[bold cyan]KP Code Agent Setup[/bold cyan]\n")

    client = OllamaClient(model=model)

    # Check if Ollama is running
    console.print("1. Checking if Ollama is running...")
    if not client.is_running():
        console.print("[red]✗ Ollama is not running![/red]")
        console.print("\nPlease install and start Ollama:")
        console.print("  1. Download from: https://ollama.ai/download")
        console.print("  2. Install and run Ollama")
        console.print("  3. Run this setup command again")
        exit(1)

    console.print("[green]✓ Ollama is running[/green]\n")

    # Check if model is available
    console.print(f"2. Checking if {model} is available...")
    if client.is_model_available():
        console.print(f"[green]✓ Model {model} is already installed[/green]\n")
    else:
        console.print(f"[yellow]Model {model} not found. Downloading...[/yellow]")
        if client.pull_model():
            console.print(f"[green]✓ Model {model} installed successfully[/green]\n")
        else:
            console.print(f"[red]✗ Failed to download model {model}[/red]")
            exit(1)

    console.print("[bold green]✓ Setup complete![/bold green]")
    console.print("\nYou can now use KP Code Agent:")
    console.print('  kp-codeagent "your task here"')


@cli.command()
@click.option('--model', '-m', default='codellama:7b', help='Model to check (default: codellama:7b)')
def check(model: str):
    """Check if Ollama is running and model is available."""
    console.print("[bold cyan]Checking KP Code Agent setup...[/bold cyan]\n")

    client = OllamaClient(model=model)

    # Check Ollama
    console.print("Ollama service: ", end="")
    if client.is_running():
        console.print("[green]✓ Running[/green]")
    else:
        console.print("[red]✗ Not running[/red]")
        console.print("\nStart Ollama or install from: https://ollama.ai/download")
        exit(1)

    # Check model
    console.print(f"Model {model}: ", end="")
    if client.is_model_available():
        console.print("[green]✓ Available[/green]")
    else:
        console.print("[red]✗ Not found[/red]")
        console.print(f"\nRun: kp-codeagent setup --model {model}")
        exit(1)

    console.print("\n[green]✓ Everything is ready![/green]")


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('task', required=True)
@click.option('--model', '-m', default='codellama:7b', help='Model to use')
@click.option('--temperature', '-t', default=0.7, help='Temperature for generation')
def modify(file_path: str, task: str, model: str, temperature: float):
    """Modify a specific file based on a task."""
    agent = CodeAgent(model=model, temperature=temperature)

    # Check setup first
    is_ready, message = agent.client.check_setup()
    if not is_ready:
        console.print(f"[red]✗ {message}[/red]")
        exit(1)

    success = agent.modify_file_interactive(Path(file_path), task)
    exit(0 if success else 1)


def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled by user[/yellow]")
        exit(130)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        exit(1)


if __name__ == '__main__':
    main()
