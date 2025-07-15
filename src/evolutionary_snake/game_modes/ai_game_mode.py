"""Module for defining the ai game mode."""

import logging
import math

import numpy as np
from neat import nn

from evolutionary_snake import enums, game_settings, machine_learning
from evolutionary_snake.game_modes import base_game_mode

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class LossComponents:  # pylint: disable=too-few-public-methods
    """Loss components to keep track of for computing loss."""

    def __init__(self) -> None:
        """Initialize the loss components object."""
        self.steps_total: int = 0
        self.direction_counts: dict[enums.Direction, int] = {
            enums.Direction.LEFT: 0,
            enums.Direction.RIGHT: 0,
            enums.Direction.UP: 0,
            enums.Direction.DOWN: 0,
        }
        self.loss: float = 0


class AiGameMode(base_game_mode.BaseGameMode):
    """The AI game mode class."""

    def __init__(
        self,
        settings: game_settings.AiGameSettings,
        name: str,
        neural_net: nn.FeedForwardNetwork,
    ) -> None:
        """Initialize the AI game mode."""
        super().__init__(settings=settings)
        self.settings: game_settings.AiGameSettings = settings
        self.name = name
        self.neural_net = neural_net
        self.steps_without_apple = 0
        self.apple_distance = self.distance_to_apple()
        self.input_vector = machine_learning.InputVector(
            snake=self.snake, apple=self.apple
        )
        self.loss_components = LossComponents()

    def process_score(self) -> None:
        """Process the score upon cleaning up."""
        if self.collided():
            self.loss_components.loss -= self.settings.collision_penalty
        self.loss_components.loss += self.loss_components.steps_total
        exploration_minimum = min(self.loss_components.direction_counts.values())
        if exploration_minimum > 0:
            msg = (
                f"{self.name} utilized all directions at least "
                f"{exploration_minimum} times."
            )
            logger.info(msg)
            self.loss_components.loss *= math.sqrt(exploration_minimum + 1)

        msg = (
            f"Loss: {self.loss_components.loss}"
            f"{self.name} finished with:\n\t"
            f"steps total: {self.loss_components.steps_total}\n\t"
            f"loss: {self.loss_components.loss}\n\t"
            f"score: {self.score}"
        )
        logger.info(msg)

    def game_ending_conditions_other(self) -> bool:
        """Extend the game ending conditions."""
        if self.steps_without_apple >= self.settings.step_limit >= 0:
            msg = f"{self.name} played too long without eating apple"
            logger.info(msg)
            return True
        return False

    def _loop(self) -> None:
        """Extend the actions that should be taken in the loop."""
        # is the snake approaching or retracting from the apple?
        apple_distance_current = self.distance_to_apple()
        if apple_distance_current <= self.apple_distance:
            self.loss_components.loss += self.settings.approaching_score
        else:
            self.loss_components.loss -= self.settings.retracting_penalty
        self.apple_distance = apple_distance_current

        if self.eaten_apple():
            self.update_eating_apple()
            self.loss_components.loss += self.settings.eat_apple_score
            self.steps_without_apple = 0
        else:
            self.steps_without_apple += 1

        self.input_vector = machine_learning.InputVector(
            snake=self.snake, apple=self.apple
        )
        self.loss_components.steps_total += 1

    def distance_to_apple(self) -> float:
        """Measure the distance to the apple."""
        dx_to_right_edge = min(
            self.snake.width - self.snake.x[0], self.snake.width - self.apple.x
        )
        dx_outer = dx_to_right_edge + min(self.snake.x[0], self.apple.x)
        dy_to_bottom_edge = min(
            self.snake.height - self.snake.y[0], self.snake.height - self.apple.y
        )
        dy_outer = dy_to_bottom_edge + min(self.snake.y[0], self.apple.y)

        dx_shortest = min(abs(self.apple.x - self.snake.x[0]), dx_outer)
        dy_shortest = min(abs(self.apple.y - self.snake.y[0]), dy_outer)

        return math.sqrt(dx_shortest**2 + dy_shortest**2)

    def get_direction(self) -> enums.Direction:
        """Return the direction the snake should go."""
        prediction = self.neural_net.activate(self.input_vector.values)
        if not isinstance(np.argmax(prediction), np.int64):
            msg = f"{prediction} is multiple maximal values"
            raise TypeError(msg)
        direction = enums.Direction(int(np.argmax(prediction)))
        self.loss_components.direction_counts[direction] += 1
        return direction
