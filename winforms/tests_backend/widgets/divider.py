import System.Windows.Forms
from System.Drawing import SystemColors

from toga_winforms.colors import toga_color_from_native_color

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = System.Windows.Forms.Panel

    def assert_background_color(self, color):
        if color is None:
            super().assert_background_color(
                toga_color_from_native_color(SystemColors.ControlDark)
            )
        else:
            super().assert_background_color(color)
