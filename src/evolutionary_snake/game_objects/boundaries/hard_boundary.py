"""The hard boundary is a rectangular boundary."""

from evolutionary_snake.game_objects.boundaries import base_boundary


class HardBoundary(base_boundary.BaseBoundary):  # pylint: disable=too-few-public-methods
    """The hard boundary game object."""

    @property
    def coordinates(self) -> list[tuple[int, int]]:
        """Returns the coordinates of the snake game boundary."""
        y_list = list(range(0, self.y_max + self.step_size, self.step_size))
        coordinates_boundary = [(-self.step_size, c) for c in y_list]
        coordinates_boundary.extend([(self.x_max, c) for c in y_list])
        coordinates_boundary.extend([(c, -self.step_size) for c in y_list])
        coordinates_boundary.extend([(c, self.y_max) for c in y_list])
        return coordinates_boundary
