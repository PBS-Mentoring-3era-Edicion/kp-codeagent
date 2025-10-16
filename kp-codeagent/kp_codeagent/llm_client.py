"""Unified LLM client supporting multiple backends."""

import os
from typing import Iterator, Optional
from abc import ABC, abstractmethod

# Import various clients conditionally
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False


class LLMBackend(ABC):
    """Abstract base class for LLM backends."""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this backend is available."""
        pass

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 120
    ) -> Iterator[str]:
        """Generate text with streaming."""
        pass


class OllamaBackend(LLMBackend):
    """Ollama backend (local)."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "codellama:7b"):
        self.base_url = base_url
        self.model = model

    def is_available(self) -> bool:
        if not HAS_REQUESTS:
            return False
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 120
    ) -> Iterator[str]:
        """Generate using Ollama API."""
        import json

        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": True
        }

        if system:
            payload["system"] = system

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=timeout
            )

            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if 'response' in data:
                        yield data['response']
                    if data.get('done', False):
                        break
        except Exception as e:
            yield f"\n[Error: {e}]"


class OpenAIBackend(LLMBackend):
    """OpenAI API backend."""

    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if HAS_OPENAI:
            self.client = openai.OpenAI(api_key=self.api_key)

    def is_available(self) -> bool:
        return HAS_OPENAI and self.api_key is not None

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 120
    ) -> Iterator[str]:
        """Generate using OpenAI API."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
                timeout=timeout
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"\n[Error: {e}]"


class GroqBackend(LLMBackend):
    """Groq API backend (fast and free)."""

    def __init__(self, api_key: str = None, model: str = "llama-3.3-70b-versatile"):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        if HAS_GROQ:
            self.client = Groq(api_key=self.api_key)

    def is_available(self) -> bool:
        return HAS_GROQ and self.api_key is not None

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 120
    ) -> Iterator[str]:
        """Generate using Groq API."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
                timeout=timeout
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"\n[Error: {e}]"


class UnifiedLLMClient:
    """Unified client that can use multiple backends."""

    def __init__(self, backend: str = "auto", **kwargs):
        """
        Initialize with a specific backend or auto-detect.

        Args:
            backend: "ollama", "openai", "groq", or "auto"
            **kwargs: Backend-specific parameters
        """
        self.backend = self._create_backend(backend, **kwargs)

    def _create_backend(self, backend: str, **kwargs) -> LLMBackend:
        """Create the appropriate backend."""
        # Filter out None values from kwargs to allow backend defaults
        filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if backend == "auto":
            # Try backends in order of preference
            backends_to_try = [
                ("groq", lambda: GroqBackend(**filtered_kwargs)),
                ("openai", lambda: OpenAIBackend(**filtered_kwargs)),
                ("ollama", lambda: OllamaBackend(**filtered_kwargs)),
            ]

            for name, creator in backends_to_try:
                try:
                    backend_instance = creator()
                    if backend_instance.is_available():
                        print(f"✓ Using {name} backend")
                        return backend_instance
                except Exception:
                    continue

            raise RuntimeError("No LLM backend available. Install Ollama or set API keys.")

        elif backend == "ollama":
            return OllamaBackend(**filtered_kwargs)
        elif backend == "openai":
            return OpenAIBackend(**filtered_kwargs)
        elif backend == "groq":
            return GroqBackend(**filtered_kwargs)
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        timeout: int = 120
    ) -> Iterator[str]:
        """Generate text using the configured backend."""
        return self.backend.generate(prompt, system, temperature, timeout)

    def is_available(self) -> bool:
        """Check if the backend is available."""
        return self.backend.is_available()

    def check_setup(self) -> tuple[bool, str]:
        """Check if the client is properly configured."""
        if self.is_available():
            return True, "Ready"
        else:
            return False, "Backend not available. Check configuration."


# Example usage
if __name__ == "__main__":
    # Auto-detect best backend
    client = UnifiedLLMClient(backend="auto")

    # Or specify backend
    # client = UnifiedLLMClient(backend="groq", api_key="your-key", model="llama-3.1-70b-versatile")
    # client = UnifiedLLMClient(backend="openai", api_key="your-key", model="gpt-4")
    # client = UnifiedLLMClient(backend="ollama", model="codellama:7b")

    for chunk in client.generate("Write a Python hello world"):
        print(chunk, end="", flush=True)
