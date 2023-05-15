import asyncio

from toga_gtk.libs import Gtk

from .base import SimpleProbe
from .properties import toga_alignment, toga_color, toga_font


class MultilineTextInputProbe(SimpleProbe):
    native_class = Gtk.ScrolledWindow

    def __init__(self, widget):
        super().__init__(widget)
        self.native_textview = self.impl.native_textview

    @property
    def value(self):
        return self.impl.buffer.get_text(
            self.impl.buffer.get_start_iter(), self.impl.buffer.get_end_iter(), True
        )

    @property
    def placeholder(self):
        return str(self.impl._placeholder)

    def placeholder_visible(self):
        return self.impl.buffer.get_start_iter().has_tag(self.impl.tag_placeholder)

    @property
    def placeholder_hides_on_focus(self):
        return True

    @property
    def color(self):
        sc = self.native_textview.get_style_context()
        return toga_color(sc.get_property("color", sc.get_state()))

    @property
    def background_color(self):
        sc = self.native_textview.get_style_context()
        return toga_color(sc.get_property("background-color", sc.get_state()))

    @property
    def font(self):
        sc = self.native_textview.get_style_context()
        return toga_font(sc.get_property("font", sc.get_state()))

    @property
    def alignment(self):
        return toga_alignment(
            self.native_textview.get_justification(),
        )

    @property
    def enabled(self):
        # Enabled is proxied onto readonly on the text view
        return self.native_textview.get_property("editable")

    @property
    def readonly(self):
        return not self.native_textview.get_property("editable")

    @property
    def visible_height(self):
        return self.native.frame.size.height

    @property
    def visible_width(self):
        return self.native.frame.size.width

    @property
    def document_height(self):
        return max(self.native.contentSize.height, self.native.frame.size.height)

    @property
    def document_width(self):
        return max(self.native.contentSize.width, self.native.frame.size.width)

    @property
    def vertical_scroll_position(self):
        return self.native.contentOffset.y

    async def wait_for_scroll_completion(self):
        position = self.vertical_scroll_position
        current = None
        # Iterate until 2 successive reads of the scroll position,
        # 0.05s apart, return the same value
        while position != current:
            position = current
            await asyncio.sleep(0.05)
            current = self.vertical_scroll_position
