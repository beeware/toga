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

    def assert_text_align(self, expected):
        # Text alignment is currently not implemented by the backend.
        return

    def assert_vertical_text_align(self, expected):
        # Textual inputs don't expose configurable vertical text alignment.
        return

    async def type_character(self, char):
        if self.widget.readonly:
            return
        if char == "\n":
            self.widget.on_confirm()
        elif char == "<esc>":
            return
        else:
            self.native._reactive_value = f"{self.widget.value}{char}"
            self.widget._value_changed()

    def set_cursor_at_end(self):
        pytest.skip("Cursor positioning is not implemented on Textual.")

    def select_range(self, start, length):
        pytest.skip("Text selection is not implemented on Textual.")
