"""The command line interface for evolutionary_snake."""

import click

from evolutionary_snake import enums, main


@click.command()
@click.option("--game-mode", default=enums.GameMode.HUMAN_PLAYER)
def start(game_mode: enums.GameMode) -> None:
    """Start the evolutionary_snake game_modes."""
    return main.main(game_mode=game_mode)
