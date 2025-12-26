from PySide6.QtWidgets import QFrame
from travertino.size import at_least

from toga.constants import Direction

from .base import Widget


class Divider(Widget):
    def create(self):
        self.native = QFrame()
        self.native.setFrameShape(QFrame.Shape.HLine)
        self.native.setFrameShadow(QFrame.Shadow.Sunken)

    def get_direction(self):
        match self.native.frameShape():
            case QFrame.Shape.HLine:
                return Direction.HORIZONTAL
            case QFrame.Shape.VLine:
                return Direction.VERTICAL
            case _:  # pragma: no cover
                raise ValueError(f"Unsupported QFrame shape {self.native.frameShape()}")

    def set_direction(self, value):
        if value == Direction.VERTICAL:
            self.native.setFrameShape(QFrame.Shape.VLine)
        else:
            self.native.setFrameShape(QFrame.Shape.HLine)

    def rehint(self):
        size = self.native.sizeHint()

        if self.get_direction() == self.interface.VERTICAL:
            self.interface.intrinsic.width = size.width()
            self.interface.intrinsic.height = at_least(size.height())
        else:
            self.interface.intrinsic.width = at_least(size.width())
            self.interface.intrinsic.height = size.height()
