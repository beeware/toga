import System.Windows.Forms
from System.Drawing import SystemColors

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = System.Windows.Forms.Panel

    @property
    def background_color(self):
        if self.native.BackColor.ToArgb() == SystemColors.ControlDark.ToArgb():
            return None
        else:
            return super().background_color
