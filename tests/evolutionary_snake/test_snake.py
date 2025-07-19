"""Test module to test the main module."""

import pathlib

import pytest

from evolutionary_snake import snake
from evolutionary_snake.utils import enums


def test_snake(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the main happy flow."""
    monkeypatch.setattr(
        "evolutionary_snake.game_modes.human_game_mode.HumanGameMode.game_continues",
        lambda _: False,
    )
    snake.run_snake(game_mode=enums.GameMode.HUMAN_PLAYER)


def test_snake_non_existing_mode() -> None:
    """Test the main when a unknown game mode is provided."""
    with pytest.raises(KeyError, match="Unknown game mode NonExistingGameMode"):
        snake.run_snake(game_mode="NonExistingGameMode")  # type: ignore[arg-type]


def test_snake_with_checkpoint() -> None:
    """Test a AI game mode with a checkpoint."""
    snake.run_snake(
        game_mode=enums.GameMode.AI_PLAYER,
        path_checkpoint=pathlib.Path(__file__).parents[1]
        / "data"
        / "test-neat-checkpoint-0",
    )
