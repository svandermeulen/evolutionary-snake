"""Module to test the AI game mode."""

import pathlib

import neat
import pygame
import pytest

from evolutionary_snake import enums, game_modes, game_objects, game_settings
from tests.evolutionary_snake.helper_methods import helper_functions


@pytest.fixture(name="path_neat_config")
def path_neat_config_fixture() -> pathlib.Path:
    """Path to a test neat config file."""
    return pathlib.Path(__file__).parents[2] / "data" / "test_neat_config"


@pytest.fixture(name="neat_config")
def neat_config_fixture(path_neat_config: pathlib.Path) -> neat.Config:
    """Fixture to return a neat config instance."""
    return neat.Config(
        genome_type=neat.DefaultGenome,
        reproduction_type=neat.DefaultReproduction,
        species_set_type=neat.DefaultSpeciesSet,
        stagnation_type=neat.DefaultStagnation,
        filename=path_neat_config,
    )


@pytest.fixture(name="neural_net")
def neural_net_fixture(neat_config: neat.Config) -> neat.nn.FeedForwardNetwork:
    """Fixture to return an AI neural network instance."""
    return neat.nn.FeedForwardNetwork.create(
        neat.DefaultGenome(key=1),
        config=neat_config,
    )


@pytest.fixture(name="game_mode")
def game_mode_fixture(
    ai_settings: game_settings.AiGameSettings,
    neural_net: neat.nn.FeedForwardNetwork,
) -> game_modes.AiGameMode:
    """Fixture to return a AI game mode instance."""
    game_mode = game_modes.AiGameMode(
        settings=ai_settings,
        name="Test Snake",
        neural_net=neural_net,
    )
    game_mode.snake.direction = enums.Direction.RIGHT
    game_mode.apple.x = (ai_settings.display_width // 2) - 2 * ai_settings.step_size
    game_mode.apple.y = (ai_settings.display_height // 2) + 2 * ai_settings.step_size

    return game_mode


def test_ai_game_mode_snake_runs_into_hard_boundary(
    game_mode: game_modes.AiGameMode,
) -> None:
    """Test the AI game mode until snake hits the hard boundary."""
    # GIVEN an AI game_mode with a hard boundary game setting
    game_mode.settings.boundary_type = enums.BoundaryType.HARD_BOUNDARY
    # WHEN the game is run
    game_mode.run()
    # THEN after the run has finished the running attribute is equal to False.
    assert not game_mode.running
    # AND the snake should have taken 10 steps
    exp_steps_without_apple = 10
    assert game_mode.steps_without_apple == exp_steps_without_apple
    # AND the loss should be equal to an expected value
    exp_loss = -997.5
    assert game_mode.loss_tracker.loss == exp_loss
    # AND the score should be equal to 0
    assert game_mode.score == 0


def test_ai_game_mode_snake_eats_apple(
    game_mode: game_modes.AiGameMode,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the AI game mode until snake eats an apple."""

    # GIVEN an AI game_mode with a hard boundary game setting
    # AND a direction that always moves to the right
    def move_to_the_right() -> enums.Direction:
        return enums.Direction.RIGHT

    monkeypatch.setattr(game_mode, "get_direction", move_to_the_right)
    # AND an apple positioned so that it gets eaten
    game_mode.apple.x = 165
    game_mode.apple.y = 150

    # AND the next apple always positioned in the same place
    def _generate_apple() -> game_objects.Apple:
        return game_mode.apple

    monkeypatch.setattr(game_mode, "generate_apple", _generate_apple)

    # AND the game is ended by running around too long without eating an apple
    game_mode.settings.step_limit = 2
    # WHEN the game is run
    game_mode.run()
    # THEN after the run has finished the running attribute is equal to False.
    assert not game_mode.running
    # AND the expected number of steps without apple matches
    exp_steps_without_apple = 2
    assert game_mode.steps_without_apple == exp_steps_without_apple
    # AND the total of steps taken matches
    exp_steps_total = 3
    assert game_mode.loss_tracker.steps_total == exp_steps_total
    # AND the loss should be equal to an expected value
    exp_loss = 101.0
    assert game_mode.loss_tracker.loss == exp_loss
    # AND the score should be equal to 0
    assert game_mode.score == 1


def test_ai_game_mode_snake_explores_all_directions(
    game_mode: game_modes.AiGameMode,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the AI game mode when snake explores all directions."""
    # GIVEN an AI game_mode with a hard boundary game setting
    # AND a direction that sequentially moves in all directions
    directions = [
        enums.Direction.UP,
        enums.Direction.LEFT,
        enums.Direction.DOWN,
        enums.Direction.RIGHT,
        enums.Direction.UP,
    ]
    monkeypatch.setattr(
        game_mode, "get_direction", helper_functions.get_direction_generator(directions)
    )
    # AND an apple positioned so that it gets eaten
    game_mode.apple.x = 165
    game_mode.apple.y = 150

    # AND the next apple always positioned in the same place
    def _generate_apple() -> game_objects.Apple:
        return game_mode.apple

    monkeypatch.setattr(game_mode, "generate_apple", _generate_apple)

    # AND the game is ended by pressing ESCAPE
    keys_pressed = [pygame.KEYUP] * 5 + [pygame.K_ESCAPE]
    monkeypatch.setattr(
        "pygame.key.get_pressed", helper_functions.get_pressed_generator(keys_pressed)
    )
    # WHEN the game is run
    game_mode.run()
    # THEN after the run has finished the running attribute is equal to False.
    assert not game_mode.running
    # AND the total of steps taken matches
    exp_steps_total = 5
    assert game_mode.loss_tracker.steps_total == exp_steps_total
    # AND the loss should be equal to an expected value
    exp_loss = 7
    assert round(game_mode.loss_tracker.loss) == exp_loss
    # AND the score should be equal to 0
    assert game_mode.score == 0
