"""
Created on: 4-8-2018
@author: Stef
"""
import json
import neat
import os

from multiprocessing import Process
from neat import DefaultGenome

from src.game.game_builder import Game
from src.config import DISPLAY_HEIGHT, DISPLAY_WIDTH, STEP_LIMIT, GENERATIONS, PATH_OUTPUT_TEMP, SCREENS_PER_ROW, \
    RUN_IN_PARALLEL
from src.visualisation import visualize


def play_snake(genome: DefaultGenome, name_snake: str, config, x: int = 30, y: int = 30, step_limit: int = STEP_LIMIT):

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

    genome.fitness = 1000
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    genome.fitness = Game(
        name=name_snake,
        neural_net=net,
        path_output=PATH_OUTPUT_TEMP,
        step_limit=step_limit
    ).on_execute()
    return genome


def retrieve_snake_scores():
    results_dict = {}
    json_paths = [os.path.join(PATH_OUTPUT_TEMP, f) for f in os.listdir(PATH_OUTPUT_TEMP) if f.endswith(".json")]
    print("Number of json-files: {}".format(len(json_paths)))
    for path in json_paths:
        file_name = os.path.basename(path)
        with open(path, "rb") as f:
            try:
                result = json.loads(f.read())
            except json.decoder.JSONDecodeError as e:
                print("{}, with path: {}".format(e, path))
                name = file_name[:file_name.find(".json")]
                result = {name: 0}
        name = file_name[:file_name.find(".json")]
        results_dict[name] = result[name]
    return results_dict


def eval_genomes_sequential(genomes: list, config: neat.config.Config) -> bool:

    for i, (genome_id, genome) in enumerate(genomes):

        snake_name = "snake_{}".format(str(i).zfill(2))
        play_snake(genome=genome, name_snake=snake_name, config=config)

    results = retrieve_snake_scores()
    for i, (_, g) in enumerate(genomes):
        g.fitness = results[f"snake_{str(i).zfill(2)}"]

    return True


def eval_genomes_parallel(genomes: list, config: neat.config.Config):
    display_y = 100
    jobs = []
    job_names = {}

    assert hasattr(eval_genomes_parallel, "counter"), "Callable 'eval_genomes_parallel' has not attribute 'counter'"
    generation = eval_genomes_parallel.counter
    step_limit = STEP_LIMIT + (generation - (generation % 5)) * 20

    for i, (genome_id, genome) in enumerate(genomes):

        snake_name = "snake_{}".format(str(i).zfill(2))
        display_x = 1.2 * (DISPLAY_WIDTH * (i % SCREENS_PER_ROW))
        if not i == 0 and i % SCREENS_PER_ROW == 0:
            display_y += 1.5 * DISPLAY_HEIGHT

        p = Process(
            target=play_snake, kwargs={
                "genome": genome, "name_snake": snake_name, "config":  config, "x": display_x, "y": display_y,
                "step_limit": step_limit
            }
        )
        job_names[p.name] = snake_name
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

    results = retrieve_snake_scores()
    for i, (_, g) in enumerate(genomes):
        g.fitness = results[f"snake_{str(i).zfill(2)}"]

    eval_genomes_parallel.counter += 1

    return True


def get_neat_config(path_neat_config: str) -> neat.Config:
    return neat.Config(
        genome_type=neat.DefaultGenome, reproduction_type=neat.DefaultReproduction,
        species_set_type=neat.DefaultSpeciesSet, stagnation_type=neat.DefaultStagnation, filename=path_neat_config
    )


def run_evolution(path_neat_config: str, path_checkpoint: str):

    neat_config = get_neat_config(path_neat_config=path_neat_config)
    neat_config.save(os.path.join(os.path.dirname(path_checkpoint), "neat_config"))

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(neat_config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10, filename_prefix=path_checkpoint))

    if RUN_IN_PARALLEL:
        # Run for up to n generations.
        eval_genomes_parallel.counter = 0
        best_genome = p.run(eval_genomes_parallel, n=GENERATIONS)
    else:
        best_genome = p.run(eval_genomes_sequential, n=GENERATIONS)

    node_names = {
        -1: 'Apple_left', -2: 'Apple_right', -3: "Apple_up", -4: "Apple_down",
        -5: "Right_clear", -6: "Left_clear", -7: "Bottom_clear", -8: "Up_clear",
        0: "RIGHT", 1: "LEFT", 2: "UP", 3: "DOWN"
    }
    visualize.draw_net(
        config=neat_config,
        genome=best_genome,
        view=True,
        node_names=node_names,
        directory=os.path.dirname(path_checkpoint)
    )
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

    return best_genome


def run_genome(winner, path_neat_config: str):

    neat_config = get_neat_config(path_neat_config=path_neat_config)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, neat_config)
    the_app = Game(name="best_genome", neural_net=winner_net, path_output=PATH_OUTPUT_TEMP, show_game=True, step_limit=-1)

    final_score = the_app.on_execute()

    print("The best genome scored {} points".format(final_score))

    return True
