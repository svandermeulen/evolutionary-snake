"""The snake game object."""

import random

from evolutionary_snake import enums

DIRECTIONS: list[enums.Direction] = list(enums.Direction)
DIRECTION_OPPOSITES: dict[enums.Direction, enums.Direction] = {
    enums.Direction.UP: enums.Direction.DOWN,
    enums.Direction.DOWN: enums.Direction.UP,
    enums.Direction.LEFT: enums.Direction.RIGHT,
    enums.Direction.RIGHT: enums.Direction.LEFT,
}


class Snake:  # pylint: disable=too-many-instance-attributes
    """Snake game object."""

    def __init__(  # pylint: disable=too-many-positional-arguments
        self,
        length: int,
        width: int,
        height: int,
        step_size: int,
        boundary: enums.Boundary,
    ) -> None:
        """Initialize the snake game object."""
        self.length = length
        self.width = width
        self.height = height
        self.step_size = step_size
        self.boundary = boundary
        self.x, self.y = [self.width // 2], [self.width // 2]
        self.direction: enums.Direction = DIRECTIONS[random.randint(0, 3)]  # noqa: S311  # nosec
        self.initialize_snake()

    def initialize_snake(self) -> None:
        """Initialize the snake."""
        raster_size = self.width // self.step_size * self.height // self.step_size
        self.x.extend([-1 * self.step_size] * (raster_size - 1))
        self.y.extend([self.y[0]] * (raster_size - 1))

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
            direction = self.direction

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

        if self.boundary == enums.Boundary.PERIODIC_BOUNDARY:
            self.periodic_boundary_conditions()

        self.direction = direction
