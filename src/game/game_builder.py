"""
Created on: 8-2-2018
@author: Stef
"""
import json
import numpy as np
import os
import pygame
import time

from neat.nn import FeedForwardNetwork
from pygame.locals import *

from src.game.snake_builder import Snake
from src.game.snake_rules import Apple, is_collision
from src.machine_learning.loss_calculator import compute_input_variables
from src.config import DISPLAY_WIDTH, DISPLAY_HEIGHT, LENGTH, STEP_SIZE, BOUNDARY, APPROACHING_SCORE, \
    RETRACTING_PENALTY, EAT_APPLE_SCORE, COLLISION_PENALTY, STEP_LIMIT, FRAME_RATE, BACKGROUND_RUN, \
    HUMAN_PLAYER, COORDINATES_BOUNDARY
from src.utils.drawing_manager import MySurface, MyFont


# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

class Game(object):

    def __init__(self, name: str, path_output: str, neural_net: FeedForwardNetwork = None, show_game: bool = None,
                 step_limit: int = None):

        self.name = name
        self.path_score = os.path.join(path_output, name + ".json")
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT
        self._running = True
        self._display_surf = True
        self._game_area = None
        self._image_surf = None
        self._apple_surf = None
        self._boundary_rect = None
        self._score_font = None
        self._loss_font = None
        self.player = Snake(length=LENGTH)
        self.apple = Apple(x_snake=self.player.x[0:self.player.length], y_snake=self.player.y[0:self.player.length])
        self.input_vector = compute_input_variables(apple=self.apple, snake=self.player)
        self.nn = neural_net
        self.score = 0
        self.apple_distance = self._distance_to_apple()
        self.show_game = show_game if show_game is not None else not BACKGROUND_RUN
        self.step_limit = step_limit if step_limit is not None else STEP_LIMIT

    def _distance_to_apple(self):

        dx_to_right_edge = min(DISPLAY_WIDTH - self.player.x[0], DISPLAY_WIDTH - self.apple.x)
        dx_outer = dx_to_right_edge + min(self.player.x[0], self.apple.x)
        dy_to_bottom_edge = min(DISPLAY_HEIGHT - self.player.y[0], DISPLAY_HEIGHT - self.apple.y)
        dy_outer = dy_to_bottom_edge + min(self.player.y[0], self.apple.y)

        dx_shortest = min(abs(self.apple.x - self.player.x[0]), dx_outer)
        dy_shortest = min(abs(self.apple.y - self.player.y[0]), dy_outer)

        return np.sqrt(dx_shortest ** 2 + dy_shortest ** 2)

    def _is_dir_allowed(self) -> dict:

        dx = self.player.x[1] - self.player.x[0]
        dy = self.player.y[1] - self.player.y[0]

        return {
            "right": False if dx % DISPLAY_WIDTH == STEP_SIZE else True,
            "left": False if dx % -DISPLAY_WIDTH == -STEP_SIZE else True,
            "up": False if dy % -DISPLAY_HEIGHT == -STEP_SIZE else True,
            "down": False if dy % DISPLAY_HEIGHT == STEP_SIZE else True
        }

    def on_init(self) -> True:

        if self.show_game:
            pygame.init()
            self._display_surf = pygame.display.set_mode((self.width, self.height + STEP_SIZE), pygame.HWSURFACE)
            pygame.display.set_caption(self.name)
            self._running = True
            self._game_area = MySurface(w=self.width, h=STEP_SIZE, rgb=(255, 255, 255)).create()
            self._score_font = MyFont(x=4 * self.width // 5, y=self.height - 2, rgb=(0, 0, 0), font_size=8)
            self._loss_font = MyFont(x=self.width // 8, y=self.height - 2, rgb=(0, 0, 0), font_size=8)
            self._image_surf = MySurface(w=STEP_SIZE, h=STEP_SIZE, rgb=(0, 0, 0)).create()
            self._apple_surf = MySurface(w=STEP_SIZE, h=STEP_SIZE, rgb=(150, 0, 0)).create()

        return True

    def on_loop(self, steps_without_apple: int) -> int:
        self.player.update()

        self.input_vector = compute_input_variables(apple=self.apple, snake=self.player)

        # is the snake approaching or retracting from the apple?
        apple_distance_current = self._distance_to_apple()
        if apple_distance_current <= self.apple_distance:
            self.score += APPROACHING_SCORE
        else:
            self.score -= RETRACTING_PENALTY
        self.apple_distance = apple_distance_current

        # does snake eat apple?
        if is_collision(self.apple.x, self.apple.y, self.player.x[0], self.player.y[0]):
            self.player.length = self.player.length + 1
            self.apple = Apple(x_snake=self.player.x[0:self.player.length], y_snake=self.player.y[0:self.player.length])
            self.score += EAT_APPLE_SCORE
            steps_without_apple = 0

        if BOUNDARY:
            if (self.player.x[0], self.player.y[0]) in COORDINATES_BOUNDARY:
                self.score -= COLLISION_PENALTY
                print(f"{self.name} collided with the wall.")
                self._running = False

        # does snake collide with itself?
        for i in range(2, self.player.length - 1):
            if is_collision(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i]):
                self.score -= COLLISION_PENALTY
                print(f"{self.name} collided with itself")
                self._running = False

        return steps_without_apple

    def on_render(self):

        self._display_surf.fill((255, 255, 255))  # background
        # self._display_surf.blit(self._game_area, (0, self.height))
        self._score_font.draw(
            surface=self._display_surf,
            my_font=self._score_font.create(),
            text="{}".format(str(self.player.length - LENGTH).zfill(5))
        )
        self._loss_font.draw(
            surface=self._display_surf,
            my_font=self._loss_font.create(),
            text="{}".format(str(self.score))
        )
        self.player.draw(surface=self._display_surf, image=self._image_surf)
        self.apple.draw(surface=self._display_surf, image=self._apple_surf)
        pygame.display.flip()

    @staticmethod
    def on_cleanup():
        pygame.quit()

    def get_direction(self) -> str:

        if not HUMAN_PLAYER:
            prediction = self.nn.activate(self.input_vector)
            assert type(np.argmax(prediction)) == np.int64, "{} is multiple maximal values"
            if np.argmax(prediction) == 0:
                return "right"
            elif np.argmax(prediction) == 1:
                return "left"
            elif np.argmax(prediction) == 2:
                return "up"
            return "down"

        keys = pygame.key.get_pressed()
        if keys[K_DOWN]:
            return "down"
        if keys[K_UP]:
            return "up"
        if keys[K_LEFT]:
            return "left"
        if keys[K_RIGHT]:
            return "right"
        return ""

    def on_execute(self) -> float:

        if not self.on_init():
            self._running = False

        # Check if snake explores all directions
        direction_count = {
            "right": False,
            "left": False,
            "up": False,
            "down": False
        }

        steps_total = 0
        steps_without_apple = 0
        while self._running:

            steps_without_apple += 1
            steps_total += 1

            with open(self.path_score, "w") as f:
                f.write(json.dumps({self.name: self.score}))

            direction = self.get_direction()

            if self.show_game:
                pygame.event.pump()

            allowed_directions = self._is_dir_allowed()

            if direction == "right" and allowed_directions[direction]:
                direction_count["right"] = True
                self.player.move_right()

            if direction == "left" and allowed_directions[direction]:
                direction_count["left"] = True
                self.player.move_left()

            if direction == "up" and allowed_directions[direction]:
                direction_count["up"] = True
                self.player.move_up()

            if direction == "down" and allowed_directions[direction]:
                direction_count["down"] = True
                self.player.move_down()

            if pygame.key.get_pressed()[K_ESCAPE] or steps_without_apple >= self.step_limit or (
                    pygame.key.get_pressed()[K_c] and pygame.key.get_pressed()[K_LCTRL]):
                # print("Snake {} has reached the step limit of: {}".format(self.name, self.step_limit))
                self._running = False

            steps_without_apple = self.on_loop(steps_without_apple=steps_without_apple)

            if self.show_game:
                self.on_render()

            if self.show_game and FRAME_RATE:
                time.sleep(FRAME_RATE)  # waiting time between frames

        self.on_cleanup()

        exploration_score = sum(direction_count.values())
        self.score += exploration_score * steps_total
        print(f"{self.name} finished with score: {self.score}")
        with open(self.path_score, "w") as f:
            f.write(json.dumps({self.name: self.score}))

        return self.score
