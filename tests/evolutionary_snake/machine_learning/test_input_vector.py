"""Tests for the input vector module."""

from evolutionary_snake import game_objects
from evolutionary_snake.machine_learning import input_vector


def test_input_vector(
    apple: game_objects.Apple,
    snake: game_objects.Snake,
) -> None:
    """Test the instantiation of a input vector class."""
    # GIVEN a predefined snake and apple object
    # WHEN an input_vector is instantiated
    iv = input_vector.compute_input_vector(snake=snake, apple=apple)
    # THEN the values of the input_vector should match with a expected list
    input_vector_values_exp = [False, True, False, True, True, True, True, True]
    assert iv.values == input_vector_values_exp
