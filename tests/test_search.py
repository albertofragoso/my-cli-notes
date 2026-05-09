"""Tests para el comando search-notes usando CliRunner con cli group."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from src.cli import cli
from src.utils import save_notes


class TestSearchCommand:
    """Tests para el comando search-notes."""

    def setup_method(self) -> None:
        """Setup para cada test."""
        self.runner = CliRunner()

    def test_search_no_notes(self) -> None:
        """Test: buscar cuando no hay notas → 'No se encontraron notas'."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                result = self.runner.invoke(cli, ["search-notes", "python"])

                assert result.exit_code == 0
                assert "No se encontraron notas" in result.output
        finally:
            temp_path.unlink()

    def test_search_single_match(self) -> None:
        """Test: buscar con 1 coincidencia → 'Total: 1 resultado'."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            notes = [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "text": "Python tips",
                    "tag": "dev",
                    "timestamp": 1234567890.0,
                },
                {
                    "id": "223e4567-e89b-12d3-a456-426614174001",
                    "text": "JavaScript notes",
                    "tag": "dev",
                    "timestamp": 1234567891.0,
                },
            ]

            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                save_notes(notes)
                result = self.runner.invoke(cli, ["search-notes", "Python"])

                assert result.exit_code == 0
                assert "Python tips" in result.output
                assert "JavaScript notes" not in result.output
                assert "Total: 1 resultado" in result.output
        finally:
            temp_path.unlink()

    def test_search_multiple_matches(self) -> None:
        """Test: buscar con 2 coincidencias → 'Total: 2 resultados'."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            notes = [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "text": "Python tips",
                    "tag": "dev",
                    "timestamp": 1234567890.0,
                },
                {
                    "id": "223e4567-e89b-12d3-a456-426614174001",
                    "text": "Learning Python",
                    "tag": "learn",
                    "timestamp": 1234567891.0,
                },
                {
                    "id": "323e4567-e89b-12d3-a456-426614174002",
                    "text": "JavaScript notes",
                    "tag": "dev",
                    "timestamp": 1234567892.0,
                },
            ]

            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                save_notes(notes)
                result = self.runner.invoke(cli, ["search-notes", "python"])

                assert result.exit_code == 0
                assert "Python tips" in result.output
                assert "Learning Python" in result.output
                assert "JavaScript notes" not in result.output
                assert "Total: 2 resultados" in result.output
        finally:
            temp_path.unlink()

    def test_search_case_insensitive(self) -> None:
        """Test: búsqueda case-insensitive → 'python' encuentra 'PYTHON PROGRAMMING'."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            notes = [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "text": "PYTHON PROGRAMMING",
                    "tag": "dev",
                    "timestamp": 1234567890.0,
                },
            ]

            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                save_notes(notes)
                result = self.runner.invoke(cli, ["search-notes", "python"])

                assert result.exit_code == 0
                assert "PYTHON PROGRAMMING" in result.output
                assert "Total: 1 resultado" in result.output
        finally:
            temp_path.unlink()

    def test_search_partial_match(self) -> None:
        """Test: coincidencia parcial → 'test' encuentra 'testing'."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            notes = [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "text": "Nota sobre testing",
                    "tag": "qa",
                    "timestamp": 1234567890.0,
                },
            ]

            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                save_notes(notes)
                result = self.runner.invoke(cli, ["search-notes", "test"])

                assert result.exit_code == 0
                assert "testing" in result.output
                assert "Total: 1 resultado" in result.output
        finally:
            temp_path.unlink()

    def test_search_displays_title(self) -> None:
        """Test: verifica que aparezca 'Búsqueda: \"query\"' en output."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            notes = [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "text": "Django framework",
                    "tag": "web",
                    "timestamp": 1234567890.0,
                },
            ]

            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                save_notes(notes)
                result = self.runner.invoke(cli, ["search-notes", "django"])

                assert result.exit_code == 0
                assert 'Búsqueda: "django"' in result.output
        finally:
            temp_path.unlink()
