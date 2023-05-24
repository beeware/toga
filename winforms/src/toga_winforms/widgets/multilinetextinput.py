from travertino.size import at_least

from toga_winforms.colors import native_color
from toga_winforms.libs import HorizontalTextAlignment, SystemColors, WinForms

from .base import Widget


class MultilineTextInput(Widget):
    # Attempting to set a background color with any alpha value other than 1 raises
    # "System.ArgumentException: Control does not support transparent background colors"
    _background_supports_alpha = False

    def create(self):
        # TextBox doesn't support automatic scroll bar visibility, so we use RichTextBox
        # (https://stackoverflow.com/a/612234).
        self.native = WinForms.RichTextBox()
        self.native.Multiline = True
        self.native.TextChanged += self.winforms_text_changed

        # When moving focus with the tab key, the Enter/Leave event handlers see the
        # wrong value of ContainsFocus, so we use GotFocus/LostFocus instead.
        self.native.GotFocus += self.winforms_got_focus
        self.native.LostFocus += self.winforms_lost_focus

        # Dummy values used during initialization
        self._value = self._placeholder = ""
        self._suppress_on_change = True
        self.set_color(None)

    def winforms_got_focus(self, sender, event):
        self._update_text()

    def winforms_lost_focus(self, sender, event):
        self._update_text()

    def get_readonly(self):
        return self.native.ReadOnly

    def set_readonly(self, value):
        self.native.ReadOnly = value

    def get_placeholder(self):
        return self._placeholder

    def set_placeholder(self, value):
        self._placeholder = value
        self._update_text()

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        if value:
            self._suppress_on_change = False
        self._update_text()

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)

    def winforms_text_changed(self, sender, event):
        if not self._suppress_on_change:
            self._value = self.native.Text
            self.interface.on_change(None)

    def _update_text(self):
        show_placeholder = (not self.native.ContainsFocus) and (self._value == "")
        if show_placeholder:
            self._suppress_on_change = True
            self.native.Text = self._placeholder
            self.native.ForeColor = SystemColors.GrayText
        else:
            if self.native.Text != self._value:  # Avoid moving cursor on focus change
                self.native.Text = self._value
            self.native.ForeColor = self._color
            self._suppress_on_change = False

    def set_color(self, color):
        self._color = (
            SystemColors.WindowText if (color is None) else native_color(color)
        )
        self._update_text()

    def set_alignment(self, value):
        original_selection = (self.native.SelectionStart, self.native.SelectionLength)
        self.native.SelectAll()
        self.native.SelectionAlignment = HorizontalTextAlignment(value)
        self.native.SelectionStart, self.native.SelectionLength = original_selection

    def set_font(self, font):
        self.native.Font = font._impl.native

    def scroll_to_bottom(self):
        self.native.SelectionStart = len(self.native.Text)
        self.native.ScrollToCaret()

    def scroll_to_top(self):
        self.native.SelectionStart = 0
        self.native.ScrollToCaret()
