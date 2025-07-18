"""Test module with tests for the loss tracking module."""

from evolutionary_snake import enums
from evolutionary_snake.machine_learning import loss_tracking


def test_loss_tracker() -> None:
    """Test the instantiation of LossTracker."""
    # GIVEN a loss tracker instance
    # WHEN the loss tracker is instantiated
    loss_tracker = loss_tracking.LossTracker()
    # THEN the steps_total should be equal to zero
    assert loss_tracker.steps_total == 0
    # AND the loss should be equal to zero
    assert loss_tracker.loss == 0
    # AND the direction counts should be equal to zero
    assert loss_tracker.direction_counts == {
        enums.Direction.LEFT: 0,
        enums.Direction.RIGHT: 0,
        enums.Direction.UP: 0,
        enums.Direction.DOWN: 0,
    }
