import System.Windows.Forms

from toga.colors import TRANSPARENT

from .base import SimpleProbe
from .properties import toga_color


class BoxProbe(SimpleProbe):
    native_class = System.Windows.Forms.Panel

    @property
    def background_color(self):
        if self.native.BackColor == self.widget.parent._impl.native.BackColor:
            return TRANSPARENT
        else:
            return toga_color(self.native.BackColor)
