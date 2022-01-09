"""
Created on: 8-2-2018
@author: Stef
"""
import pygame

from src.game.object_builder import Snake, Apple


class Canvas:

    @staticmethod
    def draw(snake: Snake, apple: Apple, score: int = None, loss: int = None) -> pygame.Surface:
        canvas = pygame.display.set_mode((snake.width, snake.height + snake.step_size), pygame.HWSURFACE)
        canvas.fill((255, 255, 255))

        image_snake = MySurface(w=snake.step_size, h=snake.step_size, rgb=(0, 0, 0)).create()
        for i in range(0, snake.length):
            canvas.blit(image_snake, (snake.x[i], snake.y[i]))

        image_apple = MySurface(w=snake.step_size, h=snake.step_size, rgb=(150, 0, 0)).create()
        canvas.blit(image_apple, (apple.x, apple.y))

        if score is not None:
            score_font = MyFont(x=4 * snake.width // 5, y=snake.height - 2, rgb=(0, 0, 0), font_size=8)
            score_font.draw(
                surface=canvas,
                my_font=score_font.create(),
                text="{}".format(str(score).zfill(5))
            )

        if loss is not None:
            loss_font = MyFont(x=1 * snake.width // 5, y=snake.height - 2, rgb=(0, 0, 0), font_size=8)
            loss_font.draw(
                surface=canvas,
                my_font=loss_font.create(),
                text="{}".format(str(loss))
            )

        pygame.display.flip()

        return canvas


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
