import logging
from collections.abc import Callable
from typing import Any

from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QPersistentModelIndex,
    QPoint,
    QRect,
    QSize,
    Qt,
)
from PySide6.QtGui import QAction, QFont, QFontMetrics, QIcon, QPainter, QPalette
from PySide6.QtWidgets import (
    QListView,
    QMenu,
    QSizePolicy,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionButton,
    QToolBar,
    QWidget,
)
from travertino.size import at_least

from toga.sources import ListSource

from .base import Widget

logger = logging.getLogger(__name__)

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
        self.native = impl.native

    def paint(self, painter: QPainter, options, index):
        style = options.widget.style()
        self.initStyleOption(options, index)
        if not options.state & QStyle.StateFlag.State_Selected:
            options.state &= ~QStyle.StateFlag.State_HasFocus
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

        text_rect = style.subElementRect(
            QStyle.SE_ItemViewItemText, options, options.widget.viewport()
        )

        x_offset = text_rect.x()
        y = options.rect.top()
        painter.drawText(x_offset, y + title_metrics.ascent(), title)
        y += title_metrics.lineSpacing()
        painter.setFont(subtitle_font)
        painter.drawText(x_offset, y + subtitle_metrics.ascent(), subtitle)

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

        rects = self._button_rects(index)

        if primary_text:
            self._draw_button(
                options, painter, primary_text, rects[0], ("primary", index)
            )

        if secondary_text:
            self._draw_button(
                options, painter, secondary_text, rects[1], ("secondary", index)
            )

        painter.restore()

    def _draw_button(self, option, painter, text, rect, role):
        button_option = QStyleOptionButton()
        button_option.initFrom(option.widget)
        button_option.rect = rect
        button_option.text = text
        button_option.state = QStyle.StateFlag.State_Enabled
        if (
            hasattr(self.native, "_hovered_button")
            and self.native._hovered_button == role
        ):
            button_option.state |= QStyle.StateFlag.State_MouseOver
        if (
            hasattr(self.native, "_pressed_button")
            and role == self.native._pressed_button
        ):
            button_option.state |= QStyle.StateFlag.State_Sunken

        option.widget.style().drawControl(
            QStyle.ControlElement.CE_PushButton, button_option, painter, option.widget
        )

    def button_at(self, index, pos):
        primary_rect, secondary_rect = self._button_rects(index)
        if primary_rect.contains(pos):
            return ("primary", index)
        if secondary_rect.contains(pos):
            return ("secondary", index)
        return None

    def _button_rects(self, index, rect=None):
        if rect is None:
            rect = self.native.visualRect(index)

        option = QStyleOptionButton()
        option.initFrom(self.native)
        fm = option.fontMetrics
        cy = rect.center().y()

        def make_rect(text, right_edge):
            if not text:
                return QRect()
            w = fm.horizontalAdvance(text) + 2 * BUTTON_PADDING
            h = fm.height() + 2 * BUTTON_PADDING
            return QRect(
                right_edge - w,
                cy - h // 2,
                w,
                h,
            )

        second_text = (
            self.impl.interface._secondary_action
            if self.impl.secondary_action_enabled
            else None
        )
        second = make_rect(second_text, rect.right() - BUTTON_MARGIN)

        first_text = (
            self.impl.interface._primary_action
            if self.impl.primary_action_enabled
            else None
        )
        right_edge = (
            second.left() - BUTTON_MARGIN
            if not second.isNull()
            else rect.right() - BUTTON_MARGIN
        )
        first = make_rect(first_text, right_edge)

        return first, second

    def sizeHint(self, options, index):
        base_size = super().sizeHint(options, index)
        self.initStyleOption(options, index)
        style = options.widget.style()

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
        text_rect = style.subElementRect(
            QStyle.SE_ItemViewItemText, options, options.widget
        )
        # options.rect is explicitly passed in here, as the visual rectangle computation
        # requires the size hint.
        min_width = (
            text_rect.x()
            + max(
                title_metrics.boundingRect(title).width(),
                subtitle_metrics.boundingRect(subtitle).width(),
            )
            + (
                self._button_rects(index, rect=options.rect)[0].width() + BUTTON_MARGIN
                if self.impl.primary_action_enabled
                else 0
            )
            + (
                self._button_rects(index, rect=options.rect)[1].width() + BUTTON_MARGIN
                if self.impl.secondary_action_enabled
                else 0
            )
        )

        return QSize(min_width, min_height)


class ButtonListView(QListView):
    """QListView to track button clicks and hover."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.viewport().setMouseTracking(True)
        self.mouse_position = QPoint(-1, -1)
        self.verticalScrollBar().valueChanged.connect(self.qtScroll)

    # This method is no-covered as it is purely cosmetic
    # and takes lots of effort to test properly across all platforms,
    # most of which doesn't do manual handling like this
    def qtScroll(self):
        self._hovered_button = None
        pos = self.mouse_position
        index = self.indexAt(pos)
        # Defensive safety catch for no index.
        if not index.isValid():
            self.viewport().update()
            return

        self._hovered_button = self.delegate.button_at(index, pos)
        self.viewport().update()

    def mouseMoveEvent(self, event):
        pos = event.position().toPoint()
        self.mouse_position = pos
        index = self.indexAt(pos)
        # Defensive safety catch for no index.
        if not index.isValid():  # pragma: no cover
            self._hovered_button = None
            self.viewport().update()
            return super().mouseMoveEvent(event)

        self._hovered_button = self.delegate.button_at(index, pos)

        self.viewport().update()
        super().mouseMoveEvent(event)

    # This is hard to get coverage for besides manual invocation, but
    # it's just cosmetic (when a hover at the edge leaves the widget)
    def leaveEvent(self, event):
        self._hovered_button = None
        self.viewport().update()
        super().leaveEvent(event)

    def _handle_click(self, event):
        index = self.indexAt(event.position().toPoint())
        if not index.isValid():  # pragma: no cover
            self._pressed_button = None
            return False

        pos = event.position().toPoint()
        self._pressed_button = self.delegate.button_at(index, pos)

        self.viewport().update()
        if not self._pressed_button:
            return False
        return True

    def mousePressEvent(self, event):
        if not self._handle_click(event):
            super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if not self._handle_click(event):
            super().mouseDoubleClickEvent(event)

    def mouseReleaseEvent(self, event):
        index = self.indexAt(event.position().toPoint())
        handled = False
        # index.isValid is defensive safety catch.
        old = self._pressed_button
        if index.isValid():  # pragma: no branch
            pos = event.position().toPoint()
            self._pressed_button = self.delegate.button_at(index, pos)
            if (
                self._pressed_button
                and self._pressed_button == old
                and self._pressed_button[0] == "primary"
            ):
                self.impl.qt_primary_action(False, index.row())
                handled = True
            elif (
                self._pressed_button
                and self._pressed_button == old
                and self._pressed_button[0] == "secondary"
            ):
                self.delegate.impl.qt_secondary_action(False, index.row())
                handled = True
            # else is defensive; no-cover.
            else:  # pragma: no cover
                pass

        self._pressed_button = None
        self.viewport().update()
        if not handled:
            super().mouseReleaseEvent(event)


class DetailedList(Widget):
    """Implementation that wraps a QListView."""

    def __del__(self):
        self.refresh_bar.setParent(None)

    def create(self):
        # Create the List widget
        self.native = ButtonListView()
        self.native.setIconSize(QSize(32, 32))
        self.native.impl = self
        self.refresh_bar = QToolBar()
        self.refresh_bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.refresh_bar.setParent(self.native)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.refresh_bar.addWidget(spacer)
        self.refreshAction = QAction(
            QIcon.fromTheme("view-refresh"), "Refresh", self.refresh_bar
        )
        self.refresh_bar.addAction(self.refreshAction)
        self.refreshAction.triggered.connect(self.qt_refresh_action)

        # Assuming self.refresh_bar is your QToolBar
        pal = self.refresh_bar.palette()
        bg = pal.color(QPalette.AlternateBase)  # Get theme-appropriate toolbar color

        # Apply via stylesheet
        self.refresh_bar.setStyleSheet(f"background-color: {bg.name()};")

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

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self.update_toolbar()

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

    def qt_primary_action(self, checked=False, row=None):
        row = row if row is not None else self.get_selection()
        row_data = self.interface.data[row]
        self.interface.on_primary_action(row=row_data)

    def qt_secondary_action(self, checked=False, row=None):
        row = row if row is not None else self.get_selection()
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

    def update_toolbar(self):
        if not self.refresh_enabled:
            self.refresh_bar.hide()
            self.native.setViewportMargins(0, 0, 0, 0)
        else:
            self.refresh_bar.show()
            self.refresh_bar.setGeometry(
                self.native.contentsMargins().top(),
                self.native.contentsMargins().left(),
                self.native.width()
                - self.native.verticalScrollBar().width()
                - self.native.contentsMargins().right(),
                self.refresh_bar.sizeHint().height(),
            )
            self.native.setViewportMargins(
                0, self.refresh_bar.sizeHint().height(), 0, 0
            )

    # Toggle actions

    def set_refresh_enabled(self, enabled):
        self.refresh_enabled = enabled
        self.update_toolbar()

    def set_primary_action_enabled(self, enabled):
        self.primary_action_enabled = enabled
        self.native.viewport().update()

    def set_secondary_action_enabled(self, enabled):
        self.secondary_action_enabled = enabled
        self.native.viewport().repaint()

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
