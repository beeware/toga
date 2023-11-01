from rubicon.objc import objc_method, objc_property
from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga_cocoa.colors import native_color
from toga_cocoa.libs import (
    NSBezelBorder,
    NSScrollView,
    NSTextAlignment,
    NSTextView,
    NSViewHeightSizable,
    NSViewWidthSizable,
)

from .base import Widget


class TogaTextView(NSTextView):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def textDidChange_(self, notification) -> None:
        self.interface.on_change()


class MultilineTextInput(Widget):
    def create(self):
        # Create a multiline view, and put it in a scroll view.
        # The scroll view is the native, because it's the outer container.
        self.native = NSScrollView.alloc().init()
        self.native.hasVerticalScroller = True
        self.native.hasHorizontalScroller = False
        self.native.autohidesScrollers = False
        self.native.borderType = NSBezelBorder

        # Create the actual text widget
        self.native_text = TogaTextView.alloc().init()
        self.native_text.interface = self.interface
        self.native_text.delegate = self.native_text

        self.native_text.editable = True
        self.native_text.selectable = True
        self.native_text.allowsUndo = True
        self.native_text.verticallyResizable = True
        self.native_text.horizontallyResizable = False
        self.native_text.usesAdaptiveColorMappingForDarkAppearance = True

        self.native_text.autoresizingMask = NSViewWidthSizable | NSViewHeightSizable

        # Put the text view in the scroll window.
        self.native.documentView = self.native_text

        # Add the layout constraints
        self.add_constraints()

    def get_placeholder(self):
        return str(self.native_text.placeholderString)

    def set_placeholder(self, value):
        self.native_text.placeholderString = value

    def get_enabled(self):
        return self.native_text.isSelectable()

    def set_enabled(self, value):
        self.native_text.editable = value
        self.native_text.selectable = value

    def get_readonly(self):
        return not self.native_text.isEditable()

    def set_readonly(self, value):
        self.native_text.editable = not value

    def get_value(self):
        return str(self.native_text.string)

    def set_value(self, value):
        self.native_text.string = value
        self.interface.on_change()

    def set_color(self, value):
        self.native_text.textColor = native_color(value)

    def set_background_color(self, color):
        if color is TRANSPARENT:
            # Both the text view and the scroll view need to be made transparent
            self.native.drawsBackground = False
            self.native_text.drawsBackground = False
        else:
            # Both the text view and the scroll view need to be opaque,
            # but only the text view needs a color.
            self.native.drawsBackground = True
            self.native_text.drawsBackground = True
            self.native_text.backgroundColor = native_color(color)

    def set_alignment(self, value):
        self.native_text.alignment = NSTextAlignment(value)

    def set_font(self, font):
        self.native_text.font = font._impl.native

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def scroll_to_bottom(self):
        self.native_text.scrollToEndOfDocument(None)

    def scroll_to_top(self):
        self.native_text.scrollToBeginningOfDocument(None)
