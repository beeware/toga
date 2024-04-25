import System.Windows.Forms
from System.Drawing import SystemColors

from toga.colors import TRANSPARENT
from toga_winforms.colors import toga_color_from_native_color

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = System.Windows.Forms.Panel

    @property
    def background_color(self):
        if self.native.BackColor.ToArgb() == SystemColors.ControlDark.ToArgb():
            return None
        else:
            return super().background_color

    def assert_background_color(self, color):
        if color is None or (color == TRANSPARENT and (not self.widget.parent)):
            assert toga_color_from_native_color(
                self.impl.native.BackColor
            ) == toga_color_from_native_color(SystemColors.ControlDark)
        else:
            super().assert_background_color(color)
