import pytest
import System.Windows.Forms

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = System.Windows.Forms.Button

    @property
    def text(self):
        # Normalize the zero width space to the empty string.
        if self.native.Text == "\u200b":
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
