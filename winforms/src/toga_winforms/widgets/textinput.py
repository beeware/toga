from ctypes import c_uint
from ctypes.wintypes import HWND, WPARAM

from travertino.size import at_least

from toga_winforms.colors import native_color
from toga_winforms.libs import HorizontalTextAlignment, WinForms, user32

from .base import Widget


class TextInput(Widget):
    _background_supports_alpha = False

    def create(self):
        self.native = WinForms.TextBox()
        self.native.Multiline = False
        self.native.TextChanged += self.winforms_text_changed
        self.native.KeyPress += self.winforms_key_press
        self.native.GotFocus += self.winforms_got_focus
        self.native.LostFocus += self.winforms_lost_focus

        self._placeholder = ""

        self.error_provider = WinForms.ErrorProvider()
        self.error_provider.SetIconAlignment(
            self.native, WinForms.ErrorIconAlignment.MiddleRight
        )
        self.error_provider.SetIconPadding(self.native, -20)
        self.error_provider.BlinkStyle = WinForms.ErrorBlinkStyle.NeverBlink

    def get_readonly(self):
        return self.native.ReadOnly

    def set_readonly(self, value):
        self.native.ReadOnly = value

    def get_placeholder(self):
        return self._placeholder

    def set_placeholder(self, value):
        self._placeholder = value
        # This solution is based on https://stackoverflow.com/questions/4902565.
        EM_SETCUEBANNER = c_uint(0x1501)
        # value 0 means placeholder is hidden as soon the input gets focus
        # value 1 means placeholder is hidden only after something is typed into input
        show_placeholder_on_focus = WPARAM(1)
        window_handle = HWND(self.native.Handle.ToInt32())
        user32.SendMessageW(
            window_handle,
            EM_SETCUEBANNER,
            show_placeholder_on_focus,
            self._placeholder,
        )

    def get_value(self):
        return self.native.Text

    def set_value(self, value):
        self.native.Text = value

    def set_alignment(self, value):
        self.native.TextAlign = HorizontalTextAlignment(value)

    def set_color(self, color):
        if color:
            self.native.ForeColor = native_color(color)
        else:
            self.native.ForeColor = self.native.DefaultForeColor

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def winforms_text_changed(self, sender, event):
        self.interface.on_change(self.interface)
        self.interface._validate()

    def winforms_key_press(self, sender, event):
        if ord(event.KeyChar) == int(WinForms.Keys.Enter):
            self.interface.on_confirm(self.interface)

    def winforms_got_focus(self, sender, event):
        self.interface.on_gain_focus(self.interface)

    def winforms_lost_focus(self, sender, event):
        self.interface.on_lose_focus(self.interface)

    def is_valid(self):
        return self.error_provider.GetError(self.native) == ""

    def clear_error(self):
        self.error_provider.SetError(self.native, "")

    def set_error(self, error_message):
        self.error_provider.SetError(self.native, error_message)
