"""All enum definitions for the project."""

import enum


class Direction(enum.Enum):
    """Enum to define the directions of the snake."""

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class GameMode(enum.StrEnum):
    """Enum to define game_modes modes."""

    HUMAN_PLAYER = "human_player"
    TRAINING = "training"
    AI_PLAYER = "ai_player"
