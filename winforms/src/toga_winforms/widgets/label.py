from decimal import ROUND_UP

import System.Windows.Forms as WinForms
from travertino.size import at_least

from toga.colors import TRANSPARENT
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

    def set_background_color(self, color):
        if color in {None, TRANSPARENT}:
            # Label though allows setting BackColor to Color.Transparent, but it doesn't
            # actually work, the background color will be white when set to Color.Transparent
            # Also tried:
            # ```
            #  label1.Parent = pictureBox1
            #  label1.BackColor = Color.Transparent
            # ```
            # But it only works if the label is inside/above a PictureBox and not for other cases.
            # So, the best bet for transparency is to make label background color same as the
            # container inside which the widget is present.
            if self.interface.parent:
                self.native.BackColor = self.interface.parent._impl.native.BackColor
        else:
            super().set_background_color(color)

    def rehint(self):
        self.interface.intrinsic.width = self.scale_out(
            at_least(self.native.PreferredSize.Width), ROUND_UP
        )
        self.interface.intrinsic.height = self.scale_out(
            self.native.PreferredSize.Height, ROUND_UP
        )
