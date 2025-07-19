"""The apple game object."""

import random

from evolutionary_snake.game_objects import boundaries
from evolutionary_snake.game_objects.boundaries import base_boundary
from evolutionary_snake.settings import game_settings


class Apple:  # pylint: disable=too-few-public-methods
    """The apple game object."""

    def __init__(
        self,
        snake_coordinates: list[tuple[int, int]],
        settings: game_settings.GameSettings,
        boundary: base_boundary.BaseBoundary,
        seed: int | None = None,
    ) -> None:
        """Initialize the apple game object."""
        self.snake_coordinates = snake_coordinates
        self.coordinates_grid = settings.coordinates_grid
        self.boundary = boundary
        self.seed = seed
        self.x, self.y = self._generate_coordinates()

    def _generate_coordinates(self) -> tuple[int, int]:
        """Generate the coordinates of the apple position.

        Return a x, y coordinate randomly chosen from a list of possible coordinates
        Removes the x,y coordinates that overlap with the snake and boundary if present
        """
        # apple cannot be generated on top of snake
        coordinates = [
            c for c in self.coordinates_grid if c not in self.snake_coordinates
        ]

        # apple cannot be generated on top of boundary
        if isinstance(self.boundary, boundaries.HardBoundary):
            coordinates = [c for c in coordinates if c not in self.boundary.coordinates]

        if self.seed:
            random.seed(self.seed)

        return random.choice(coordinates)  # noqa: S311 #  nosec
