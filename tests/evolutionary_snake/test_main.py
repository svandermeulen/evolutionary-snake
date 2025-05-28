"""Test module to test the main module."""

import pytest

from evolutionary_snake import main
from evolutionary_snake.enums import GameMode


def test_main(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the main happy flow."""
    monkeypatch.setattr(
        "evolutionary_snake.game_modes.human_game_mode.HumanGameMode.game_continues",
        lambda _: False,
    )
    main.main(game_mode=GameMode.HUMAN_PLAYER)


def test_main_non_existing_mode() -> None:
    """Test the main when a unknown game mode is provided."""
    with pytest.raises(KeyError, match="Unknown game mode NonExistingGameMode"):
        main.main(game_mode="NonExistingGameMode")  # type: ignore[arg-type]
