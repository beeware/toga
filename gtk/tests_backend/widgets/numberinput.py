import pytest

from toga.constants import JUSTIFY, LEFT
from toga_gtk.libs import Gtk

from .base import SimpleProbe
from .properties import toga_xalignment


class NumberInputProbe(SimpleProbe):
    native_class = Gtk.SpinButton
    allows_invalid_value = False
    allows_empty_value = False
    allows_extra_digits = False

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
    def alignment(self):
        return toga_xalignment(self.native.get_alignment())

    def assert_alignment(self, expected):
        if expected == JUSTIFY:
            assert self.alignment == LEFT
        else:
            assert self.alignment == expected

    def assert_vertical_alignment(self, expected):
        # GTK.SpinButton vertical alignment is non-configurable
        pass

    @property
    def readonly(self):
        return not self.native.get_property("editable")

    def set_cursor_at_end(self):
        pytest.skip("Cursor positioning not supported on this platform")
