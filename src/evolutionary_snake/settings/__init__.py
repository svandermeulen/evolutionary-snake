"""All public settings objects."""

from evolutionary_snake.settings.game_settings import AiGameSettings, GameSettings
from evolutionary_snake.settings.training_settings import TrainingSettings

__all__ = [
    "AiGameSettings",
    "GameSettings",
    "TrainingSettings",
]
