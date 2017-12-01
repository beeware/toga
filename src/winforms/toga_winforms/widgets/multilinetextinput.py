from toga_winforms.libs import *

from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        # because https://stackoverflow.com/a/612234
        self.native = WinForms.RichTextBox()
        self.native.Multiline = True

    def set_readonly(self, value):
        self.native.ReadOnly = value

    def set_placeholder(self, value):
        # self.native.cell.placeholderString = self._placeholder
        pass

    def set_value(self, value):
        self.native.Text = value

    def rehint(self):
        # Width must be > 100
        s = Size(self.native.Width, 0)
        self.interface.style.hint(
            height=self.native.GetPreferredSize(s).Height,
            min_width=100,
        )

