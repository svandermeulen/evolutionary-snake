"""Module for defining the human game mode."""

import logging

import pygame

from evolutionary_snake.game_modes import base_game_mode
from evolutionary_snake.utils import enums

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class HumanGameMode(base_game_mode.BaseGameMode):
    """Class definition of the human game mode."""

    def game_ending_conditions_other(self) -> bool:
        """Extend the game ending conditions."""
        return False

    def get_direction(self) -> enums.Direction:
        """Get the direction of the human game mode."""
        direction = self.snake.direction
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    return enums.Direction.DOWN
                if event.key == pygame.K_UP:
                    return enums.Direction.UP
                if event.key == pygame.K_LEFT:
                    return enums.Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    return enums.Direction.RIGHT
        return direction

    def _loop(self, direction: enums.Direction) -> None:
        """Extend the loop function."""
        del direction
        if self.eaten_apple():
            self.update_eating_apple()

    def process_score(self) -> None:
        """Process the score upon cleaning up."""
        msg = f"Your final score is: {self.score}"
        logger.info(msg)
