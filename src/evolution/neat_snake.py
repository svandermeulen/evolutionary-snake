"""
Created on: 4-8-2018
@author: Stef
"""
import multiprocessing
import neat
import os

from multiprocessing import Process
from neat import DefaultGenome

from src.config import Config
from src.game.game_builder import GameNeuralNet
from src.visualisation import visualize


def play_snake(
        genome: DefaultGenome,
        snake_id: int,
        config_game: Config,
        config_neat: neat.config.Config,
        genome_dict: dict = None,
        x: int = 30,
        y: int = 30
) -> dict:

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

    genome.fitness = 1000
    net = neat.nn.FeedForwardNetwork.create(genome, config_neat)

    snake_game = GameNeuralNet(
        config=config_game,
        name="snake_{}".format(str(snake_id).zfill(2)),
        neural_net=net,
    )
    snake_game.execute()
    genome.fitness = snake_game.loss
    genome_dict[snake_id] = genome
    return genome_dict


def eval_genomes_sequential(genomes: list, config_neat: neat.config.Config) -> bool:
    config_game = Config()
    for (genome_id, genome) in genomes:
        _ = play_snake(genome=genome, snake_id=genome_id, config_game=config_game, config_neat=config_neat)

    return True


def eval_genomes_parallel(genomes: list, config_neat: neat.config.Config):
    display_y = 100
    jobs = []
    job_names = {}
    config_game = Config()

    assert hasattr(eval_genomes_parallel, "counter"), "Callable 'eval_genomes_parallel' has no attribute 'counter'"
    generation = eval_genomes_parallel.counter
    step_limit = config_game.step_limit + (generation - (generation % 5)) * 20

    genome_dict = multiprocessing.Manager().dict()
    for i, (genome_id, genome) in enumerate(genomes):
        display_x = 1.2 * (config_game.display_width * (i % config_game.screens_per_row))
        if not i == 0 and i % config_game.screens_per_row == 0:
            display_y += 1.5 * config_game.display_height

        p = Process(
            target=play_snake, kwargs={
                "genome": genome, "snake_id": genome_id, "config_game": config_game, "config_neat": config_neat,
                "x": display_x, "y": display_y, "genome_dict": genome_dict
            }
        )
        job_names[p.name] = genome_id
        jobs.append(p)
        p.start()

    while True:
        snakes_alive = [p for p in jobs if p.is_alive()]
        if len(snakes_alive) == 0:
            print(f"All snakes have taken {step_limit} steps or collided to itself or the wall")
            break

    for p in jobs:
        if p.is_alive():
            p.terminate()
        p.join()

    for (genome_id, genome) in genomes:
        genome.fitness = genome_dict[genome_id].fitness

    eval_genomes_parallel.counter += 1

    return True


def get_neat_config(path_neat_config: str) -> neat.Config:
    return neat.Config(
        genome_type=neat.DefaultGenome, reproduction_type=neat.DefaultReproduction,
        species_set_type=neat.DefaultSpeciesSet, stagnation_type=neat.DefaultStagnation, filename=path_neat_config
    )


def run_evolution(path_neat_config: str, path_checkpoint: str, config_game: Config):
    config_neat = get_neat_config(path_neat_config=path_neat_config)
    config_neat.save(os.path.join(os.path.dirname(path_checkpoint), "neat_config"))

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config_neat)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(generation_interval=1, filename_prefix=path_checkpoint))

    if config_game.run_in_parallel:
        # Run for up to n generations.
        eval_genomes_parallel.counter = 0
        best_genome = p.run(eval_genomes_parallel, n=config_game.generations)
    else:
        best_genome = p.run(eval_genomes_sequential, n=config_game.generations)

    node_names = {
        -1: 'Apple_left', -2: 'Apple_right', -3: "Apple_up", -4: "Apple_down",
        -5: "Right_clear", -6: "Left_clear", -7: "Bottom_clear", -8: "Up_clear",
        0: "RIGHT", 1: "LEFT", 2: "UP", 3: "DOWN"
    }
    visualize.draw_net(
        config=config_neat,
        genome=best_genome,
        view=True,
        node_names=node_names,
        directory=os.path.dirname(path_checkpoint)
    )
    visualize.plot_stats(stats, ylog=False, view=True,
                         filename=os.path.join(os.path.dirname(path_checkpoint), "avg_fitness.svg"))
    visualize.plot_species(stats, view=True, filename=os.path.join(os.path.dirname(path_checkpoint), "speciation.svg"))

    return best_genome


def run_genome(winner, path_neat_config: str, config_game: Config):
    neat_config = get_neat_config(path_neat_config=path_neat_config)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, neat_config)
    the_app = GameNeuralNet(
        config=config_game,
        name="best_genome",
        neural_net=winner_net
    )

    final_score = the_app.execute()

    print("The best genome scored {} points".format(final_score))

    return True
