from __future__ import print_function, absolute_import, division

from ..libs import get_NSString, NSTextView, NSScrollView, NSBezelBorder
from .base import Widget


class MultilineTextInput(Widget):

    def __init__(self, initial=None):
        super(MultilineTextInput, self).__init__()
        self.initial = initial

        self._text = None

        self.startup()

    def startup(self):
        # Create a multiline view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(True)
        self._impl.setHasHorizontalScroller_(False)
        self._impl.setAutohidesScrollers_(False)
        self._impl.setBorderType_(NSBezelBorder)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._text = NSTextView.alloc().init()

        if self.initial:
            self._text.insertText_(get_NSString(self.initial))

        self._text.setEditable_(True)
        self._text.setVerticallyResizable_(True)
        self._text.setHorizontallyResizable_(True)

        self._impl.setDocumentView_(self._text)
