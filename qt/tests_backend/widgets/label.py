from PySide6.QtWidgets import QLabel

from .base import SimpleProbe
from .properties import toga_x_text_align, toga_y_text_align


class LabelProbe(SimpleProbe):
    native_class = QLabel

    def __init__(self, widget):
        super().__init__(widget)
        assert self.native.autoFillBackground()

    @property
    def text(self):
        return self.native.text()

    @property
    def text_align(self):
        return toga_x_text_align(self.native.alignment())

    @property
    def vertical_text_align(self):
        return

    def assert_vertical_text_align(self, expected):
        assert toga_y_text_align(self.native.alignment()) == expected
