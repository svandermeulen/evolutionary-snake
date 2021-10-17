"""
Created on: 8-2-2018
@author: Stef
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from src.utils.drawing_manager import generate_coordinate


class Apple(object):

    def __init__(self, x_snake: list, y_snake):

        coordinates_apple = [(a, b) for a, b in zip(x_snake, y_snake)]
        self.x, self.y = generate_coordinate(coordinates_snake=coordinates_apple)

    def draw(self, surface: pygame.Surface, image: pygame.Surface):
        surface.blit(image, (self.x, self.y))


def is_collision(x1: int, y1: int, x2: int, y2: int):

    if x2 == x1:
        if y2 == y1:
            return True
    return False
