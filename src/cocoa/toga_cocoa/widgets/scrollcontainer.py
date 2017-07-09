from .base import Widget
from ..container import Container
from ..libs import *


class ScrollContainer(Widget):
    _CONTAINER_CLASS = Container

    def create(self):
        self.native = NSScrollView.alloc().init()
        self.native.setAutohidesScrollers_(True)
        self.native.setBorderType_(NSNoBorder)
        self.native.setBackgroundColor_(NSColor.windowBackgroundColor)
        # self._impl.setBackgroundColor_(NSColor.blueColor)
        self.native.setAutoresizesSubviews_(True)

        # Add the layout constraints
        self.add_constraints()

    def set_content(self, widget):
        if widget.native is None:
            self._inner_container = Container()
            self._inner_container.root_content = widget
        else:
            self._inner_container = widget
        self.native.setDocumentView_(self._inner_container.native)

    def _update_child_layout(self):
        if self.interface.content is not None:
            self._inner_container._update_layout()

    def set_vertical(self, value):
        self.native.setHasVerticalScroller_(value)

    def set_horizontal(self, value):
        self.native.setHasHorizontalScroller_(value)
