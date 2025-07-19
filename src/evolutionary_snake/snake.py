"""Main entry point to run snake."""

import operator
import pathlib
import typing

import neat
from neat import nn

from evolutionary_snake import game_modes
from evolutionary_snake.game_modes import base_game_mode
from evolutionary_snake.settings import game_settings
from evolutionary_snake.utils import enums, utility_functions


class GameModeFactory:  # pylint: disable=too-few-public-methods
    """Factory to compose a game mode with settings."""

    def __init__(
        self,
        game_mode: type[base_game_mode.BaseGameMode],
        settings: type[game_settings.GameSettings],
    ) -> None:
        """Initialize the game mode factory."""
        self.game_mode = game_mode
        self.settings = settings

    def __call__(self, **kwargs: dict[str, typing.Any]) -> base_game_mode.BaseGameMode:
        """Compose the game mode with its settings."""
        return self.game_mode(self.settings(**kwargs))


GamaModeDict: dict[enums.GameMode, GameModeFactory] = {
    enums.GameMode.HUMAN_PLAYER: GameModeFactory(
        settings=game_settings.GameSettings, game_mode=game_modes.HumanGameMode
    ),
    enums.GameMode.AI_PLAYER: GameModeFactory(
        settings=game_settings.AiGameSettings, game_mode=game_modes.AiGameMode
    ),
}


def _get_neural_net_from_checkpoint(
    path_checkpoint: pathlib.Path,
) -> nn.FeedForwardNetwork:
    """Create a neural network from a checkpoint."""
    checkpoint = neat.Checkpointer.restore_checkpoint(path_checkpoint).population
    path_neat_config = pathlib.Path(path_checkpoint).parent / "neat_config"
    neat_config = utility_functions.get_neat_config(path_neat_config)
    d = {k: v.fitness for k, v in checkpoint.items() if v.fitness is not None}
    best_genome_key = max(d.items(), key=operator.itemgetter(1))[0]
    genome = checkpoint[best_genome_key]
    return nn.FeedForwardNetwork.create(genome, neat_config)


def run_snake(
    game_mode: enums.GameMode, path_checkpoint: pathlib.Path | None = None
) -> None:
    """Main entry point to run snake."""
    game_mode_factory = GamaModeDict.get(game_mode)
    if game_mode_factory is None:
        message = f"Unknown game mode {game_mode}"
        raise KeyError(message)

    kwargs = {}
    if path_checkpoint:
        kwargs["neural_net"] = _get_neural_net_from_checkpoint(path_checkpoint)
    game = game_mode_factory(**kwargs)
    return game.run()
