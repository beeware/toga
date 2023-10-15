from toga.colors import TRANSPARENT
from toga.constants import RIGHT
from toga_cocoa.libs import (
    NSLeftTextAlignment,
    NSRange,
    NSRightTextAlignment,
    NSTextField,
    NSTextView,
)

from .base import SimpleProbe
from .properties import toga_alignment, toga_color


class TextInputProbe(SimpleProbe):
    native_class = NSTextField

    @property
    def value(self):
        return str(
            self.native.placeholderString
            if self.placeholder_visible
            else self.native.stringValue
        )

    @property
    def value_hidden(self):
        return False

    @property
    def placeholder_visible(self):
        # macOS manages it's own placeholder visibility.
        # We can use the existence of widget text as a proxy.
        return not bool(self.native.stringValue)

    @property
    def placeholder_hides_on_focus(self):
        return False

    @property
    def color(self):
        return toga_color(self.native.textColor)

    @property
    def background_color(self):
        if self.native.drawsBackground:
            # Confirm the widget is bezeled
            assert self.native.isBezeled()
            if self.native.backgroundColor:
                return toga_color(self.native.backgroundColor)
            else:
                return None
        else:
            # Confirm the widget is not bezeled
            assert not self.native.isBezeled()
            return TRANSPARENT

    @property
    def font(self):
        return self.native.font

    @property
    def alignment(self):
        result = toga_alignment(self.native.alignment)
        if result == RIGHT:
            assert self.impl.error_label.alignment == NSLeftTextAlignment
        else:
            assert self.impl.error_label.alignment == NSRightTextAlignment
        return result

    def assert_vertical_alignment(self, expected):
        # Vertical alignment isn't configurable on NSTextField
        pass

    @property
    def readonly(self):
        return not self.native.isEditable()

    @property
    def has_focus(self):
        # When the NSTextField gets focus, a field editor is created, and that editor
        # has the original widget as the delegate. The first responder is the Field Editor.
        return isinstance(self.native.window.firstResponder, NSTextView) and (
            self.native.window.firstResponder.delegate == self.native
        )

    def set_cursor_at_end(self):
        self.native.currentEditor().selectedRange = NSRange(len(self.value), 0)
