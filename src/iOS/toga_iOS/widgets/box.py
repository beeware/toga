from rubicon.objc import *

from toga.interface import Box as BoxInterface

from .base import WidgetMixin
from ..libs import *


class Box(BoxInterface, WidgetMixin):
    def __init__(self, id=None, style=None, children=None):
        super().__init__(id=id, style=style, children=children)
        self._create()

    def create(self):
        self._constraints = None