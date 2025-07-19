"""Config of the evolutionary snake game."""

import itertools
import pathlib

import neat
import pydantic

from evolutionary_snake.utils import enums


class GameSettings(pydantic.BaseModel):
    """Settings of the evolutionary snake game."""

    game_size: int = 3
    step_size: int = 5 * game_size
    snake_length_init: int = 3
    display_width: int = 100 * game_size
    display_height: int = 100 * game_size
    boundary_type: enums.BoundaryType = enums.BoundaryType.HARD_BOUNDARY
    frame_rate_fps: float = 20
    run_in_background: bool = False

    @property
    def coordinates_grid(self) -> list[tuple[int, int]]:
        """Returns the coordinates of the snake game grid."""
        x_list = list(range(0, self.display_width + self.step_size, self.step_size))
        y_list = list(range(0, self.display_height + self.step_size, self.step_size))
        return list(itertools.product(x_list, y_list))


class AiGameSettings(GameSettings):
    """Settings of the AI game mode."""

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)
    name: str = "AI Snake"
    path_neat_config: pathlib.Path = (
        pathlib.Path(__file__).parents[3] / "data" / "neat_config"
    )
    neural_net: neat.nn.FeedForwardNetwork
    step_limit: int = 50
    approaching_score: int = 1
    retracting_penalty: float = 1.5
    eat_apple_score: int = 100
    collision_penalty: int = 1000
    node_names: dict[int, str] = {
        -1: "Apple_left",
        -2: "Apple_right",
        -3: "Apple_up",
        -4: "Apple_down",
        -5: "Right_clear",
        -6: "Left_clear",
        -7: "Bottom_clear",
        -8: "Up_clear",
        0: "RIGHT",
        1: "LEFT",
        2: "UP",
        3: "DOWN",
    }
