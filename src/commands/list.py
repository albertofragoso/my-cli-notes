"""Command to list notes."""

from typing import Optional

import click

from src.utils import display_notes_table, load_notes


@click.command()
@click.option("--tag", "-t", default=None, help="Filter by tag")
def list_notes(tag: Optional[str]) -> None:
    """List all notes."""
    try:
        notes = load_notes()
    except Exception as e:
        raise click.ClickException(f"Error al cargar notas: {str(e)}")

    if tag:
        notes = [n for n in notes if n.get("tag") == tag]

    display_notes_table(notes)
