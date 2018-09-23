from travertino.size import at_least

from toga_winforms.libs import WinForms, TextAlignment

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = WinForms.Label()

    def set_alignment(self, value):
        self.native.TextAlign = TextAlignment(value)

    def set_text(self, value):
        self.native.Text = self.interface._text

    def rehint(self):
        # Width & height of a label is known and fixed.
        # self.native.Size = Size(0, 0)
        # print("REHINT label", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
