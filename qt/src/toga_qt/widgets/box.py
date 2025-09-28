from PySide6.QtWidgets import QWidget
from travertino.size import at_least

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = QWidget()
        self.native.setAutoFillBackground(True)

    def rehint(self):
        self.interface.intrinsic.width = at_least(0)
        self.interface.intrinsic.height = at_least(0)
