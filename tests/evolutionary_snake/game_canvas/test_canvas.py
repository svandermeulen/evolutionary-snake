"""Test module to test the canvas module."""

import pygame

from evolutionary_snake import game_canvas, game_settings


def test_canvas_init(settings: game_settings.Settings) -> None:
    """Test that the canvas object is initialized correctly."""
    # GIVEN common settings
    # AND that pygame is not initialized
    assert not pygame.get_init()
    # WHEN a canvas object is instantiated
    canvas = game_canvas.Canvas(
        settings=settings,
    )
    # THEN pygame should have been initialized
    assert pygame.get_init()
    # AND the canvas attribute should not be equal to None
    assert canvas.canvas is not None
