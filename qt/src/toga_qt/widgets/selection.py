from contextlib import contextmanager

from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QComboBox
from travertino.size import at_least

from .base import Widget


class Selection(Widget):
    def create(self):
        self.native = QComboBox()
        self.native.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.native.currentIndexChanged.connect(self.qt_on_current_index_changed)
        self._item_id_count = 0
        self._last_selected_item_id = 0

        self._send_notifications = True
        # QComboBox uses default background and foreground roles to draw the dropdown,
        # so we need to explicitly override.
        self._background_color_role = QPalette.ColorRole.Button
        self._foreground_color_role = QPalette.ColorRole.ButtonText

    @contextmanager
    def suspend_notifications(self):
        self._send_notifications = False
        yield
        self._send_notifications = True

    def qt_on_current_index_changed(self):
        # Insertions can change the current index, but we should only keep track
        # of things if the current change is an actual change in the *item*, not
        # just the index.
        if self._last_selected_item_id != self.native.currentData():
            if self._send_notifications:
                self.interface.on_change()
            self._last_selected_item_id = self.native.currentData()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def clear(self):
        import warnings

        warnings.warn(
            "The clear() method is deprecated. Use source_clear() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_clear()

    def source_clear(self):
        self.native.clear()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def insert(self, index, item):
        import warnings

        warnings.warn(
            "The insert() method is deprecated. Use source_insert() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_insert(index=index, item=item)

    def source_insert(self, *, index, item):
        self._item_id_count += 1
        self.native.insertItem(
            index, self.interface._title_for_item(item), self._item_id_count
        )

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def change(self, item):
        import warnings

        warnings.warn(
            "The change() method is deprecated. Use source_change() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_change(item=item)

    def source_change(self, *, item):
        index = self.interface._items.index(item)
        self.native.setItemText(index, self.interface._title_for_item(item))
        self.interface.refresh()

    # Alias for backwards compatibility:
    # March 2026: In 0.5.3 and earlier, notification methods
    # didn't start with 'source_'
    def remove(self, index, item):
        import warnings

        warnings.warn(
            "The remove() method is deprecated. Use source_remove() instead.",
            DeprecationWarning,
            stacklevel=1,
        )
        self.source_remove(index=index, item=item)

    def source_remove(self, *, index, item):
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
