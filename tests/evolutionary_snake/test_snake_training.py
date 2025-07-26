"""Module with tests for snake_training module."""

import pathlib
import shutil

from evolutionary_snake.settings import TrainingSettings
from evolutionary_snake.snake_training import run_snake_training
from evolutionary_snake.utils import enums


def test_run_snake_training_sequential() -> None:
    """Test running the snake_training sequentially."""
    # GIVEN a training settings object with test locations
    training_settings = TrainingSettings(
        generations=1,
        path_neat_config=pathlib.Path(__file__).parents[1] / "data" / "neat_config",
        checkpoint_prefix=pathlib.Path(__file__).parents[1]
        / "data"
        / "temp"
        / "checkpoint-",
    )
    # WHEN the run_snake_training function is called
    run_snake_training(
        training_mode=enums.TrainingMode.SEQUENTIAL,
        training_settings=training_settings,
    )
    # THEN the given locations should contain 2 files
    n_files_exp = 2
    assert (
        len(list(training_settings.checkpoint_prefix.parent.iterdir())) == n_files_exp  # pylint: disable=E1101
    )
    shutil.rmtree(training_settings.checkpoint_prefix.parent)  # pylint: disable=E1101


def test_run_snake_training_parallel() -> None:
    """Test running the snake_training parallel.."""
    # GIVEN a training settings object with test locations
    training_settings = TrainingSettings(
        generations=1,
        path_neat_config=pathlib.Path(__file__).parents[1] / "data" / "neat_config",
        checkpoint_prefix=pathlib.Path(__file__).parents[1]
        / "data"
        / "temp"
        / "checkpoint-",
    )
    # WHEN the run_snake_training function is called
    run_snake_training(
        training_mode=enums.TrainingMode.PARALLEL,
        training_settings=training_settings,
    )
    # THEN the given locations should contain 2 files
    n_files_exp = 2
    assert (
        len(list(training_settings.checkpoint_prefix.parent.iterdir())) == n_files_exp  # pylint: disable=E1101
    )
    shutil.rmtree(training_settings.checkpoint_prefix.parent)  # pylint: disable=E1101
