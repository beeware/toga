from rubicon.objc import *

# from toga.interface import Box as BoxInterface

from ..libs import *
from .base import Widget


class Box(Widget):
    def __init__(self, interface):
        self._interface = interface
        self._create()
        self._native = None

    def _create(self):
        self._constraints = None
