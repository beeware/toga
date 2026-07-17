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

    def set_background_color(self, value):
        # Do nothing, since background color of Divider shouldn't be changed.
        pass

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
        # Do not use self.native.Width or self.native.Height here, as rehint is not
        # necessarily called just after set_direction, in which case the Width/Height
        # will reflect the real width/height and be incorrectly used as minimums.
        # This issue can be manifested when moving a window with a divider between two
        # monitors, where the width of the divider will be incorrectly set as the new
        # minimum.
        if self.get_direction() == self.interface.HORIZONTAL:
            self.interface.intrinsic.width = at_least(0)
            self.interface.intrinsic.height = self.scale_out(2, ROUND_UP)
        else:
            self.interface.intrinsic.width = self.scale_out(2, ROUND_UP)
            self.interface.intrinsic.height = at_least(0)
