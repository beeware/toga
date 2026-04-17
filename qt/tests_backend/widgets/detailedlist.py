import asyncio

from PySide6.QtCore import QEvent, QModelIndex, QPoint, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QListView

import toga

from .base import SimpleProbe


class DetailedListProbe(SimpleProbe):
    native: QListView
    native_class = QListView
    supports_actions = True
    supports_refresh = True

    def _row_to_index(self, row):
        model = self.native.model()
        return model.index(row)

    @property
    def row_count(self):
        return self.native.model().rowCount()

    def assert_cell_content(self, row, title, subtitle, icon=None):
        index = self._row_to_index(row)
        user_data = self.impl._format_missing(index.data(Qt.ItemDataRole.UserRole))

        assert user_data[0] == title
        assert user_data[1] == subtitle

        decoration = self.native.model().data(index, Qt.ItemDataRole.DecorationRole)

        if icon is not None:
            assert decoration.cacheKey() == icon._impl.native.cacheKey()
        else:
            assert decoration.isNull()

    @property
    def max_scroll_position(self):
        return self.native.verticalScrollBar().maximum()

    @property
    def scroll_position(self):
        return self.native.verticalScrollBar().value()

    def scroll_to_top(self):
        return self.native.verticalScrollBar().setValue(0)

    async def wait_for_scroll_completion(self):
        # No animation associated with scroll, so this is a no-op
        pass

    def row_position(self, row):
        index = self._row_to_index(row)
        rect = self.native.rectForIndex(index)
        return rect.center()

    async def select_row(self, row, add=False):
        index = self._row_to_index(row)
        self.native.selectionModel().select(index, self.native.selectionCommand(index))

    def refresh_available(self):
        # need scroll position 0 to be comptaible with tests for pull-down scroll
        return (
            self.impl.refresh_enabled
            and self.scroll_position == 0
            and self.impl.refresh_bar.isVisible()
        )

    async def non_refresh_action(self):
        # don't select the menu item... no-op
        pass

    async def refresh_action(self, active=True):
        if active:
            assert self.refresh_available()

            # ask for the menu
            await self._perform_menu_action(0, -1, noop=True)

            # Use the button
            self.impl.refreshAction.triggered.emit()

            # A short pause to allow the click handler to be processed.
            await asyncio.sleep(0.1)
        else:
            assert not self.refresh_available()

    async def _perform_menu_action(self, row, index, noop=False):
        if row is not None:
            pos = self.row_position(row)
        else:
            pos = self.native.rect().center()

        # select the row if there is one
        if row is not None:
            await self.select_row(row)

        menu = self.impl._menu

        def trigger_action():
            action = menu.actions()[index]
            if not noop:
                action.triggered.emit()
            if toga.App.app.run_slow:
                print("Action has been selected")
            menu.close()
            if toga.App.app.run_slow:
                print("Menu is closed")

        asyncio.get_running_loop().call_soon_threadsafe(trigger_action)
        self.impl.qt_context_menu(pos)
        await self.redraw("Action menu has been displayed")

    async def _perform_button_action(self, row, button_index):
        # Scroll into view.
        self.impl.scroll_to_row(row)
        await self.redraw("Scrolling into row")

        index = self.native.model().index(row, 0, QModelIndex())
        rect = self.impl.native_delegate._button_rects(index)[button_index]
        # width - 25 is an approximate mock, verifying that the position is no longer
        # clickable.
        center_pos = (
            rect.center()
            if rect.isValid()
            else QPoint(self.row_position(row).y(), self.width - 25)
        )

        hover_event = QMouseEvent(
            QEvent.MouseMove,
            center_pos,
            self.native.mapToGlobal(center_pos),
            Qt.NoButton,
            Qt.NoButton,
            Qt.NoModifier,
        )
        self.native.mouseMoveEvent(hover_event)
        await self.redraw("Button has been hovered over")

        if rect.isValid():
            # With all those assertions below -- the premise for doing them instead of
            # actually inspecting the button state is that it's not easy to inspect the
            # actual drawing results.
            assert self.native._hovered_button == (
                "primary" if button_index == 0 else "secondary",
                index,
            )

        press_event = QMouseEvent(
            QEvent.MouseButtonPress,
            center_pos,
            self.native.mapToGlobal(center_pos),
            Qt.LeftButton,
            Qt.LeftButton,
            Qt.NoModifier,
        )
        self.native.mousePressEvent(press_event)
        # This is to get coverage, as actually clicking twice will emit the event
        # twice.
        self.native.mouseDoubleClickEvent(press_event)
        await self.redraw("Button has been pressed down")

        if rect.isValid():
            assert self.native._pressed_button == (
                "primary" if button_index == 0 else "secondary",
                index,
            )

        release_event = QMouseEvent(
            QEvent.MouseButtonRelease,
            center_pos,
            self.native.mapToGlobal(center_pos),
            Qt.LeftButton,
            Qt.NoButton,
            Qt.NoModifier,
        )
        self.native.mouseReleaseEvent(release_event)
        await self.redraw("Button has been pressed up")

        if rect.isValid():
            assert self.native._hovered_button == (
                "primary" if button_index == 0 else "secondary",
                index,
            )
            assert self.native._pressed_button is None

            # More coverage-grabbing things.

            # Emit a scroll event; this doesn't actually do scrolling,
            # but verify that the recomputation works correctly
            _hovered_button = self.native._hovered_button
            self.native.verticalScrollBar().valueChanged.emit(
                self.native.verticalScrollBar().value()
            )
            await self.redraw("Scrolling occurred")
            assert _hovered_button == self.native._hovered_button

            # Verify that leaving the area with the mouse
            # gets you no hover.
            leave_event = QEvent(QEvent.Leave)
            self.native.leaveEvent(leave_event)
            await self.redraw("Mouse has left view")
            assert self.native._hovered_button is None

    async def perform_primary_action(self, row, active=True):
        await self._perform_button_action(row, 0)
        # Test the context menu, but don't call it again
        await self._perform_menu_action(row, 0, noop=True)

    async def perform_secondary_action(self, row, active=True):
        await self._perform_button_action(row, 1)
        # Test the context menu, but don't call it again
        await self._perform_menu_action(
            row, 1 if self.impl.primary_action_enabled else 0, noop=True
        )
