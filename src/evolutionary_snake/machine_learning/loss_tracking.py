"""Loss tracking module."""

import pydantic

from evolutionary_snake import enums


class LossTracker(pydantic.BaseModel):
    """Loss Tracker to keep track of for computing the loss."""

    steps_total: int = 0
    direction_counts: dict[enums.Direction, int] = {
        enums.Direction.LEFT: 0,
        enums.Direction.RIGHT: 0,
        enums.Direction.UP: 0,
        enums.Direction.DOWN: 0,
    }
    loss: float = 0
