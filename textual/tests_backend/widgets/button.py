import pytest
from textual.widgets import Button as TextualButton

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = TextualButton
    minimum_required_height = 80

    @property
    def text(self):
        return str(self.native.label)

    def assert_no_icon(self):
        assert self.widget.icon is None

    def assert_icon_size(self):
        pytest.skip("Button icons are not implemented on Textual.")

    async def press(self):
        self.native.press()
        await self.redraw("Button should be pressed")
