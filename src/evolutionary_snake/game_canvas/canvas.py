"""The game canvas."""

import pygame

from evolutionary_snake import game_objects


def draw(
    snake: game_objects.Snake,
    apple: game_objects.Apple | None = None,
    score: int | None = None,
    loss: int | None = None,
) -> pygame.Surface:
    """Draw the game canvas."""
    if not pygame.get_init():
        pygame.init()

    canvas = pygame.display.set_mode(
        (snake.width, snake.height + snake.step_size), pygame.HWSURFACE
    )
    canvas.fill((255, 255, 255))

    image_snake = MySurface(
        width=snake.step_size, height=snake.step_size, rgb=(0, 0, 0)
    ).create()
    for i in range(snake.length):
        canvas.blit(image_snake, (snake.x[i], snake.y[i]))

    if apple is not None:
        image_apple = MySurface(
            width=snake.step_size, height=snake.step_size, rgb=(150, 0, 0)
        ).create()
        canvas.blit(image_apple, (apple.x, apple.y))

    if score is not None:
        score_font = MyFont(
            x=4 * snake.width // 5, y=snake.height - 2, rgb=(0, 0, 0), font_size=8
        )
        score_font.draw(
            surface=canvas,
            my_font=score_font.create(),
            text=f"{str(score).zfill(5)}",
        )

    if loss is not None:
        loss_font = MyFont(
            x=1 * snake.width // 5, y=snake.height - 2, rgb=(0, 0, 0), font_size=8
        )
        loss_font.draw(surface=canvas, my_font=loss_font.create(), text=f"{loss!s}")

    pygame.display.flip()

    return canvas


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
