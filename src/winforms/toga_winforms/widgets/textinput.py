from toga_winforms.libs import WinForms, HorizontalTextAlignment, Color
from travertino.size import at_least

from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = WinForms.TextBox()
        self.native.Multiline = False
        self.native.TextChanged += self.winforms_onTextChanged
        self.native.Leave += self.winforms_onFocusLost

    def set_readonly(self, value):
        self.native.ReadOnly = value

    def set_placeholder(self, value):
        if self.interface.placeholder and not self.interface.value:
            self.native.Click += self.winforms_Click
            self.native.Text = self.interface.placeholder
            self.native.ForeColor = Color.FromName('GRAY')

    def get_value(self):
        return self.native.Text

    def set_value(self, value):
        if value:
            self.native.ForeColor = Color.FromName('BLACK')
            self.native.Text = value

    def set_alignment(self, value):
        self.native.TextAlign = HorizontalTextAlignment(value)

    def set_font(self, value):
        if value:
            self.native.Font = value._impl.native

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

    def winforms_Click(self, sender, event):
        self.native.SelectAll()
        if self.interface.placeholder and self.get_value() == self.interface.placeholder:
            self.native.Clear()
            self.native.ForeColor = Color.FromName('BLACK')

    def winforms_onFocusLost(self, sender, event):
        if not self.native.Text and self.interface.placeholder:
            self.set_placeholder(None)

