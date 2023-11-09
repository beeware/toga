from decimal import ROUND_UP

import System.Windows.Forms as WinForms
from travertino.size import at_least

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
            self.interface.intrinsic.width = self.scale_out(
                at_least(self.native.Width), ROUND_UP
            )
            self.interface.intrinsic.height = self.scale_out(
                self.native.Height, ROUND_UP
            )
        else:
            self.interface.intrinsic.width = self.scale_out(self.native.Width, ROUND_UP)
            self.interface.intrinsic.height = self.scale_out(
                at_least(self.native.Height), ROUND_UP
            )
