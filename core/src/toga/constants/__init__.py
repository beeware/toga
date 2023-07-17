from enum import Enum

from travertino.constants import *  # noqa: F401, F403


class Direction(Enum):
    "The direction a given property should act"
    HORIZONTAL = 0
    VERTICAL = 1
