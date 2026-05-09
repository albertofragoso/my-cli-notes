"""Tests for the add command."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from src.commands.add import add_note
from src.utils import load_notes


@pytest.fixture
def runner():
    """Provide a Click CLI runner."""
    return CliRunner()


@pytest.fixture
def temp_notes_file():
    """Provide a temporary notes file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump({"notes": []}, f)
        temp_path = f.name

    yield Path(temp_path)

    Path(temp_path).unlink()


def test_add_note_with_tag(runner, temp_notes_file):
    """Test adding a note with a tag."""
    with patch("src.utils.get_notes_file_path", return_value=temp_notes_file):
        result = runner.invoke(add_note, ["Test note", "--tag", "important"])

        assert result.exit_code == 0
        assert "Nota creada" in result.output

        notes = load_notes()
        assert len(notes) == 1
        assert notes[0]["text"] == "Test note"
        assert notes[0]["tag"] == "important"


def test_add_note_without_tag(runner, temp_notes_file):
    """Test adding a note without a tag."""
    with patch("src.utils.get_notes_file_path", return_value=temp_notes_file):
        result = runner.invoke(add_note, ["Test note"])

        assert result.exit_code == 0
        assert "Nota creada" in result.output

        notes = load_notes()
        assert len(notes) == 1
        assert notes[0]["text"] == "Test note"
        assert notes[0]["tag"] is None


def test_add_note_empty_text(runner, temp_notes_file):
    """Test adding a note with empty text."""
    with patch("src.utils.get_notes_file_path", return_value=temp_notes_file):
        result = runner.invoke(add_note, [""])

        assert result.exit_code != 0
        assert "vacío" in result.output.lower()


def test_add_note_whitespace_only(runner, temp_notes_file):
    """Test adding a note with whitespace only."""
    with patch("src.utils.get_notes_file_path", return_value=temp_notes_file):
        result = runner.invoke(add_note, ["   "])

        assert result.exit_code != 0
        assert "vacío" in result.output.lower()


def test_add_multiple_notes(runner, temp_notes_file):
    """Test adding multiple notes."""
    with patch("src.utils.get_notes_file_path", return_value=temp_notes_file):
        runner.invoke(add_note, ["First note", "--tag", "one"])
        runner.invoke(add_note, ["Second note", "--tag", "two"])
        runner.invoke(add_note, ["Third note"])

        notes = load_notes()
        assert len(notes) == 3
        assert notes[0]["text"] == "First note"
        assert notes[1]["text"] == "Second note"
        assert notes[2]["text"] == "Third note"
