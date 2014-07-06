from __future__ import print_function, absolute_import, division

from ..libs import *
from .base import Widget


class SplitContainer(Widget):
    HORIZONTAL = False
    VERTICAL = True
    def __init__(self, direction=VERTICAL):
        super(SplitContainer, self).__init__()
        self._impl = None
        self._content = None

        self.direction = direction

    def _startup(self):
        self._impl = NSSplitView.alloc().init()
        self._impl.setVertical_(self.direction)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        if self.content:
            self._set_content()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content
        if self._impl:
            self._set_content()

    def _set_content(self):
        for widget in self._content:
            widget.app = self.app
            self._impl.addSubview_(widget._impl)
