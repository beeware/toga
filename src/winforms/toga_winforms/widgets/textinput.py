from ctypes import c_uint
from ctypes.wintypes import HWND, WPARAM

from travertino.size import at_least

from toga_winforms.libs import HorizontalTextAlignment, WinForms, user32

from .base import Widget


class TextInput(Widget):
    def create(self):
        self.native = WinForms.TextBox()
        self.native.Multiline = False
        self.native.Click += self.winforms_Click
        self.native.TextChanged += self.winforms_onTextChanged

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

    def set_font(self, value):
        if value:
            self.native.Font = value._impl.native

    def rehint(self):
        # Height of a text input is known and fixed.
        # Width must be > 100
        # print("REHINT TextInput", self, self.native.PreferredSize)
        self.interface.intrinsic.width = at_least(self.interface.MIN_WIDTH)
        self.interface.intrinsic.height = self.native.PreferredSize.Height

    def set_on_change(self, handler):
        pass

    def winforms_onTextChanged(self, sender, event):
        if self.interface._on_change:
            self.interface.on_change(self.interface)

    def winforms_Click(self, sender, event):
        self.native.SelectAll()
