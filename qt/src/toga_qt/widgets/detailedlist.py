import logging
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QPersistentModelIndex,
    QSize,
    Qt,
)
from PySide6.QtGui import QAction, QFont, QFontMetrics, QIcon, QPainter
from PySide6.QtWidgets import QListView, QMenu, QStyle, QStyledItemDelegate
from travertino.size import at_least

from toga.sources import ListSource

from .base import Widget

logger = logging.getLogger(__name__)

ICON_SIZE = 32

MISSING = object()

INVALID_INDEX = QModelIndex()

# Utility functions


def get_str(row, accessor):
    value = getattr(row, accessor, None)
    return None if value is None else str(value)


def user_formatter(row, accessors):
    title = get_str(row, accessors[0])
    subtitle = get_str(row, accessors[1])
    return (title, subtitle)


def icon_formatter(row, accessors):
    icon = getattr(row, accessors[2], None)
    qt_icon = QIcon() if icon is None else icon._impl.native
    return qt_icon


class ListSourceModel(QAbstractListModel):
    """Qt list model that wraps a ListSource."""

    source: ListSource | None
    formatters: dict[int, Callable[[object, list[str]], object]]

    def __init__(self, source, formatters, **kwargs):
        super().__init__(**kwargs)
        self.source = source
        self.formatters = formatters

    def set_source(self, source):
        self.beginResetModel()
        self.source = source
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
        if self.source is not None:  # pragma: no branch
            index = self.index(self.source.index(item))
            self.dataChanged.emit(index, index)

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = INVALID_INDEX
    ) -> int:
        # this could call out to end-user data sources, so could fail.
        try:
            if self.source is not None:
                return len(self.source)
        except Exception:  # pragma: no cover
            logger.exception("Could not get data length.")
        return 0

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        /,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        # Return empty data if index is invalid, shouldn't happen in normal operation
        # but checking prevents crashes
        if index.isValid():  # pragma: no branch
            # this could call out to end-user data sources, so could fail.
            try:
                row = index.row()
                if self.source is None or row >= len(self.source):  # pragma: no cover
                    return None

                value = self.source[row]
                if role in self.formatters:
                    return self.formatters[role](value, self.source._accessors)
            except Exception:  # pragma: no cover
                logger.exception("Could not get data for row {row}")
        if role == Qt.ItemDataRole.UserRole:
            # Our user data should always be a tuple of two values.
            # Shouldn't reach this in normal operation, but will if there
            # is an error in a user data source.
            return (None, None)  # pragma: no cover
        else:
            return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        /,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        # Not used by the list view, but from QAbstractListModel docs:
        # "Well behaved models also provide a headerData() implementation."
        return None  # pragma: no cover


class DetailedListDelegate(QStyledItemDelegate):
    """Qt Item Delegate to display items with title and subtitle."""

    def __init__(self, impl, **kwargs):
        super().__init__(**kwargs)
        self.impl = impl

    def paint(self, painter: QPainter, options, index):
        self.initStyleOption(options, index)
        painter.save()

        title, subtitle = self.impl._format_missing(
            index.data(Qt.ItemDataRole.UserRole)
        )

        options.widget.style().drawControl(
            QStyle.ControlElement.CE_ItemViewItem, options, painter
        )
        title_metrics = QFontMetrics(options.font)
        line_spacing = title_metrics.lineSpacing()
        subtitle_font = QFont(options.font)
        subtitle_font.setPointSizeF(subtitle_font.pointSizeF() * 0.89)
        subtitle_metrics = QFontMetrics(subtitle_font)

        painter.translate(options.rect.left() + ICON_SIZE + 4, options.rect.top())

        painter.drawText(0, title_metrics.height(), title)

        painter.setFont(subtitle_font)
        painter.drawText(0, line_spacing + subtitle_metrics.height(), subtitle)

        painter.restore()

    def sizeHint(self, options, index):
        base_size = super().sizeHint(options, index)
        self.initStyleOption(options, index)

        title, subtitle = self.impl._format_missing(
            index.data(Qt.ItemDataRole.UserRole)
        )

        title_metrics = QFontMetrics(options.font)
        subtitle_font = QFont(options.font)
        subtitle_font.setPointSizeF(subtitle_font.pointSizeF() * 0.89)
        subtitle_metrics = QFontMetrics(subtitle_font)

        min_height = max(
            title_metrics.lineSpacing() + subtitle_metrics.lineSpacing() + 4,
            base_size.height(),
        )
        min_width = (
            base_size.width()
            + 4
            + max(
                title_metrics.boundingRect(title).width(),
                subtitle_metrics.boundingRect(subtitle).width(),
            )
        )

        return QSize(min_width, min_height)


class DetailedList(Widget):
    """Implementation that wraps a QListView."""

    def create(self):
        # Create the List widget
        self.native = QListView()
        self.native.setIconSize(QSize(ICON_SIZE, ICON_SIZE))

        self.native_model = ListSourceModel(
            self.interface.data,
            {
                Qt.ItemDataRole.UserRole: user_formatter,
                Qt.ItemDataRole.DecorationRole: icon_formatter,
            },
            parent=self.native,
        )
        self.native.setModel(self.native_model)

        self.native_delegate = DetailedListDelegate(self, parent=self.native)
        self.native.setItemDelegate(self.native_delegate)
        self.native.setSelectionMode(QListView.SelectionMode.SingleSelection)
        self.native.selectionModel().selectionChanged.connect(self.qt_selection_changed)

        # Disable all actions by default.
        self.primary_action_enabled = False
        self.secondary_action_enabled = False
        self.refresh_enabled = False

        # Set up context menu
        self.native.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.native.customContextMenuRequested.connect(self.qt_context_menu)
        self._menu = QMenu(self.native)

    def _format_missing(self, user_data):
        return tuple(
            x if x is not None else self.interface.missing_value for x in user_data
        )

    def _get_context_menu(self):
        self._menu.clear()
        actions = []
        # Primary and secondary actions only show when an item is selected
        if self.native.selectedIndexes():  # pragma: no branch
            if self.primary_action_enabled:
                primary_action = QAction(
                    self.interface._primary_action, parent=self._menu
                )
                primary_action.triggered.connect(self.qt_primary_action)
                actions.append(primary_action)
            if self.secondary_action_enabled and self.native.selectedIndexes():
                secondary_action = QAction(
                    self.interface._secondary_action, parent=self._menu
                )
                secondary_action.triggered.connect(self.qt_secondary_action)
                actions.append(secondary_action)
        if self.refresh_enabled:  # pragma: no branch
            refresh_action = QAction("Refresh", parent=self._menu)
            refresh_action.triggered.connect(self.qt_refresh_action)
            actions.append(refresh_action)
        self._menu.addActions(actions)

    def qt_selection_changed(self, selected, deselected):
        self.interface.on_select()

    def qt_context_menu(self, pos):
        self._get_context_menu()
        if not self._menu.isEmpty():  # pragma: no branch
            self._menu.exec()

    def qt_primary_action(self, checked):
        row = self.get_selection()
        row_data = self.interface.data[row]
        self.interface.on_primary_action(row=row_data)

    def qt_secondary_action(self, checked):
        row = self.get_selection()
        row_data = self.interface.data[row]
        self.interface.on_secondary_action(row=row_data)

    def qt_refresh_action(self, checked):
        self.interface.on_refresh()

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

    # Toggle actions

    def set_refresh_enabled(self, enabled):
        self.refresh_enabled = enabled

    def set_primary_action_enabled(self, enabled):
        self.primary_action_enabled = enabled

    def set_secondary_action_enabled(self, enabled):
        self.secondary_action_enabled = enabled

    def after_on_refresh(self, widget, result):
        self.native_model.reset_source()

    def get_selection(self):
        indexes = self.native.selectedIndexes()
        return indexes[0].row() if len(indexes) != 0 else None

    def scroll_to_row(self, row):
        index = self.native.model().index(row, 0, QModelIndex())
        self.native.scrollTo(index)

    # sizing

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
