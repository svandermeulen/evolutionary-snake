"""Module to define the InputVector class."""

import typing

from evolutionary_snake import game_objects


class InputVector(typing.NamedTuple):
    """Input vector NamedTyple class."""

    right_to_apple: bool
    left_to_apple: bool
    above_apple: bool
    below_apple: bool
    right_side_clear: bool
    left_side_clear: bool
    top_side_clear: bool
    bottom_side_clear: bool

    @property
    def values(self) -> list[bool]:
        """Return the values of the input vector."""
        return [
            self.right_to_apple,
            self.left_to_apple,
            self.above_apple,
            self.below_apple,
            self.right_side_clear,
            self.left_side_clear,
            self.bottom_side_clear,
            self.top_side_clear,
        ]


def compute_input_vector(
    snake: game_objects.Snake,
    apple: game_objects.Apple,
) -> InputVector:
    """Compute the input vector given the apple, snake and boundary."""
    return InputVector(
        right_to_apple=apple.x < snake.x[0],
        left_to_apple=apple.x > snake.x[0],
        above_apple=apple.y > snake.y[0],
        below_apple=apple.y < snake.y[0],
        left_side_clear=snake.left_side_clear(),
        right_side_clear=snake.right_side_clear(),
        top_side_clear=snake.top_side_clear(),
        bottom_side_clear=snake.bottom_side_clear(),
    )
