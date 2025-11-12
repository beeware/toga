from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton
from travertino.size import at_least

from .base import Widget


class Button(Widget):
    def create(self):
        self.native = QPushButton()
        self.native.setIconSize(QSize(32, 32))

        self.native.clicked.connect(self.clicked)

        self._icon = None

    def clicked(self):
        self.interface.on_press()

    def get_text(self):
        return str(self.native.text())

    def set_text(self, text):
        self.native.setText(text)

    def get_icon(self):
        return self._icon

    def set_icon(self, icon):
        if icon is not None:
            self.native.setIcon(icon._impl.native)
        else:
            self.native.setIcon(QIcon())
        # Qt does not round-trip the same instance of the icon back.
        self._icon = icon

    def rehint(self):
        width = self.native.sizeHint().width()
        height = self.native.sizeHint().height()

        self.interface.intrinsic.width = at_least(width)
        # Height of a button is known.
        self.interface.intrinsic.height = height

    def set_color(self, color):
        super().set_color(color)

    def set_background_color(self, color):
        if color == "transparent":
            color = None
        super().set_background_color(color)
