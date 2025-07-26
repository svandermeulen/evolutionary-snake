"""Conftest containing fixtures for test modules."""

import pathlib

import neat
import pytest

from evolutionary_snake import game_objects, settings
from evolutionary_snake.game_objects.boundaries import base_boundary, boundary_factory
from evolutionary_snake.utils import enums, utility_functions


@pytest.fixture(name="game_settings")
def game_settings_fixture() -> settings.GameSettings:
    """Fixture of settings."""
    return settings.GameSettings(
        run_in_background=True,
        boundary_type=enums.BoundaryType.PERIODIC_BOUNDARY,
    )


@pytest.fixture(name="neat_config")
def neat_config_fixture(path_neat_config: pathlib.Path) -> neat.Config:
    """Fixture to return a neat config instance."""
    return utility_functions.get_neat_config(path_neat_config)


@pytest.fixture(name="neural_net")
def neural_net_fixture(neat_config: neat.Config) -> neat.nn.FeedForwardNetwork:
    """Fixture to return an AI neural network instance."""
    return neat.nn.FeedForwardNetwork.create(
        neat.DefaultGenome(key=1),
        config=neat_config,
    )


@pytest.fixture(name="ai_settings")
def ai_settings_fixture(
    game_settings: settings.GameSettings,
    neural_net: neat.nn.FeedForwardNetwork,
) -> settings.AiGameSettings:
    """Fixture of AI settings."""
    game_settings.boundary_type = enums.BoundaryType.HARD_BOUNDARY
    return settings.AiGameSettings(**game_settings.model_dump(), neural_net=neural_net)


@pytest.fixture(name="boundary")
def boundary_fixture(
    game_settings: settings.GameSettings,
) -> base_boundary.BaseBoundary:
    """Fixture of boundary."""
    return boundary_factory.boundary_factory(game_settings)


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
    game_settings: settings.GameSettings,
    boundary: base_boundary.BaseBoundary,
    snake: game_objects.Snake,
) -> game_objects.Apple:
    """Fixture to create an apple object."""
    return game_objects.Apple(
        boundary=boundary,
        snake_coordinates=snake.coordinates,
        settings=game_settings,
    )
