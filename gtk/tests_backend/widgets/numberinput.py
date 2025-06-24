import pytest

from toga.constants import JUSTIFY, LEFT
from toga_gtk.libs import GTK_VERSION, Gtk

from .base import SimpleProbe
from .properties import toga_x_text_align


class NumberInputProbe(SimpleProbe):
    native_class = Gtk.SpinButton
    allows_invalid_value = False
    allows_empty_value = False
    allows_extra_digits = False

    if GTK_VERSION >= (4, 0, 0):
        pytest.skip("GTK4 doesn't support number input yet")

    def clear_input(self):
        self.native.set_text("")

    @property
    def value(self):
        return self.native.get_text()

    async def increment(self):
        self.native.spin(
            Gtk.SpinType.STEP_FORWARD, self.impl.adjustment.get_step_increment()
        )

    async def decrement(self):
        self.native.spin(
            Gtk.SpinType.STEP_BACKWARD, self.impl.adjustment.get_step_increment()
        )

    @property
    def text_align(self):
        return toga_x_text_align(self.native.get_alignment())

    def assert_text_align(self, expected):
        if expected == JUSTIFY:
            assert self.text_align == LEFT
        else:
            assert self.text_align == expected

    def assert_vertical_text_align(self, expected):
        # GTK.SpinButton vertical alignment is non-configurable
        pass

    @property
    def readonly(self):
        return not self.native.get_property("editable")

    def set_cursor_at_end(self):
        pytest.skip("Cursor positioning not supported on this platform")
