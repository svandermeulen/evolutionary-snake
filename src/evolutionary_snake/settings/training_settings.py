"""Settings for the training mode."""

import datetime
import pathlib
import zoneinfo

import neat
import pydantic

from evolutionary_snake.utils import utility_functions

DATETIME_NOW = datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/Amsterdam"))
DATE = DATETIME_NOW.strftime("%Y%m%d")
TIME = DATETIME_NOW.strftime("%H%M%S")


class TrainingSettings(pydantic.BaseModel):
    """Settings for the training mode."""

    generations: int = 25
    step_limit: int = 50
    checkpoint_prefix: pathlib.Path = pydantic.Field(
        default=pathlib.Path(__file__).parents[3]
        / "data"
        / DATE
        / TIME
        / "neat-checkpoint-",
        validate_default=True,
    )
    path_neat_config: pathlib.Path = (
        pathlib.Path(__file__).parents[3] / "data" / "neat_config"
    )

    @pydantic.field_validator("checkpoint_prefix")
    @classmethod
    def validate_checkpoint_prefix(
        cls, checkpoint_prefix: pathlib.Path
    ) -> pathlib.Path:
        """Validate checkpoint prefix field."""
        if not checkpoint_prefix.parent.exists():
            checkpoint_prefix.parent.mkdir(parents=True)
        return checkpoint_prefix

    @property
    def neat_config(self) -> neat.Config:
        """Returns the neat config instance."""
        return utility_functions.get_neat_config(self.path_neat_config)
