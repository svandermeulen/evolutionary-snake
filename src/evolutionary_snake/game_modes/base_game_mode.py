"""Base game mode definition."""

import abc
import os
import time

import pygame

from evolutionary_snake import enums, game_objects, game_settings
from evolutionary_snake.game_canvas import canvas

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"


class BaseGameMode(abc.ABC):
    """Base game mode."""

    def __init__(self, settings: game_settings.Settings) -> None:
        """Initialize the base game mode."""
        self.settings = settings
        self.running = True
        self.score = 0
        self.snake = game_objects.Snake(
            length=settings.snake_length_init,
            width=settings.display_width,
            height=settings.display_height,
            step_size=settings.step_size,
            boundary=settings.boundary,
        )
        self.apple = self.generate_apple()
        self.canvas = (
            canvas.Canvas(settings=settings) if not settings.run_in_background else None
        )

    def run(self) -> None:
        """Run the snake game."""
        pygame.init()
        while self.running:
            if not self.game_continues():
                self.running = False
                break
            self.loop()
            self.render()
            time.sleep(1 / self.settings.frame_rate_fps)
        self.cleanup()

    def game_continues(self) -> bool:
        """Return True if the game should continue."""
        return not (
            self.game_ending_key_press()
            or self.collided()
            or self.game_ending_conditions_other()
        )

    def loop(self) -> None:
        """The main loop of the game mode."""
        pygame.event.pump()
        direction = self.get_direction()
        self.snake.update(direction=direction)
        self._loop()

    def generate_apple(self) -> game_objects.Apple:
        """Generate an apple for the game mode."""
        return game_objects.Apple(
            snake_coordinates=[
                self.snake.x[0 : self.snake.length],
                self.snake.y[0 : self.snake.length],
            ],
            settings=self.settings,
        )

    @abc.abstractmethod
    def get_direction(self) -> enums.Direction:
        """Return the direction the snake should go."""

    @abc.abstractmethod
    def _loop(self) -> None:
        """Extend the actions that should be taken in the loop."""

    def render(self) -> None:
        """Project game state on a canvas."""
        if not self.settings.run_in_background and self.canvas:
            self.canvas.draw(score=self.score, snake=self.snake, apple=self.apple)

    def collided(self) -> bool:
        """Return True if the snake collided with anything."""
        return self.collided_with_itself() or self.collided_with_boundary()

    def collided_with_boundary(self) -> bool:
        """Return True if the snake collides with the boundary."""
        if self.settings.boundary == enums.Boundary.PERIODIC_BOUNDARY:
            return False
        if self.settings.boundary == enums.Boundary.HARD_BOUNDARY:
            return (
                self.snake.x[0],
                self.snake.y[0],
            ) in self.settings.get_coordinates_boundary()
        msg = f"Unexpected boundary type: {self.settings.boundary}"
        raise NotImplementedError(msg)

    def collided_with_itself(self) -> bool:
        """Return True if the snake collides with itself."""
        return any(
            self.snake.x[0] == x and self.snake.y[0] == y
            for x, y in zip(self.snake.x[1:], self.snake.y[1:], strict=False)
        )

    def eaten_apple(self) -> bool:
        """Return True if the snake eaten the apple."""
        return self.apple.x == self.snake.x[0] and self.apple.y == self.snake.y[0]

    def update_eating_apple(self) -> None:
        """Update game state when eaten an apple."""
        self.snake.length += 1
        self.apple = self.generate_apple()
        self.score += 1

    @staticmethod
    def game_ending_key_press() -> bool:
        """Keys to end the game."""
        return pygame.key.get_pressed()[pygame.K_ESCAPE]

    @abc.abstractmethod
    def game_ending_conditions_other(self) -> bool:
        """Extend the game ending conditions."""

    def cleanup(self) -> None:
        """Clean up after quiting the game mode."""
        self.process_score()
        self.render()
        pygame.quit()

    @abc.abstractmethod
    def process_score(self) -> None:
        """Process the score upon cleaning up."""
