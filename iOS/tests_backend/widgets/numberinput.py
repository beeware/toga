from pytest import xfail
from rubicon.objc import NSRange

from toga_iOS.libs import UITextField

from .base import SimpleProbe
from .properties import toga_alignment, toga_color, toga_font


class NumberInputProbe(SimpleProbe):
    native_class = UITextField
    allows_invalid_value = True

    def clear_input(self):
        self.widget.value = ""

    @property
    def value(self):
        return str(self.native.text)

    async def increment(self):
        xfail("iOS doesn't support stepped increments")

    async def decrement(self):
        xfail("iOS doesn't support stepped increments")

    @property
    def color(self):
        return toga_color(self.native.textColor)

    @property
    def font(self):
        return toga_font(self.native.font)

    @property
    def alignment(self):
        return toga_alignment(self.native.textAlignment)

    def assert_vertical_alignment(self, expected):
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
