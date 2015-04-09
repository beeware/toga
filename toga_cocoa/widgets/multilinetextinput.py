from __future__ import print_function, absolute_import, division, unicode_literals

<<<<<<< HEAD
from ..libs import get_NSString, NSTextView, NSScrollView, NSBezelBorder, text, cfstring_to_string
=======
from ..libs import NSTextView, NSScrollView, NSBezelBorder
>>>>>>> Factored Objective C interface into Rubicon library.
from .base import Widget


class MultilineTextInput(Widget):

    def __init__(self, initial=None, **style):
        super(MultilineTextInput, self).__init__(**style)
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


        self._text = NSTextView.alloc().init()

        # Use autolayout for the inner widget.
        self._text.setTranslatesAutoresizingMaskIntoConstraints_(True)

        if self.initial:
            self._text.insertText_(self.initial)

        self._text.setEditable_(True)
        self._text.setVerticallyResizable_(True)
        self._text.setHorizontallyResizable_(True)

        self._impl.setDocumentView_(self._text)

    @property
    def value(self):
        return cfstring_to_string(self._text.string)

    @value.setter
    def value(self, value):
        if value:
            self._text.insertText_(get_NSString(text(value)))
