"""Entry point de la CLI."""

import click

from src.commands.add import add_note
from src.commands.list import list_notes
from src.commands.search import search_notes


@click.group()
@click.version_option(version="0.1.0")
def cli() -> None:
    """My CLI Notes"""
    pass


cli.add_command(add_note)
cli.add_command(list_notes)
cli.add_command(search_notes)

if __name__ == "__main__":
    cli()
