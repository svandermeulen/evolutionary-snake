"""
Created on: 8-2-2018
@author: Stef
"""
import pygame

from pygame.surface import Surface

from src.config import DISPLAY_HEIGHT, DISPLAY_WIDTH, STEP_SIZE, RASTER_SIZE, BOUNDARY
from src.utils.drawing_manager import generate_coordinate


class Apple(object):

    def __init__(self, x_snake: list, y_snake):

        coordinates_apple = [(a, b) for a, b in zip(x_snake, y_snake)]
        self.x, self.y = generate_coordinate(coordinates_snake=coordinates_apple)

    def draw(self, surface: pygame.Surface, image: pygame.Surface):
        surface.blit(image, (self.x, self.y))


class Snake(object):

    def __init__(self, length: int):

        # initialize snake in center of display
        self.x, self.y = [DISPLAY_HEIGHT // 2], [DISPLAY_WIDTH // 2]
        self.direction = 0
        self.update_count_max = 0
        self.update_count = 0
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

    def update(self):

        self.update_count += 1
        while self.update_count > self.update_count_max:

            # update previous positions
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            if self.direction == 0:
                self.x[0] = self.x[0] + STEP_SIZE
            if self.direction == 1:
                self.x[0] = self.x[0] - STEP_SIZE
            if self.direction == 2:
                self.y[0] = self.y[0] - STEP_SIZE
            if self.direction == 3:
                self.y[0] = self.y[0] + STEP_SIZE

            if not BOUNDARY:
                self.periodic_boundary_conditions()

            self.update_count = 0

    def draw(self, surface: Surface, image: Surface):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))

    def move_right(self):
        self.direction = 0

    def move_left(self):
        self.direction = 1

    def move_up(self):
        self.direction = 2

    def move_down(self):
        self.direction = 3
