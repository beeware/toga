from toga_winforms.libs import WinForms, HorizontalTextAlignment, Color
from travertino.size import at_least

from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = WinForms.TextBox()
        self.native.Multiline = False
        self.native.TextChanged += self.winforms_onTextChanged

    def set_readonly(self, value):
        self.native.ReadOnly = value

    def set_placeholder(self, value):
        #TODO Placeholder should reappear when the user leaves the field blank
        if self.interface.placeholder:
            self.native.Click += self.winforms_Click
            self.native.KeyDown += self.winforms_KeyDown
            self.native.Text = self.interface.placeholder
            self.native.ForeColor = Color.FromName('GRAY')

    def get_value(self):
        return self.native.Text

    def set_value(self, value):
        self.native.Text = value

    def set_alignment(self, value):
        self.native.TextAlign = HorizontalTextAlignment(value)

    def set_font(self, value):
        self.interface.factory.not_implemented('TextInput.set_font()')

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def set_on_change(self, handler):
        pass

    def winforms_onTextChanged(self, sender, event):
         if self.interface._on_change:
             self.interface.on_change(self.interface)

    def winforms_KeyDown(self, sender, event):
        self.native.Text = ""
        self.native.ForeColor = Color.FromName('BLACK')
        self.native.KeyDown -= self.winforms_KeyDown

    def winforms_Click(self, sender, event):
        self.native.SelectAll()
        self.native.Click -= self.winforms_Click
