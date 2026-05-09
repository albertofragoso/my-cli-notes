"""Tests para el comando list-notes usando CliRunner con cli group."""

import json
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from src.cli import cli
from src.utils import save_notes


class TestListCommand:
    """Tests para el comando list-notes."""

    def setup_method(self) -> None:
        """Inicializa el runner para cada test."""
        self.runner = CliRunner()

    def test_list_empty_notes(self) -> None:
        """Test de lista vacía: debe mostrar 'No hay notas'."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                result = self.runner.invoke(cli, ["list-notes"])

                assert result.exit_code == 0
                assert "No hay notas" in result.output
        finally:
            temp_path.unlink()

    def test_list_single_note(self) -> None:
        """Test con una nota: debe mostrar tabla + 'Total: 1 nota'."""
        notes = [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "text": "Test note",
                "tag": "important",
                "timestamp": time.time(),
            }
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                save_notes(notes)
                result = self.runner.invoke(cli, ["list-notes"])

                assert result.exit_code == 0
                assert "Test note" in result.output
                assert "important" in result.output
                assert "Total: 1 nota" in result.output
        finally:
            temp_path.unlink()

    def test_list_multiple_notes(self) -> None:
        """Test con tres notas: debe mostrar tabla + 'Total: 3 notas'."""
        notes = [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "text": "First note",
                "tag": "one",
                "timestamp": time.time(),
            },
            {
                "id": "223e4567-e89b-12d3-a456-426614174001",
                "text": "Second note",
                "tag": "two",
                "timestamp": time.time(),
            },
            {
                "id": "323e4567-e89b-12d3-a456-426614174002",
                "text": "Third note",
                "tag": None,
                "timestamp": time.time(),
            },
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                save_notes(notes)
                result = self.runner.invoke(cli, ["list-notes"])

                assert result.exit_code == 0
                assert "First note" in result.output
                assert "Second note" in result.output
                assert "Third note" in result.output
                assert "Total: 3 notas" in result.output
        finally:
            temp_path.unlink()

    def test_list_filter_by_tag(self) -> None:
        """Test de filtro por tag: debe mostrar solo notas con ese tag."""
        notes = [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "text": "First note",
                "tag": "one",
                "timestamp": time.time(),
            },
            {
                "id": "223e4567-e89b-12d3-a456-426614174001",
                "text": "Second note",
                "tag": "two",
                "timestamp": time.time(),
            },
            {
                "id": "323e4567-e89b-12d3-a456-426614174002",
                "text": "Third note",
                "tag": "one",
                "timestamp": time.time(),
            },
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                save_notes(notes)
                result = self.runner.invoke(cli, ["list-notes", "--tag", "one"])

                assert result.exit_code == 0
                assert "First note" in result.output
                assert "Third note" in result.output
                assert "Second note" not in result.output
                assert "Total: 2 notas" in result.output
        finally:
            temp_path.unlink()

    def test_list_filter_no_results(self) -> None:
        """Test de filtro sin resultados: debe mostrar 'No hay notas'."""
        notes = [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "text": "First note",
                "tag": "one",
                "timestamp": time.time(),
            },
            {
                "id": "223e4567-e89b-12d3-a456-426614174001",
                "text": "Second note",
                "tag": "two",
                "timestamp": time.time(),
            },
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                save_notes(notes)
                result = self.runner.invoke(cli, ["list-notes", "--tag", "nonexistent"])

                assert result.exit_code == 0
                assert "No hay notas" in result.output
        finally:
            temp_path.unlink()

    def test_list_short_option_tag(self) -> None:
        """Test de opción corta -t: debe funcionar igual que --tag."""
        notes = [
            {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "text": "Work task",
                "tag": "trabajo",
                "timestamp": time.time(),
            },
            {
                "id": "223e4567-e89b-12d3-a456-426614174001",
                "text": "Personal note",
                "tag": "personal",
                "timestamp": time.time(),
            },
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                save_notes(notes)
                result = self.runner.invoke(cli, ["list-notes", "-t", "trabajo"])

                assert result.exit_code == 0
                assert "Work task" in result.output
                assert "Personal note" not in result.output
                assert "Total: 1 nota" in result.output
        finally:
            temp_path.unlink()
