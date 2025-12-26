from PySide6.QtWidgets import QFrame

from .base import SimpleProbe


class DividerProbe(SimpleProbe):
    native_class = QFrame
