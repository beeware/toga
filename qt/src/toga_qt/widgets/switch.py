from PySide6.QtWidgets import QCheckBox
from travertino.size import at_least

from .base import Widget


class Switch(Widget):
    def create(self):
        self.native = QCheckBox()
        self.native.setText("\u200b")
        self.native.setMinimumHeight(self.native.sizeHint().height())
        self.native.setText("")
        self.native.checkStateChanged.connect(self.qt_on_change)

    def qt_on_change(self, state):
        self.interface.on_change()

    def get_text(self):
        return self.native.text()

    def set_text(self, text):
        self.native.setText(text)
        self.refresh()

    def get_value(self):
        return self.native.isChecked()

    def set_value(self, value):
        self.native.setChecked(value)

    def rehint(self):
        content_size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(content_size.width())
        self.interface.intrinsic.height = content_size.height()

    def focus(self):
        # We can actually focus in Qt, however, keep it consistent with the GTK backend.
        pass
