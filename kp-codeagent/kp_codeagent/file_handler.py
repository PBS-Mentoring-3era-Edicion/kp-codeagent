"""Safe file operations with backups and confirmations."""

import os
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime
from rich.console import Console
from rich.prompt import Confirm
from rich.syntax import Syntax

console = Console()


class FileHandler:
    """Handles file operations with safety measures."""

    def __init__(self, backup_dir: str = ".kp-codeagent-backups"):
        self.backup_dir = Path.cwd() / backup_dir
        self.backup_dir.mkdir(exist_ok=True)

    def backup_file(self, file_path: Path) -> Optional[Path]:
        """Create a backup of the file before modification."""
        if not file_path.exists():
            return None

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.name}.{timestamp}.backup"
            backup_path = self.backup_dir / backup_name

            shutil.copy2(file_path, backup_path)
            console.print(f"[dim]Backup created: {backup_path}[/dim]")
            return backup_path

        except Exception as e:
            console.print(f"[yellow]Warning: Could not create backup: {e}[/yellow]")
            return None

    def restore_backup(self, original_path: Path, backup_path: Path) -> bool:
        """Restore a file from backup."""
        try:
            shutil.copy2(backup_path, original_path)
            console.print(f"[green]✓ File restored from backup[/green]")
            return True
        except Exception as e:
            console.print(f"[red]✗ Failed to restore backup: {e}[/red]")
            return False

    def show_diff(self, file_path: Path, new_content: str):
        """Show a visual diff of file changes."""
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    old_content = f.read()

                console.print(f"\n[bold]Changes to {file_path}:[/bold]")
                console.print("[dim]Old content:[/dim]")
                syntax = Syntax(old_content[:500], "python", theme="monokai", line_numbers=True)
                console.print(syntax)

                console.print("\n[dim]New content:[/dim]")
                syntax = Syntax(new_content[:500], "python", theme="monokai", line_numbers=True)
                console.print(syntax)

                if len(new_content) > 500:
                    console.print("[dim]... (content truncated)[/dim]")

            except Exception:
                console.print("[dim]Could not display diff[/dim]")
        else:
            console.print(f"\n[bold]New file: {file_path}[/bold]")
            syntax = Syntax(new_content[:500], "python", theme="monokai", line_numbers=True)
            console.print(syntax)

            if len(new_content) > 500:
                console.print("[dim]... (content truncated)[/dim]")

    def create_file(
        self,
        file_path: Path,
        content: str,
        force: bool = False,
        show_preview: bool = True
    ) -> bool:
        """Create a new file with confirmation."""
        file_path = Path(file_path)

        if file_path.exists() and not force:
            console.print(f"[yellow]File {file_path} already exists![/yellow]")
            return False

        # Show preview
        if show_preview:
            self.show_diff(file_path, content)

        # Ask for confirmation
        if not force:
            if not Confirm.ask(f"\nCreate file {file_path}?", default=True):
                console.print("[yellow]File creation cancelled[/yellow]")
                return False

        # Create parent directories if needed
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            console.print(f"[green]✓ Created {file_path}[/green]")
            return True

        except Exception as e:
            console.print(f"[red]✗ Failed to create file: {e}[/red]")
            return False

    def modify_file(
        self,
        file_path: Path,
        new_content: str,
        force: bool = False,
        show_preview: bool = True
    ) -> bool:
        """Modify an existing file with backup and confirmation."""
        file_path = Path(file_path)

        if not file_path.exists():
            console.print(f"[red]File {file_path} does not exist![/red]")
            return False

        # Create backup
        backup_path = self.backup_file(file_path)

        # Show preview
        if show_preview:
            self.show_diff(file_path, new_content)

        # Ask for confirmation
        if not force:
            if not Confirm.ask(f"\nModify file {file_path}?", default=True):
                console.print("[yellow]File modification cancelled[/yellow]")
                return False

        # Modify file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            console.print(f"[green]✓ Modified {file_path}[/green]")
            return True

        except Exception as e:
            console.print(f"[red]✗ Failed to modify file: {e}[/red]")

            # Try to restore backup
            if backup_path:
                console.print("[yellow]Attempting to restore from backup...[/yellow]")
                self.restore_backup(file_path, backup_path)

            return False

    def delete_file(self, file_path: Path, force: bool = False) -> bool:
        """Delete a file with confirmation."""
        file_path = Path(file_path)

        if not file_path.exists():
            console.print(f"[red]File {file_path} does not exist![/red]")
            return False

        # Create backup first
        self.backup_file(file_path)

        # Ask for confirmation
        if not force:
            if not Confirm.ask(f"\nDelete file {file_path}?", default=False):
                console.print("[yellow]File deletion cancelled[/yellow]")
                return False

        try:
            os.remove(file_path)
            console.print(f"[green]✓ Deleted {file_path}[/green]")
            return True

        except Exception as e:
            console.print(f"[red]✗ Failed to delete file: {e}[/red]")
            return False

    def check_permissions(self, file_path: Path) -> bool:
        """Check if we have write permissions for a file."""
        file_path = Path(file_path)

        if file_path.exists():
            return os.access(file_path, os.W_OK)
        else:
            # Check if we can write to the parent directory
            return os.access(file_path.parent, os.W_OK)

    def read_file(self, file_path: Path) -> Optional[str]:
        """Safely read a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            console.print(f"[red]✗ Failed to read file: {e}[/red]")
            return None
