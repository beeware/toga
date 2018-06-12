from toga_winforms.libs import WinForms
from travertino.size import at_least

from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        # because https://stackoverflow.com/a/612234
        self.native = WinForms.RichTextBox()
        self.native.Multiline = True

    def set_readonly(self, value):
        self.native.ReadOnly = self.interface.readonly

    def set_placeholder(self, value):
        # self.native.cell.placeholderString = self._placeholder
        self.interface.factory.not_implemented('MultilineTextInput.set_placeholder()')

    def set_value(self, value):
        self.native.Text = value

    def get_value(self):
        return self.native.Text

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)
