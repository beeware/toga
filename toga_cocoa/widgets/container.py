from __future__ import print_function, absolute_import, division, unicode_literals

from rubicon.objc import *

from ..libs import *
from .base import Widget


class ContainerImpl(NSView):
    @objc_method('B')
    def isFlipped(self):
        # Default Cocoa coordinate frame is around the wrong way.
        return True


class Container(Widget):

    def __init__(self):
        super(Container, self).__init__()
        self.children = []

        self.startup()

    def startup(self):
        self._impl = ContainerImpl.alloc().init()
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

    def add(self, widget):
        self.children.append(widget)
        self._css.children.append(widget._css)
        widget.app = self.app
        self._impl.addSubview_(widget._impl)

    def _set_app(self, app):
        for child in self.children:
            child.app = app

    def _set_window(self, window):
        for child in self.children:
            child.window = window

    def _update_layout(self):
        super(Container, self)._update_layout()
        for child in self.children:
            child._update_layout()
