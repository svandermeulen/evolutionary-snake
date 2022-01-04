"""
Created on: 8-2-2018
@author: Stef
"""
import pygame


class MySurface:

    def __init__(self, w: int, h: int, rgb: tuple):
        self.width = w
        self.height = h
        self.rgb = rgb

    def create(self) -> pygame.Surface:
        my_surface = pygame.Surface((self.width, self.height))
        my_surface.fill(self.rgb)
        return my_surface


class MyFont:

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
