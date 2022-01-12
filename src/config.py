"""
Created on: 8-2-2018
@author: Stef
"""
import itertools
import numpy as np

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Config:
    human_player: bool = True
    run_in_parallel: bool = True

    game_size: int = 1 if not human_player else 3
    step_size: int = 5 * game_size
    snake_length: int = 3
    display_width: int = 100 * game_size
    display_height: int = 100 * game_size
    boundary: bool = False
    frame_rate: float = 50 / 500  # if human_player else none

    # neuroevolution settings
    screens_per_row: int = 10
    step_limit: int = np.inf if human_player else 200
    generations: int = 50
    eat_apple_score: int = 100
    approaching_score: int = 1
    retracting_penalty: int = 1.5
    collision_penalty: int = 1000

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
