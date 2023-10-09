from enum import Enum, auto

from travertino.constants import *  # noqa: F401, F403  pragma: no cover


class Direction(Enum):
    "The direction a given property should act"
    HORIZONTAL = 0
    VERTICAL = 1


class Baseline(Enum):
    "The meaning of a Y coordinate when drawing text."
    ALPHABETIC = auto()  #: Alphabetic baseline of the first line
    TOP = auto()  #: Top of text
    MIDDLE = auto()  #: Middle of text
    BOTTOM = auto()  #: Bottom of text


class FillRule(Enum):
    "The rule to use when filling paths."
    EVENODD = 0
    NONZERO = 1
