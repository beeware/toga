from rubicon.objc import *

# from toga.interface import Box as BoxInterface

from ..libs import *
from .base import Widget


class Box(Widget):
    def __init__(self, creator):
        self._creator = creator
        self._create()
        self._native = None

    def _create(self):
        self._constraints = None
