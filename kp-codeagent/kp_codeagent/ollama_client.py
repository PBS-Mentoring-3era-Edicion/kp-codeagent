"""Ollama API client for KP Code Agent."""

import json
import requests
from typing import Iterator, Optional, Dict, Any
from rich.console import Console

console = Console()


class OllamaClient:
    """Client for interacting with local Ollama API."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "codellama:7b"):
        self.base_url = base_url
        self.model = model

    def is_running(self) -> bool:
        """Check if Ollama service is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def is_model_available(self) -> bool:
        """Check if the specified model is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [m.get('name', '') for m in data.get('models', [])]
                return self.model in models
            return False
        except requests.exceptions.RequestException:
            return False

    def pull_model(self) -> bool:
        """Pull the model if not present."""
        console.print(f"[yellow]Downloading {self.model}... This may take several minutes.[/yellow]")

        try:
            response = requests.post(
                f"{self.base_url}/api/pull",
                json={"name": self.model},
                stream=True,
                timeout=600
            )

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        status = data.get('status', '')
                        if 'total' in data and 'completed' in data:
                            percent = (data['completed'] / data['total']) * 100
                            console.print(f"[cyan]{status}: {percent:.1f}%[/cyan]", end='\r')

                console.print(f"[green]✓ Model {self.model} downloaded successfully![/green]")
                return True
            else:
                console.print(f"[red]✗ Failed to download model: {response.status_code}[/red]")
                return False

        except requests.exceptions.RequestException as e:
            console.print(f"[red]✗ Error downloading model: {e}[/red]")
            return False

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        stream: bool = True,
        timeout: int = 120
    ) -> Iterator[str]:
        """Generate text from the model with streaming support."""

        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": stream
        }

        if system:
            payload["system"] = system

        try:
            console.print(f"[dim]🔄 Conectando con {self.model}...[/dim]")

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=stream,
                timeout=timeout
            )

            if response.status_code != 200:
                yield f"Error: API returned status {response.status_code}"
                return

            if stream:
                line_count = 0
                for line in response.iter_lines():
                    if line:
                        data = json.loads(line)
                        if 'response' in data:
                            if line_count == 0:
                                console.print("[green]✓ Recibiendo respuesta...[/green]")
                            yield data['response']
                            line_count += 1
                        if data.get('done', False):
                            break
            else:
                data = response.json()
                yield data.get('response', '')

        except requests.exceptions.Timeout:
            yield f"\n\n[red]✗ Timeout: El modelo tardó más de {timeout} segundos. Intenta:[/red]\n"
            yield "1. Reiniciar Ollama: ollama serve\n"
            yield "2. Usar un modelo más pequeño: --model phi:latest\n"
            yield "3. Reducir el tamaño del contexto\n"
        except requests.exceptions.RequestException as e:
            yield f"\n[red]✗ Error comunicando con Ollama: {e}[/red]"

    def generate_full(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """Generate text and return the full response (non-streaming)."""
        result = "".join(self.generate(prompt, system, temperature, stream=False))
        return result

    def check_setup(self) -> tuple[bool, str]:
        """
        Check if Ollama is properly set up.
        Returns: (is_ready, message)
        """
        if not self.is_running():
            return False, "Ollama is not running. Please start Ollama first."

        if not self.is_model_available():
            return False, f"Model {self.model} not found. Use --pull to download it."

        return True, "Ready"
