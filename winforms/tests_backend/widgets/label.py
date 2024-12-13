import System.Windows.Forms

from .base import SimpleProbe
from .properties import toga_x_text_align, toga_y_text_align


class LabelProbe(SimpleProbe):
    native_class = System.Windows.Forms.Label

    @property
    def text(self):
        return self.native.Text

    @property
    def text_align(self):
        return toga_x_text_align(self.native.TextAlign)

    def assert_vertical_text_align(self, expected):
        assert toga_y_text_align(self.native.TextAlign) == expected
