import System.Windows.Forms
from pytest import skip

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = System.Windows.Forms.Button

    @property
    def text(self):
        return self.native.Text

    @property
    def font(self):
        skip("Font probe not implemented")

    def assert_display_properties(self):
        # No special display properties to assert
        pass
