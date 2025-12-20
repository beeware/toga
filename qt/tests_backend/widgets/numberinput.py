from PySide6.QtWidgets import QDoubleSpinBox

from .base import SimpleProbe
from .properties import toga_x_text_align, toga_y_text_align


class NumberInputProbe(SimpleProbe):
    native_class = QDoubleSpinBox
    allows_invalid_value = False
    allows_empty_value = True
    allows_extra_digits = False
    allows_unchanged_updates = False

    def clear_input(self):
        self.native.clear()

    @property
    def value(self):
        return self.native.text()

    async def increment(self):
        self.native.stepBy(1)

    async def decrement(self):
        self.native.stepBy(-1)

    @property
    def text_align(self):
        return toga_x_text_align(self.native.alignment())

    def assert_text_align(self, expected):
        assert self.text_align == expected

    def assert_vertical_text_align(self, expected):
        assert toga_y_text_align(self.native.alignment()) == expected

    @property
    def readonly(self):
        return self.native.isReadOnly()

    def set_cursor_at_end(self):
        self.native.lineEdit().setCursorPosition(len(self.native.text()))
