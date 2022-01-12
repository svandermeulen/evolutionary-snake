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
from src.config import Config
from src.machine_learning.input_vector import InputVector
from src.utils.drawing_manager import Canvas

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Game(ABC):

    def __init__(self, config: Config):
        self.name = ""
        self.width = config.display_width
        self.height = config.display_height
        self.step_size: int = config.step_size
        self.snake_length: int = config.snake_length
        self.boundary = config.boundary
        self.coordinates_grid = config.get_coordinates_grid()
        self.coordinates_boundary = config.get_coordinates_boundary()
        self.frame_rate = config.frame_rate
        self.score = 0
        self.loss = None
        self.snake = Snake(
            length=self.snake_length,
            x_init=self.width // 2,
            y_init=self.height // 2,
            width=self.width,
            height=self.height,
            step_size=self.step_size,
            boundary=self.boundary
        )
        self.apple = Apple(
            snake=self.snake,
            coordinates_grid=self.coordinates_grid,
            coordinates_boundary=self.coordinates_boundary
        )
        self.canvas = Canvas()

    def execute(self) -> bool:

        pygame.init()
        while self.game_continues():
            self.loop()
            self.render()
            if self.frame_rate:
                time.sleep(self.frame_rate)  # waiting time between frames
        self.cleanup()

        return True

    def render(self) -> None:
        self.canvas.draw(score=self.score, loss=self.loss, snake=self.snake, apple=self.apple)

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
        if self.boundary:
            if (self.snake.x[0], self.snake.y[0]) in self.coordinates_boundary:
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
        self.apple = Apple(
            snake=self.snake,
            coordinates_grid=self.coordinates_grid,
            coordinates_boundary=self.coordinates_boundary
        )
        self.score = self.snake.length - self.snake_length

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

    def get_direction(self) -> int:
        direction = self._get_direction()
        if self.is_valid_direction(direction=direction):
            return direction
        return self.snake.direction

    def is_valid_direction(self, direction: int) -> bool:

        if direction == 0 and self.snake.direction == 1:
            return False
        if direction == 1 and self.snake.direction == 0:
            return False
        if direction == 2 and self.snake.direction == 3:
            return False
        if direction == 3 and self.snake.direction == 2:
            return False
        return True

    @abstractmethod
    def _get_direction(self) -> int:
        pass

    def loop(self):

        pygame.event.pump()
        direction = self.get_direction()
        self.snake.update(direction=direction)
        self._loop()

    @abstractmethod
    def _loop(self):
        pass


class GameHumanPlayer(Game):
    name: str = "Human player"

    def game_ending_conditions_other(self) -> bool:
        return False

    def _get_direction(self) -> int:

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

    def __init__(self, config: Config, name: str, neural_net: FeedForwardNetwork):
        super().__init__(config=config)
        self.name = name
        self.step_limit = config.step_limit
        self.approaching_score = config.approaching_score
        self.retracting_penalty = config.retracting_penalty
        self.eat_apple_score = config.eat_apple_score
        self.collision_penalty = config.collision_penalty
        self.neural_net = neural_net
        self.apple_distance = self.distance_to_apple()
        self.input_vector = InputVector(snake=self.snake, apple=self.apple).compute()
        self.steps_without_apple = 0
        self.loss = 0
        self.steps_total = 0
        self.direction_counts = {
            0: 0,
            1: 0,
            2: 0,
            3: 0
        }

    def process_score(self):

        self.loss += self.steps_total
        exploration_minimum = min(self.direction_counts.values())
        if exploration_minimum > 0:
            print(f"{self.name} utilized all directions at least {exploration_minimum} times.")
            self.loss *= exploration_minimum

        print(f"{self.name} finished with loss: {self.loss}")

    def game_ending_conditions_other(self) -> bool:

        if self.steps_without_apple >= self.step_limit >= 0:
            print(f"{self.name} played too long without eating apple")
            return True
        return False

    def _loop(self) -> int:

        # is the snake approaching or retracting from the apple?
        apple_distance_current = self.distance_to_apple()
        if apple_distance_current <= self.apple_distance:
            self.loss += self.approaching_score
        else:
            self.loss -= self.retracting_penalty
        self.apple_distance = apple_distance_current

        if self.eaten_apple():
            self.update_eating_apple()
            self.loss += self.eat_apple_score
            self.steps_without_apple = 0
        else:
            self.steps_without_apple += 1

        self.input_vector = InputVector(snake=self.snake, apple=self.apple).compute()
        self.steps_total += 1

        return True

    def distance_to_apple(self):
        dx_to_right_edge = min(self.width - self.snake.x[0], self.width - self.apple.x)
        dx_outer = dx_to_right_edge + min(self.snake.x[0], self.apple.x)
        dy_to_bottom_edge = min(self.height - self.snake.y[0], self.height - self.apple.y)
        dy_outer = dy_to_bottom_edge + min(self.snake.y[0], self.apple.y)

        dx_shortest = min(abs(self.apple.x - self.snake.x[0]), dx_outer)
        dy_shortest = min(abs(self.apple.y - self.snake.y[0]), dy_outer)

        return np.sqrt(dx_shortest ** 2 + dy_shortest ** 2)

    def collided(self) -> bool:
        if self.collided_with_itself() or self.collided_with_boundary():
            self.loss -= self.collision_penalty
            return True
        return False

    def _get_direction(self) -> int:
        prediction = self.neural_net.activate(self.input_vector)
        assert type(np.argmax(prediction)) == np.int64, "{} is multiple maximal values"
        direction = int(np.argmax(prediction))
        self.direction_counts[direction] += 1
        return direction
