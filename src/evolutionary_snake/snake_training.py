"""Main entry point to run evolutionary snake."""

import os
import typing

import neat

from evolutionary_snake import game_modes, settings
from evolutionary_snake.settings import TrainingSettings
from evolutionary_snake.utils import enums

GenomesType: typing.TypeAlias = list[tuple[int, neat.DefaultGenome]]  # noqa: UP040


def _run_snake(
    genome: neat.DefaultGenome,
    genome_id: int,
    neat_config: neat.Config,
    x: int = 30,
    y: int = 30,
) -> neat.DefaultGenome:
    """Run a snake game with a neural network."""
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{x},{y}"

    genome.fitness = 1000
    neural_net = neat.nn.FeedForwardNetwork.create(genome, neat_config)
    game_settings = settings.AiGameSettings(
        name=f"snake_{str(genome_id).zfill(2)}",
        neural_net=neural_net,
        run_in_background=True,
    )

    snake_game = game_modes.AiGameMode(game_settings=game_settings)
    snake_game.run()
    genome.fitness = snake_game.loss_tracker.loss
    return genome


def _eval_genomes_sequential(genomes: GenomesType, neat_config: neat.Config) -> None:
    """Evaluate genomes sequentially."""
    genome_dict = {}
    for genome_id, genome in genomes:
        genome_evaluated = _run_snake(
            genome=genome, genome_id=genome_id, neat_config=neat_config
        )
        genome_dict[genome_id] = genome_evaluated


TrainingFunctionsDict: dict[
    enums.TrainingMode, typing.Callable[[GenomesType, neat.Config], None]
] = {enums.TrainingMode.SEQUENTIAL: _eval_genomes_sequential}


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
    population.run(training_mode_func, n=training_settings.generations)
    training_settings.neat_config.save(
        training_settings.checkpoint_prefix.parent / "neat_config"
    )
