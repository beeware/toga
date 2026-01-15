from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QComboBox
from toga_qt.colors import toga_color

from .base import SimpleProbe


class SelectionProbe(SimpleProbe):
    native_class = QComboBox

    def assert_resizes_on_content_change(self):
        pass

    @property
    def titles(self):
        titles = [self.native.itemText(index) for index in range(self.native.count())]
        return titles

    @property
    def selected_title(self):
        if self.native.currentIndex() < 0:
            return None
        else:
            return self.native.currentText()

    async def select_item(self):
        self.native.setCurrentIndex(1)

    @property
    def color(self):
        return toga_color(self.native.palette().color(QPalette.ColorRole.ButtonText))

    @property
    def background_color(self):
        return toga_color(self.native.palette().color(QPalette.ColorRole.Button))
