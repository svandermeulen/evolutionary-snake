"""Tests for the input vector module."""

from evolutionary_snake import game_objects, machine_learning


def test_input_vector(snake: game_objects.Snake, apple: game_objects.Apple) -> None:
    """Test the instantiation of a input vector class."""
    # GIVEN a predefined snake and apple object
    # WHEN an input_vector is instantiated
    input_vector = machine_learning.InputVector(snake=snake, apple=apple)
    # THEN the values of the input_vector should match with a expected list
    input_vector_values_exp = [False, True, False, True, True, True, True, True]
    assert input_vector.values == input_vector_values_exp
