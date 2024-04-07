import System.Windows.Forms

from toga.colors import TRANSPARENT

from .base import SimpleProbe
from .properties import toga_color, toga_xalignment, toga_yalignment


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

    @property
    def background_color(self):
        if self.native.BackColor == self.widget.parent._impl.native.BackColor:
            return TRANSPARENT
        else:
            return toga_color(self.native.BackColor)
