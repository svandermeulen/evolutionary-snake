"""Module for defining the human game mode."""

import pygame

from evolutionary_snake import enums
from evolutionary_snake.game_modes import base_game_mode


class HumanGameMode(base_game_mode.BaseGameMode):
    """Class definition of the human game mode."""

    def game_ending_conditions_other(self) -> bool:
        """Extend the game ending conditions."""
        return False

    def get_direction(self) -> enums.Direction:
        """Get the direction of the human game mode."""
        direction = self.snake.direction
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            direction = enums.Direction.DOWN
        if keys[pygame.K_UP]:
            direction = enums.Direction.UP
        if keys[pygame.K_LEFT]:
            direction = enums.Direction.LEFT
        if keys[pygame.K_RIGHT]:
            direction = enums.Direction.RIGHT
        return direction

    def _loop(self) -> None:
        """Extend the loop function."""
        if self.eaten_apple():
            self.update_eating_apple()

    def process_score(self) -> None:
        """Process the score upon cleaning up."""
        return
