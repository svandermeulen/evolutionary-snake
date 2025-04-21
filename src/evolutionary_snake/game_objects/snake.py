"""The snake game object."""

import random

from evolutionary_snake import enums, game_settings

DIRECTIONS: list[enums.Direction] = list(enums.Direction)
DIRECTION_OPPOSITES: dict[enums.Direction, enums.Direction] = {
    enums.Direction.UP: enums.Direction.DOWN,
    enums.Direction.DOWN: enums.Direction.UP,
    enums.Direction.LEFT: enums.Direction.RIGHT,
    enums.Direction.RIGHT: enums.Direction.LEFT,
}


class Snake:  # pylint: disable=too-many-instance-attributes
    """Snake game object."""

    def __init__(
        self, settings: game_settings.Settings, x_init: int, y_init: int
    ) -> None:
        """Initialize the snake game object."""
        self.length = settings.snake_length_init
        self.width = settings.display_width
        self.height = settings.display_height
        self.step_size = settings.step_size
        self.boundary = settings.boundary
        self.x, self.y = [x_init], [y_init]
        self.direction: enums.Direction = DIRECTIONS[random.randint(0, 3)]  # noqa: S311  # nosec
        self.initialize_snake()

    def initialize_snake(self) -> None:
        """Initialize the snake."""
        raster_size = self.width // self.step_size * self.height // self.step_size
        self.x.extend([-1 * self.step_size for _ in range(1, raster_size)])
        self.y.extend([self.y[0] for _ in range(1, raster_size)])

    def periodic_boundary_conditions(self) -> None:
        """The snake appears at the opposite screen side upon hitting the edge."""
        if self.x[0] > self.width - self.step_size:
            self.x[0] = 0
        if self.x[0] < 0:
            self.x[0] = self.width - self.step_size
        if self.y[0] > self.height - self.step_size:
            self.y[0] = 0
        if self.y[0] < 0:
            self.y[0] = self.height - self.step_size

    def update(self, direction: enums.Direction) -> None:
        """Update the body of the snake."""
        if direction == DIRECTION_OPPOSITES[self.direction]:
            return

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update the movement of the head of the snake
        if direction == enums.Direction.RIGHT:
            self.x[0] = self.x[0] + self.step_size
        if direction == enums.Direction.LEFT:
            self.x[0] = self.x[0] - self.step_size
        if direction == enums.Direction.UP:
            self.y[0] = self.y[0] - self.step_size
        if direction == enums.Direction.DOWN:
            self.y[0] = self.y[0] + self.step_size

        if not self.boundary:
            self.periodic_boundary_conditions()

        self.direction = direction
