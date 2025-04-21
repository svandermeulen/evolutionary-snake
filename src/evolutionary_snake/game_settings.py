"""Config of the evolutionary snake game."""

import itertools

import pydantic


class Settings(pydantic.BaseModel):
    """Settings of the evolutionary snake game."""

    game_size: int = 3
    step_size: int = 5 * game_size
    snake_length_init: int = 3
    display_width: int = 100 * game_size
    display_height: int = 100 * game_size
    boundary: bool = False
    frame_rate_fps: float = 60
    run_in_background: bool = False

    def get_coordinates_grid(self) -> list[tuple[int, int]]:
        """Returns the coordinates of the snake game grid."""
        x_list = list(range(0, self.display_width + self.step_size, self.step_size))
        y_list = list(range(0, self.display_height + self.step_size, self.step_size))
        return list(itertools.product(x_list, y_list))

    def get_coordinates_boundary(self) -> list[tuple[int, int]]:
        """Returns the coordinates of the snake game boundary."""
        y_list = list(range(0, self.display_height + self.step_size, self.step_size))
        coordinates_boundary = [(-self.step_size, c) for c in y_list]
        coordinates_boundary.extend([(self.display_width, c) for c in y_list])
        coordinates_boundary.extend([(c, -self.step_size) for c in y_list])
        coordinates_boundary.extend([(c, self.display_height) for c in y_list])
        return coordinates_boundary
