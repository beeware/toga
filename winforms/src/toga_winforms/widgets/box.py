import System.Windows.Forms as WinForms

from toga.colors import TRANSPARENT

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = WinForms.Panel()

    def set_background_color(self, color):
        if color is None:
            super().set_background_color(TRANSPARENT)
        else:
            super().set_background_color(color)
