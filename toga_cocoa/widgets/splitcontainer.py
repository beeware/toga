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

        self.startup()

    def startup(self):
        self._impl = NSSplitView.alloc().init()
        self._impl.setVertical_(self.direction)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if len(content) != 2:
            raise ValueError('SplitContainer content must be a 2-tuple')
        self._content = content

        self._content[0].window = self.window
        self._content[0].app = self.app
        self._impl.addSubview_(self._content[0]._impl)

        self._content[1].window = self.window
        self._content[1].app = self.app
        self._impl.addSubview_(self._content[1]._impl)

    def _set_app(self, app):
        if self._content:
            self._content[0].app = self.app
            self._content[1].app = self.app

    def _set_window(self, window):
        if self._content:
            self._content[0].window = self.window
            self._content[1].window = self.window
