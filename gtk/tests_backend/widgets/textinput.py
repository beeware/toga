import pytest

from toga.constants import JUSTIFY, LEFT
from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe
from .properties import toga_x_text_align


class TextInputProbe(SimpleProbe):
    native_class = Gtk.Entry

    if GTK_VERSION >= (4, 0, 0):
        pytest.skip("GTK4 doesn't support text input yet")

    @property
    def value(self):
        return (
            self.native.get_placeholder_text()
            if self.placeholder_visible
            else self.native.get_text()
        )

    @property
    def value_hidden(self):
        return not self.native.get_visibility()

    @property
    def placeholder_visible(self):
        # GTK manages it's own placeholder visibility.
        # We can use the existence of widget text as a proxy.
        return not bool(self.native.get_text())

    @property
    def placeholder_hides_on_focus(self):
        return False

    @property
    def text_align(self):
        return toga_x_text_align(self.native.get_alignment())

    def assert_text_align(self, expected):
        if expected == JUSTIFY:
            assert self.text_align == LEFT
        else:
            assert self.text_align == expected

    def assert_vertical_text_align(self, expected):
        # GTK.Entry vertical alignment is non-configurable
        pass

    @property
    def readonly(self):
        return not self.native.get_property("editable")

    def set_cursor_at_end(self):
        pytest.skip("Cursor positioning not supported on this platform")
