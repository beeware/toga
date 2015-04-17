from __future__ import print_function, absolute_import, division, unicode_literals

<<<<<<< HEAD
<<<<<<< HEAD
from ..libs import get_NSString, NSTextView, NSScrollView, NSBezelBorder, text, cfstring_to_string
=======
from ..libs import NSTextView, NSScrollView, NSBezelBorder
>>>>>>> Factored Objective C interface into Rubicon library.
=======
from ..libs import NSTextView, NSScrollView, NSBezelBorder, NSViewWidthSizable, NSViewHeightSizable
>>>>>>> Port all widgets to use CSS layout.
from .base import Widget


class MultilineTextInput(Widget):

    def __init__(self, initial=None, **style):
        super(MultilineTextInput, self).__init__(**style)
        self.startup()

        self.value = initial

    def startup(self):
        # Create a multiline view, and put it in a scroll view.
        # The scroll view is the _impl, because it's the outer container.
        self._impl = NSScrollView.alloc().init()
        self._impl.setHasVerticalScroller_(True)
        self._impl.setHasHorizontalScroller_(False)
        self._impl.setAutohidesScrollers_(False)
        self._impl.setBorderType_(NSBezelBorder)
        self._impl.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)

        # Disable all autolayout functionality on the outer widget
        # self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        # self._impl.setAutoresizesSubviews_(False)
        # self._impl.setAutoresizesSubviews_(True)

        # Use a dummy size initially.
        self._text = NSTextView.alloc().init()

        # Disable all autolayout functionality on the inner widget
        # self._text.setTranslatesAutoresizingMaskIntoConstraints_(False)
        # self._text.setAutoresizesSubviews_(False)

        self._text.setEditable_(True)
        self._text.setVerticallyResizable_(True)
        self._text.setHorizontallyResizable_(False)
        self._text.setAutoresizingMask_(NSViewWidthSizable)

        self._impl.setDocumentView_(self._text)

    @property
    def value(self):
        return cfstring_to_string(self._text.string)

    @value.setter
    def value(self, value):
        if value:
<<<<<<< HEAD
            self._text.insertText_(get_NSString(text(value)))
=======
            self._text.insertText_(value)

    def _set_frame(self, frame):
        self._impl.setFrame_(frame)
        self._impl.contentView.setFrame_(frame)
        self._impl.setNeedsDisplay_(True)
>>>>>>> Port all widgets to use CSS layout.
