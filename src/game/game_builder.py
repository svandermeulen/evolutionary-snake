"""
Created on: 8-2-2018
@author: Stef
"""
import numpy as np
import os
import pygame
import time

from abc import ABC, abstractmethod
from neat.nn import FeedForwardNetwork
from pygame.locals import *

from src.game.object_builder import Snake, Apple
from src.config import DISPLAY_WIDTH, DISPLAY_HEIGHT, LENGTH, STEP_SIZE, BOUNDARY, APPROACHING_SCORE, \
    RETRACTING_PENALTY, EAT_APPLE_SCORE, COLLISION_PENALTY, STEP_LIMIT, FRAME_RATE, COORDINATES_BOUNDARY
from src.machine_learning.input_vector import compute_input_variables
from src.utils.drawing_manager import MySurface, MyFont

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Game(ABC):

    def __init__(self):

        pygame.init()
        self.name = ""
        self.running = True
        self.game_canvas = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT + STEP_SIZE), pygame.HWSURFACE)
        self.image_snake = MySurface(w=STEP_SIZE, h=STEP_SIZE, rgb=(0, 0, 0)).create()
        self.image_apple = MySurface(w=STEP_SIZE, h=STEP_SIZE, rgb=(150, 0, 0)).create()
        self.score_font = MyFont(x=4 * DISPLAY_WIDTH // 5, y=DISPLAY_HEIGHT - 2, rgb=(0, 0, 0), font_size=8)
        self.snake = Snake(length=LENGTH, x_init=DISPLAY_WIDTH // 2, y_init=DISPLAY_HEIGHT // 2)
        self.apple = Apple(snake=self.snake)
        self.input_vector = compute_input_variables(apple=self.apple, snake=self.snake)
        self.score = 0

    def is_valid_direction(self, direction: int) -> bool:

        dx = self.snake.x[1] - self.snake.x[0]
        dy = self.snake.y[1] - self.snake.y[0]

        if direction == 0:
            return False if dx % DISPLAY_WIDTH == STEP_SIZE else True
        elif direction == 1:
            return False if dx % -DISPLAY_WIDTH == -STEP_SIZE else True
        elif direction == 2:
            return False if dy % -DISPLAY_HEIGHT == -STEP_SIZE else True
        elif direction == 3:
            return False if dy % DISPLAY_HEIGHT == STEP_SIZE else True
        return True

    def render_canvas(self):
        self.game_canvas.fill((255, 255, 255))

    def render_score(self):
        self.score_font.draw(
            surface=self.game_canvas,
            my_font=self.score_font.create(),
            text="{}".format(str(self.score).zfill(5))
        )

    def render_metrics(self):
        self.render_score()

    def render_objects(self):
        self.snake.draw(surface=self.game_canvas, image=self.image_snake)
        self.apple.draw(surface=self.game_canvas, image=self.image_apple)

    def render(self) -> None:

        self.render_canvas()
        self.render_metrics()
        self.render_objects()
        pygame.display.flip()

    @abstractmethod
    def process_score(self):
        pass

    def cleanup(self) -> None:
        self.process_score()
        pygame.quit()

    @staticmethod
    def is_collision(x1: int, y1: int, x2: int, y2: int) -> bool:

        if x2 == x1 and y2 == y1:
            return True
        return False

    def collided(self) -> bool:

        if self.collided_with_itself() or self.collided_with_boundary():
            return True
        return False

    def collided_with_boundary(self) -> bool:
        if BOUNDARY:
            if (self.snake.x[0], self.snake.y[0]) in COORDINATES_BOUNDARY:
                print(f"{self.name} collided with the boundary")
                return True
        return False

    def collided_with_itself(self) -> bool:

        if any([self.snake.x[0] == x and self.snake.y[0] == y for x, y in zip(self.snake.x[1:], self.snake.y[1:])]):
            print(f"{self.name} collided with itself")
            return True
        return False

    def eaten_apple(self) -> bool:
        if self.apple.x == self.snake.x[0] and self.apple.y == self.snake.y[0]:
            return True
        return False

    def update_eating_apple(self):
        self.snake.length = self.snake.length + 1
        self.apple = Apple(snake=self.snake)
        self.score = self.snake.length - LENGTH

    @staticmethod
    def game_ending_key_press() -> bool:
        if pygame.key.get_pressed()[K_ESCAPE]:
            return True
        elif pygame.key.get_pressed()[K_c] and pygame.key.get_pressed()[K_LCTRL]:
            return True
        return False

    def game_continues(self) -> bool:
        if self.game_ending_key_press():
            return False
        if self.collided():
            return False
        if self.game_ending_conditions_other():
            return False
        return True

    @abstractmethod
    def game_ending_conditions_other(self) -> bool:
        pass

    @abstractmethod
    def get_direction(self) -> int:
        pass

    def execute(self) -> bool:

        while self.game_continues():
            self.loop()
            self.render()
            if FRAME_RATE:
                time.sleep(FRAME_RATE)  # waiting time between frames
        self.cleanup()

        return True

    def loop(self):

        pygame.event.pump()

        direction = self.get_direction()

        if self.is_valid_direction(direction=direction):
            self.snake.update(direction=direction)
        self._loop()

    @abstractmethod
    def _loop(self):
        pass


class GameHumanPlayer(Game):

    def __init__(self):
        super().__init__()
        self.name = "Human player"

    def game_ending_conditions_other(self) -> bool:
        return False

    def get_direction(self) -> int:

        keys = pygame.key.get_pressed()
        if keys[K_DOWN]:
            return 3
        if keys[K_UP]:
            return 2
        if keys[K_LEFT]:
            return 1
        if keys[K_RIGHT]:
            return 0
        return self.snake.direction

    def _loop(self):
        if self.eaten_apple():
            self.update_eating_apple()

    def process_score(self):
        print(f"{self.name} score: {self.score}")


class GameNeuralNet(Game):

    def __init__(self, name: str, neural_net: FeedForwardNetwork, step_limit: int = STEP_LIMIT):
        super().__init__()
        self.name = name
        self.nn = neural_net
        self.apple_distance = self.distance_to_apple()
        self.step_limit = step_limit
        self.steps_without_apple = 0
        self.loss = 0
        self.loss_font = MyFont(x=1 * DISPLAY_WIDTH // 5, y=DISPLAY_HEIGHT - 2, rgb=(0, 0, 0), font_size=8)
        self.steps_total = 0

    def process_score(self):

        self.loss += self.steps_total
        print(f"{self.name} finished with loss: {self.loss}")

    def game_ending_conditions_other(self) -> bool:

        if self.steps_without_apple >= self.step_limit:
            print(f"{self.name} played too long without catching apple")
            return True
        return False

    def render_metrics(self):
        self.render_score()
        self.render_loss()

    def render_loss(self):
        self.loss_font.draw(
            surface=self.game_canvas,
            my_font=self.loss_font.create(),
            text="{}".format(str(self.loss))
        )

    def _loop(self) -> int:

        # is the snake approaching or retracting from the apple?
        apple_distance_current = self.distance_to_apple()
        if apple_distance_current <= self.apple_distance:
            self.loss += APPROACHING_SCORE
        else:
            self.loss -= RETRACTING_PENALTY
        self.apple_distance = apple_distance_current

        if self.eaten_apple():
            self.update_eating_apple()
            self.loss += EAT_APPLE_SCORE
            self.steps_without_apple = 0
        else:
            self.steps_without_apple += 1

        self.steps_total += 1

        return True

    def distance_to_apple(self):
        dx_to_right_edge = min(DISPLAY_WIDTH - self.snake.x[0], DISPLAY_WIDTH - self.apple.x)
        dx_outer = dx_to_right_edge + min(self.snake.x[0], self.apple.x)
        dy_to_bottom_edge = min(DISPLAY_HEIGHT - self.snake.y[0], DISPLAY_HEIGHT - self.apple.y)
        dy_outer = dy_to_bottom_edge + min(self.snake.y[0], self.apple.y)

        dx_shortest = min(abs(self.apple.x - self.snake.x[0]), dx_outer)
        dy_shortest = min(abs(self.apple.y - self.snake.y[0]), dy_outer)

        return np.sqrt(dx_shortest ** 2 + dy_shortest ** 2)

    def collided(self) -> bool:
        if self.collided_with_itself() or self.collided_with_boundary():
            self.loss -= COLLISION_PENALTY
            return True
        return False

    def get_direction(self) -> int:
        prediction = self.nn.activate(self.input_vector)
        assert type(np.argmax(prediction)) == np.int64, "{} is multiple maximal values"
        return int(np.argmax(prediction))
