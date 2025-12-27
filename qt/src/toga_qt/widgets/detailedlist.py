from collections.abc import Callable
from typing import Any

from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QPersistentModelIndex,
    QSize,
    Qt,
)
from PySide6.QtGui import QAction, QCursor, QFont, QFontMetrics, QIcon, QPainter
from PySide6.QtWidgets import QListView, QMenu, QStyle, QStyledItemDelegate
from travertino.size import at_least

from toga.sources import ListSource

from .base import Widget

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
        if self.source is None:
            return
        self.dataChanged.emit(self.index(self.source.index(item)))
        # Nothing to do, removal has already happened
        self.endInsertRows()

    def rowCount(
        self, parent: QModelIndex | QPersistentModelIndex = INVALID_INDEX
    ) -> int:
        if self.source is None:
            return 0
        return len(self.source)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        /,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        if not index.isValid():
            return None
        if self.source is None:
            return None
        if index.row() >= len(self.source):
            return None

        value = self.source[index.row()]
        if role in self.formatters:
            result = self.formatters[role](value, self.source._accessors)
            return result
        else:
            return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        /,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        return None


class DetailedListDelegate(QStyledItemDelegate):
    """Qt Item Delegate to display items with title and subtitle."""

    def __init__(self, impl, **kwargs):
        super().__init__(**kwargs)
        self.impl = impl

    def paint(self, painter: QPainter, options, index):
        self.initStyleOption(options, index)
        painter.save()

        title, subtitle = index.data(Qt.ItemDataRole.UserRole)
        title = self.impl.interface.missing_value if title is None else title
        subtitle = self.impl.interface.missing_value if subtitle is None else subtitle

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

        title, subtitle = index.data(Qt.ItemDataRole.UserRole)
        title = self.impl.interface.missing_value if title is MISSING else title
        subtitle = (
            self.impl.interface.missing_value if subtitle is MISSING else subtitle
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

        # Disable all actions by default.
        self.primary_action_enabled = False
        self.secondary_action_enabled = False
        self.refresh_enabled = False

        # Set up context menu
        self.native.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.native.customContextMenuRequested.connect(self.qt_context_menu)

        self.native.show()

    def qt_context_menu(self, pos):
        actions = []
        if self.primary_action_enabled:
            primary_action = QAction(self.interface._primary_action)
            primary_action.triggered.connect(self.qt_primary_action)
            actions.append(primary_action)
        if self.secondary_action_enabled:
            secondary_action = QAction(self.interface._secondary_action)
            secondary_action.triggered.connect(self.qt_secondary_action)
            actions.append(secondary_action)
        if self.refresh_enabled:
            refresh_action = QAction("Refresh")
            refresh_action.triggered.connect(self.qt_refresh_action)
            actions.append(refresh_action)
        if actions:
            menu = QMenu(self.native)
            menu.addActions(actions)
            menu.exec(QCursor.pos())
        else:
            menu = None
        # for testing
        self._menu = menu

    def qt_primary_action(self, checked):
        index = self.native.selectionModel().currentIndex()
        row = self.interface.data[index.row()]
        self.interface.on_primary_action(row=row)

    def qt_secondary_action(self, checked):
        index = self.native.selectionModel().currentIndex()
        row = self.interface.data[index.row()]
        self.interface.on_secondary_action(row=row)

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
        return indexes[0].row() if len(indexes) == 0 else None

    def scroll_to_row(self, row):
        index = self.native.model().index(row, 0, QModelIndex())
        self.native.scrollTo(index)

    # sizing

    def rehint(self):
        self.interface.intrinsic.width = at_least(self.interface._MIN_WIDTH)
        self.interface.intrinsic.height = at_least(self.interface._MIN_HEIGHT)
