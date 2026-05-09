"""Tests para el comando add-note usando CliRunner con cli group."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from src.cli import cli


class TestAddCommand:
    """Tests para el comando add-note."""

    def setup_method(self) -> None:
        """Setup para cada test."""
        self.runner = CliRunner()

    def test_add_basic_usage(self) -> None:
        """Test de uso básico: agregar nota con texto básico."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                result = self.runner.invoke(cli, ["add-note", "Mi primer nota"])

                assert result.exit_code == 0
                assert "Nota creada" in result.output
                assert "✓" in result.output

                # Verificar que la nota se guardó
                with open(temp_path) as f:
                    data = json.load(f)
                    assert len(data["notes"]) == 1
                    assert data["notes"][0]["text"] == "Mi primer nota"
        finally:
            temp_path.unlink()

    def test_add_with_tag(self) -> None:
        """Test de agregar nota con tag."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                result = self.runner.invoke(
                    cli, ["add-note", "Nota importante", "--tag", "trabajo"]
                )

                assert result.exit_code == 0
                assert "Nota creada" in result.output

                with open(temp_path) as f:
                    data = json.load(f)
                    assert data["notes"][0]["text"] == "Nota importante"
                    assert data["notes"][0]["tag"] == "trabajo"
        finally:
            temp_path.unlink()

    def test_add_with_tag_short_option(self) -> None:
        """Test de agregar nota con tag usando opción corta -t."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                result = self.runner.invoke(
                    cli, ["add-note", "Nota personal", "-t", "personal"]
                )

                assert result.exit_code == 0

                with open(temp_path) as f:
                    data = json.load(f)
                    assert data["notes"][0]["tag"] == "personal"
        finally:
            temp_path.unlink()

    def test_add_without_tag(self) -> None:
        """Test de agregar nota sin tag (tag debe ser None)."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                result = self.runner.invoke(cli, ["add-note", "Nota sin etiqueta"])

                assert result.exit_code == 0

                with open(temp_path) as f:
                    data = json.load(f)
                    assert data["notes"][0]["text"] == "Nota sin etiqueta"
                    assert data["notes"][0]["tag"] is None
        finally:
            temp_path.unlink()

    def test_add_empty_text_fails(self) -> None:
        """Test de texto vacío: debe fallar."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                result = self.runner.invoke(cli, ["add-note", ""])

                assert result.exit_code != 0
                assert "vacío" in result.output.lower()
        finally:
            temp_path.unlink()

    def test_add_whitespace_only_fails(self) -> None:
        """Test de texto solo con espacios: debe fallar."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                result = self.runner.invoke(cli, ["add-note", "   "])

                assert result.exit_code != 0
                assert "vacío" in result.output.lower()
        finally:
            temp_path.unlink()

    def test_add_missing_argument_fails(self) -> None:
        """Test de argumento faltante: debe fallar."""
        result = self.runner.invoke(cli, ["add-note"])

        assert result.exit_code != 0
        assert "Missing argument" in result.output or "error" in result.output.lower()

    def test_add_multiple_notes(self) -> None:
        """Test de agregar múltiples notas."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                # Agregar primera nota
                result1 = self.runner.invoke(
                    cli, ["add-note", "Primera nota", "--tag", "uno"]
                )
                assert result1.exit_code == 0

                # Agregar segunda nota
                result2 = self.runner.invoke(
                    cli, ["add-note", "Segunda nota", "--tag", "dos"]
                )
                assert result2.exit_code == 0

                # Agregar tercera nota sin tag
                result3 = self.runner.invoke(cli, ["add-note", "Tercera nota"])
                assert result3.exit_code == 0

                # Verificar que las 3 notas se guardaron
                with open(temp_path) as f:
                    data = json.load(f)
                    assert len(data["notes"]) == 3
                    assert data["notes"][0]["tag"] == "uno"
                    assert data["notes"][1]["tag"] == "dos"
                    assert data["notes"][2]["tag"] is None
        finally:
            temp_path.unlink()

    def test_add_note_has_uuid(self) -> None:
        """Test: la nota creada debe tener un ID único (UUID)."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                result = self.runner.invoke(cli, ["add-note", "Nota con UUID"])

                assert result.exit_code == 0

                with open(temp_path) as f:
                    data = json.load(f)
                    note_id = data["notes"][0]["id"]
                    # UUID v4 tiene el formato xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
                    assert "-" in note_id
                    assert len(note_id) == 36  # longitud de UUID v4
        finally:
            temp_path.unlink()

    def test_add_note_has_timestamp(self) -> None:
        """Test: la nota creada debe tener timestamp."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"notes": []}, f)
            temp_path = Path(f.name)

        try:
            with patch("src.utils.get_notes_file_path", return_value=temp_path):
                result = self.runner.invoke(cli, ["add-note", "Nota con timestamp"])

                assert result.exit_code == 0

                with open(temp_path) as f:
                    data = json.load(f)
                    timestamp = data["notes"][0]["timestamp"]
                    assert isinstance(timestamp, (int, float))
                    assert timestamp > 0
        finally:
            temp_path.unlink()
