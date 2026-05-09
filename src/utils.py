"""Utility functions for managing notes."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

import click

# Display constants
UUID_DISPLAY_LENGTH = 8
TABLE_COLUMN_TEXT_WIDTH = 30
TABLE_COLUMN_TAG_WIDTH = 10
TABLE_COLUMN_DATE_WIDTH = 19


def get_notes_file_path() -> Path:
    """Get the path to the notes JSON file, creating directory if needed."""
    notes_dir = Path.home() / ".notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    return notes_dir / "notes.json"


def load_notes() -> list[dict[str, Any]]:
    """Load notes from JSON file. Return empty list if file doesn't exist."""
    file_path = get_notes_file_path()
    if not file_path.exists():
        return []

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return data.get("notes", [])
    except (json.JSONDecodeError, IOError):
        return []


def save_notes(notes: list[dict[str, Any]]) -> None:
    """Save notes to JSON file."""
    file_path = get_notes_file_path()
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w") as f:
        json.dump({"notes": notes}, f, indent=2)


def generate_note_id() -> str:
    """Generate a unique note ID using UUID v4."""
    return str(uuid.uuid4())


def format_timestamp(timestamp: float) -> str:
    """Format a Unix timestamp to readable date-time string."""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def _format_note(note: dict[str, Any]) -> str:
    """Format a single note for display."""
    note_id = note.get("id", "")[:UUID_DISPLAY_LENGTH]  # First 8 chars of UUID
    text = note.get("text", "")
    tag = note.get("tag") or "-"
    timestamp = format_timestamp(note.get("timestamp", 0))

    return f"{note_id:<{UUID_DISPLAY_LENGTH}} | {text:<{TABLE_COLUMN_TEXT_WIDTH}} | {tag:<{TABLE_COLUMN_TAG_WIDTH}} | {timestamp}"


def format_notes_table(notes: list[dict[str, Any]]) -> str:
    """Format multiple notes as a table."""
    if not notes:
        return "No hay notas."

    lines = []
    header = f"{'ID':<{UUID_DISPLAY_LENGTH}} | {'Texto':<{TABLE_COLUMN_TEXT_WIDTH}} | {'Tag':<{TABLE_COLUMN_TAG_WIDTH}} | {'Fecha':<{TABLE_COLUMN_DATE_WIDTH}}"
    separator = "-" * (len(header))

    lines.append(header)
    lines.append(separator)

    for note in notes:
        lines.append(_format_note(note))

    return "\n".join(lines)


def display_notes_table(
    notes: list[dict[str, Any]],
    title: str = "",
    item_label: str = "nota",
) -> None:
    """Display a formatted table of notes with title and count.

    Args:
        notes: List of note dictionaries to display.
        title: Optional title to show before the table (e.g., 'Búsqueda: "python"').
        item_label: Label for items in count (default: "nota", use "resultado" for search).
    """
    if not notes:
        click.echo("No hay notas.")
        return

    if title:
        click.echo(f"{title}\n")

    click.echo(format_notes_table(notes))
    click.echo()

    plural = item_label if len(notes) == 1 else f"{item_label}s"
    click.echo(f"Total: {len(notes)} {plural}")
