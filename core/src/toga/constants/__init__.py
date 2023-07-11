from enum import Enum

from travertino.constants import *  # noqa: F401, F403


class FillRule(Enum):
    "The fill rule to use when filling curves."
    EVENODD = 0
    NONZERO = 1
