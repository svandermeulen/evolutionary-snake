"""Module to build a boundary factory."""

from evolutionary_snake import enums, game_settings
from evolutionary_snake.game_objects import boundaries
from evolutionary_snake.game_objects.boundaries import base_boundary

BoundaryDict: dict[enums.BoundaryType, type[base_boundary.BaseBoundary]] = {
    enums.BoundaryType.HARD_BOUNDARY: boundaries.HardBoundary,
    enums.BoundaryType.PERIODIC_BOUNDARY: boundaries.PeriodicBoundary,
}


def boundary_factory(settings: game_settings.Settings) -> base_boundary.BaseBoundary:
    """Factory method for creating a boundary object."""
    boundary = BoundaryDict.get(settings.boundary_type)
    if boundary is None:
        msg = f"{settings.boundary_type} is not a valid boundary type"
        raise NotImplementedError(msg)
    return boundary(settings)
