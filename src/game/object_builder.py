"""
Created on: 8-2-2018
@author: Stef
"""
import numpy as np

from random import choice


class Snake:

    def __init__(self, length: int, x_init: int, y_init: int, width: int, height: int, step_size: int, boundary: bool):

        self.length = length
        self.width = width
        self.height = height
        self.step_size = step_size
        self.boundary = boundary
        self.x, self.y = [x_init], [y_init]
        self.direction = np.random.randint(0, 4)
        self.initialize_snake()

    def initialize_snake(self):

        raster_size = self.width // self.step_size * self.height // self.step_size
        self.x.extend([-1 * self.step_size for _ in range(1, raster_size)])
        self.y.extend([self.y[0] for _ in range(1, raster_size)])

    def periodic_boundary_conditions(self):
        """
        Let the snake appear at the opposite side of the screen when it reaches the edge
        """
        if self.x[0] > self.width - self.step_size:
            self.x[0] = 0
        if self.x[0] < 0:
            self.x[0] = self.width - self.step_size
        if self.y[0] > self.height - self.step_size:
            self.y[0] = 0
        if self.y[0] < 0:
            self.y[0] = self.height - self.step_size

    def update(self, direction: int):

        # update the body of the snake
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update the movement of the head of the snake
        if direction == 0:
            self.x[0] = self.x[0] + self.step_size
        if direction == 1:
            self.x[0] = self.x[0] - self.step_size
        if direction == 2:
            self.y[0] = self.y[0] - self.step_size
        if direction == 3:
            self.y[0] = self.y[0] + self.step_size

        if not self.boundary:
            self.periodic_boundary_conditions()

        self.direction = direction


class Apple:

    def __init__(self, snake: Snake, coordinates_grid: list, coordinates_boundary: list):
        self.snake = snake
        self.coordinates_grid = coordinates_grid
        self.coordinates_boundary = coordinates_boundary
        self.x, self.y = self.generate_coordinates()

    def generate_coordinates(self) -> tuple:
        """
        Return a x, y coordinate randomly chosen from a list of possible coordinates
        Removes the x,y coordinates that overlap with the snake and boundary if present
        """
        snake_coordinates_x = self.snake.x[0:self.snake.length]
        snake_coordinates_y = self.snake.y[0:self.snake.length]
        coordinates_snake = [(a, b) for a, b in zip(snake_coordinates_x, snake_coordinates_y)]
        coordinates = [c for c in self.coordinates_grid if
                       c not in coordinates_snake]  # apple cannot be generated on top of snake
        coordinates = [c for c in coordinates if
                       c not in self.coordinates_boundary]  # apple cannot be generated on top of boundary
        return choice(coordinates)
