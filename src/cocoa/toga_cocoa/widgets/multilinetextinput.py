from toga_cocoa.colors import native_color
from toga_cocoa.libs import (NSBezelBorder, NSScrollView, NSTextView,
                             NSViewWidthSizable, objc_method)
from travertino.size import at_least

from .base import Widget


class TogaTextView(NSTextView):
    @objc_method
    def touchBar(self):
        # Disable the touchbar.
        return None


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
        self.text.editable = True
        self.text.selectable = True
        self.text.verticallyResizable = True
        self.text.horizontallyResizable = False

        self.text.autoresizingMask = NSViewWidthSizable

        # Put the text view in the scroll window.
        self.native.documentView = self.text

        # Add the layout constraints
        self.add_constraints()

    def set_placeholder(self, value):
        self.text.placeholderString = self.interface._value

    def set_readonly(self, value):
        self.text.editable = not self.interface._readonly

    def get_value(self):
        return self.text.string

    def set_value(self, value):
        self.text.string = self.interface._value

    def set_color(self, value):
        if value:
            self.text.textColor = native_color(value)

    def set_font(self, value):
        if value:
            self.text.font = value._impl.native

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
