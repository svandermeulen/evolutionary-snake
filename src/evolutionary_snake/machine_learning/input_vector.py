"""Module to define the InputVector class."""

from evolutionary_snake import enums, game_objects


class InputVector:  # pylint: disable=too-few-public-methods
    """Input vector acting as input to the neural network."""

    def __init__(self, snake: game_objects.Snake, apple: game_objects.Apple) -> None:
        """Initialize the input vector."""
        self.snake = snake
        self.apple = apple
        self.width = self.snake.width
        self.height = self.snake.height
        self.step_size = self.snake.step_size
        self.boundary = self.snake.boundary

    @property
    def values(self) -> list[bool]:
        """Compute the input vector."""
        vector_apple = self._respect_to_apple()
        vector_collision_object = self._check_sides()
        return vector_apple + vector_collision_object

    def _respect_to_apple(self) -> list[bool]:
        """Return which direction the apple is."""
        return [
            self.apple.x < self.snake.x[0],
            self.apple.x > self.snake.x[0],
            self.apple.y < self.snake.y[0],
            self.apple.y > self.snake.y[0],
        ]

    def _check_sides(self) -> list[bool]:
        """Return which directions are clear."""
        return [self._side_clear(side=side) for side in enums.Direction]

    def _side_clear(self, side: enums.Direction) -> bool:
        """Check if side is clear."""
        if side == enums.Direction.RIGHT:
            return self._right_side_clear()
        if side == enums.Direction.LEFT:
            return self._left_side_clear()
        if side == enums.Direction.UP:
            return self._top_side_clear()
        return self._bottom_side_clear()

    def _right_side_clear(self) -> bool:
        """Check if right side is clear."""
        return not (
            (self.boundary and self.snake.x[0] == self.width)
            or self._periodic_obstruction_horizontal(
                edge=self.width - self.step_size, x_obstruction=0
            )
            or self._snake_obstruction_horizontal(
                x_obstruction=self.snake.x[0] + self.step_size
            )
        )

    def _left_side_clear(self) -> bool:
        """Check if left side is clear."""
        return not (
            (self.boundary and self.snake.x[0] == 0)
            or self._periodic_obstruction_horizontal(edge=0, x_obstruction=self.width)
            or self._snake_obstruction_horizontal(
                x_obstruction=self.snake.x[0] - self.step_size
            )
        )

    def _bottom_side_clear(self) -> bool:
        """Check if bottom side is clear."""
        return not (
            (self.boundary and self.snake.y[0] == self.height)
            or self._periodic_obstruction_vertical(
                edge=0, y_obstruction=self.height - self.step_size
            )
            or self._snake_obstruction_vertical(
                y_obstruction=self.snake.y[0] + self.step_size
            )
        )

    def _top_side_clear(self) -> bool:
        """Check if top side is clear."""
        return not (
            (self.boundary and self.snake.y[0] == 0)
            or self._periodic_obstruction_vertical(
                edge=self.height - self.step_size, y_obstruction=0
            )
            or self._snake_obstruction_vertical(
                y_obstruction=self.snake.y[0] - self.step_size
            )
        )

    def _periodic_obstruction_horizontal(self, edge: int, x_obstruction: int) -> bool:
        """Check if any obstruction on horizontal axis due to periodic conditions."""
        return self.snake.x[0] == edge and any(
            x == x_obstruction and y == self.snake.y[0]
            for x, y in self.snake.coordinates[1:]
        )

    def _periodic_obstruction_vertical(self, edge: int, y_obstruction: int) -> bool:
        """Check if any obstruction on the vertical axis due to periodic conditions."""
        return self.snake.y[0] == edge and any(
            x == self.snake.x[0] and y == y_obstruction
            for x, y in self.snake.coordinates[1:]
        )

    def _snake_obstruction_horizontal(self, x_obstruction: int) -> bool:
        """Check if any obstruction on the horizontal axis due to the snake itself."""
        return any(
            a == (x_obstruction, self.snake.y[0]) for a in self.snake.coordinates
        )

    def _snake_obstruction_vertical(self, y_obstruction: int) -> bool:
        """Check if any obstruction on the vertical axis due to the snake itself."""
        return any(
            a == (self.snake.x[0], y_obstruction) for a in self.snake.coordinates
        )
