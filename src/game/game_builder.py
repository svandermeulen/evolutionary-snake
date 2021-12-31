"""
Created on: 8-2-2018
@author: Stef
"""
import json
from abc import ABC, abstractmethod

import numpy as np
import os
import pygame
import time

from neat.nn import FeedForwardNetwork
from pygame.locals import *

from src.game.object_builder import Snake, Apple
from src.config import DISPLAY_WIDTH, DISPLAY_HEIGHT, LENGTH, STEP_SIZE, BOUNDARY, APPROACHING_SCORE, \
    RETRACTING_PENALTY, EAT_APPLE_SCORE, COLLISION_PENALTY, STEP_LIMIT, FRAME_RATE, BACKGROUND_RUN, \
    HUMAN_PLAYER, COORDINATES_BOUNDARY
from src.machine_learning.loss_calculator import compute_input_variables
from src.utils.drawing_manager import MySurface, MyFont


# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Game(ABC):

    def __init__(self):

        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        self.running = True
        self.game_area = None
        self.image_surf = None
        self.apple_surf = None
        self._boundary_rect = None
        self.score_font = None
        self.snake = Snake(length=LENGTH)
        self.apple = Apple(snake=self.snake)

    def _is_direction_allowed(self, direction: int) -> bool:

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

    def on_init(self) -> bool:
        pygame.init()
        self.display_surf = pygame.display.set_mode((self.width, self.height + STEP_SIZE), pygame.HWSURFACE)
        self.game_area = MySurface(w=self.width, h=STEP_SIZE, rgb=(255, 255, 255)).create()
        self.score_font = MyFont(x=4 * self.width // 5, y=self.height - 2, rgb=(0, 0, 0), font_size=8)
        self.loss_font = MyFont(x=self.width // 8, y=self.height - 2, rgb=(0, 0, 0), font_size=8)
        self.image_surf = MySurface(w=STEP_SIZE, h=STEP_SIZE, rgb=(0, 0, 0)).create()
        self.apple_surf = MySurface(w=STEP_SIZE, h=STEP_SIZE, rgb=(150, 0, 0)).create()
        return True

    def on_render(self):

        self.display_surf.fill((255, 255, 255))  # background
        # self._display_surf.blit(self._game_area, (0, self.height))
        self.score_font.draw(
            surface=self.display_surf,
            my_font=self.score_font.create(),
            text="{}".format(str(self.snake.length - LENGTH).zfill(5))
        )
        self.snake.draw(surface=self.display_surf, image=self.image_surf)
        self.apple.draw(surface=self.display_surf, image=self.apple_surf)
        pygame.display.flip()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    @staticmethod
    def is_collision(x1: int, y1: int, x2: int, y2: int):

        if x2 == x1 and y2 == y1:
            return True
        return False

    def collided_with_boundary(self) -> bool:
        if BOUNDARY:
            if (self.snake.x[0], self.snake.y[0]) in COORDINATES_BOUNDARY:
                return True
        return False

    def collided_with_itself(self) -> bool:

        if any([self.snake.x[0] == x and self.snake.y[0] == y for x, y in zip(self.snake.x[1:], self.snake.y[1:])]):
            return True
        return False

    def eaten_apple(self) -> bool:
        if self.apple.x == self.snake.x[0] and self.apple.y == self.snake.y[0]:
            return True
        return False

    @abstractmethod
    def execute(self) -> float:
        pass


class GameHumanPlayer(Game):

    def execute(self) -> float:

        if not self.on_init():
            self.running = False

        while self.running:

            pygame.event.pump()

            direction = self.get_direction()
            if self._is_direction_allowed(direction=direction):
                self.snake.update(direction=direction)

            if pygame.key.get_pressed()[K_ESCAPE] or (
                    pygame.key.get_pressed()[K_c] and pygame.key.get_pressed()[K_LCTRL]):
                self.running = False

            if self.eaten_apple():
                self.snake.length = self.snake.length + 1
                self.apple = Apple(snake=self.snake)

            if self.collided_with_boundary():
                print("You collided with the boundary")
                self.running = False

            if self.collided_with_itself():
                print("You collided with yourself")
                self.running = False

            self.on_render()

            if FRAME_RATE:
                time.sleep(FRAME_RATE)  # waiting time between frames

        self.on_cleanup()

        return True

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


class GameNeuralNet(Game):

    def __init__(self, name: str, neural_net: FeedForwardNetwork, step_limit: int, path_output: str,
                 show_game: bool = True):
        super().__init__()
        self.name = name
        self.path_score = os.path.join(path_output, name + ".json")
        self.input_vector = compute_input_variables(apple=self.apple, snake=self.snake)
        self.nn = neural_net
        self.score = 0
        self.apple_distance = self._distance_to_apple()
        self.show_game = show_game if show_game is not None else not BACKGROUND_RUN
        self.step_limit = step_limit if step_limit is not None else STEP_LIMIT
        self.loss_font = None

    def execute(self) -> float:

        if not self.on_init():
            self.running = False

        # Check if snake explores all directions
        exploration_score = 0
        steps_total = 0
        steps_without_apple = 0
        while self.running:

            steps_without_apple += 1
            steps_total += 1

            with open(self.path_score, "w") as f:
                f.write(json.dumps({self.name: self.score}))

            if self.show_game:
                pygame.event.pump()

            if pygame.key.get_pressed()[K_ESCAPE] or steps_without_apple >= self.step_limit or (
                    pygame.key.get_pressed()[K_c] and pygame.key.get_pressed()[K_LCTRL]):
                # print("Snake {} has reached the step limit of: {}".format(self.name, self.step_limit))
                self.running = False

            steps_without_apple = self.on_loop(steps_without_apple=steps_without_apple)

            if self.show_game:
                self.on_render()
                self.loss_font.draw(
                    surface=self.display_surf,
                    my_font=self.loss_font.create(),
                    text="{}".format(str(self.score))
                )

            if self.show_game and FRAME_RATE:
                time.sleep(FRAME_RATE)  # waiting time between frames

        self.on_cleanup()

        self.score += exploration_score * steps_total
        print(f"{self.name} finished with score: {self.score}")
        with open(self.path_score, "w") as f:
            f.write(json.dumps({self.name: self.score}))

        return self.score

    def on_loop(self, steps_without_apple: int) -> int:

        direction = self.get_direction()
        if self._is_direction_allowed(direction=direction):
            self.snake.update(direction=direction)

        self.input_vector = compute_input_variables(apple=self.apple, snake=self.snake)

        # is the snake approaching or retracting from the apple?
        apple_distance_current = self._distance_to_apple()
        if apple_distance_current <= self.apple_distance:
            self.score += APPROACHING_SCORE
        else:
            self.score -= RETRACTING_PENALTY
        self.apple_distance = apple_distance_current

        # does snake eat apple?
        if self.is_collision(self.apple.x, self.apple.y, self.snake.x[0], self.snake.y[0]):
            self.snake.length = self.snake.length + 1
            self.apple = Apple(x_snake=self.snake.x[0:self.snake.length], y_snake=self.snake.y[0:self.snake.length])
            self.score += EAT_APPLE_SCORE
            steps_without_apple = 0

        if BOUNDARY:
            if (self.snake.x[0], self.snake.y[0]) in COORDINATES_BOUNDARY:
                self.score -= COLLISION_PENALTY
                print(f"{self.name} collided with the wall.")
                self.running = False

        # does snake collide with itself?
        for i in range(2, self.snake.length - 1):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.score -= COLLISION_PENALTY
                print(f"{self.name} collided with itself")
                self.running = False

        return steps_without_apple

    def _distance_to_apple(self):
        dx_to_right_edge = min(DISPLAY_WIDTH - self.snake.x[0], DISPLAY_WIDTH - self.apple.x)
        dx_outer = dx_to_right_edge + min(self.snake.x[0], self.apple.x)
        dy_to_bottom_edge = min(DISPLAY_HEIGHT - self.snake.y[0], DISPLAY_HEIGHT - self.apple.y)
        dy_outer = dy_to_bottom_edge + min(self.snake.y[0], self.apple.y)

        dx_shortest = min(abs(self.apple.x - self.snake.x[0]), dx_outer)
        dy_shortest = min(abs(self.apple.y - self.snake.y[0]), dy_outer)

        return np.sqrt(dx_shortest ** 2 + dy_shortest ** 2)

    def _on_init(self) -> bool:
        if self.show_game:
            self.on_init()
            pygame.display.set_caption(self.name)
            return True
        return False

    def get_direction(self) -> int:
        prediction = self.nn.activate(self.input_vector)
        assert type(np.argmax(prediction)) == np.int64, "{} is multiple maximal values"
        return int(np.argmax(prediction))
