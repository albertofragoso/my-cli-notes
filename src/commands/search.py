"""Command to search notes."""

import click

from src.utils import display_notes_table, load_notes


@click.command()
@click.argument("query")
def search_notes(query: str) -> None:
    """Search notes by text."""
    try:
        notes = load_notes()
    except Exception as e:
        raise click.ClickException(f"Error al cargar notas: {str(e)}")

    matching_notes = [n for n in notes if query.lower() in n.get("text", "").lower()]

    if not matching_notes:
        click.echo(f'No se encontraron notas para: "{query}"')
        return

    display_notes_table(
        matching_notes,
        title=f'Búsqueda: "{query}"',
        item_label="resultado",
    )
