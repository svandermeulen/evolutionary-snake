"""
Created on: 13-7-2018
@author: Stef
"""
import neat
import operator
import os

from datetime import datetime
from neat.checkpoint import Checkpointer

from src.evolution.neat_snake import run_evolution, run_genome
from src.game.game_builder import GameHumanPlayer
from src.config import Config
from src.paths import Paths
from src.visualisation.visualize import generate_plots


MODES_ALLOWED = ["train", "human_player", "ai_player"]


def get_neat_config(path_neat_config: str) -> neat.Config:
    return neat.Config(
        genome_type=neat.DefaultGenome, reproduction_type=neat.DefaultReproduction,
        species_set_type=neat.DefaultSpeciesSet, stagnation_type=neat.DefaultStagnation, filename=path_neat_config
    )


def run_checkpoint(checkpoint: dict, config_neat: neat.Config, config_game: Config):
    d = {k: v.fitness for k, v in checkpoint.items() if v.fitness is not None}
    best_genome_key = max(d.items(), key=operator.itemgetter(1))[0]
    best_genome = checkpoint[best_genome_key]
    run_genome(winner=best_genome, config_neat=config_neat, config_game=config_game)

    return True


def main(mode: str, datetime_run: str = None, checkpoint: int = None) -> bool:
    datetime_run = datetime_run if datetime_run is not None and mode == "ai_player" else \
        datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
    config_game = Config(mode=mode)
    paths = Paths(datetime_run=datetime_run)

    if mode == "human_player":
        GameHumanPlayer(config=config_game).execute()
        return True

    elif mode == "train":
        config_neat = get_neat_config(path_neat_config=paths.path_neat_config)
        best_genome, stats = run_evolution(
            config_game=config_game,
            config_neat=config_neat,
            checkpoint_prefix=paths.path_checkpoint_prefix
        )

        config_neat.save(os.path.join(os.path.dirname(paths.path_checkpoint_prefix), "neat_config"))
        generate_plots(
            config_neat=config_neat,
            checkpoint_prefix=paths.path_checkpoint_prefix,
            best_genome=best_genome,
            node_names=config_game.node_names,
            stats=stats
        )
        print('\nBest genome:\n{!s}'.format(best_genome))

        return True

    elif mode == "ai_player":
        checkpoint = Checkpointer.restore_checkpoint(paths.path_checkpoint_prefix + str(checkpoint)).population
        config_neat = get_neat_config(path_neat_config=os.path.join(paths.path_output, "neat_config"))
        return run_checkpoint(checkpoint=checkpoint, config_neat=config_neat, config_game=config_game)

    else:
        print(f"Invalid mode {mode} given")

    return True


if __name__ == "__main__":
    game_mode = "train"
    assert game_mode in MODES_ALLOWED, f"Given game mode is not valid: {game_mode}"

    print("=" * 20, f" running mode: {game_mode} ", "=" * 20)
    main(mode=game_mode, datetime_run="20220202_113524", checkpoint=2)
