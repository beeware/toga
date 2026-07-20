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

    def rehint(self):
        # A previous attempt at direction setting hardcoded widths and heights in
        # set_direction onto the native widget, and used self.native.Width and
        # self.native.Height in this block.  This is unreliable, as if rehint
        # does not immediately happen after set_direction (such as in DPI scaling
        # adjustments), the current length of the divider would be enforced as the
        # minimum length.  Thus, all divider-related layout happens at the rehint,
        # which will manifest the correct direction in set_bounds once Toga's
        # layout finishes.
        if self.get_direction() == self.interface.HORIZONTAL:
            self.interface.intrinsic.width = at_least(0)
            self.interface.intrinsic.height = self.scale_out(2, ROUND_UP)
        else:
            self.interface.intrinsic.width = self.scale_out(2, ROUND_UP)
            self.interface.intrinsic.height = at_least(0)
