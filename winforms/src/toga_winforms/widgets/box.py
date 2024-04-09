import System.Windows.Forms as WinForms

from toga.colors import TRANSPARENT

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = WinForms.Panel()

    def set_background_color(self, color):
        if color in {None, TRANSPARENT}:
            if self.interface.parent:
                self.native.BackColor = self.interface.parent._impl.native.BackColor
        else:
            super().set_background_color(color)
