"""Module with helper functions."""

import pathlib

import neat


def get_neat_config(path_neat_config: pathlib.Path) -> neat.Config:
    """Function to return a neat config instance."""
    return neat.Config(
        genome_type=neat.DefaultGenome,
        reproduction_type=neat.DefaultReproduction,
        species_set_type=neat.DefaultSpeciesSet,
        stagnation_type=neat.DefaultStagnation,
        filename=path_neat_config,
    )
