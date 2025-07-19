"""The snake game object."""

import random

from evolutionary_snake.game_objects import boundaries
from evolutionary_snake.game_objects.boundaries import base_boundary
from evolutionary_snake.utils import enums

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
        boundary: base_boundary.BaseBoundary,
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

    @property
    def coordinates(self) -> list[tuple[int, int]]:
        """Return list of snake coordinates."""
        return list(
            zip(
                self.x[: self.length],
                self.y[: self.length],
                strict=False,
            )
        )

    def collided_with_boundary(self) -> bool:
        """Check if the snake collides with the boundary."""
        if isinstance(self.boundary, boundaries.HardBoundary):
            return (self.x[0], self.y[0]) in self.boundary.coordinates
        return False

    def collided_with_itself(self) -> bool:
        """Return True if the snake collides with itself."""
        return any(
            self.x[0] == x and self.y[0] == y
            for x, y in zip(self.x[1:], self.y[1:], strict=False)
        )

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

        if isinstance(self.boundary, boundaries.PeriodicBoundary):
            self.periodic_boundary_conditions()

        self.direction = direction

    def right_side_clear(self) -> bool:
        """Return True if the right side of the snake is clear."""
        if isinstance(self.boundary, boundaries.HardBoundary):
            return self.x[0] != self.width
        return not (
            self._periodic_obstruction_horizontal(
                edge=self.width - self.step_size, x_obstruction=0
            )
            or any(
                a == (self.x[0] + self.step_size, self.y[0]) for a in self.coordinates
            )
        )

    def left_side_clear(self) -> bool:
        """Return True if the left side of the snake is clear."""
        if isinstance(self.boundary, boundaries.HardBoundary):
            return self.x[0] != 0
        return not (
            self._periodic_obstruction_horizontal(edge=0, x_obstruction=self.width)
            or any(
                a == (self.x[0] - self.step_size, self.y[0]) for a in self.coordinates
            )
        )

    def bottom_side_clear(self) -> bool:
        """Return True if the top side of the snake is clear."""
        if isinstance(self.boundary, boundaries.HardBoundary):
            return self.y[0] != self.height
        return not (
            self._periodic_obstruction_vertical(
                edge=0, y_obstruction=self.height - self.step_size
            )
            or any(
                a == (self.x[0], self.y[0] + self.step_size) for a in self.coordinates
            )
        )

    def top_side_clear(self) -> bool:
        """Return True if the top side of the snake is clear."""
        if isinstance(self.boundary, boundaries.HardBoundary):
            return self.y[0] != 0
        return not (
            self._periodic_obstruction_vertical(
                edge=self.height - self.step_size, y_obstruction=0
            )
            or any(
                a == (self.x[0], self.y[0] - self.step_size) for a in self.coordinates
            )
        )

    def _periodic_obstruction_horizontal(self, edge: int, x_obstruction: int) -> bool:
        """Check if any obstruction on horizontal axis due to periodic conditions."""
        return self.x[0] == edge and any(
            x == x_obstruction and y == self.y[0] for x, y in self.coordinates[1:]
        )

    def _periodic_obstruction_vertical(self, edge: int, y_obstruction: int) -> bool:
        """Check if any obstruction on the vertical axis due to periodic conditions."""
        return self.y[0] == edge and any(
            x == self.x[0] and y == y_obstruction for x, y in self.coordinates[1:]
        )
