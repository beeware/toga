from pytest import xfail
from rubicon.objc import NSRange

from toga.constants import TOP
from toga_iOS.libs import UITextField

from .base import SimpleProbe
from .properties import toga_alignment, toga_color, toga_font


class NumberInputProbe(SimpleProbe):
    native_class = UITextField

    @property
    def empty_value(self):
        return None

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

    @property
    def vertical_alignment(self):
        # FIXME; This is a lie - but it's also non-configurable.
        return TOP

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
