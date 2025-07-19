"""The command line interface for evolutionary_snake."""

import pathlib

import click

from evolutionary_snake import snake, snake_training
from evolutionary_snake.utils import enums


@click.command()
@click.option("--game-mode", default=enums.GameMode.AI_PLAYER)
@click.option("--path_checkpoint", default=None, type=click.Path(exists=True))
def start(game_mode: enums.GameMode, path_checkpoint: pathlib.Path | None) -> None:
    """Start the evolutionary_snake game_modes."""
    if game_mode == enums.GameMode.AI_PLAYER and not path_checkpoint:
        msg = "Path to a checkpoint not provided."
        raise click.BadOptionUsage(message=msg, option_name="path_checkpoint")
    return snake.run_snake(game_mode=game_mode, path_checkpoint=path_checkpoint)


@click.command()
@click.option("--training-mode", default=enums.TrainingMode.SEQUENTIAL)
def start_training(training_mode: enums.TrainingMode) -> None:
    """Start the evolutionary_snake training mode."""
    return snake_training.run_snake_training(training_mode=training_mode)
