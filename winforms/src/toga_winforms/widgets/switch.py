from decimal import ROUND_UP

import System.Windows.Forms as WinForms
from travertino.size import at_least

from ..libs.wrapper import WeakrefCallable
from .base import Widget


class Switch(Widget):
    def create(self):
        self.native = WinForms.CheckBox()
        self.native.CheckedChanged += WeakrefCallable(self.winforms_checked_changed)

    def winforms_checked_changed(self, sender, event):
        self.interface.on_change()

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

    def get_value(self):
        return self.native.Checked

    def set_value(self, value):
        self.native.Checked = value

    def rehint(self):
        self.interface.intrinsic.width = self.scale_out(
            at_least(self.native.PreferredSize.Width), ROUND_UP
        )
        self.interface.intrinsic.height = self.scale_out(
            self.native.PreferredSize.Height, ROUND_UP
        )
