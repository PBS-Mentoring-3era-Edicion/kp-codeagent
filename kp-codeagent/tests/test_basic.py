"""Basic tests for KP Code Agent."""

import pytest
from pathlib import Path
from kp_codeagent.utils import is_binary_file, should_ignore_file, count_tokens


def test_count_tokens():
    """Test token counting."""
    text = "Hello world"
    tokens = count_tokens(text)
    assert tokens > 0
    assert tokens == len(text) // 4


def test_should_ignore_file():
    """Test file ignore patterns."""
    # Should ignore Python cache
    assert should_ignore_file(Path("__pycache__/test.pyc"), [])

    # Should ignore node modules
    assert should_ignore_file(Path("node_modules/package.json"), [])

    # Should not ignore regular Python files
    assert not should_ignore_file(Path("main.py"), [])


def test_binary_file_detection(tmp_path):
    """Test binary file detection."""
    # Create a text file
    text_file = tmp_path / "test.txt"
    text_file.write_text("Hello world")
    assert not is_binary_file(text_file)

    # Create a binary file
    binary_file = tmp_path / "test.bin"
    binary_file.write_bytes(b'\x00\x01\x02\x03')
    assert is_binary_file(binary_file)
