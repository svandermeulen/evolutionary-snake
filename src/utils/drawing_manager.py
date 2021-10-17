"""
Created on: 8-2-2018
@author: Stef
"""
import time

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

from typing import List
from random import choice, seed

import src.config as config


class MySurface(object):

    def __init__(self, w: int, h: int,  rgb: tuple):
        self.width = w
        self.height = h
        self.rgb = rgb

    def create(self) -> pygame.Surface:

        my_surface = pygame.Surface((self.width, self.height))
        my_surface.fill(self.rgb)
        return my_surface


class MyFont(object):

    def __init__(self, x: int, y: int, rgb: tuple, font_size: int):
        self.rgb = rgb
        self.x = x
        self.y = y
        self.font_size = font_size

    def create(self) -> pygame.font:
        return pygame.font.SysFont("Arial", self.font_size)

    def draw(self, surface: pygame.Surface, my_font: pygame.font, text: str):
        label = my_font.render(text, True, self.rgb)
        surface.blit(label, (self.x, self.y))
        # surface.blit(label, ((surface.get_width() - label.get_width()) // 2, self.y))


def generate_coordinate(coordinates_snake: List[tuple]) -> tuple:
    """
    Return a x, y coordinate randomnly chosen from a list of possible coordinates
    Removes the x,y coordinates that overlap with the snake and boundary if present
    """
    coordinates = [c for c in config.COORDINATES if c not in coordinates_snake]  # apple cannot be generated on top of snake
    coordinates = [c for c in coordinates if c not in config.COORDINATES_BOUNDARY]  # apple cannot be generated on top of boundary
    seed(time.time())
    return choice(coordinates)
