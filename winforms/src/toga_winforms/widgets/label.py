from decimal import ROUND_UP

import System.Drawing
import System.Windows.Forms as WinForms
from travertino.size import at_least
from ..libs.wrapper import WeakrefCallable

from toga_winforms.libs.fonts import TextAlignment

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = WinForms.Label()
        self.native.AutoSizeMode = WinForms.AutoSizeMode.GrowAndShrink
        self._wrap = False

    def set_alignment(self, value):
        self.native.TextAlign = TextAlignment(value)

    def get_text(self):
        return self.native.Text

    def set_text(self, value):
        self.native.Text = value

    def get_wrap(self):
        return self._wrap
    
    def set_wrap(self, wrap):
        self._wrap = wrap

    def rehint(self):
        if self._wrap:
            # When text wrapping is enabled we need to return the minimum width.
            proposed_size =  System.Drawing.Size(1, 0)
            width = WinForms.TextRenderer.MeasureText( self.native.Text,  self.native.Font, proposed_size, WinForms.TextFormatFlags.WordBreak).Width
        else:
            width = self.native.PreferredSize.Width
        self.interface.intrinsic.width = self.scale_out(at_least(width), ROUND_UP)
        self.interface.intrinsic.height = self.scale_out(
            self.native.PreferredSize.Height, ROUND_UP
        )

    def compute_size(self, width, height):
        if self._wrap:
            # When text wrapping is enabled, we need to do additional calculation to determine the proper height.
            width = self.scale_out(width,ROUND_UP)
            proposed_size = System.Drawing.Size(width, 0)
            height = WinForms.TextRenderer.MeasureText( self.native.Text,  self.native.Font, proposed_size, WinForms.TextFormatFlags.WordBreak).Height
        return  width, height