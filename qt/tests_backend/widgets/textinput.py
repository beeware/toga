from PySide6.QtWidgets import QLineEdit

from .base import SimpleProbe
from .properties import toga_x_text_align, toga_y_text_align


class TextInputProbe(SimpleProbe):
    native_class = QLineEdit
    redo_available = True

    @property
    def value(self):
        return (
            self.native.placeholderText()
            if self.placeholder_visible
            else self.native.text()
        )

    @property
    def placeholder_visible(self):
        return not self.native.text()

    @property
    def value_hidden(self):
        return self.native.echoMode() == QLineEdit.Password

    @property
    def placeholder_hides_on_focus(self):
        return False

    @property
    def readonly(self):
        return self.native.isReadOnly()

    @property
    def text_align(self):
        return toga_x_text_align(self.native.alignment())

    def assert_text_align(self, expected):
        assert self.text_align == expected

    def assert_vertical_text_align(self, expected):
        assert toga_y_text_align(self.native.alignment()) == expected

    def set_cursor_at_end(self):
        self.native.setCursorPosition(len(self.native.text()))

    def select_range(self, start, length):  # Start after the start-th character
        self.native.setSelection(start, length)

    def end_undo_block(self):
        self.native.editingFinished.emit()
