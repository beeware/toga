from rubicon.objc import *

from toga.interface.widgets.container import Container as ContainerInterface

from ..libs import *
from .base import Widget


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
        super(Container, self).__init__(style=style)
        self._children = []
        self.startup()

        if children:
            for child in children:
                self.add(child)


    def startup(self):
        self._impl = TogaContainer.alloc().init()

        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.setAutoresizesSubviews_(False)

        # self._impl.setWantsLayer_(True)
        # self._impl.setBackgroundColor_(NSColor.blueColor())

    def _add_child(self, child):
        child.app = self.app
        self._impl.addSubview_(child._impl)

    def _hint_size(self, width, height, min_width=None, min_height=None):
        if width is not None:
            self.width = width
        else:
            del(self.width)

        if min_width is not None:
            self.min_width = min_width
        else:
            del(self.min_width)

        if height is not None:
            self.height = height
        else:
            del(self.height)

        if min_height is not None:
            self.min_height = min_height
        else:
            del(self.min_height)
