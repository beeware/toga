from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class Button(Widget):
    def create(self):
        self.native = WinForms.Button()
        self.native.AutoSizeMode = WinForms.AutoSizeMode.GrowAndShrink
        self.native.Click += self.winforms_click

    def winforms_click(self, sender, event):
        self.interface.on_press(None)

    def get_text(self):
        value = self.native.Text
        # Normalize a standalone ZERO WIDTH SPACE to an empty string.
        if value == "\u200B":
            return ""
        return value

    def set_text(self, text):
        if text == "":
            # An empty label would cause the widget's height to collapse, so display a
            # Unicode ZERO WIDTH SPACE instead.
            text = "\u200B"
        self.native.Text = text

    def set_font(self, font):
        self.native.Font = font._impl.native

    def rehint(self):
        # self.native.Size = Size(0, 0)
        # print("REHINT Button", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
