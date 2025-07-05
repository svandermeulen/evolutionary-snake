"""Module to test the human game mode."""

from collections.abc import Callable

import pygame
import pytest

from evolutionary_snake import enums, game_modes, game_objects, game_settings


@pytest.fixture(name="settings")
def settings_fixture() -> game_settings.Settings:
    """Fixture of settings."""
    return game_settings.Settings(run_in_background=True)


@pytest.fixture(name="game_mode")
def game_mode_fixture(settings: game_settings.Settings) -> game_modes.HumanGameMode:
    """Fixture to return a human game mode instance."""
    game_mode = game_modes.HumanGameMode(
        settings=settings,
    )
    snake = game_objects.Snake(
        settings=settings,
    )
    snake.direction = enums.Direction.RIGHT
    game_mode.snake = snake
    game_mode.apple.x = (settings.display_width // 2) - 2 * settings.step_size
    game_mode.apple.y = (settings.display_height // 2) + 2 * settings.step_size

    return game_mode


def get_event_generator(
    events: list[pygame.event.Event],
) -> Callable[[], list[pygame.event.Event]]:
    """Helper function to return an event generator."""
    events_generator = ([event] for event in events)
    return lambda: next(events_generator)


def get_pressed_generator(events: list[int]) -> Callable[[], tuple[bool, ...]]:
    """Helper function to return key pressed generator."""
    scan_code_wrappers = []
    for event in events:
        scan_code_wrapper = [False] * 1000
        scan_code_wrapper[event] = True
        scan_code_wrappers.append(tuple(scan_code_wrapper))
    events_generator = (wrapper for wrapper in scan_code_wrappers)
    return lambda: next(events_generator)


def test_human_game_mode_run(
    game_mode: game_modes.HumanGameMode,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test if the score grows if the snake eats an apple."""
    # GIVEN a game_mode
    events = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE),
    ]
    monkeypatch.setattr("pygame.event.get", get_event_generator(events))

    keys_pressed = [pygame.KEYDOWN, pygame.KEYUP, pygame.K_ESCAPE]
    monkeypatch.setattr("pygame.key.get_pressed", get_pressed_generator(keys_pressed))
    # WHEN the run method of the game_mode is called
    game_mode.run()
    # THEN the running attribute is equal to False.
    assert not game_mode.running


def test_human_game_mode_no_movements(
    game_mode: game_modes.HumanGameMode,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the human game mode without any movements."""
    # GIVEN a HumanGameMode instance
    # AND a series of non-direction keys are pressed
    events = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE),
    ]
    monkeypatch.setattr("pygame.event.get", get_event_generator(events))
    keys_pressed = [pygame.KEYDOWN, pygame.KEYUP, pygame.K_ESCAPE]
    monkeypatch.setattr("pygame.key.get_pressed", get_pressed_generator(keys_pressed))
    # AND a initial direction
    direction_initial = game_mode.snake.direction
    # WHEN the game is started
    game_mode.run()
    # THEN the snake direction should be equal to the initial direction
    assert game_mode.snake.direction == direction_initial


def test_human_game_mode_move_up(
    game_mode: game_modes.HumanGameMode,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the human game mode get_direction."""
    # GIVEN a HumanGameMode instance
    # WHEN the up key is pressed
    events = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP),
    ]
    monkeypatch.setattr("pygame.event.get", get_event_generator(events))
    keys_pressed = [pygame.KEYUP, pygame.K_ESCAPE]
    monkeypatch.setattr("pygame.key.get_pressed", get_pressed_generator(keys_pressed))
    game_mode.run()
    # THEN the direction of the snake should also be UP
    assert game_mode.snake.direction == enums.Direction.UP


def test_human_game_mode_eats_apple(
    game_mode: game_modes.HumanGameMode,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test if the score grows if the snake eats an apple."""
    # GIVEN a game_mode with an apple on a predefined position
    # AND a sequence of direction events
    events = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT),
    ]
    monkeypatch.setattr("pygame.event.get", get_event_generator(events))
    keys_pressed = [
        pygame.KEYDOWN,
        pygame.KEYDOWN,
        pygame.KEYDOWN,
        pygame.KEYDOWN,
        pygame.KEYDOWN,
        pygame.K_ESCAPE,
    ]
    monkeypatch.setattr("pygame.key.get_pressed", get_pressed_generator(keys_pressed))
    # WHEN the game loop is run
    game_mode.run()
    # THEN the score of the game should be equal to 1.
    assert game_mode.score == 1
