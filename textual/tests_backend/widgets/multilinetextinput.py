import pytest
from textual.widgets import TextArea as TextualTextArea

from toga.constants import LEFT

from .base import SimpleProbe


class MultilineTextInputProbe(SimpleProbe):
    native_class = TextualTextArea
    redo_available = True
    supports_simulate_mouse_wheel = False
    minimum_required_height = 80

    @property
    def value(self):
        return (
            self.impl.get_placeholder()
            if self.placeholder_visible
            else self.native.text
        )

    @property
    def value_hidden(self):
        return False

    @property
    def placeholder_visible(self):
        return self.impl.placeholder_visible

    @property
    def placeholder_hides_on_focus(self):
        return True

    @property
    def readonly(self):
        return self.native.read_only

    @property
    def document_width(self):
        return self.width + self.impl.scale_out_horizontal(self.native.max_scroll_x)

    @property
    def document_height(self):
        return self.height + self.impl.scale_out_vertical(self.native.max_scroll_y)

    @property
    def vertical_scroll_position(self):
        return self.impl.scale_out_vertical(self.native.scroll_y)

    async def wait_for_scroll_completion(self):
        await self.redraw("Waiting for scroll completion")

    @property
    def text_align(self):
        # Text alignment is currently not implemented by the backend.
        return LEFT

    def assert_text_align(self, expected):
        # Text alignment is currently not implemented by the backend.
        return

    def assert_vertical_text_align(self, expected):
        # Textual TextArea doesn't expose configurable vertical text alignment.
        return

    async def type_character(self, char):
        if self.widget.readonly or char == "<esc>":
            return

        if self.placeholder_visible:
            self.impl.on_focus()

        if char == "<backspace>":
            self.native.action_delete_left()
        else:
            self.native.insert(char)

    async def undo(self):
        self.native.undo()

    async def redo(self):
        self.native.redo()

    def set_cursor_at_end(self):
        if self.placeholder_visible:
            self.impl.on_focus()
        self.native.move_cursor(self.native.document.end)

    def select_range(self, start, length):
        pytest.skip("Text selection is not implemented on Textual.")
