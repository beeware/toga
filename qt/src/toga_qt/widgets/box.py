from PySide6.QtWidgets import QWidget
from travertino.constants import TRANSPARENT
from travertino.size import at_least

from .base import Widget


class Box(Widget):
    def create(self):
        self.native = QWidget()
        self.native.setAutoFillBackground(True)
        # Background is not autofilled by default; but since we're
        # enabling it here, let the default color be transparent
        # so it autofills nothing by default.
        self._default_background_color = TRANSPARENT

    def rehint(self):
        self.interface.intrinsic.width = at_least(0)
        self.interface.intrinsic.height = at_least(0)
