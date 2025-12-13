import pytest
from PySide6.QtWidgets import QTextEdit

from .base import SimpleProbe
from .properties import toga_x_text_align, toga_y_text_align


class MultilineTextInputProbe(SimpleProbe):
    native_class = QTextEdit
    redo_available = True

    @property
    def value(self):
        return (
            self.native.placeholderText()
            if self.placeholder_visible
            else self.native.toPlainText()
        )

    @property
    def placeholder_visible(self):
        return not self.native.toPlainText()

    @property
    def value_hidden(self):
        pytest.xfail("Hiddem values not supported")

    @property
    def placeholder_hides_on_focus(self):
        return False

    @property
    def readonly(self):
        return self.native.isReadOnly()

    @property
    def document_width(self):
        return self.native.document().size().width()

    @property
    def document_height(self):
        margins = self.native.contentsMargins()
        return (
            self.native.document().size().height()
            + margins.top()
            + margins.bottom()
            + 1
        )

    @property
    def vertical_scroll_position(self):
        scrollbar = self.native.verticalScrollBar()
        return scrollbar.value()

    @property
    def horizontal_scroll_position(self):
        scrollbar = self.native.horizontalScrollBar()
        return scrollbar.value()

    async def wait_for_scroll_completion(self):
        pass

    @property
    def text_align(self):
        return toga_x_text_align(self.native.document().defaultTextOption().alignment())

    def assert_text_align(self, expected):
        assert self.text_align == expected

    def assert_vertical_text_align(self, expected):
        assert (
            toga_y_text_align(self.native.document().defaultTextOption().alignment())
            == expected
        )

    def set_cursor_at_end(self):
        cursor = self.native.textCursor()
        cursor.setPosition(len(self.native.toPlainText()))
        self.native.setTextCursor(cursor)

    def select_range(self, start, length):  # Start after the start-th character
        self.native.setSelection(start, length)

    def end_undo_block(self):
        self.native.editingFinished.emit()
