from PySide6.QtWidgets import QWidget

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = QWidget
    invalid_size_while_hidden = False

    def __init__(self, widget):
        super().__init__(widget)
        assert self.native.autoFillBackground()
