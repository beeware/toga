import warnings

import pytest
from PySide6.QtCore import QAbstractTableModel, QItemSelection, QItemSelectionModel, Qt
from PySide6.QtWidgets import QTableView

from .base import SimpleProbe


class TableProbe(SimpleProbe):
    native_class = QTableView
    supports_icons = 2  # All columns
    supports_keyboard_shortcuts = False
    supports_widgets = False

    def __init__(self, widget):
        super().__init__(widget)
        self.native_model: QAbstractTableModel = widget._impl.native_model
        assert isinstance(self.native_model, QAbstractTableModel)

    @property
    def has_focus(self):
        return self.native.hasFocus()

    @property
    def row_count(self):
        return self.native_model.rowCount()

    @property
    def column_count(self):
        return self.native_model.columnCount()

    @property
    def header_visible(self):
        return self.native.horizontalHeader().isVisible()

    @property
    def header_titles(self):
        return [
            self.native_model.headerData(i, Qt.Orientation.Horizontal)
            for i in range(self.native_model.columnCount())
        ]

    def column_width(self, col):
        return self.native.horizontalHeader().sectionSize(col)

    def assert_cell_content(self, row, col, value=None, icon=None, widget=None):
        if widget:
            pytest.skip("Qt doesn't support widgets in Tables")
        else:
            # Ignore warnings about widgets in Tables when we're just looking at
            # the cell data, as opposed to when the table is rendering it.
            with warnings.catch_warnings(category=UserWarning):
                warnings.simplefilter("ignore")
                index = self.native_model.index(row, col)
                if value:
                    assert value == self.native_model.data(
                        index,
                        Qt.ItemDataRole.DisplayRole,
                    )
                if icon:
                    assert (
                        icon._impl.native.cacheKey()
                        == self.native_model.data(
                            index,
                            Qt.ItemDataRole.DecorationRole,
                        ).cacheKey()
                    )

    @property
    def max_scroll_position(self):
        return self.native.verticalScrollBar().maximum() * self.native.rowHeight(0)

    @property
    def scroll_position(self):
        return self.native.verticalScrollBar().value() * self.native.rowHeight(0)

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    async def select_row(self, row, add=False):
        if add and self.widget.multiple_select:
            selection = QItemSelection()
            index = self.native_model.index(row, 0)
            selection.select(index, index)
            mode = (
                QItemSelectionModel.SelectionFlag.Toggle
                | QItemSelectionModel.SelectionFlag.Rows
            )
            self.native.selectionModel().select(selection, mode)
        else:
            self.native.selectRow(row)

    async def activate_row(self, row):
        await self.select_row(row)
        index = self.native_model.index(row, 0)
        self.native.activated.emit(index)

    async def select_first_row_keyboard(self):
        pytest.skip("test not implemented for this platform")
