from PySide6.QtCore import QSize
from PySide6.QtWidgets import QPushButton

from .base import SimpleProbe


class ButtonProbe(SimpleProbe):
    native_class = QPushButton

    @property
    def text(self):
        # Normalize the zero width space to the empty string.
        if self.native.text() == "\u200b":
            return ""
        return self.native.text()

    def assert_no_icon(self):
        assert self.native.icon().isNull()

    def assert_icon_size(self):
        assert self.native.iconSize() == QSize(32, 32)
