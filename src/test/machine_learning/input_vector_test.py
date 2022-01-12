"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 09/01/2022
"""

import numpy as np
import unittest

from unittest.mock import Mock

from src.game.object_builder import Snake
from src.machine_learning.input_vector import InputVector
from src.utils.drawing_manager import Canvas


class TestInputVector(unittest.TestCase):

    def setUp(self) -> None:
        self.snake = Snake(
            width=100,
            height=100,
            step_size=5,
            length=5,
            x_init=0,
            y_init=0,
            boundary=False
        )

    def test_respect_to_apple(self):
        self.snake.x = [50]
        self.snake.y = [50]
        self.snake.length = 1
        iv = InputVector(snake=self.snake, apple=Mock())
        iv.apple.x = 15
        iv.apple.y = 15
        vector = iv.respect_to_apple()
        self.assertTrue(np.array_equal(vector, np.array([1, 0, 1, 0])))

    def test_right_side_not_clear(self):
        self.snake.x = [30, 30, 30, 35, 35, 35]
        self.snake.y = [5, 10, 15, 15, 10, 5]
        self.snake.length = len(self.snake.x)

        iv = InputVector(snake=self.snake, apple=Mock())
        clear_right_side = iv.right_side_clear()
        self.assertFalse(clear_right_side)

    def test_right_side_not_clear_periodic(self):
        self.snake.x = [95, 100, 100, 100, 0, 0, 0]
        self.snake.y = [5, 5, 10, 15, 15, 10, 5]
        self.snake.length = len(self.snake.x)

        iv = InputVector(snake=self.snake, apple=Mock())
        clear_right_side = iv.right_side_clear()
        self.assertFalse(clear_right_side)

    def test_left_side_not_clear(self):
        self.snake.x = [35, 35, 35, 30, 30, 30]
        self.snake.y = [5, 10, 15, 15, 10, 5]
        self.snake.length = len(self.snake.x)
        iv = InputVector(snake=self.snake, apple=Mock())
        clear_left_edge = iv.left_side_clear()
        self.assertFalse(clear_left_edge)

    def test_left_side_not_clear_periodic(self):
        self.snake.x = [0, 0, 0, 100, 100, 100]
        self.snake.y = [5, 10, 15, 15, 10, 5]
        self.snake.length = len(self.snake.x)
        iv = InputVector(snake=self.snake, apple=Mock())
        clear_left_edge = iv.left_side_clear()
        self.assertFalse(clear_left_edge)

    def test_top_side_not_clear(self):
        self.snake.x = [0, 5, 10, 15, 15, 10, 5, 0]
        self.snake.y = [95, 95, 95, 95, 0, 0, 0, 0]
        self.snake.length = len(self.snake.x)
        iv = InputVector(snake=self.snake, apple=Mock())
        clear_top_edge = iv.top_side_clear()
        self.assertFalse(clear_top_edge)

    def test_bottom_side_not_clear(self):
        self.snake.x = [5, 10, 15, 15, 10, 5]
        self.snake.y = [30, 30, 30, 35, 35, 35]
        self.snake.length = len(self.snake.x)
        iv = InputVector(snake=self.snake, apple=Mock())
        clear_bottom_side = iv.bottom_side_clear()
        self.assertFalse(clear_bottom_side)

    def test_bottom_side_not_clear_periodic(self):
        self.snake.x = [0, 5, 10, 15, 15, 10, 5, 0]
        self.snake.y = [0, 0, 0, 0, 95, 95, 95, 95]
        self.snake.length = len(self.snake.x)
        iv = InputVector(snake=self.snake, apple=Mock())
        clear_bottom_edge = iv.bottom_side_clear()
        self.assertFalse(clear_bottom_edge)


if __name__ == '__main__':
    unittest.main()
