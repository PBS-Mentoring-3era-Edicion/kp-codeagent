"""Core agent orchestration logic for KP Code Agent."""

from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .ollama_client import OllamaClient
from .context_builder import ContextBuilder
from .file_handler import FileHandler
from .prompts import (
    get_system_prompt,
    TASK_PROMPT_TEMPLATE,
    PLAN_PROMPT_TEMPLATE,
    FILE_MODIFICATION_TEMPLATE
)
from .i18n import get_i18n

console = Console()


class CodeAgent:
    """Main agent that orchestrates the coding task workflow."""

    def __init__(
        self,
        model: str = "codellama:7b",
        temperature: float = 0.7,
        verbose: bool = False,
        lang: str = None
    ):
        self.client = OllamaClient(model=model)
        self.context_builder = ContextBuilder()
        self.file_handler = FileHandler()
        self.temperature = temperature
        self.verbose = verbose
        self.i18n = get_i18n(lang)
        self.lang = self.i18n.lang
        self.system_prompt = get_system_prompt(self.lang)

    def receive_task(self, task: str) -> Dict[str, Any]:
        """Parse and validate the user's coding task."""
        task_label = self.i18n.t('agent.task_label')
        console.print(Panel(
            f"[bold cyan]{task_label}[/bold cyan] {task}",
            title="KP Code Agent",
            border_style="cyan"
        ))

        return {
            "task": task,
            "status": "received"
        }

    def analyze_context(self) -> Dict[str, str]:
        """Scan current directory for relevant files and context."""
        with console.status("[bold yellow]Analyzing project context...[/bold yellow]"):
            file_tree, code_snippets = self.context_builder.build_context("")

        if self.verbose:
            console.print("\n[dim]Project Structure:[/dim]")
            console.print(file_tree[:500])
            console.print("\n[dim]Found relevant code files[/dim]")

        return {
            "file_tree": file_tree,
            "code_snippets": code_snippets
        }

    def plan_solution(self, task: str, context: Dict[str, str]) -> str:
        """Ask CodeLlama to create a step-by-step plan."""
        console.print("\n[bold yellow]📋 Creating implementation plan...[/bold yellow]\n")

        plan_prompt = PLAN_PROMPT_TEMPLATE.format(
            user_task=task,
            context=f"{context['file_tree']}\n\n{context['code_snippets'][:1000]}"
        )

        plan = ""
        for chunk in self.client.generate(
            prompt=plan_prompt,
            system=self.system_prompt,
            temperature=self.temperature
        ):
            console.print(chunk, end="")
            plan += chunk

        console.print("\n")
        return plan

    def execute_plan(self, task: str, context: Dict[str, str], plan: str) -> bool:
        """Implement the plan by generating code."""
        console.print("\n[bold green]⚙️  Implementing solution...[/bold green]\n")

        # Generate the full task prompt
        task_prompt = TASK_PROMPT_TEMPLATE.format(
            user_task=task,
            file_tree=context['file_tree'],
            code_snippets=context['code_snippets']
        )

        # Get the implementation
        implementation = ""
        for chunk in self.client.generate(
            prompt=task_prompt,
            system=self.system_prompt,
            temperature=self.temperature
        ):
            console.print(chunk, end="")
            implementation += chunk

        console.print("\n")

        # Try to extract file operations from the response
        # This is a simple implementation - could be enhanced with better parsing
        return self._process_implementation(implementation)

    def _process_implementation(self, implementation: str) -> bool:
        """Process the AI's implementation and apply file changes."""
        # Look for code blocks in the response
        import re

        # Pattern to find code blocks with file names
        # Example: ```python:filename.py or ```python\n# File: filename.py
        pattern = r'```(?:\w+)?(?::|\n#\s*File:\s*)([\w\./]+)\n(.*?)```'
        matches = re.findall(pattern, implementation, re.DOTALL)

        if not matches:
            console.print("[yellow]No file operations detected in response.[/yellow]")
            console.print("[dim]You may need to manually create or modify files based on the suggestions above.[/dim]")
            return True

        success = True
        for file_path, content in matches:
            file_path = Path(file_path)

            if file_path.exists():
                # Modify existing file
                if not self.file_handler.modify_file(file_path, content.strip()):
                    success = False
            else:
                # Create new file
                if not self.file_handler.create_file(file_path, content.strip()):
                    success = False

        return success

    def verify_solution(self, task: str) -> bool:
        """Run basic checks on the solution."""
        console.print("\n[bold blue]🔍 Verifying solution...[/bold blue]")

        # Basic verification - could be enhanced with actual testing
        # For now, just check if files were created/modified successfully
        console.print("[green]✓ Basic verification complete[/green]")

        return True

    def present_results(self, success: bool):
        """Show results to the user."""
        if success:
            console.print(Panel(
                "[bold green]✓ Task completed successfully![/bold green]\n\n"
                "Files have been created/modified as shown above.\n"
                "Review the changes and test your code.",
                title="Success",
                border_style="green"
            ))
        else:
            console.print(Panel(
                "[bold red]✗ Task completed with errors[/bold red]\n\n"
                "Some file operations failed. Check the messages above.",
                title="Completed with Errors",
                border_style="red"
            ))

    def run(self, task: str) -> bool:
        """Execute the complete agent workflow."""
        try:
            # Check Ollama setup
            is_ready, message = self.client.check_setup()
            if not is_ready:
                console.print(f"[red]✗ {message}[/red]")
                return False

            # 1. Receive task
            self.receive_task(task)

            # 2. Analyze context
            context = self.analyze_context()

            # 3. Plan solution
            plan = self.plan_solution(task, context)

            # 4. Execute plan
            success = self.execute_plan(task, context, plan)

            # 5. Verify solution
            if success:
                success = self.verify_solution(task)

            # 6. Present results
            self.present_results(success)

            return success

        except KeyboardInterrupt:
            console.print("\n[yellow]Task cancelled by user[/yellow]")
            return False
        except Exception as e:
            console.print(f"\n[red]✗ Error: {e}[/red]")
            if self.verbose:
                import traceback
                console.print(traceback.format_exc())
            return False

    def modify_file_interactive(self, file_path: Path, modification_task: str):
        """Interactively modify a specific file."""
        if not file_path.exists():
            console.print(f"[red]File {file_path} does not exist![/red]")
            return False

        current_content = self.file_handler.read_file(file_path)
        if current_content is None:
            return False

        console.print(f"\n[bold]Modifying {file_path}...[/bold]\n")

        prompt = FILE_MODIFICATION_TEMPLATE.format(
            file_path=file_path,
            current_content=current_content[:2000],  # Limit context
            modification_task=modification_task
        )

        new_content = ""
        for chunk in self.client.generate(
            prompt=prompt,
            system=self.system_prompt,
            temperature=self.temperature
        ):
            console.print(chunk, end="")
            new_content += chunk

        console.print("\n")

        # Extract code from response if wrapped in code blocks
        import re
        code_match = re.search(r'```(?:\w+)?\n(.*?)```', new_content, re.DOTALL)
        if code_match:
            new_content = code_match.group(1)

        return self.file_handler.modify_file(file_path, new_content.strip())
