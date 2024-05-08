from decimal import ROUND_UP

import System.Windows.Forms as WinForms
from System.Drawing import SystemColors
from travertino.size import at_least

from toga.colors import TRANSPARENT
from toga_winforms.colors import toga_color_from_native_color

from ..libs.wrapper import WeakrefCallable
from .base import Widget


class Button(Widget):

    def create(self):
        self.native = WinForms.Button()
        self.native.AutoSizeMode = WinForms.AutoSizeMode.GrowAndShrink
        self.native.Click += WeakrefCallable(self.winforms_click)

        self._icon = None

    def winforms_click(self, sender, event):
        self.interface.on_press()

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

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        self._icon = icon
        if icon:
            self.native.Image = icon._impl.native.ToBitmap()
        else:
            self.native.Image = None

    def set_background_color(self, color):
        if color in {None, TRANSPARENT}:
            super().set_background_color(
                toga_color_from_native_color(SystemColors.Control)
            )
        else:
            super().set_background_color(color)

    def rehint(self):
        self.interface.intrinsic.width = self.scale_out(
            at_least(self.native.PreferredSize.Width), ROUND_UP
        )
        self.interface.intrinsic.height = self.scale_out(
            self.native.PreferredSize.Height, ROUND_UP
        )
