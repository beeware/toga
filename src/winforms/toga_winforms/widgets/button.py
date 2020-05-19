from travertino.size import at_least
from toga_winforms.libs import WinForms
from toga_winforms.colors import native_color
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

    def set_label(self, label):
        self.native.Text = self.interface.label
        self.rehint()

    def set_enabled(self, value):
        self.native.Enabled = self.interface._enabled

    def set_on_press(self, handler):
        # No special handling required
        pass

    def set_background_color(self, value):
        new_color = native_color(value)
        self.native.BackColor = new_color

    def rehint(self):
        # self.native.Size = Size(0, 0)
        # print("REHINT Button", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
