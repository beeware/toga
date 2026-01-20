import logging
import warnings
from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtWidgets import QHeaderView, QTableView
from travertino.size import at_least

from toga.sources import ListSource

from .base import Widget

logger = logging.getLogger(__name__)

# convenience root/invalid index object
INVALID_INDEX = QModelIndex()


class TableSourceModel(QAbstractTableModel):
    _source: ListSource | None
    headings: list[str]

    def __init__(self, source, columns, missing_value, **kwargs):
        super().__init__(**kwargs)
        self._source = source
        self._columns = columns
        self._missing_value = missing_value

    def set_source(self, source):
        self.beginResetModel()
        self._source = source
        self.endResetModel()

    def reset_source(self):
        self.beginResetModel()
        # Nothing to do, clear has already happened
        self.endResetModel()

    def insert_item(self, index):
        self.beginInsertRows(QModelIndex(), index, index)
        # Nothing to do, insertion has already happened
        self.endInsertRows()

    def remove_item(self, index):
        self.beginRemoveRows(QModelIndex(), index, index)
        # Nothing to do, removal has already happened
        self.endRemoveRows()

    def item_changed(self, item):
        if self._source is None:
            return  # pragma: no cover
        self.dataChanged.emit(
            self.index(self._source.index(item), 0),
            self.index(self._source.index(item), len(self._columns)),
        )

    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = INVALID_INDEX,
    ) -> int:
        # this could call out to end-user data sources, so could fail.
        try:
            if self._source is not None:
                return len(self._source)
        except Exception:  # pragma: no cover
            logger.exception("Could not get data length.")
        return 0  # pragma: no cover

    def columnCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = INVALID_INDEX,
    ) -> int:
        # this could call out to end-user data sources, so could fail.
        try:
            if self._columns is not None:
                return len(self._columns)
        except Exception:  # pragma: no cover
            logger.exception("Could not get number of columns.")
        return 0  # pragma: no cover

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        /,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        # Return empty data if index is invalid, shouldn't happen in normal operation
        # but checking prevents crashes
        if index.isValid():  # pragma: no branch
            row_index = index.row()
            column_index = index.column()
            # this could call out to end-user data sources, so could fail.
            try:
                if (source := self._source) is None:
                    # this can happen briefly during initialization
                    return None  # pragma: no cover
                if row_index >= len(source):
                    # This should not happen in normal operation, but could occur
                    # if data changed and notification hasn't been sent
                    return None  # pragma: no cover

                columns = self._columns
                if column_index >= len(columns):
                    # This should not happen in normal operation, but could occur
                    # if data changed and notification hasn't been sent
                    return None  # pragma: no cover

                row = source[row_index]
                column = columns[column_index]
                if column.widget(row) is not None:
                    warnings.warn(
                        "Qt does not support the use of widgets in cells",
                        stacklevel=2,
                    )

                # currently only handle icons and text
                if role == Qt.ItemDataRole.DecorationRole:
                    icon = column.icon(row)
                    if icon is not None:
                        return icon._impl.native
                elif role == Qt.ItemDataRole.DisplayRole:
                    return column.text(row, self._missing_value)
            except Exception:  # pragma: no cover
                logger.exception(
                    f"Could not get data for row {row_index}, column {column_index}"
                )
        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        /,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if orientation == Qt.Orientation.Horizontal:
            columns = self._columns
            # this could call out to end-user data sources, so could fail.
            try:
                if section < len(columns):  # pragma: no branch
                    if role == Qt.ItemDataRole.DisplayRole:
                        return columns[section].heading
            except Exception:  # pragma: no cover
                logger.exception(f"Could not header for column {section}.")

        return None


class Table(Widget):
    def create(self):
        # Create the List widget
        self.native = QTableView()

        self.native_model = TableSourceModel(
            getattr(self.interface, "_data", ListSource(self.interface.accessors)),
            self.interface._columns[:],
            self.interface.missing_value,
            parent=self.native,
        )
        self.native.setModel(self.native_model)

        self.native.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        if self.interface.multiple_select:
            self.native.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        else:
            self.native.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        if not self.interface._show_headings:
            # Hide the header
            self.native.horizontalHeader().hide()

        self.native.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.native.selectionModel().selectionChanged.connect(self.qt_selection_changed)
        self.native.activated.connect(self.qt_activated)

    def qt_selection_changed(self, added, removed):
        self.interface.on_select()

    def qt_activated(self, index):
        # Invalid index shouldn't occur in normal operation.
        if index.isValid():  # pragma: no branch
            self.interface.on_activate(row=self.interface.data[index.row()])

    def change_source(self, source):
        self.native_model.set_source(source)
        self.native.horizontalHeader().resizeSections(QHeaderView.ResizeMode.Stretch)

    # Listener Protocol implementation

    def insert(self, index, item):
        self.native_model.insert_item(index)

    def change(self, item):
        self.native_model.item_changed(item)

    def remove(self, index, item):
        self.native_model.remove_item(index)

    def clear(self):
        self.native_model.reset_source()

    def get_selection(self):
        indexes = self.native.selectedIndexes()
        if self.interface.multiple_select:
            return sorted({index.row() for index in indexes})
        else:
            return indexes[0].row() if len(indexes) != 0 else None

    def scroll_to_row(self, row):
        index = self.native.model().index(row, 0, QModelIndex())
        self.native.scrollTo(index)

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
        self.native.horizontalHeader().resizeSections(QHeaderView.ResizeMode.Stretch)

    def insert_column(self, index, heading, accessor):
        self.native_model._columns.insert(index, self.interface._columns[index])
        self.native_model.beginInsertColumns(QModelIndex(), index, index)
        self.native_model.endInsertColumns()
        self.native.horizontalHeader().resizeSections(QHeaderView.ResizeMode.Stretch)

    def remove_column(self, index):
        del self.native_model._columns[index]
        self.native_model.beginRemoveColumns(QModelIndex(), index, index)
        self.native_model.endRemoveColumns()
        self.native.horizontalHeader().resizeSections(QHeaderView.ResizeMode.Stretch)
