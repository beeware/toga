from ..libs import *
from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = WinForms.TextBox()
        self.native.Multiline = False

    def set_readonly(self, value):
        self.native.ReadOnly = value

    def set_placeholder(self, value):
        # self.native.cell.placeholderString = self._placeholder
        pass

    def get_value(self):
        return self.native.Text

    def set_value(self, value):
        self.native.Text = value

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self.native.PreferredSize)
        self.interface.style.hint(
            height=self.native.PreferredSize.Height,
            min_width=100,
        )
