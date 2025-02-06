import pytest
from System.Windows.Forms import NumericUpDown

from .base import SimpleProbe
from .properties import toga_x_text_align


class NumberInputProbe(SimpleProbe):
    native_class = NumericUpDown
    allows_invalid_value = False
    allows_empty_value = True
    allows_extra_digits = True
    fixed_height = 23

    @property
    def value(self):
        return self.native.Text

    @property
    def readonly(self):
        return self.native.ReadOnly

    def clear_input(self):
        self.native.Text = ""

    async def increment(self):
        self.widget.focus()
        await self.type_character("<up>")

    async def decrement(self):
        self.widget.focus()
        await self.type_character("<down>")

    @property
    def text_align(self):
        return toga_x_text_align(self.native.TextAlign)

    def assert_vertical_text_align(self, expected):
        # Vertical text alignment isn't configurable in this native widget.
        pass

    def set_cursor_at_end(self):
        pytest.skip("Cursor positioning not supported on this platform")
