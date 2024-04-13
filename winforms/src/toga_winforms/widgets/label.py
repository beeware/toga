from decimal import ROUND_UP

import System.Windows.Forms as WinForms
from travertino.size import at_least

from toga_winforms.libs.fonts import TextAlignment

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = WinForms.Label()
        self.native.AutoSizeMode = WinForms.AutoSizeMode.GrowAndShrink

    def set_alignment(self, value):
        self.native.TextAlign = TextAlignment(value)

    def get_text(self):
        return self.native.Text

    def set_text(self, value):
        self.native.Text = value

    def rehint(self):
        self.interface.intrinsic.width = self.scale_out(
            at_least(self.native.PreferredSize.Width), ROUND_UP
        )
        self.interface.intrinsic.height = self.scale_out(
            self.native.PreferredSize.Height, ROUND_UP
        )
