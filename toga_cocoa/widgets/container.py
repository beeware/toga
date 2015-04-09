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

    def __init__(self, *children, **style):
        super(Container, self).__init__(**style)
        self._children = children

        self.startup()

    def startup(self):
        print("STARTUP CONTAINER", self.layout)
        self._impl = ContainerImpl.alloc().init()
        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        for child in self._children:
            self.add(child)
        # del(self._children)

        # self._impl.setWantsLayer_(True)
        # self._impl.setBackgroundColor_(NSColor.blueColor())

    def add(self, child):
        self.children.append(child)
        self._add_child(child)

    def _add_child(self, child):
        child.app = self.app
        self._impl.addSubview_(child._impl)

    def _set_app(self, app):
        for child in self.children:
            child.app = app

    def _set_window(self, window):
        for child in self.children:
            child.window = window

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

    def _update_child_layout(self, **style):
        """Force a layout update on children of this container.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        for child in self.children:
            # print ('   ',self,' child:', child)
            child._update_layout(
                # width=self._impl.frame().size.width,
                # height=self._impl.frame().size.height
            )
