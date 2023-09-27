from enum import Enum, auto

from travertino.constants import *  # noqa: F401, F403  pragma: no cover


class Direction(Enum):
    "The direction a given property should act"
    HORIZONTAL = 0
    VERTICAL = 1


class Baseline(Enum):
    "The meaning of a Y coordinate when drawing text."
    ALPHABETIC = auto()  #: Alphabetic baseline
    TOP = auto()  #: Top of line
    MIDDLE = auto()  #: Middle of line
    BOTTOM = auto()  #: Bottom of line


class FillRule(Enum):
    "The rule to use when filling paths."
    EVENODD = 0
    NONZERO = 1
