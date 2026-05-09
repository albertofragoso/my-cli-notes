"""Command to add a new note."""

import time
from typing import Optional

import click

from src.utils import generate_note_id, load_notes, save_notes


@click.command()
@click.argument("text")
@click.option("--tag", "-t", default=None, help="Optional tag for the note")
def add_note(text: str, tag: Optional[str]) -> None:
    """Create a new note."""
    if not text or not text.strip():
        raise click.ClickException("El texto no puede estar vacío")

    try:
        notes = load_notes()

        new_note = {
            "id": generate_note_id(),
            "text": text,
            "tag": tag,
            "timestamp": time.time(),
        }

        notes.append(new_note)
        save_notes(notes)

        click.echo(f"✓ Nota creada con ID: {new_note['id'][:8]}")
    except Exception as e:
        raise click.ClickException(f"Error al guardar nota: {str(e)}")
