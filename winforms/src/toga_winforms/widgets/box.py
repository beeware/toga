import System.Windows.Forms as WinForms

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = WinForms.Panel()
