"""Main entry point to run evolutionary snake."""

import functools
import logging
import multiprocessing
import typing

import neat

from evolutionary_snake import game_modes, settings
from evolutionary_snake.settings import TrainingSettings
from evolutionary_snake.utils import enums

GenomesType: typing.TypeAlias = list[tuple[int, neat.DefaultGenome]]  # noqa: UP040
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def _run_snake(
    game_settings: settings.AiGameSettings,
    genome: neat.DefaultGenome,
    genome_id: int,
    genome_dict: dict[int, neat.DefaultGenome],
) -> neat.DefaultGenome:
    """Run a snake game with a neural network."""
    snake_game = game_modes.AiGameMode(game_settings=game_settings)
    snake_game.run()
    genome.fitness = snake_game.loss_tracker.loss
    genome_dict[genome_id] = genome
    return genome


def _eval_genomes_sequential(
    genomes: GenomesType,
    neat_config: neat.Config,
    step_limit: int,
) -> None:
    """Evaluate genomes sequentially."""
    genome_dict: dict[int, neat.DefaultGenome] = {}
    for genome_id, genome in genomes:
        neural_net = neat.nn.FeedForwardNetwork.create(genome, neat_config)
        game_settings = settings.AiGameSettings(
            name=f"snake_{str(genome_id).zfill(2)}",
            neural_net=neural_net,
            run_in_background=False,
            step_limit=step_limit,
        )
        genome_evaluated = _run_snake(
            game_settings=game_settings,
            genome=genome,
            genome_id=genome_id,
            genome_dict=genome_dict,
        )
        genome_dict[genome_id] = genome_evaluated


def _eval_genomes_parallel(
    genomes: list[tuple[int, neat.DefaultGenome]],
    neat_config: neat.config.Config,
    step_limit: int,
) -> None:
    """Evaluate genomes in parallel."""
    jobs: list[multiprocessing.Process] = []
    job_names: dict[str, int] = {}

    genome_dict = multiprocessing.Manager().dict()
    for i, (genome_id, genome) in enumerate(genomes):
        neural_net = neat.nn.FeedForwardNetwork.create(genome, neat_config)
        game_settings = settings.AiGameSettings(
            name=f"snake_{str(genome_id).zfill(2)}",
            neural_net=neural_net,
            run_in_background=False,
            step_limit=step_limit,
        )
        game_settings.display_y = 100 + int(
            1.1 * game_settings.display_height * (i // game_settings.screens_per_row)
        )
        game_settings.display_x = int(
            1.1 * (game_settings.display_width * (i % game_settings.screens_per_row))
        )

        p = multiprocessing.Process(
            target=_run_snake,
            kwargs={
                "game_settings": game_settings,
                "genome": genome,
                "genome_id": genome_id,
                "genome_dict": genome_dict,
            },
        )
        job_names[p.name] = genome_id
        jobs.append(p)
        p.start()

    while True:
        snakes_alive = [p for p in jobs if p.is_alive()]
        if len(snakes_alive) == 0:
            msg = (
                f"All snakes have taken {step_limit} steps without taking an apple "
                f"or collided to itself or the wall"
            )

            logger.info(msg)
            break

    for p in jobs:
        p.join()

    for genome_id, genome in genomes:
        genome.fitness = genome_dict[genome_id].fitness


class EvaluationFunction(typing.Protocol):  # pylint: disable=too-few-public-methods
    """Interface for a training evaluation function."""

    def __call__(
        self,
        genomes: list[tuple[int, neat.DefaultGenome]],
        neat_config: neat.config.Config,
        step_limit: int,
    ) -> None:
        """Run the training evaluation function."""


TrainingFunctionsDict: dict[enums.TrainingMode, EvaluationFunction] = {
    enums.TrainingMode.SEQUENTIAL: _eval_genomes_sequential,
    enums.TrainingMode.PARALLEL: _eval_genomes_parallel,
}


def run_snake_training(
    training_mode: enums.TrainingMode,
    training_settings: settings.TrainingSettings | None = None,
) -> None:
    """Main entry point to run snake."""
    training_settings = training_settings or TrainingSettings()
    population = neat.Population(training_settings.neat_config)

    # Add a stdout reporter to show progress in the terminal.
    population.add_reporter(neat.StdOutReporter(show_species_detail=True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    population.add_reporter(
        neat.Checkpointer(
            generation_interval=1,
            filename_prefix=training_settings.checkpoint_prefix.as_posix(),
        )
    )

    training_mode_func = TrainingFunctionsDict[training_mode]
    population.run(
        functools.partial(training_mode_func, step_limit=training_settings.step_limit),
        n=training_settings.generations,
    )
    training_settings.neat_config.save(
        training_settings.checkpoint_prefix.parent / "neat_config"
    )


if __name__ == "__main__":  # pragma: no cover
    run_snake_training(
        training_mode=enums.TrainingMode.PARALLEL,
        training_settings=TrainingSettings(),
    )
