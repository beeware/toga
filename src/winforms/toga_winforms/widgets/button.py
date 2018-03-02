from travertino.size import at_least
from toga_winforms.libs import WinForms
from toga_winforms import color
from .base import Widget


class TogaButton(WinForms.Button):
    def __init__(self, interface):
        super().__init__()
        self.interface = interface
        self.Click += self.on_click

    def on_click(self, sender, event):
        if self.interface.on_press:
            self.interface.on_press(self.interface)


class Button(Widget):
    def create(self):
        self.native = TogaButton(self.interface)
        self.set_enabled(self.interface._enabled)

    def set_label(self, label):
        self.native.Text = self.interface.label
        self.rehint()

    def set_enabled(self, value):
        self.native.Enabled = self.interface._enabled

    def set_on_press(self, handler):
        # No special handling required
        pass

    def set_background_color(self, value):
        if value is not None:
            new_color = color.native_color(value)
            self.native.BackColor = new_color

    def rehint(self):
        # self.native.Size = Size(0, 0)
        # print("REHINT Button", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
