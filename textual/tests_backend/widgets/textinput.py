import pytest
from textual.widgets import Input as TextualInput

from toga.constants import LEFT

from .base import SimpleProbe


class TextInputProbe(SimpleProbe):
    native_class = TextualInput
    redo_available = False
    minimum_required_height = 80

    @property
    def value(self):
        return (
            self.native.placeholder if self.placeholder_visible else self.native.value
        )

    @property
    def value_hidden(self):
        return False

    @property
    def placeholder_visible(self):
        return self.native.value == ""

    @property
    def placeholder_hides_on_focus(self):
        return False

    @property
    def readonly(self):
        return self.native.disabled

    @property
    def text_align(self):
        # Text alignment is currently not implemented by the backend.
        return LEFT

    async def type_character(self, char):
        if self.widget.readonly:
            return
        if char == "\n":
            await self.native.action_submit()
        elif char == "<esc>":
            return
        else:
            self.native.insert_text_at_cursor(char)

    def set_cursor_at_end(self):
        self.native.action_end()

    def select_range(self, start, length):
        pytest.skip("Text selection is not implemented on Textual.")
