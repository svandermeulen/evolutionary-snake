"""Module to test the boundary factory."""

import pytest

from evolutionary_snake import game_settings
from evolutionary_snake.game_objects import boundaries
from evolutionary_snake.game_objects.boundaries import boundary_factory


def test_boundary_factory(settings: game_settings.Settings) -> None:
    """Test the boundary factory."""
    boundary = boundary_factory.boundary_factory(settings=settings)
    assert isinstance(boundary, boundaries.PeriodicBoundary)


def test_boundary_factory_with_invalid_input(settings: game_settings.Settings) -> None:
    """Test the boundary factory with invalid settings."""
    settings.boundary_type = "invalid_boundary_type"  # type: ignore[assignment]
    with pytest.raises(NotImplementedError):
        boundary_factory.boundary_factory(settings=settings)
