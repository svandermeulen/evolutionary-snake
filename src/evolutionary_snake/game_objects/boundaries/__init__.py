"""Boundaries package."""

from evolutionary_snake.game_objects.boundaries.hard_boundary import HardBoundary
from evolutionary_snake.game_objects.boundaries.periodic_boundary import (
    PeriodicBoundary,
)

__all__ = [
    "HardBoundary",
    "PeriodicBoundary",
]
