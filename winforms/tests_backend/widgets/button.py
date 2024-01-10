import pytest
import System.Windows.Forms
from System.Drawing import SystemColors

from .base import SimpleProbe
from .properties import toga_color


class ButtonProbe(SimpleProbe):
    native_class = System.Windows.Forms.Button
    background_supports_alpha = False

    @property
    def text(self):
        # Normalize the zero width space to the empty string.
        if self.native.Text == "\u200B":
            return ""
        return self.native.Text

    def assert_no_icon(self):
        assert self.native.Image is None

    def assert_icon_size(self):
        icon = self.native.Image
        if icon:
            assert (icon.Size.Width, icon.Size.Height) == (32, 32)
        else:
            pytest.fail("Icon does not exist")

    @property
    def background_color(self):
        if self.native.BackColor == SystemColors.Control:
            return None
        else:
            return toga_color(self.native.BackColor)
