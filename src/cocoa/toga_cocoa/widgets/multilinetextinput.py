from toga.interface import MultilineTextInput as MultilineTextInputInterface

from ..libs import (
    NSTextView, NSScrollView,
    NSBezelBorder, NSViewWidthSizable, NSViewHeightSizable,
    NSRect, NSPoint, NSSize
)
from .base import WidgetMixin


class MultilineTextInput(MultilineTextInputInterface, WidgetMixin):
    def __init__(self, initial=None, style=None):
        super(MultilineTextInput, self).__init__(style=style)
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

        # Disable all autolayout functionality on the outer widget
        self._impl.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._impl.contentView.setTranslatesAutoresizingMaskIntoConstraints_(False)

        # self._impl.setBackgroundColor_(NSColor.blueColor)
        self._impl.setAutoresizesSubviews_(True)

        # Use a dummy size initially.
        self._text = NSTextView.alloc().init()

        # Disable all autolayout functionality on the inner widget
        self._text.setTranslatesAutoresizingMaskIntoConstraints_(False)
        self._text.editable = True
        self._text.verticallyResizable = True
        self._text.horizontallyResizable = False

        self._impl.setDocumentView_(self._text)

        # Add the layout constraints
        self._add_constraints()

    @property
    def value(self):
        return self._text.string

    @value.setter
    def value(self, value):
        if value:
            self._text.insertText(value)

    def rehint(self):
        self.style.hint(
            min_height=100,
            min_width=100
        )
