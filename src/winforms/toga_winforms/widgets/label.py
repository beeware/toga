from toga.constants import LEFT_ALIGNED

from toga_winforms.libs import *

from .base import Widget


class Label(Widget):
    def create(self):
        self.native = WinForms.Label()

    def set_alignment(self, value):
        # self.native.setAlignment_(NSTextAlignment(value))
        pass

    def set_text(self, value):
        self.native.Text = value

    def rehint(self):
        # Width & height of a label is known and fixed.
        # self.native.Size = Size(0, 0)
        # print("REHINT label", self, self.native.PreferredSize)
        self.interface.style.hint(
            height=self.native.PreferredSize.Height,
            width=self.native.PreferredSize.Width,
        )
