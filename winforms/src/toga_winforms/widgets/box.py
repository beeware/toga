import System.Windows.Forms as WinForms
from travertino.size import at_least

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = WinForms.Panel()

    def rehint(self):
        self.interface.intrinsic.width = at_least(0)
        self.interface.intrinsic.height = at_least(0)
