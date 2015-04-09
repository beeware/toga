from __future__ import print_function, absolute_import, division, unicode_literals

from ..libs import *
from .base import Widget


class ScrollContainer(Widget):
    def __init__(self, horizontal=True, vertical=True, **style):
        super(ScrollContainer, self).__init__(**style)
        self.horizontal = horizontal
        self.vertical = vertical

        self._content = None

        self.startup()

    def startup(self):
        print("STARTUP SCROLL CONTAINER", self.layout)
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(self.vertical)
        self._impl.setHasHorizontalScroller_(self.horizontal)
        self._impl.setAutohidesScrollers_(True)
        self._impl.setBorderType_(NSNoBorder)
        # Disable all autolayout functionality
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

    def _update_child_layout(self, **style):
        """Force a layout update on the children of the scroll container.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        # print ('    content:', (self.content._impl.frame.size.width, self.content._impl.frame.size.height), (self.content._impl.frame.origin.x, self.content._impl.frame.origin.y))

        # Pass the update request through to the content. Along the way, any
        # hard width/height constraints get turned into min width/height
        # constraints in the axes where scrolling is allowed.
        child_style = {}
        for key, value in style.items():
            if key == 'width':
                if self.horizontal:
                    child_style['min_width'] = value
                else:
                    child_style[key] = value
            elif key == 'height':
                if self.vertical:
                    child_style['min_height'] = value
                else:
                    child_style[key] = value
            else:
                child_style[key] = value

        self._content._update_layout(**child_style)
