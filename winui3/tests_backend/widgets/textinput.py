from win32more.Microsoft.UI.Xaml.Controls import TextBox
from win32more.Windows.Win32.UI.Input.KeyboardAndMouse import VK_CONTROL

from .base import SimpleProbe
from .properties import toga_x_text_align


class TextInputProbe(SimpleProbe):
    native_class = TextBox
    redo_available = True

    @property
    def placeholder_visible(self):
        return not self.native.Text

    @property
    def value(self):
        return (
            self.native.PlaceholderText
            if self.placeholder_visible
            else self.native.Text
        )

    @property
    def value_hidden(self):
        return False

    @property
    def placeholder_hides_on_focus(self):
        return False

    @property
    def readonly(self):
        return self.native.IsReadOnly

    def assert_text_align(self, expected):
        assert expected == toga_x_text_align(self.native.TextAlignment)

    def assert_vertical_text_align(self, expected):
        # Vertical text alignment is not configurable for TextBlock.
        pass

    def set_cursor_at_end(self):
        self.native.SelectionStart = len(self.native.Text)
        self.native.SelectionLength = 0

    async def undo(self):
        await self._send_key(key_code=VK_CONTROL, up=False)
        await self.type_character("z")
        await self._send_key(key_code=VK_CONTROL, down=False)

    async def redo(self):
        await self._send_key(key_code=VK_CONTROL, up=False)
        await self.type_character("y")
        await self._send_key(key_code=VK_CONTROL, down=False)
