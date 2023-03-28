from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class Switch(Widget):
    def create(self):
        self.native = WinForms.CheckBox()
        self.native.CheckedChanged += self.winforms_checked_changed

    def winforms_checked_changed(self, sender, event):
        if self.interface.on_change:
            self.interface.on_change(self.interface)

    def get_text(self):
        return self.native.Text

    def set_text(self, text):
        self.native.Text = text

    def get_value(self):
        return self.native.Checked

    def set_value(self, value):
        old_value = self.native.Checked
        self.native.Checked = value

        if self.interface.on_change and old_value != value:
            self.interface.on_change(self.interface)

    def set_on_change(self, handler):
        pass

    def set_font(self, font):
        self.native.Font = font._impl.native

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height
