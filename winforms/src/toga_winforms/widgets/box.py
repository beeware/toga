import System.Windows.Forms as WinForms

from toga.colors import TRANSPARENT

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = WinForms.Panel()

    def set_background_color(self, color):
        super().set_background_color(TRANSPARENT if color is None else color)
