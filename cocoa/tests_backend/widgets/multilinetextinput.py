from rubicon.objc import ObjCClass

from toga.colors import TRANSPARENT
from toga_cocoa.libs import (
    NSAttributedString,
    NSColor,
    NSFont,
    NSFontAttributeName,
    NSMutableDictionary,
    NSRange,
    NSScrollView,
    NSTextView,
)

from .base import SimpleProbe
from .properties import toga_color, toga_text_align

NSPasteboard = ObjCClass("NSPasteboard")


class MultilineTextInputProbe(SimpleProbe):
    native_class = NSScrollView
    redo_available = True
    supports_simulate_mouse_wheel = False

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
            # None as a background color is misconfigured, and produces
            # incorrect results.
            assert self.native_text.backgroundColor is not None
            if self.native_text.backgroundColor != NSColor.textBackgroundColor:
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
    def text_align(self):
        return toga_text_align(self.native_text.alignment)

    def assert_vertical_text_align(self, expected):
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

    def paste_rich_text(self, text):
        "Paste bold, large text through a private pasteboard."
        attributes = NSMutableDictionary.alloc().init()
        attributes[NSFontAttributeName] = NSFont.boldSystemFontOfSize(36)
        styled = NSAttributedString.alloc().initWithString(text, attributes=attributes)
        pasteboard = NSPasteboard.pasteboardWithUniqueName()
        pasteboard.clearContents()
        pasteboard.setData(
            styled.RTFFromRange(NSRange(0, styled.length()), documentAttributes={}),
            forType="public.rtf",
        )
        pasteboard.setString(text, forType="public.utf8-plain-text")
        try:
            assert self.native_text.readSelectionFromPasteboard(pasteboard)
        finally:
            pasteboard.releaseGlobally()

    @property
    def text_fonts(self):
        storage = self.native_text.textStorage
        fonts = [
            storage.attribute(NSFontAttributeName, atIndex=i, effectiveRange=None)
            for i in range(storage.length())
        ]
        return [(str(font.fontName), float(font.pointSize)) for font in fonts]

    @property
    def typing_font(self):
        font = self.native_text.typingAttributes[NSFontAttributeName]
        return str(font.fontName), float(font.pointSize)
