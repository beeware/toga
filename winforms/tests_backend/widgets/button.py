import System.Windows.Forms
from System.Drawing import SystemColors

from .base import SimpleProbe
from .properties import toga_color


class ButtonProbe(SimpleProbe):
    native_class = System.Windows.Forms.Button

    @property
    def text(self):
        return self.native.Text

    @property
    def background_color(self):
        if self.native.BackColor == SystemColors.Control:
            return None
        else:
            return toga_color(self.native.BackColor)
