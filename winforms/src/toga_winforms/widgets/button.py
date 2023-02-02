from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga_winforms.colors import native_color
from toga_winforms.libs import SystemColors, WinForms

from .base import Widget


class Button(Widget):
    def create(self):
        self.native = WinForms.Button()
        self.native.AutoSizeMode = WinForms.AutoSizeMode.GrowAndShrink
        self.native.Click += self.winforms_click
        self.set_enabled(self.interface._enabled)

    def winforms_click(self, sender, event):
        if self.interface.on_press:
            self.interface.on_press(self.interface)

    def get_text(self):
        return self.native.Text

    def set_text(self, text):
        self.native.Text = text

    def set_font(self, font):
        self.native.Font = font._impl.native

    def set_background_color(self, color):
        if color is None or color == TRANSPARENT:
            self.native.BackColor = SystemColors.Control
        else:
            self.native.BackColor = native_color(color)

    def set_enabled(self, value):
        self.native.Enabled = self.interface._enabled

    def set_on_press(self, handler):
        # No special handling required
        pass

    def rehint(self):
        # self.native.Size = Size(0, 0)
        # print("REHINT Button", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
