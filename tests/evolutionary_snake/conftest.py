"""Conftest containing fixtures for test modules."""

import pytest

from evolutionary_snake import enums, game_objects, game_settings
from evolutionary_snake.game_objects.boundaries import base_boundary, boundary_factory


@pytest.fixture(name="settings")
def ai_settings() -> game_settings.Settings:
    """Fixture of settings."""
    return game_settings.Settings(
        run_in_background=True,
        boundary_type=enums.BoundaryType.PERIODIC_BOUNDARY,
    )


@pytest.fixture(name="ai_settings")
def ai_settings_fixture(
    settings: game_settings.Settings,
) -> game_settings.AiGameSettings:
    """Fixture of AI settings."""
    settings.boundary_type = enums.BoundaryType.HARD_BOUNDARY
    return game_settings.AiGameSettings(**settings.model_dump())


@pytest.fixture(name="boundary")
def boundary_fixture(settings: game_settings.Settings) -> base_boundary.BaseBoundary:
    """Fixture of boundary."""
    return boundary_factory.boundary_factory(settings)


@pytest.fixture(name="snake")
def snake_fixture(boundary: base_boundary.BaseBoundary) -> game_objects.Snake:
    """Fixture to create a snake object."""
    return game_objects.Snake(
        length=3,
        width=300,
        height=300,
        step_size=15,
        boundary=boundary,
    )


@pytest.fixture(name="apple")
def apple_fixture(
    settings: game_settings.Settings,
    boundary: base_boundary.BaseBoundary,
    snake: game_objects.Snake,
) -> game_objects.Apple:
    """Fixture to create an apple object."""
    return game_objects.Apple(
        boundary=boundary,
        snake_coordinates=snake.coordinates,
        settings=settings,
        seed=1234,
    )
