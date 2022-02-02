"""
Created on: 8-2-2018
@author: Stef
"""
import itertools
import numpy as np

from dataclasses import dataclass
from typing import List, Tuple


class Config:

    def __init__(self, mode: str):

        self.mode: str = mode
        self.human_player: bool = True if mode == "human_player" else False
        self.run_in_parallel: bool = True

        self.game_size: int = 1 if not self.human_player else 3
        self.step_size: int = 5 * self.game_size
        self.snake_length: int = 3
        self.display_width: int = 100 * self.game_size
        self.display_height: int = 100 * self.game_size
        self.boundary: bool = False
        self.frame_rate: float = 1 / 10 if self.human_player else None

        # neuroevolution settings
        self.screens_per_row: int = 10
        self.step_limit: int = np.inf if self.human_player else 50
        self.generations: int = 100
        self.eat_apple_score: int = 100
        self.approaching_score: int = 1
        self.retracting_penalty: float = 1.5
        self.collision_penalty: int = 1000

    def get_coordinates_grid(self) -> List[Tuple[int, int]]:
        x_list = list(range(0, self.display_width + self.step_size, self.step_size))
        y_list = list(range(0, self.display_height + self.step_size, self.step_size))
        return list(itertools.product(x_list, y_list))

    def get_coordinates_boundary(self) -> List[Tuple[int, int]]:
        y_list = list(range(0, self.display_height + self.step_size, self.step_size))
        coordinates_boundary = [(-self.step_size, c) for c in y_list]
        coordinates_boundary.extend([(self.display_width, c) for c in y_list])
        coordinates_boundary.extend([(c, -self.step_size) for c in y_list])
        coordinates_boundary.extend([(c, self.display_height) for c in y_list])
        return coordinates_boundary
