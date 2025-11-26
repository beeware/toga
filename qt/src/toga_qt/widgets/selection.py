from contextlib import contextmanager

from PySide6.QtWidgets import QComboBox
from travertino.size import at_least

from .base import Widget


class Selection(Widget):
    def create(self):
        self.native = QComboBox()
        self.native.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.native.currentTextChanged.connect(self.qt_on_current_text_changed)
        self._send_notifications = True

    @contextmanager
    def suspend_notifications(self):
        self._send_notifications = False
        yield
        self._send_notifications = True

    def qt_on_current_text_changed(self, text):
        if self._send_notifications:
            self.interface.on_change()

    def clear(self):
        self.native.clear()

    def insert(self, index, item):
        self.native.insertItem(index, self.interface._title_for_item(item))

    def change(self, item):
        index = self.interface._items.index(item)
        with self.suspend_notifications():
            self.native.setItemText(index, self.interface._title_for_item(item))
        self.interface.refresh()

    def remove(self, index, item):
        current_index = self.native.currentIndex()
        with self.suspend_notifications():
            self.native.removeItem(index)
        if index == current_index:
            if self.native.count() > 0:
                self.native.setCurrentIndex(0)
            else:
                self.interface.on_change()

    def select_item(self, index, item):
        self.native.setCurrentIndex(index)

    def get_selected_index(self):
        index = self.native.currentIndex()
        return None if index == -1 else index

    def rehint(self):
        content_size = self.native.sizeHint()
        self.interface.intrinsic.width = at_least(content_size.width())
        self.interface.intrinsic.height = content_size.height()
