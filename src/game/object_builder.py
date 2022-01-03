"""
Created on: 8-2-2018
@author: Stef
"""
from abc import abstractmethod, ABC

import numpy as np
import pygame

from pygame.surface import Surface

from src.config import DISPLAY_HEIGHT, DISPLAY_WIDTH, STEP_SIZE, RASTER_SIZE, BOUNDARY
from src.utils.drawing_manager import generate_coordinate


class Object(ABC):

    @abstractmethod
    def draw(self, surface: pygame.Surface, image: pygame.Surface):
        pass


class Snake(Object):

    def __init__(self, length: int, x_init: int, y_init: int):

        self.x, self.y = [x_init], [y_init]
        self.direction = np.random.randint(0, 4)
        self.length = length
        self.initialize_snake()

    def periodic_boundary_conditions(self):

        if self.x[0] > DISPLAY_WIDTH - STEP_SIZE:
            self.x[0] = 0
        if self.x[0] < 0:
            self.x[0] = DISPLAY_WIDTH - STEP_SIZE
        if self.y[0] > DISPLAY_HEIGHT - STEP_SIZE:
            self.y[0] = 0
        if self.y[0] < 0:
            self.y[0] = DISPLAY_HEIGHT - STEP_SIZE

    def initialize_snake(self):

        self.x.extend([self.x[0] + -1 * DISPLAY_WIDTH * STEP_SIZE for _ in range(1, RASTER_SIZE)])
        self.y.extend([self.y[0] for _ in range(1, RASTER_SIZE)])

    def update(self, direction: int):

        # update previous positions
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if direction == 0:
            self.x[0] = self.x[0] + STEP_SIZE
        if direction == 1:
            self.x[0] = self.x[0] - STEP_SIZE
        if direction == 2:
            self.y[0] = self.y[0] - STEP_SIZE
        if direction == 3:
            self.y[0] = self.y[0] + STEP_SIZE

        if not BOUNDARY:
            self.periodic_boundary_conditions()

        self.direction = direction

    def draw(self, surface: Surface, image: Surface):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))


class Apple(Object):

    def __init__(self, snake: Snake):
        snake_coordinates_x = snake.x[0:snake.length]
        snake_coordinates_y = snake.y[0:snake.length]
        coordinates_snake = [(a, b) for a, b in zip(snake_coordinates_x, snake_coordinates_y)]
        self.x, self.y = generate_coordinate(coordinates_snake=coordinates_snake)

    def draw(self, surface: pygame.Surface, image: pygame.Surface):
        surface.blit(image, (self.x, self.y))



