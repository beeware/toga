from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class Divider(Widget):
    def create(self):
        self.native = WinForms.Label()
        self.native.BorderStyle = WinForms.BorderStyle.Fixed3D
        self.native.AutoSize = False

        self._direction = self.interface.HORIZONTAL

    def get_direction(self):
        return self._direction

    def set_direction(self, value):
        self._direction = value
        if value == self.interface.HORIZONTAL:
            self.native.Height = 2
            self.native.Width = 0
        else:
            self.native.Height = 0
            self.native.Width = 2

    def rehint(self):
        if self.get_direction() == self.interface.HORIZONTAL:
            self.interface.intrinsic.width = at_least(self.native.Width)
            self.interface.intrinsic.height = self.native.Height
        else:
            self.interface.intrinsic.width = self.native.Width
            self.interface.intrinsic.height = at_least(self.native.Height)
