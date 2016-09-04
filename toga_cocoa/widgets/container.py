from rubicon.objc import *

from toga.interface.widgets.container import Container as ContainerInterface

from ..libs import *
from .base import Widget, Constraints


class TogaContainer(NSView):
    @objc_method
    def isFlipped(self) -> bool:
        # Default Cocoa coordinate frame is around the wrong way.
        return True

    @objc_method
    def display(self) -> None:
        self.layer.setNeedsDisplay_(True)
        self.layer.displayIfNeeded()


class Container(ContainerInterface, Widget):
    def __init__(self, children=None, style=None):
        super().__init__(style=style)
        self._children = []
        self.startup()

        if children:
            for child in children:
                self.add(child)


    def startup(self):
        self._impl = TogaContainer.alloc().init()
        self._impl._interface = self

        # self._impl.setWantsLayer_(True)
        # self._impl.setBackgroundColor_(NSColor.blueColor())

        self._add_constraints()
