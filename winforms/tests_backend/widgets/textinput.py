import ctypes
from ctypes import c_uint
from ctypes.wintypes import HWND, LPARAM

from System.Windows.Forms import TextBox

from .base import SimpleProbe
from .properties import toga_x_text_align


class TextInputProbe(SimpleProbe):
    native_class = TextBox
    fixed_height = 23
    redo_available = True

    @property
    def value(self):
        return self._placeholder if self.placeholder_visible else self.native.Text

    @property
    def value_hidden(self):
        return self.native.UseSystemPasswordChar

    @property
    def _placeholder(self):
        buffer = ctypes.create_unicode_buffer(1024)
        buffer_address = ctypes.cast(buffer, ctypes.c_void_p).value
        result = ctypes.windll.user32.SendMessageW(
            HWND(self.native.Handle.ToInt32()),
            c_uint(0x1502),  # EM_GETCUEBANNER
            buffer_address,
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
        return False

    @property
    def readonly(self):
        return self.native.ReadOnly

    @property
    def text_align(self):
        return toga_x_text_align(self.native.TextAlign)

    def assert_vertical_text_align(self, expected):
        # Vertical text alignment isn't configurable in this native widget.
        pass

    def set_cursor_at_end(self):
        self.native.SelectionStart = len(self.native.Text)
        self.native.SelectionLength = 0
