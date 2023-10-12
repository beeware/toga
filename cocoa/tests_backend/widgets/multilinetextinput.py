from toga.colors import TRANSPARENT
from toga_cocoa.libs import NSRange, NSScrollView, NSTextView

from .base import SimpleProbe
from .properties import toga_alignment, toga_color


class MultilineTextInputProbe(SimpleProbe):
    native_class = NSScrollView

    def __init__(self, widget):
        super().__init__(widget)
        self.native_text = widget._impl.native_text
        assert isinstance(self.native_text, NSTextView)

    @property
    def value(self):
        return str(
            self.native_text.placeholderString
            if self.placeholder_visible
            else self.native_text.string
        )

    @property
    def placeholder_visible(self):
        # macOS manages it's own placeholder visibility.
        # We can use the existence of widget text as a proxy.
        return not bool(self.native_text.string)

    @property
    def placeholder_hides_on_focus(self):
        return False

    @property
    def value_hidden(self):
        return False

    @property
    def color(self):
        return toga_color(self.native_text.textColor)

    @property
    def background_color(self):
        if self.native_text.drawsBackground:
            # Confirm the scroll container is also opaque
            assert self.native.drawsBackground
            if self.native_text.backgroundColor:
                return toga_color(self.native_text.backgroundColor)
            else:
                return None
        else:
            # Confirm the scroll container is also transparent
            assert not self.native.drawsBackground
            return TRANSPARENT

    @property
    def font(self):
        return self.native_text.font

    @property
    def alignment(self):
        return toga_alignment(self.native_text.alignment)

    def assert_vertical_alignment(self, expected):
        # Vertical alignment isn't configurable on NSTextView
        pass

    @property
    def enabled(self):
        return self.native_text.isSelectable()

    @property
    def readonly(self):
        return not self.native_text.isEditable()

    @property
    def has_focus(self):
        return self.native.window.firstResponder == self.native_text

    @property
    def document_height(self):
        return self.native_text.bounds.size.height

    @property
    def document_width(self):
        return self.native_text.bounds.size.width

    @property
    def horizontal_scroll_position(self):
        return self.native.contentView.bounds.origin.x

    @property
    def vertical_scroll_position(self):
        return self.native.contentView.bounds.origin.y

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    def set_cursor_at_end(self):
        self.native.selectedRange = NSRange(len(self.value), 0)
