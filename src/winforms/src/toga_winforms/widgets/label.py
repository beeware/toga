from travertino.constants import TRANSPARENT
from travertino.size import at_least

from toga_winforms.libs import TextAlignment, WinForms
from toga_winforms.colors import native_color

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = WinForms.Label()

    def set_alignment(self, value):
        self.native.TextAlign = TextAlignment(value)

    def set_text(self, value):
        self.native.Text = self.interface._text

    def set_font(self, font):
        if font:
            self.native.Font = font.bind(self.interface.factory).native

    def set_color(self, value):
        if value:
            self.native.ForeColor = native_color(value)
        else:
            self.native.ForeColor = native_color(TRANSPARENT)

    def set_background_color(self, value):
        if value:
            self.native.BackColor = native_color(value)
        else:
            self.native.BackColor = native_color(TRANSPARENT)

    def rehint(self):
        # Width & height of a label is known and fixed.
        # self.native.Size = Size(0, 0)
        # print("REHINT label", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
