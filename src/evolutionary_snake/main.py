"""Main entry point to run evolutionary-snake."""

from evolutionary_snake import enums, game_modes, game_settings
from evolutionary_snake.game_modes import base_game_mode


class GameModeFactory:  # pylint: disable=too-few-public-methods
    """Factory to compose a game mode with settings."""

    def __init__(
        self,
        game_mode: type[base_game_mode.BaseGameMode],
        settings: type[game_settings.Settings],
    ) -> None:
        """Initialize the game mode factory."""
        self.game_mode = game_mode
        self.settings = settings

    def __call__(self) -> base_game_mode.BaseGameMode:
        """Compose the game mode with its settings."""
        return self.game_mode(self.settings())


GamaModeDict: dict[enums.GameMode, GameModeFactory] = {
    enums.GameMode.HUMAN_PLAYER: GameModeFactory(
        settings=game_settings.Settings, game_mode=game_modes.HumanGameMode
    ),
    enums.GameMode.AI_PLAYER: GameModeFactory(
        settings=game_settings.AiGameSettings, game_mode=game_modes.AiGameMode
    ),
}


def main(game_mode: enums.GameMode) -> None:
    """Main entry point to run evolutionary-snake."""
    game_mode_factory = GamaModeDict.get(game_mode)
    if game_mode_factory is None:
        message = f"Unknown game mode {game_mode}"
        raise KeyError(message)
    game = game_mode_factory()
    return game.run()
