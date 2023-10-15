import ctypes
from ctypes import c_uint
from ctypes.wintypes import HWND, LPARAM

import pytest
from System.Windows.Forms import TextBox

from .base import SimpleProbe
from .properties import toga_xalignment


class TextInputProbe(SimpleProbe):
    native_class = TextBox
    background_supports_alpha = False
    fixed_height = 23

    @property
    def value(self):
        return self._placeholder if self.placeholder_visible else self.native.Text

    @property
    def value_hidden(self):
        return self.native.UseSystemPasswordChar

    @property
    def _placeholder(self):
        buffer = ctypes.create_unicode_buffer(1024)
        result = ctypes.windll.user32.SendMessageW(
            HWND(self.native.Handle.ToInt32()),
            c_uint(0x1502),  # EM_GETCUEBANNER
            buffer,
            LPARAM(ctypes.sizeof(buffer)),
        )
        if not result:
            raise RuntimeError("EM_GETCUEBANNER failed")
        return buffer.value

    @property
    def placeholder_visible(self):
        return not self.native.Text

    @property
    def placeholder_hides_on_focus(self):
        False

    @property
    def readonly(self):
        return self.native.ReadOnly

    @property
    def alignment(self):
        return toga_xalignment(self.native.TextAlign)

    def assert_vertical_alignment(self, expected):
        # Vertical alignment isn't configurable in this native widget.
        pass

    def set_cursor_at_end(self):
        pytest.skip("Cursor positioning not supported on this platform")
