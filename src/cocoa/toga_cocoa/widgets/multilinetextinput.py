from ..libs import NSTextView, NSScrollView, NSBezelBorder, NSViewWidthSizable, NSViewHeightSizable
from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        # Create a multiline view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        self.native = NSScrollView.alloc().init()
        self.native.setHasVerticalScroller_(True)
        self.native.setHasHorizontalScroller_(False)
        self.native.setAutohidesScrollers_(False)
        self.native.setBorderType_(NSBezelBorder)
        self.native.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)

        # Disable all autolayout functionality on the outer widget
        # self.native.setTranslatesAutoresizingMaskIntoConstraints_(False)
        # self.native.setAutoresizesSubviews_(False)

        # self.native.contentView.setTranslatesAutoresizingMaskIntoConstraints_(False)
        # self.native.contentView.setAutoresizesSubviews_(False)

        # Use a dummy size initially.
        self._text = NSTextView.alloc().init()

        # Disable all autolayout functionality on the inner widget
        # self._text.setTranslatesAutoresizingMaskIntoConstraints_(False)
        # self._text.setAutoresizesSubviews_(False)

        self._text.setEditable_(True)
        self._text.setVerticallyResizable_(True)
        self._text.setHorizontallyResizable_(False)
        self._text.setAutoresizingMask_(NSViewWidthSizable)

        self.native.setDocumentView_(self._text)

        # Add the layout constraints
        self.add_constraints()

    @property
    def value(self):
        return self._text.string

    @value.setter
    def value(self, value):
        if value:
            self._text.insertText_(value)

    def _apply_layout(self):
        frame = NSRect(NSPoint(self.layout.left, self.layout.top),
                       NSSize(self.layout.width, self.layout.height))
        self.native.setFrame_(frame)
        self.native.contentView.setFrame_(frame)
        self.native.setNeedsDisplay_(True)
