import toga
from toga_winforms.libs import WinForms
from travertino.size import at_least

from .base import Widget


class Divider(Widget):
    def create(self):
        self.native = WinForms.Label()
        self.native.BorderStyle = WinForms.BorderStyle.Fixed3D
        self.native.AutoSize = False

    def set_direction(self, value):
        if value == toga.Divider.HORIZONTAL:
            self.native.Height = 2
        else:
            self.native.Width = 2

    def rehint(self):
        if self.interface.direction == toga.Divider.HORIZONTAL:
            self.interface.intrinsic.width = at_least(self.native.Width)
            self.interface.intrinsic.height = self.native.Height
        else:
            self.interface.intrinsic.width = self.native.Width
            self.interface.intrinsic.height = at_least(self.native.Height)
