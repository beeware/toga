import System.Windows.Forms

from .base import SimpleProbe
from .properties import to_toga_x_text_align, to_toga_y_text_align


class LabelProbe(SimpleProbe):
    native_class = System.Windows.Forms.Label

    @property
    def text(self):
        return self.native.Text

    @property
    def text_align(self):
        return to_toga_x_text_align(self.native.TextAlign)

    def assert_vertical_text_align(self, expected):
        assert to_toga_y_text_align(self.native.TextAlign) == expected
