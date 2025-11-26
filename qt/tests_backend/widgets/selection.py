from PySide6.QtWidgets import QComboBox

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
