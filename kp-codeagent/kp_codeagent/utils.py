"""Utility functions for KP Code Agent."""

from pathlib import Path
from typing import List


def is_binary_file(file_path: Path) -> bool:
    """Check if a file is binary."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except Exception:
        return True


def should_ignore_file(file_path: Path, gitignore_patterns: List[str]) -> bool:
    """Check if file should be ignored based on gitignore patterns."""
    file_str = str(file_path)

    # Default ignores
    default_ignores = [
        '__pycache__', '.git', 'node_modules', '.venv', 'venv',
        '.idea', '.vscode', '*.pyc', '*.pyo', '*.so', '*.dll',
        '*.exe', '*.bin', '*.jpg', '*.png', '*.gif', '*.pdf'
    ]

    for pattern in default_ignores + gitignore_patterns:
        if pattern in file_str or file_str.endswith(pattern.replace('*', '')):
            return True

    return False


def count_tokens(text: str) -> int:
    """Rough estimate of token count (1 token ≈ 4 characters)."""
    return len(text) // 4
