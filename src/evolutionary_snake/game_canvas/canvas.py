"""The game canvas."""

import pygame

from evolutionary_snake import game_objects, game_settings


class Canvas:
    """The game canvas."""

    def __init__(self, settings: game_settings.Settings) -> None:
        """Initialize the game canvas."""
        if not pygame.get_init():
            pygame.init()
        self.settings = settings
        self.canvas = pygame.display.set_mode(
            (settings.display_width, settings.display_height + settings.step_size),
            pygame.HWSURFACE,
        )
        self.canvas.fill((255, 255, 255))

    def draw_snake(self, snake: game_objects.Snake) -> None:
        """Draw the snake."""
        image_snake = MySurface(
            width=snake.step_size, height=snake.step_size, rgb=(0, 0, 0)
        ).create()
        self.canvas.fill((255, 255, 255))
        for i in range(snake.length):
            self.canvas.blit(image_snake, (snake.x[i], snake.y[i]))

    def draw_apple(self, apple: game_objects.Apple) -> None:
        """Draw the apple."""
        image_apple = MySurface(
            width=self.settings.step_size,
            height=self.settings.step_size,
            rgb=(150, 0, 0),
        ).create()
        self.canvas.blit(image_apple, (apple.x, apple.y))

    def draw_score(self, score: int) -> None:
        """Draw the score."""
        score_font = MyFont(
            x=4 * self.settings.display_width // 5,
            y=self.settings.display_height - 2,
            rgb=(0, 0, 0),
            font_size=8,
        )
        score_font.draw(
            surface=self.canvas,
            my_font=score_font.create(),
            text=f"{str(score).zfill(5)}",
        )

    def draw(
        self,
        snake: game_objects.Snake,
        apple: game_objects.Apple,
        score: int = 0,
    ) -> pygame.Surface:
        """Draw the canvas and its objects."""
        self.draw_snake(snake)
        self.draw_apple(apple)
        self.draw_score(score)
        pygame.display.flip()
        return self.canvas


class MySurface:  # pylint: disable=too-few-public-methods
    """Canvas surface object."""

    def __init__(self, width: int, height: int, rgb: tuple[int, int, int]) -> None:
        """Initialize the surface."""
        self.width = width
        self.height = height
        self.rgb = rgb

    def create(self) -> pygame.Surface:
        """Create the surface."""
        my_surface = pygame.Surface((self.width, self.height))
        my_surface.fill(self.rgb)
        return my_surface


class MyFont:
    """Font object."""

    def __init__(
        self, x: int, y: int, rgb: tuple[int, int, int], font_size: int
    ) -> None:
        """Initialize the font object."""
        self.rgb = rgb
        self.x = x
        self.y = y
        self.font_size = font_size

    def create(self) -> pygame.font.Font:
        """Create the font."""
        return pygame.font.SysFont("Arial", self.font_size)

    def draw(
        self,
        surface: pygame.Surface,
        my_font: pygame.font.Font,
        text: str,
        *,
        anti_alias: bool = True,
    ) -> None:
        """Draw the font."""
        label = my_font.render(text, anti_alias, self.rgb)
        surface.blit(label, (self.x, self.y))
