from __future__ import print_function, absolute_import, division

from ..libs import *
from .base import Widget


class ScrollView(Widget):
    def __init__(self, horizontal=True, vertical=True):
        super(ScrollView, self).__init__()
        self.horizontal = horizontal
        self.vertical = vertical

        self._impl = None
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, widget):
        self._content = widget
        self._content.window = self.window
        if self._impl:
            self._set_content()

    def _set_content(self):
        self.content.app = self.app
        self._impl.setDocumentView_(self._content._impl)

    def _startup(self):
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(self.vertical)
        self._impl.setHasHorizontalScroller_(self.horizontal)
        self._impl.setAutohidesScrollers_(True)
        self._impl.setBorderType_(NSNoBorder)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._impl.backgroundColor = NSColor.windowBackgroundColor()

        if self.content:
            self._set_content()
