"""Conftest containing fixtures for test modules."""

import pytest

from evolutionary_snake import enums, game_objects, game_settings


@pytest.fixture(name="settings")
def settings_fixture() -> game_settings.Settings:
    """Fixture of settings."""
    return game_settings.Settings(
        run_in_background=True,
        boundary=enums.Boundary.PERIODIC_BOUNDARY,
    )


@pytest.fixture(name="snake")
def snake_fixture() -> game_objects.Snake:
    """Fixture to create a snake object."""
    return game_objects.Snake(
        length=3,
        width=300,
        height=300,
        step_size=15,
        boundary=enums.Boundary.PERIODIC_BOUNDARY,
    )


@pytest.fixture(name="apple")
def apple_fixture(
    settings: game_settings.Settings, snake: game_objects.Snake
) -> game_objects.Apple:
    """Fixture to create an apple object."""
    return game_objects.Apple(
        snake_coordinates=snake.coordinates,
        settings=settings,
        seed=1234,
    )
