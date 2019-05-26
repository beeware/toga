from toga_winforms.libs import WinForms
from travertino.size import at_least

from .base import Widget


class TogaSwitch(WinForms.CheckBox):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.CheckedChanged += self.on_toggle

    def on_toggle(self, sender, event):
        if self.interface.on_toggle:
            self.interface.on_toggle(self.interface)


class Switch(Widget):
    def create(self):
        self.native = TogaSwitch(self.interface)

    def set_label(self, label):
        self.native.Text = self.interface.label

    def set_is_on(self, value):
        if value is True:
            self.native.Checked = True
        elif value is False:
            self.native.Checked = False

    def get_is_on(self):
        return self.native.Checked

    def set_on_toggle(self, handler):
        pass

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
