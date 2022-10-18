from ctypes import c_uint
from ctypes.wintypes import HWND, WPARAM

from travertino.size import at_least
from travertino.constants import TRANSPARENT

from toga_winforms.colors import native_color
from toga_winforms.libs import HorizontalTextAlignment, WinForms, user32

from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = WinForms.TextBox()
        self.native.Multiline = False
        self.native.DoubleClick += self.winforms_double_click
        self.native.TextChanged += self.winforms_text_changed
        self.native.Validated += self.winforms_validated
        self.native.GotFocus += self.winforms_got_focus
        self.native.LostFocus += self.winforms_lost_focus

        self.error_provider = WinForms.ErrorProvider()
        self.error_provider.SetIconAlignment(
            self.native, WinForms.ErrorIconAlignment.MiddleRight
        )
        self.error_provider.SetIconPadding(self.native, -20)
        self.error_provider.BlinkStyle = WinForms.ErrorBlinkStyle.NeverBlink

    def set_readonly(self, value):
        self.native.ReadOnly = value

    def set_placeholder(self, value):
        # This solution is based on https://stackoverflow.com/questions/4902565/watermark-textbox-in-winforms
        if self.interface.placeholder:
            # Message Code for setting Cue Banner (Placeholder)
            EM_SETCUEBANNER = c_uint(0x1501)
            # value 0 means placeholder is hidden as soon the input gets focus
            # value 1 means placeholder is hidden only after something is typed into input
            show_placeholder_on_focus = WPARAM(1)
            window_handle = HWND(self.native.Handle.ToInt32())
            user32.SendMessageW(window_handle, EM_SETCUEBANNER, show_placeholder_on_focus, self.interface.placeholder)

    def get_value(self):
        return self.native.Text

    def set_value(self, value):
        self.native.Text = value

    def set_alignment(self, value):
        self.native.TextAlign = HorizontalTextAlignment(value)

    def set_font(self, font):
        if font:
            self.native.Font = font.bind(self.interface.factory).native

    def set_color(self, color):
        if color:
            self.native.ForeColor = native_color(color)
        else:
            self.native.ForeColor = self.native.DefaultForeColor

    def set_background_color(self, value):
        if value:
            self.native.BackColor = native_color(value)
        else:
            self.native.BackColor = native_color(TRANSPARENT)

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def set_on_change(self, handler):
        # No special handling required
        pass

    def set_on_gain_focus(self, handler):
        # No special handling required
        pass

    def set_on_lose_focus(self, handler):
        # No special handling required
        pass

    def winforms_text_changed(self, sender, event):
        if self.interface._on_change:
            self.interface.on_change(self.interface)

    def winforms_validated(self, sender, event):
        self.interface.validate()

    def winforms_got_focus(self, sender, event):
        if self.container and self.interface.on_gain_focus:
            self.interface.on_gain_focus(self.interface)

    def winforms_lost_focus(self, sender, event):
        if self.container and self.interface.on_lose_focus:
            self.interface.on_lose_focus(self.interface)

    def is_valid(self):
        return self.error_provider.GetError(self.native) == ""

    def clear_error(self):
        self.error_provider.SetError(self.native, "")

    def set_error(self, error_message):
        self.error_provider.SetError(self.native, error_message)

    def winforms_double_click(self, sender, event):
        self.native.SelectAll()
