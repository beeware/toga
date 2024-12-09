import System.Windows.Forms

from .base import SimpleProbe
from .properties import toga_x_text_alignment, toga_y_text_alignment


class LabelProbe(SimpleProbe):
    native_class = System.Windows.Forms.Label

    @property
    def text(self):
        return self.native.Text

    @property
    def text_alignment(self):
        return toga_x_text_alignment(self.native.TextAlign)

    def assert_vertical_text_alignment(self, expected):
        assert toga_y_text_alignment(self.native.TextAlign) == expected
