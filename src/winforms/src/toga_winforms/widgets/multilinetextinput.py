from travertino.size import at_least

from toga_winforms.libs import WinForms, SystemColors
from toga_winforms.colors import native_color

from .base import Widget


class MultilineTextInput(Widget):
    def create(self):
        # because https://stackoverflow.com/a/612234
        self.native = WinForms.RichTextBox()
        self.native.Multiline = True
        self.native.TextChanged += self.winforms_text_changed
        self.native.Enter += self.winforms_enter
        self.native.Leave += self.winforms_leave
        self._placeholder = None
        self._color = SystemColors.WindowText

    def winforms_enter(self, sender, event):
        if self._placeholder != '' and self.native.Text == self._placeholder:
            self.native.Text = ""
            self._update_text_color()

    def winforms_leave(self, sender, event):
        self._update_text()

    def set_font(self, font):
        if font:
            self.native.Font = font.bind(self.interface.factory).native

    def set_readonly(self, value):
        self.native.ReadOnly = self.interface.readonly

    def set_placeholder(self, value):
        self._placeholder = value
        self._update_text()

    def set_value(self, value):
        self.native.Text = value
        self._update_text()

    def get_value(self):
        if self._placeholder != '' and self.native.Text == self._placeholder:
            return ''
        else:
            return self.native.Text

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface.MIN_HEIGHT)

    def set_on_change(self, handler):
        pass

    def winforms_text_changed(self, sender, event):
        if self.interface.on_change:
            self.interface.on_change(self.interface)

    def _update_text(self):
        if self._placeholder != '' and self.native.Text == "":
            self.native.Text = self._placeholder
            self._update_placeholder_color()
        else:
            self._update_text_color()

    def _update_text_color(self):
        self.native.ForeColor = self._color

    def _update_placeholder_color(self):
        self.native.ForeColor = SystemColors.GrayText

    def set_color(self, color):
        if color:
            self._color = native_color(color)
            self._update_text_color()

    def set_background_color(self, value):
        if value:
            self.native.BackColor = native_color(value)
