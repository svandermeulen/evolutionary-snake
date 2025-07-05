"""Conftest containing fixtures for test modules."""

import pytest

from evolutionary_snake import enums, game_settings


@pytest.fixture(name="settings")
def settings_fixture() -> game_settings.Settings:
    """Fixture of settings."""
    return game_settings.Settings(
        run_in_background=True,
        boundary=enums.Boundary.PERIODIC_BOUNDARY,
    )
