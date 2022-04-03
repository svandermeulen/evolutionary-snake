"""
Created on: 25-6-2018
@author: Stef
"""

import copy

import graphviz
import neat
import numpy as np
from neat import StatisticsReporter, DefaultGenome
from plotly.graph_objs import Scatter, Figure
from plotly.subplots import make_subplots


def plot_stats(fig: Figure, statistics: StatisticsReporter, ylog: bool = False) -> Figure:
    """ Plots the population's average and best fitness. """

    generations = list(range(len(statistics.most_fit_genomes)))
    best_fitness = [c.fitness for c in statistics.most_fit_genomes]
    avg_fitness = np.array(statistics.get_fitness_mean())
    stdev_fitness = np.array(statistics.get_fitness_stdev())

    sd_minus = avg_fitness - stdev_fitness
    sd_plus = avg_fitness + stdev_fitness

    fig.add_trace(Scatter(x=generations, y=avg_fitness, mode="lines", line=dict(color="blue"), name="average"), 1, 1)
    fig.add_trace(Scatter(x=generations, y=sd_minus, mode="lines", line=dict(color="green", dash="dot"), name="-1 sd"),
                  1, 1)
    fig.add_trace(Scatter(x=generations, y=sd_plus, mode="lines", line=dict(color="green", dash="dot"), name="+1 sd"),
                  1, 1)
    fig.add_trace(Scatter(x=generations, y=best_fitness, mode="lines", line=dict(color="red"), name="best"), 1, 1)
    fig.update_xaxes(title="Generations", row=1, col=1)
    y_scale_type = "log" if ylog else "-"
    fig.update_yaxes(title="Fitness", type=y_scale_type, row=1, col=1)
    return fig


def plot_species(fig: Figure, statistics: StatisticsReporter) -> Figure:
    """ Visualizes speciation throughout evolution. """

    species_sizes = statistics.get_species_sizes()
    generations = list(range(len(species_sizes)))
    curves = np.array(species_sizes).T

    for i, curve in enumerate(curves):
        fig.add_trace(
            Scatter(
                x=generations,
                y=curve,
                mode="none",
                name=f"species_{i}",
                stackgroup='one',
                showlegend=False
            ), 2, 1
        )

    fig.update_xaxes(title="Generations", row=2, col=1)
    fig.update_yaxes(title="Size per Species", row=2, col=1)

    return fig


def draw_net(config: neat.Config, genome: DefaultGenome, node_names: dict = None, show_disabled: bool = True,
             prune_unused: bool = False, node_colors: dict = None, fmt: str = 'svg') -> graphviz.Digraph:
    """ Receives a genome and draws a neural network with arbitrary topology. """

    node_names = node_names if node_names is not None else {}
    node_colors = node_colors if node_colors is not None else {}

    node_attrs = {
        'shape': 'circle',
        'fontsize': '9',
        'height': '0.2',
        'width': '0.2'
    }

    dot = graphviz.Digraph(format=fmt, node_attr=node_attrs)

    inputs = set()
    for k in config.genome_config.input_keys:
        inputs.add(k)
        name = node_names.get(k, str(k))
        input_attrs = {'style': 'filled', 'shape': 'box', 'fillcolor': node_colors.get(k, 'lightgray')}
        dot.node(name, _attributes=input_attrs)

    outputs = set()
    for k in config.genome_config.output_keys:
        outputs.add(k)
        name = node_names.get(k, str(k))
        node_attrs = {'style': 'filled', 'fillcolor': node_colors.get(k, 'lightblue')}

        dot.node(name, _attributes=node_attrs)

    if prune_unused:
        connections = set()
        for cg in genome.connections.values():
            if cg.enabled or show_disabled:
                connections.add((cg.in_node_id, cg.out_node_id))

        used_nodes = copy.copy(outputs)
        pending = copy.copy(outputs)
        while pending:
            new_pending = set()
            for a, b in connections:
                if b in pending and a not in used_nodes:
                    new_pending.add(a)
                    used_nodes.add(a)
            pending = new_pending
    else:
        used_nodes = set(genome.nodes.keys())

    for n in used_nodes:
        if n in inputs or n in outputs:
            continue

        attrs = {'style': 'filled', 'fillcolor': node_colors.get(n, 'white')}
        dot.node(str(n), _attributes=attrs)

    for cg in genome.connections.values():
        if cg.enabled or show_disabled:
            input, output = cg.key
            a = node_names.get(input, str(input))
            b = node_names.get(output, str(output))
            style = 'solid' if cg.enabled else 'dotted'
            color = 'green' if cg.weight > 0 else 'red'
            width = str(0.1 + abs(cg.weight / 5.0))
            dot.edge(a, b, _attributes={'style': style, 'color': color, 'penwidth': width})

    return dot


def generate_plots(config_neat: neat.Config, best_genome: DefaultGenome, node_names: dict,
                   stats: StatisticsReporter) -> (graphviz.Digraph, Figure):
    dot = draw_net(config=config_neat, genome=best_genome, node_names=node_names)

    subplot_titles = ["Population's average and best fitness", "Speciation"]
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=subplot_titles)
    fig = plot_stats(fig=fig, statistics=stats, ylog=False)
    fig = plot_species(fig=fig, statistics=stats)
    return dot, fig
