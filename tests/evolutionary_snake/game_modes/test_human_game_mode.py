"""Module to test the human game mode."""

import pygame
import pytest

from evolutionary_snake import enums, game_modes, game_objects, game_settings


@pytest.fixture(name="settings")
def settings_fixture() -> game_settings.Settings:
    """Fixture of settings."""
    return game_settings.Settings()


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


def test_human_game_mode_no_movements(
    game_mode: game_modes.HumanGameMode,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the human game mode without any movements."""
    # GIVEN a HumanGameMode instance
    # AND a series of non-direction keys are pressed
    events = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE),
        pygame.event.Event(pygame.KEYUP, key=pygame.K_SPACE),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a),
    ]
    events_generator = ([event] for event in events)

    def get_new_event() -> list[pygame.event.Event]:
        return next(events_generator)

    monkeypatch.setattr("pygame.event.get", get_new_event)
    # WHEN the game_loop is started
    direction_initial = game_mode.snake.direction
    game_mode.loop()
    # THEN the snake direction should be equal to the initial direction
    assert game_mode.snake.direction == direction_initial


def test_human_game_mode_move_up(
    game_mode: game_modes.HumanGameMode,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the human game mode get_direction."""

    # GIVEN a HumanGameMode instance
    # WHEN an up direction is pressed
    def get_new_event() -> list[pygame.event.Event]:
        return [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)]

    monkeypatch.setattr("pygame.event.get", get_new_event)
    game_mode.loop()
    # THEN the direction of the snake should also be UP
    assert game_mode.snake.direction == enums.Direction.UP


def test_human_game_mode_eats_apple(
    game_mode: game_modes.HumanGameMode,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test if the score grows if the snake eats an apple."""
    # GIVEN a game_mode with an apple on a predefined position
    # AND a sequence of direction events
    new_events = [
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT),
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT),
    ]
    events_generator = ([event] for event in new_events)

    def get_new_event() -> list[pygame.event.Event]:
        return next(events_generator)

    monkeypatch.setattr("pygame.event.get", get_new_event)
    # WHEN the game loop is run
    try:
        while True:
            game_mode.loop()
    except StopIteration:
        pass
    # THEN the score of the game should be equal to 1.
    assert game_mode.score == 1
