from rubicon.objc import *

from .base import Widget
from ..libs import *


class Box(Widget):
    def __init__(self, interface):
        self._interface = interface
        self._create()

    def _create(self):
        self._native = None
        self._constraints = None