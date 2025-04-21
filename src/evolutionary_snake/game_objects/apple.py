"""The apple game object."""

import random

from evolutionary_snake import game_settings


class Apple:  # pylint: disable=too-few-public-methods
    """The apple game object."""

    def __init__(
        self,
        snake_coordinates: list[list[int]],
        settings: game_settings.Settings,
    ) -> None:
        """Initialize the apple game object."""
        self.snake_coordinates = snake_coordinates
        self.coordinates_grid = settings.get_coordinates_grid()
        self.coordinates_boundary = settings.get_coordinates_boundary()
        self.x, self.y = self.generate_coordinates()

    def generate_coordinates(self) -> tuple[int, int]:
        """Generate the coordinates of the apple position.

        Return a x, y coordinate randomly chosen from a list of possible coordinates
        Removes the x,y coordinates that overlap with the snake and boundary if present
        """
        snake_coordinates_x = self.snake_coordinates[0]
        snake_coordinates_y = self.snake_coordinates[1]
        coordinates_snake = list(
            zip(snake_coordinates_x, snake_coordinates_y, strict=False)
        )

        # apple cannot be generated on top of snake
        coordinates = [c for c in self.coordinates_grid if c not in coordinates_snake]

        # apple cannot be generated on top of boundary
        coordinates = [c for c in coordinates if c not in self.coordinates_boundary]
        return random.choice(coordinates)  # noqa: S311 #  nosec
