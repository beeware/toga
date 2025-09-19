from PySide6.QtWidgets import QWidget

from .base import SimpleProbe


class BoxProbe(SimpleProbe):
    native_class = QWidget
