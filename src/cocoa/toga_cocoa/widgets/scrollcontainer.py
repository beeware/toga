from .base import Widget
from ..container import Container
from ..libs import *


class ScrollContainer(Widget):
    def create(self):
        self.native = NSScrollView.alloc().init()
        self.native.setAutohidesScrollers_(True)
        self.native.setBorderType_(NSNoBorder)
        self.native.setBackgroundColor_(NSColor.windowBackgroundColor)
        # self._impl.setBackgroundColor_(NSColor.blueColor)
        self.native.setAutoresizesSubviews_(True)

        # Add the layout constraints
        self.add_constraints()

    def set_content(self, container, widget):
        self.native.setDocumentView_(container._impl.native)

    def _update_child_layout(self):
        if self.interface.content is not None:
            self.interface._inner_container._update_layout()

    def set_vertical(self, value):
        self.native.setHasVerticalScroller_(value)

    def set_horizontal(self, value):
        self.native.setHasHorizontalScroller_(value)

