from __future__ import print_function, absolute_import, division

from ..libs import get_NSString, cfstring_to_string, NSTextView, NSScrollView, NSBezelBorder
from .base import Widget


class MultilineTextInput(Widget):

    def __init__(self, initial=None):
        super(MultilineTextInput, self).__init__()
        self.initial = initial

        self._text = None

    def _startup(self):
        # Create a multiline view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(True)
        self._impl.setHasHorizontalScroller_(True)
        self._impl.setAutohidesScrollers_(False)
        self._impl.setBorderType_(NSBezelBorder)
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)

        self._text = NSTextView.new()
        if self.initial:
            self._text.setStringValue_(get_NSString(self.initial))

        self._text.setEditable_(True)
        # self._text.setBezeled_(True)
        # self._text.setBezelStyle_(NSTextFieldSquareBezel)
        self._text.setTranslatesAutoresizingMaskIntoConstraints_(False)

    def value(self):
        return cfstring_to_string(self._text.stringValue)
