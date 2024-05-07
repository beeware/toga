import System.Windows.Forms

from .base import SimpleProbe
from .properties import toga_xalignment, toga_yalignment


class LabelProbe(SimpleProbe):
    native_class = System.Windows.Forms.Label

    @property
    def text(self):
        return self.native.Text

    @property
    def alignment(self):
        return toga_xalignment(self.native.TextAlign)

    def assert_vertical_alignment(self, expected):
        assert toga_yalignment(self.native.TextAlign) == expected
