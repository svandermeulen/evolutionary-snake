"""Helper functions to aid the unittests."""

from collections.abc import Callable

import pygame

from evolutionary_snake import enums


def get_event_generator(
    events: list[pygame.event.Event],
) -> Callable[[], list[pygame.event.Event]]:
    """Helper function to return an event generator."""
    events_generator = ([event] for event in events)
    return lambda: next(events_generator)


def get_pressed_generator(events: list[int]) -> Callable[[], tuple[bool, ...]]:
    """Helper function to return key pressed generator."""
    scan_code_wrappers = []
    for event in events:
        scan_code_wrapper = [False] * 1000
        scan_code_wrapper[event] = True
        scan_code_wrappers.append(tuple(scan_code_wrapper))
    events_generator = (wrapper for wrapper in scan_code_wrappers)
    return lambda: next(events_generator)


def get_direction_generator(
    directions: list[enums.Direction],
) -> Callable[[], enums.Direction]:
    """Helper function to return direction generator."""
    directions_generator = (direction for direction in directions)
    return lambda: next(directions_generator)
