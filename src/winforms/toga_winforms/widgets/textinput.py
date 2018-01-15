from travertino.size import at_least

from toga_winforms.libs import *

from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = WinForms.TextBox()
        self.native.Multiline = False

    def set_readonly(self, value):
        self.native.ReadOnly = value

    def set_placeholder(self, value):
        # self.native.cell.placeholderString = self._placeholder
        raise NotImplementedError()

    def get_value(self):
        return self.native.Text

    def set_value(self, value):
        self.native.Text = self.interface.value

    def set_alignment(self, value):
        raise NotImplementedError()

    def set_font(self, value):
        raise NotImplementedError()

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def set_on_change(self, handler):
        pass
