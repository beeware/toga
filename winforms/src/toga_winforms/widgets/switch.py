import System.Windows.Forms as WinForms
from travertino.size import at_least

from ..libs.wrapper import WeakrefCallable
from .base import Widget


class Switch(Widget):
    def create(self):
        self.native = WinForms.CheckBox()
        self.native.CheckedChanged += WeakrefCallable(self.winforms_checked_changed)

    def winforms_checked_changed(self, sender, event):
        self.interface.on_change(None)

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
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
