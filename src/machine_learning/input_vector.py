"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 17/10/2021
"""

import numpy as np

from src.game.object_builder import Snake, Apple
from src.config import DISPLAY_WIDTH, DISPLAY_HEIGHT, STEP_SIZE
from src.config import BOUNDARY


def respect_to_apple(apple: Apple, snake: Snake) -> np.ndarray:
    vector = np.zeros(4)

    # is the apple to the left
    if apple.x < snake.x[0]:
        vector[0] = 1

    # is the apple to the right
    if apple.x > snake.x[0]:
        vector[1] = 1

    # is the apple above
    if apple.y < snake.y[1]:
        vector[2] = 1

    # is the apple below
    if apple.y > snake.y[1]:
        vector[3] = 1

    return vector


def _right_edge_clear(snake: Snake) -> bool:
    if BOUNDARY and snake.x[0] == DISPLAY_WIDTH:
        return False
    if snake.x[0] == 0 and any([a == DISPLAY_WIDTH - STEP_SIZE for a in snake.x[1:snake.length]]) and \
            any([a == snake.y[0] for a in snake.y[1:snake.length]]):
        return False
    return True


def _left_edge_clear(snake: Snake) -> bool:
    if BOUNDARY and snake.x[0] == 0:
        return False
    if snake.x[0] == DISPLAY_WIDTH - STEP_SIZE and any([a == 0 for a in snake.x[1:snake.length]]) and \
            any([a == snake.y[0] for a in snake.y[1:snake.length]]):
        return False
    return True


def _bottom_edge_clear(snake: Snake) -> bool:
    if BOUNDARY and snake.y[0] == DISPLAY_HEIGHT:
        return False
    if snake.y[0] == 0 and any([a == DISPLAY_HEIGHT - STEP_SIZE for a in snake.y[1:snake.length]]) and \
            any([a == snake.x[0] for a in snake.x[1:snake.length]]):
        return False
    return True


def _top_edge_clear(snake: Snake) -> bool:
    if BOUNDARY and snake.y[0] == 0:
        return False
    if snake.y[0] == DISPLAY_HEIGHT - STEP_SIZE and any([a == 0 for a in snake.y[1:snake.length]]) and \
            any([a == snake.x[0] for a in snake.x[1:snake.length]]):
        return False
    return True


def respect_to_self(snake: Snake) -> np.ndarray:
    vector = np.zeros(4)
    snake_coordinates = [(a, b) for a, b in zip(snake.x[:snake.length], snake.y[:snake.length])]

    # is it clear to the left?
    if _right_edge_clear(snake) and not any([a == (snake.x[0] - STEP_SIZE, snake.y[0]) for a in snake_coordinates]):
        vector[0] = 1

    # is it clear to the right
    if _left_edge_clear(snake) and not any([a == (snake.x[0] + STEP_SIZE, snake.y[0]) for a in snake_coordinates]):
        vector[1] = 1

    # is it clear above
    if _bottom_edge_clear(snake) and not any([a == (snake.x[0], snake.y[0] - STEP_SIZE) for a in snake_coordinates]):
        vector[2] = 1

    # is it clear below
    if _top_edge_clear(snake) and not any([a == (snake.x[0], snake.y[0] + STEP_SIZE) for a in snake_coordinates]):
        vector[3] = 1

    return vector


def compute_input_variables(apple: Apple, snake: Snake) -> list:
    vector = respect_to_apple(apple=apple, snake=snake)
    vector = np.append(vector, respect_to_self(snake=snake))
    return list(vector)


def main():
    pass


if __name__ == "__main__":
    main()
