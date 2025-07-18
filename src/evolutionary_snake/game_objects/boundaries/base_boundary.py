"""Base boundary game object."""

from evolutionary_snake import game_settings


class BaseBoundary:  # pylint: disable=too-few-public-methods
    """Base Boundary game object."""

    def __init__(self, settings: game_settings.Settings) -> None:
        """Initialize the boundary game object."""
        self.y_max = settings.display_height
        self.x_max = settings.display_width
        self.step_size = settings.step_size
