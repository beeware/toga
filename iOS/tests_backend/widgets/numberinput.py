import pytest
from rubicon.objc import NSRange

from toga_iOS.libs import UITextField

from .base import SimpleProbe
from .properties import toga_color, toga_text_align


class NumberInputProbe(SimpleProbe):
    native_class = UITextField
    allows_invalid_value = True

    def clear_input(self):
        self.widget.value = ""

    @property
    def value(self):
        return str(self.native.text)

    async def increment(self):
        pytest.xfail("iOS doesn't support stepped increments")

    async def decrement(self):
        pytest.xfail("iOS doesn't support stepped increments")

    @property
    def color(self):
        return toga_color(self.native.textColor)

    @property
    def text_align(self):
        return toga_text_align(self.native.textAlignment)

    def assert_vertical_text_align(self, expected):
        # Vertical alignment isn't configurable on a UITextField
        pass

    @property
    def readonly(self):
        return not self.native.isEnabled()

    def _prevalidate_input(self, char):
        # Trigger the textField:shouldChangeCharactersInRange:replacementString:
        # delegate handler.
        return self.native.textField(
            self.native,
            shouldChangeCharactersInRange=NSRange(len(self.native.text), 0),
            replacementString=char,
        )

    def set_cursor_at_end(self):
        pytest.skip("Cursor positioning not supported on this platform")
