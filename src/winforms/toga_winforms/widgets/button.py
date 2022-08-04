from travertino.constants import TRANSPARENT
from travertino.size import at_least

from toga_winforms.colors import native_color
from toga_winforms.libs import WinForms

from .base import Widget


class Button(Widget):
    def create(self):
        self.native = WinForms.Button()
        self.native.Click += self.winforms_click
        self.set_enabled(self.interface._enabled)

    def winforms_click(self, sender, event):
        if self.container:
            if self.interface.on_press:
                self.interface.on_press(self.interface)

    def set_text(self, text):
        self.native.Text = self.interface.text
        self.rehint()

    def set_font(self, font):
        if font:
            self.native.Font = font.bind(self.interface.factory).native

    def set_enabled(self, value):
        self.native.Enabled = self.interface._enabled

    def set_on_press(self, handler):
        # No special handling required
        pass

    def set_color(self, value):
        if value:
            self.native.ForeColor = native_color(value)
        else:
            self.native.ForeColor = native_color(TRANSPARENT)

    def set_background_color(self, value):
        if value:
            self.native.BackColor = native_color(value)
        else:
            self.native.BackColor = native_color(TRANSPARENT)

    def rehint(self):
        # self.native.Size = Size(0, 0)
        # print("REHINT Button", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
