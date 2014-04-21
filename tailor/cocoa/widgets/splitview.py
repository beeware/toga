from tailor.cocoa.libs import *
from tailor.cocoa.widgets.base import Widget


class SplitView(Widget):
    HORIZONTAL = False
    VERTICAL = True
    def __init__(self, direction=VERTICAL):
        super(SplitView, self).__init__()
        self.direction = direction
        self._impl = NSSplitView.alloc().init()
        self._impl.setVertical_(direction)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content
        for widget in self._content:
            self._impl.addSubview_(widget._impl)
