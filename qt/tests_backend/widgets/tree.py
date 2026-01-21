import asyncio
import warnings

import pytest
from PySide6.QtCore import QAbstractItemModel, QItemSelection, QItemSelectionModel, Qt
from PySide6.QtWidgets import QTreeView

from .base import SimpleProbe


class TreeProbe(SimpleProbe):
    native_class = QTreeView
    supports_keyboard_shortcuts = False
    supports_widgets = False

    def __init__(self, widget):
        super().__init__(widget)
        self.native_model: QAbstractItemModel = widget._impl.native_model
        assert isinstance(self.native_model, QAbstractItemModel)

    @property
    def has_focus(self):
        return self.native.hasFocus()

    async def expand_tree(self):
        self.native.expandAll()
        await asyncio.sleep(0.1)

    def is_expanded(self, node):
        self.native.isExpanded(self.native_model._get_index(node))

    def child_count(self, row_path=None):
        if row_path:
            row = self.native.get_model()[row_path]
            return len(list(row.iterchildren()))
        else:
            return len(self.native_tree.get_model())

    @property
    def column_count(self):
        return self.native_model.columnCount()

    @property
    def header_visible(self):
        return self.native.header().isVisible()

    @property
    def header_titles(self):
        return [
            self.native_model.headerData(i, Qt.Orientation.Horizontal)
            for i in range(self.native_model.columnCount())
        ]

    def column_width(self, col):
        return self.native.header().sectionSize(col)

    def assert_cell_content(self, row_path, col, value=None, icon=None, widget=None):
        if widget:
            pytest.skip("Qt doesn't support widgets in Trees")
        else:
            # Ignore warnings about widgets in Trees when we're just looking at
            # the cell data, as opposed to when the tree is rendering it.
            with warnings.catch_warnings(category=UserWarning):
                warnings.simplefilter("ignore")
                index = self.native_model.index(row_path, col)
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
