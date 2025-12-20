from PySide6.QtWidgets import QCheckBox

from .base import SimpleProbe


class SwitchProbe(SimpleProbe):
    native_class = QCheckBox

    @property
    def text(self):
        return self.native.text()
