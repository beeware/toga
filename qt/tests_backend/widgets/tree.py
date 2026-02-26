import asyncio
import warnings

import pytest
from PySide6.QtCore import (
    QAbstractItemModel,
    QItemSelection,
    QItemSelectionModel,
    QModelIndex,
    Qt,
)
from PySide6.QtWidgets import QTreeView

from .base import SimpleProbe


class TreeProbe(SimpleProbe):
    native_class = QTreeView
    supports_keyboard_shortcuts = False
    supports_widgets = False
    selection_cleared_on_insert_delete = True
    collapse_on_insert_delete = True

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
        index = self.native_model._get_index(node)
        return self.native.isExpanded(index)

    def _get_index_from_path(self, row_path=None, col=0):
        index = QModelIndex()
        if row_path:
            columns = [0] * len(row_path)
            columns[-1] = col
            for row, col in zip(row_path, columns, strict=True):
                index = self.native_model.index(row, col, index)
        return index

    def child_count(self, row_path=None):
        index = self._get_index_from_path(row_path)
        return self.native_model.rowCount(index)

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
                index = self._get_index_from_path(row_path, col)
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

    async def select_row(self, row_path, add=False):
        index = self._get_index_from_path(row_path)
        selection = QItemSelection()
        selection.select(index, index)
        if add and self.widget.multiple_select:
            mode = (
                QItemSelectionModel.SelectionFlag.Toggle
                | QItemSelectionModel.SelectionFlag.Rows
            )
            self.native.selectionModel().select(selection, mode)
        else:
            self.native.selectionModel().select(
                selection,
                QItemSelectionModel.SelectionFlag.ClearAndSelect
                | QItemSelectionModel.SelectionFlag.Rows,
            )

    async def activate_row(self, row_path):
        await self.select_row(row_path)
        index = self._get_index_from_path(row_path)
        self.native.activated.emit(index)

    async def select_first_row_keyboard(self):
        pytest.skip("test not implemented for this platform")
