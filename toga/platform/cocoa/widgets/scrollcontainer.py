from __future__ import print_function, absolute_import, division

from ..libs import *
from .base import Widget


class ScrollContainer(Widget):
    def __init__(self, horizontal=True, vertical=True):
        super(ScrollContainer, self).__init__()
        self.horizontal = horizontal
        self.vertical = vertical

        self._content = None

        self.startup()

    def startup(self):
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(self.vertical)
        self._impl.setHasHorizontalScroller_(self.horizontal)
        self._impl.setAutohidesScrollers_(True)
        self._impl.setBorderType_(NSNoBorder)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._impl.setBackgroundColor_(NSColor.windowBackgroundColor())

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self.window
        self._content.app = self.app
        self._impl.setDocumentView_(self._content._impl)

    def _set_app(self, app):
        if self._content:
            self._content.app = self.app

    def _set_window(self, window):
        if self._content:
            self._content.window = self.window
