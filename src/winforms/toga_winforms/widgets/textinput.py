from toga_winforms.libs import WinForms
from travertino.size import at_least

from .base import Widget


class TogaTextInput(WinForms.TextBox):
    def __init__(self, interface):
        super().__init__()
        self.Multiline = False
        self.interface = interface

    def on_text_change(self, sender, event):
        if self.interface._on_change:
            self.interface.on_change(self.interface)


class TextInput(Widget):
    def create(self):
        self.native = TogaTextInput(self.interface)

    def set_readonly(self, value):
        self.native.ReadOnly = value

    def set_placeholder(self, value):
        self.native.Text = self.interface.placeholder

    def get_value(self):
        return self.native.Text

    def set_value(self, value):
        self.native.Text = value

    def set_alignment(self, value):
        print('Alignment: ', value)
        if value == 'center':
            win_value = WinForms.HorizontalAlignment.Center
        elif value == 'left':
            win_value = WinForms.HorizontalAlignment.Left
        elif value == 'right':
            win_value = WinForms.HorizontalAlignment.Right
        else:
            raise ValueError("Justify alignment is not supported in Windows; "
                             "choose left, right or center")
        self.native.TextAlign = win_value

    def set_font(self, value):
        self.interface.factory.not_implemented('TextInput.set_font()')

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def set_on_change(self, handler):
        self.native.TextChanged += self.native.on_text_change
