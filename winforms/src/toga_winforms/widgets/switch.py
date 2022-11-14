from travertino.size import at_least

from toga_winforms.libs import WinForms

from .base import Widget


class Switch(Widget):
    def create(self):
        self.native = WinForms.CheckBox()
        self.native.CheckedChanged += self.winforms_checked_changed

    def winforms_checked_changed(self, sender, event):
        if self.container:
            if self.interface.on_change:
                self.interface.on_change(self.interface)

    def set_text(self, text):
        self.native.Text = self.interface.text

    def set_value(self, value):
        if value is True:
            self.native.Checked = True
        elif value is False:
            self.native.Checked = False

    def get_value(self):
        return self.native.Checked

    def set_on_change(self, handler):
        pass

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.native.PreferredSize.Width)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def set_font(self, font):
        if font:
            self.native.Font = font._impl.native
