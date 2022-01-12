"""
Created on: 13-7-2018
@author: Stef
"""
import operator
import os
import shutil

from datetime import datetime
from neat.checkpoint import Checkpointer

from src.evolution.neat_snake import run_evolution, run_genome
from src.game.game_builder import GameHumanPlayer
from src.config import Config
from src.paths import Paths


def run_checkpoint(path_checkpoint: str, path_neat_config: str, config_game: Config):
    population = Checkpointer.restore_checkpoint(path_checkpoint).population
    d = {k: v.fitness for k, v in population.items() if v.fitness is not None}
    best_genome_key = max(d.items(), key=operator.itemgetter(1))[0]
    best_genome = population[best_genome_key]
    run_genome(winner=best_genome, path_neat_config=path_neat_config, config_game=config_game)

    return True


def main():

    config = Config()
    paths = Paths()

    datetime_run = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
    path_output = os.path.join(paths.path_output, datetime_run)
    os.mkdir(path_output)

    if not os.path.isdir(paths.path_output_temp):
        os.mkdir(paths.path_output_temp)
    [os.remove(os.path.join(paths.path_output_temp, p)) for p in os.listdir(paths.path_output_temp) if
     os.path.isfile(os.path.join(paths.path_output_temp, p))]

    path_neat_config = os.path.join(paths.path_input, "neat_config")

    if not config.human_player:
        best_genome = run_evolution(
            path_neat_config=path_neat_config,
            path_checkpoint=os.path.join(path_output, "neat-checkpoint-"),
            config_game=config
        )
        print('\nBest genome:\n{!s}'.format(best_genome))
        run_genome(winner=best_genome, path_neat_config=path_neat_config, config_game=config)
    else:
        GameHumanPlayer(config=config).execute()

    # move all created output visualizations and checkpoints
    [shutil.move(p, os.path.join(path_output, p)) for p in os.listdir(".") if
     os.path.isfile(p) and not p.endswith(".py")]

    return True


if __name__ == "__main__":

    # config = Config()
    # path_run = os.path.abspath("D:/Stack/stef/software/python/snake/output/20220110_145705")
    # path_checkpoint = os.path.join(path_run, "neat-checkpoint-21")
    # path_config = os.path.join(path_run, "neat_config")
    # run_checkpoint(path_checkpoint, path_config, config_game=config)

    main()
