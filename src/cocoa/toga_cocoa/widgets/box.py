from rubicon.objc import *

from toga.interface import Box as BoxInterface

from ..libs import *
from .base import WidgetMixin


class Box(BoxInterface, WidgetMixin):
    def __init__(self, id=id, style=None, children=None):
        super().__init__(id=id, style=style, children=children)
        self._create()

    def create(self):
        # # self._impl.setWantsLayer_(True)
        # # self._impl.setBackgroundColor_(NSColor.blueColor())

        self._constraints = None
