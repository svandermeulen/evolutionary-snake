"""Module with training settings tests."""

import pathlib
import shutil

from evolutionary_snake.settings import training_settings
from evolutionary_snake.settings.training_settings import DATE, TIME


def test_training_settings() -> None:
    """Test instantiating a training settings object with the default checkpoint."""
    # GIVEN a checkpoint_prefix which parent folder does not yet exist
    checkpoint_location = pathlib.Path(__file__).parents[1] / "data" / DATE / TIME
    # AND a checkpoint prefix
    checkpoint_prefix = "test-checkpoint-"
    # WHEN a TrainingSettings object is instantiated
    settings = training_settings.TrainingSettings(
        checkpoint_prefix=checkpoint_location / checkpoint_prefix,
    )
    # THEN the parent folder must exist
    assert settings.checkpoint_prefix.parent.exists()  # pylint: disable=E1101
    # AND a new TrainingsSettings object would use that same directory
    settings = training_settings.TrainingSettings(
        checkpoint_prefix=checkpoint_location / checkpoint_prefix,
    )
    assert settings.checkpoint_prefix.parent.exists()  # pylint: disable=E1101
    shutil.rmtree(settings.checkpoint_prefix.parents[1])  # pylint: disable=E1101
