from rubicon.objc import *

from toga.interface import Container as ContainerInterface

from .base import WidgetMixin
from ..libs import *


class Container(ContainerInterface, WidgetMixin):
    def __init__(self, id=None, style=None, children=None):
        super().__init__(id=id, style=style, children=children)
        self.startup()

        if children:
            for child in children:
                self.add(child)

    def startup(self):
        self._impl = UIView.alloc().init()
        self._impl._interface = self

        self._impl.setBackgroundColor_(UIColor.whiteColor())

        self._add_constraints()
