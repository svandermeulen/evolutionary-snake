"""Module to test the snake object."""

import pytest

from evolutionary_snake import game_objects, game_settings
from evolutionary_snake.game_objects import boundaries


def test_snake(snake: game_objects.Snake) -> None:
    """Test the snake object."""
    # GIVEN common snake settings
    # WHEN a snake object is instantiated
    # THEN the x and y coordinates should be of an expected length
    x_length_expected, y_length_expected = 400, 400
    assert len(snake.x) == x_length_expected
    assert len(snake.y) == y_length_expected
    # AND the first item of x should be equal to and expected value
    x_exp_first = 150
    assert snake.x[0] == x_exp_first
    # AND the remaining items in x should be equal to and expected value
    x_exp_remaining = -15
    assert all(val == x_exp_remaining for val in snake.x[1:])
    # AND all items in y should be equal to an expected value
    assert all(val == x_exp_first for val in snake.y)


@pytest.mark.parametrize(
    (
        "x_pos",
        "y_pos",
        "x_pos_exp",
        "y_pos_exp",
    ),
    [
        (300, 150, 0, 150),
        (-15, 150, 285, 150),
        (150, 300, 150, 0),
        (150, -15, 150, 285),
    ],
)
def test_snake_periodic_boundary_conditions(
    snake: game_objects.Snake,
    x_pos: int,
    y_pos: int,
    x_pos_exp: int,
    y_pos_exp: int,
) -> None:
    """Test the periodic boundary conditions when moving out of the playing field."""
    # GIVEN a snake object
    # AND the first item for both x and y are set to x_pos and y_pos
    snake.x[0] = x_pos
    snake.y[0] = y_pos
    # WHEN the periodic_boundary_conditions method is called
    snake.periodic_boundary_conditions()
    # THEN the first items of both x and y should be equal to expected values
    assert snake.x[0] == x_pos_exp
    assert snake.y[0] == y_pos_exp


def test_snake_hard_boundary(
    settings: game_settings.Settings, snake: game_objects.Snake
) -> None:
    """Test the hard boundary conditions."""
    # GIVEN a snake object where the boundary is set to HARD_BOUNDARY
    snake.boundary = boundaries.HardBoundary(settings)
    direction_init = snake.direction
    # WHEN the update method is called
    snake.update(direction=direction_init)
    # THEN the direction should not have changed
    assert snake.direction == direction_init
