from toga.interface import ScrollContainer as ScrollContainerInterface

from .base import WidgetMixin
from ..container import Container
from ..libs import *


class ScrollContainer(ScrollContainerInterface, WidgetMixin):
    _CONTAINER_CLASS = Container

    def __init__(self, id=None, style=None, horizontal=True, vertical=True, content=None):
        super().__init__(id=None, style=style, horizontal=horizontal, vertical=vertical, content=content)
        self._create()

    def create(self):
        self._impl = NSScrollView.alloc().init()
        self._impl.setAutohidesScrollers_(True)
        self._impl.setBorderType_(NSNoBorder)
        self._impl.setBackgroundColor_(NSColor.windowBackgroundColor())
        # self._impl.setBackgroundColor_(NSColor.blueColor())
        self._impl.setAutoresizesSubviews_(True)

        self._inner_container = None

        # Add the layout constraints
        self._add_constraints()

    def _set_content(self, container, widget):
        self._impl.setDocumentView_(container._impl)

    def _update_child_layout(self):
        if self._content is not None:
            self._inner_container._update_layout()

    def _set_vertical(self, value):
        self._impl.setHasVerticalScroller_(value)

    def _set_horizontal(self, value):
        self._impl.setHasHorizontalScroller_(value)
