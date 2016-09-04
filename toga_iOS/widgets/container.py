from rubicon.objc import *

from toga.interface.widgets.container import Container as ContainerInterface

from ..libs import *
from .base import Widget, Constraints


class Container(ContainerInterface, Widget):
    def __init__(self, children=None, style=None):
        super().__init__(style=style)
        self._children = []
        self.startup()

        if children:
            for child in children:
                self.add(child)

    def startup(self):
        self._impl = UIView.alloc().init()
        self._impl.interface = self

        # self._impl.setWantsLayer_(True)
        self._impl.setBackgroundColor_(UIColor.whiteColor())

        self._add_constraints()
