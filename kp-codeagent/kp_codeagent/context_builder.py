"""Context builder for gathering project information."""

import os
from pathlib import Path
from typing import List, Dict, Tuple
from .utils import is_binary_file, should_ignore_file, count_tokens


class ContextBuilder:
    """Builds context from the current project for the AI agent."""

    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.gitignore_patterns = self._load_gitignore()

    def _load_gitignore(self) -> List[str]:
        """Load patterns from .gitignore if it exists."""
        gitignore_path = Path.cwd() / '.gitignore'
        patterns = []

        if gitignore_path.exists():
            try:
                with open(gitignore_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            patterns.append(line)
            except Exception:
                pass

        return patterns

    def build_file_tree(self, root_dir: Path = None, max_depth: int = 3) -> str:
        """Build a text representation of the file tree."""
        if root_dir is None:
            root_dir = Path.cwd()

        tree_lines = [f"Project Root: {root_dir.name}/"]

        def add_tree_lines(directory: Path, prefix: str = "", depth: int = 0):
            if depth >= max_depth:
                return

            try:
                items = sorted(directory.iterdir(), key=lambda x: (not x.is_dir(), x.name))

                for i, item in enumerate(items):
                    if should_ignore_file(item, self.gitignore_patterns):
                        continue

                    is_last = i == len(items) - 1
                    current_prefix = "└── " if is_last else "├── "
                    next_prefix = "    " if is_last else "│   "

                    if item.is_dir():
                        tree_lines.append(f"{prefix}{current_prefix}{item.name}/")
                        add_tree_lines(item, prefix + next_prefix, depth + 1)
                    else:
                        tree_lines.append(f"{prefix}{current_prefix}{item.name}")

            except PermissionError:
                pass

        add_tree_lines(root_dir)
        return "\n".join(tree_lines)

    def find_relevant_files(
        self,
        task: str,
        root_dir: Path = None,
        file_extensions: List[str] = None
    ) -> List[Path]:
        """Find files relevant to the task."""
        if root_dir is None:
            root_dir = Path.cwd()

        if file_extensions is None:
            # Common code file extensions
            file_extensions = [
                '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
                '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala',
                '.html', '.css', '.scss', '.sql', '.sh', '.bat', '.json', '.yaml', '.yml'
            ]

        relevant_files = []
        task_lower = task.lower()

        try:
            for root, dirs, files in os.walk(root_dir):
                # Remove ignored directories from dirs to prevent walking them
                dirs[:] = [d for d in dirs if not should_ignore_file(Path(root) / d, self.gitignore_patterns)]

                for file in files:
                    file_path = Path(root) / file

                    # Skip if should be ignored or is binary
                    if should_ignore_file(file_path, self.gitignore_patterns):
                        continue

                    if is_binary_file(file_path):
                        continue

                    # Check if file extension matches
                    if not any(file.endswith(ext) for ext in file_extensions):
                        continue

                    # Basic relevance check based on filename
                    if any(keyword in file.lower() for keyword in task_lower.split()):
                        relevant_files.append(file_path)
                        continue

                    # If not many files yet, add common entry points
                    if len(relevant_files) < 5 and file in ['main.py', 'app.py', 'index.js', 'main.js', 'Main.java']:
                        relevant_files.append(file_path)

        except Exception:
            pass

        return relevant_files[:10]  # Limit to 10 most relevant files

    def read_file_content(self, file_path: Path, max_lines: int = 200) -> str:
        """Read file content with size limits."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

                if len(lines) > max_lines:
                    return (
                        f"# File: {file_path} (truncated - showing first {max_lines} lines)\n" +
                        "".join(lines[:max_lines]) +
                        f"\n... ({len(lines) - max_lines} more lines)"
                    )
                else:
                    return f"# File: {file_path}\n" + "".join(lines)

        except Exception as e:
            return f"# File: {file_path}\n# Error reading file: {e}"

    def build_context(self, task: str) -> Tuple[str, str]:
        """
        Build complete context for the AI agent.
        Returns: (file_tree, code_snippets)
        """
        file_tree = self.build_file_tree()
        relevant_files = self.find_relevant_files(task)

        code_snippets = []
        total_tokens = count_tokens(file_tree)

        for file_path in relevant_files:
            content = self.read_file_content(file_path)
            content_tokens = count_tokens(content)

            if total_tokens + content_tokens > self.max_tokens:
                break

            code_snippets.append(content)
            total_tokens += content_tokens

        return file_tree, "\n\n".join(code_snippets) if code_snippets else "No relevant files found."

    def get_file_content(self, file_path: Path) -> str:
        """Get the full content of a specific file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
