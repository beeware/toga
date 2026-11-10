import System.Windows.Forms as WinForms
from System.Drawing import Color

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = WinForms.Panel()
        self._default_background_color = Color.Transparent
