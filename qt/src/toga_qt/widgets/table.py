import warnings
from typing import Any

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtWidgets import QHeaderView, QTableView
from travertino.size import at_least

from toga.sources import ListSource

from .base import Widget

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
            return
        self.dataChanged.emit(
            self.index(self._source.index(item), 0),
            self.index(self._source.index(item), len(self._columns)),
        )

    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = INVALID_INDEX,
    ) -> int:
        if self._source is None:
            return 0
        return len(self._source)

    def columnCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = INVALID_INDEX,
    ) -> int:
        if self._columns is None:
            return 0
        return len(self._columns)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        /,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid():
            return None
        source = self._source
        if source is None:
            return None
        if (row_index := index.row()) >= len(source):
            return None

        columns = self._columns
        if (column_index := index.column()) >= len(columns):
            return None

        row = source[row_index]
        column = columns[column_index]
        if column.widget(row) is not None:
            warnings.warn(
                "Qt does not support the use of widgets in cells",
                stacklevel=2,
            )
        if role == Qt.ItemDataRole.DecorationRole:
            icon = column.icon(row)
            if icon is not None:
                return icon._impl.native
        elif role == Qt.ItemDataRole.DisplayRole:
            return column.text(row, self._missing_value)
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
            if section >= len(columns):
                return None
            if role == Qt.ItemDataRole.DisplayRole:
                return columns[section].heading

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
        if index.isValid():
            self.interface.on_activate(row=self.interface.data[index.row()])

    def change_source(self, source):
        self.native_model.set_source(source)

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

    def insert_column(self, index, heading, accessor):
        self.native_model._columns.insert(index, self.interface._columns[index])
        self.native_model.beginInsertColumns(QModelIndex(), index, index)
        self.native_model.endInsertColumns()

    def remove_column(self, index):
        del self.native_model._columns[index]
        self.native_model.beginRemoveColumns(QModelIndex(), index, index)
        self.native_model.endRemoveColumns()
