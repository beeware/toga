import logging
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QPersistentModelIndex,
    QRect,
    QSize,
    Qt,
)
from PySide6.QtGui import QAction, QFont, QFontMetrics, QIcon, QPainter
from PySide6.QtWidgets import (
    QListView,
    QMenu,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionButton,
)
from travertino.size import at_least

from toga.sources import ListSource

from .base import Widget

logger = logging.getLogger(__name__)

ICON_SIZE = 32
BUTTON_PADDING = 6
BUTTON_MARGIN = 6

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
            # this could call out to end-user data sources, so could fail.
            try:
                row = index.row()
                if self.source is None or row >= len(self.source):  # pragma: no cover
                    return None

                value = self.source[row]
                if role in self.formatters:
                    return self.formatters[role](value, self.source._accessors)
            except Exception:  # pragma: no cover
                logger.exception(f"Could not get data for row {row}")
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

        # Draw the normal item background
        options.widget.style().drawControl(
            QStyle.ControlElement.CE_ItemViewItem,
            options,
            painter,
            options.widget,
        )

        # Draw title and subtitle
        title_metrics = QFontMetrics(options.font)
        subtitle_font = QFont(options.font)
        subtitle_font.setPointSizeF(subtitle_font.pointSizeF() * 0.89)
        subtitle_metrics = QFontMetrics(subtitle_font)

        x_offset = ICON_SIZE + 4
        y = options.rect.top()
        painter.drawText(
            options.rect.left() + x_offset, y + title_metrics.ascent(), title
        )
        y += title_metrics.lineSpacing()
        painter.setFont(subtitle_font)
        painter.drawText(
            options.rect.left() + x_offset, y + subtitle_metrics.ascent(), subtitle
        )

        primary_text = (
            self.impl.interface._primary_action
            if self.impl.primary_action_enabled
            else None
        )
        secondary_text = (
            self.impl.interface._secondary_action
            if self.impl.secondary_action_enabled
            else None
        )

        if primary_text:
            primary_rect = self._primary_button_rect(index)
            self._draw_button(
                options, painter, primary_text, primary_rect, ("primary", index)
            )

        if secondary_text:
            secondary_rect = self._secondary_button_rect(index)
            self._draw_button(
                options, painter, secondary_text, secondary_rect, ("secondary", index)
            )

        painter.restore()

    def _draw_button(self, option, painter, text, rect, role):
        button_option = QStyleOptionButton()
        button_option.rect = rect
        button_option.text = text
        button_option.state = QStyle.StateFlag.State_Enabled
        if hasattr(self, "_hovered_button") and self._hovered_button == role:
            button_option.state |= QStyle.StateFlag.State_MouseOver
        if hasattr(self, "_pressed_button") and role == self._pressed_button:
            button_option.state |= QStyle.StateFlag.State_Sunken

        option.widget.style().drawControl(
            QStyle.ControlElement.CE_PushButton, button_option, painter, option.widget
        )

    def _secondary_button_rect(self, index, rect=None):
        if rect is None:
            rect = self.impl.native.visualRect(index)
        text = (
            self.impl.interface._secondary_action
            if self.impl.secondary_action_enabled
            else None
        )
        if not text:
            return QRect()  # empty rect if no button

        option = QStyleOptionButton()
        fm = option.fontMetrics
        width = fm.horizontalAdvance(text) + 2 * BUTTON_PADDING
        height = fm.height() + 2 * BUTTON_PADDING

        return QRect(
            rect.right() - width - BUTTON_MARGIN,
            rect.center().y() - height // 2,
            width,
            height,
        )

    def button_at(self, index: QModelIndex, pos):
        primary_rect, secondary_rect = (
            self._primary_button_rect(index),
            self._secondary_button_rect(index),
        )
        if primary_rect and primary_rect.contains(pos):
            return "primary", index
        if secondary_rect and secondary_rect.contains(pos):
            return "secondary", index
        return None

    def _primary_button_rect(self, index, rect=None):
        if rect is None:
            rect = self.impl.native.visualRect(index)
        text = (
            self.impl.interface._primary_action
            if self.impl.primary_action_enabled
            else None
        )
        if text is None:
            return QRect()

        secondary_rect = self._secondary_button_rect(index, rect)
        option = QStyleOptionButton()
        fm = option.fontMetrics
        width = fm.horizontalAdvance(text) + 2 * BUTTON_PADDING
        height = fm.height() + 2 * BUTTON_PADDING

        # Position primary to the left of secondary if secondary exists, otherwise
        # align to right
        x = (
            secondary_rect.left() - width - BUTTON_MARGIN
            if not secondary_rect.isNull()
            else option.rect.right() - width - BUTTON_MARGIN
        )
        return QRect(x, rect.center().y() - height // 2, width, height)

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
        # options.rect is explicitly passed in here, as the visual rectangle computation
        # requires the size hint.
        min_width = (
            base_size.width()
            + 4
            + max(
                title_metrics.boundingRect(title).width(),
                subtitle_metrics.boundingRect(subtitle).width(),
            )
            + (
                self._primary_button_rect(index, rect=options.rect).width()
                + BUTTON_MARGIN
                if self.impl.primary_action_enabled
                else 0
            )
            + (
                self._secondary_button_rect(index, rect=options.rect).width()
                + BUTTON_MARGIN
                if self.impl.secondary_action_enabled
                else 0
            )
        )

        return QSize(min_width, min_height)


class ButtonListView(QListView):
    """QListView to track button clicks and hover."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.position().toPoint())
        # Defensive safety catch for no index.
        if not index.isValid():  # pragma: no cover
            self.delegate._hovered_button = None
            self.viewport().update()
            return super().mouseMoveEvent(event)

        pos = event.position().toPoint()
        self.delegate._hovered_button = self.delegate.button_at(index, pos)

        self.viewport().update()
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        index = self.indexAt(event.position().toPoint())
        if not index.isValid():  # pragma: no cover
            self.delegate._pressed_button = None
            return super().mousePressEvent(event)

        pos = event.position().toPoint()
        self.delegate._pressed_button = self.delegate.button_at(index, pos)
        # print(self.delegate._pressed_button)

        self.viewport().update()
        if not self.delegate._pressed_button:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        index = self.indexAt(event.position().toPoint())
        handled = False
        # index.isValid is defensive safety catch; pressed_button is to prevent
        # dragging into the button without pressing.  The latter does not have a
        # cross-platform test case, and is tedious to trigger.
        if index.isValid() and self.delegate._pressed_button:  # pragma: no branch
            pos = event.position().toPoint()
            self.delegate._pressed_button = self.delegate.button_at(index, pos)
            if (
                self.delegate._pressed_button
                and self.delegate._pressed_button[0] == "primary"
            ):
                self.delegate.impl.qt_primary_action(False, index.row())
                handled = True
            elif (
                self.delegate._pressed_button
                and self.delegate._pressed_button[0] == "secondary"
            ):
                self.delegate.impl.qt_secondary_action(False, index.row())
                handled = True
            # else is defensive; no-cover.
            else:  # pragma: no cover
                pass

        self.delegate._pressed_button = None
        self.viewport().update()
        if not handled:
            super().mouseReleaseEvent(event)


class DetailedList(Widget):
    """Implementation that wraps a QListView."""

    def create(self):
        # Create the List widget
        self.native = ButtonListView()
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
        # This is necessary, as the result of itemDelegate somehow does not synchronize
        # attributes such as _hovered_button properly
        self.native.delegate = self.native_delegate
        self.native.setItemDelegate(self.native_delegate)
        self.native.setEditTriggers(QListView.NoEditTriggers)
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
            self._menu.exec(self.native.mapToGlobal(pos))

    def qt_primary_action(self, checked, row):
        row_data = self.interface.data[row]
        self.interface.on_primary_action(row=row_data)

    def qt_secondary_action(self, checked, row):
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
