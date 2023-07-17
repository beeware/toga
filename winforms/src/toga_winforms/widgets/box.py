from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga_winforms.colors import native_color
from toga_winforms.libs import WinForms

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = WinForms.Panel()
        self.native.interface = self.interface

    def set_background_color(self, value):
        if value:
            self.native.BackColor = native_color(value)
        else:
            self.native.BackColor = native_color(TRANSPARENT)

    def rehint(self):
        self.interface.intrinsic.width = at_least(0)
        self.interface.intrinsic.height = at_least(0)
