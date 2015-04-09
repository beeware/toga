from __future__ import print_function, absolute_import, division, unicode_literals

from ..libs import *
from .base import Widget


class SplitViewDelegate(NSObject):
    @objc_method('v@')
    def splitViewDidResizeSubviews_(self, notification):
        # If the split has moved, a resize of all the content panels is required.
        self.__dict__['interface']._update_layout(
            width=self.__dict__['interface']._impl.frame.size.width,
            height=self.__dict__['interface']._impl.frame.size.height
        )

class SplitContainer(Widget):
    HORIZONTAL = False
    VERTICAL = True
    def __init__(self, direction=VERTICAL, **style):
        super(SplitContainer, self).__init__(**style)
        self._impl = None
        self._content = None
        self._right_content = None

        self.direction = direction

        self.startup()

    def startup(self):
        print("STARTUP SPLIT CONTAINER", self.layout)
        self._impl = NSSplitView.alloc().init()
        self._impl.setVertical_(self.direction)
        # Disable all autolayout functionality
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._delegate = SplitViewDelegate.alloc().init()
        self._delegate.__dict__['interface'] = self

        self._impl.setDelegate_(self._delegate)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        if len(content) < 2:
            raise ValueError('SplitContainer content must have at least 2 elements')

        self._content = content

        for cont in self._content:
            cont.window = self.window
            cont.app = self.app
            self._impl.addSubview_(cont._impl)


    def _set_app(self, app):
        if self._content:
            for content in self._content:
                content.app = self.app

    def _set_window(self, window):
        if self._content:
            for content in self._content:
                content.window = self.window

    def _update_child_layout(self, **style):
        """Force a layout update on the widget.

        The update request can be accompanied by additional style information
        (probably min_width, min_height, width or height) to control the
        layout.
        """
        for content in self._content:
            # print ('    sub frame:', (content._impl.frame.size.width, content._impl.frame.size.height), (content._impl.frame.origin.x, content._impl.frame.origin.y))
            frame = content._impl.frame
            content._update_layout(
                left=frame.origin.x,
                top=frame.origin.y,
                width=frame.size.width,
                height=frame.size.height
            )
