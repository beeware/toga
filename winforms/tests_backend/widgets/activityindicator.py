import System.Windows.Forms

from .base import SimpleProbe


class ActivityIndicatorProbe(SimpleProbe):
    native_class = System.Windows.Forms.PictureBox

    def assert_is_hidden(self, value):
        assert (not self.native.Visible) == value
