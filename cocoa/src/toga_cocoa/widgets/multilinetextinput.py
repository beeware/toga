from travertino.size import at_least

from toga_cocoa.colors import native_color
from toga_cocoa.libs import (
    NSBezelBorder,
    NSScrollView,
    NSTextView,
    NSViewWidthSizable,
    objc_method,
)

from .base import Widget


class TogaTextView(NSTextView):
    @objc_method
    def touchBar(self):
        # Disable the touchbar.
        return None

    @objc_method
    def textDidChange_(self, notification) -> None:
        self.interface.on_change(None)


class MultilineTextInput(Widget):
    def create(self):
        # Create a multiline view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        self.native = NSScrollView.alloc().init()
        self.native.hasVerticalScroller = True
        self.native.hasHorizontalScroller = False
        self.native.autohidesScrollers = False
        self.native.borderType = NSBezelBorder

        # Disable all autolayout functionality on the outer widget
        self.native.translatesAutoresizingMaskIntoConstraints = False

        # Create the actual text widget
        self.text = TogaTextView.alloc().init()
        self.text.interface = self.interface
        self.text.delegate = self.text

        self.text.editable = True
        self.text.selectable = True
        self.text.verticallyResizable = True
        self.text.horizontallyResizable = False
        self.text.usesAdaptiveColorMappingForDarkAppearance = True

        self.text.autoresizingMask = NSViewWidthSizable

        # Put the text view in the scroll window.
        self.native.documentView = self.text

        # Add the layout constraints
        self.add_constraints()

    def get_placeholder(self):
        return self.text.placeholderString

    def set_placeholder(self, value):
        self.text.placeholderString = value

    def get_readonly(self):
        return not self.text.isEditable()

    def set_readonly(self, value):
        self.text.editable = not value

    def get_value(self):
        return self.text.string

    def set_value(self, value):
        self.text.string = value

    def set_color(self, value):
        self.text.textColor = native_color(value)

    def set_font(self, font):
        if font:
            self.text.font = font._impl.native

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def scroll_to_bottom(self):
        self.text.scrollToEndOfDocument(None)

    def scroll_to_top(self):
        self.text.scrollToBeginningOfDocument(None)
