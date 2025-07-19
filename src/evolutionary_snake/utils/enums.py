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


class BoundaryType(enum.StrEnum):
    """Enum to define the boundaries of the game."""

    HARD_BOUNDARY = "hard_boundary"
    PERIODIC_BOUNDARY = "periodic_boundary"


class TrainingMode(enum.StrEnum):
    """Enum to define the training modes."""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
