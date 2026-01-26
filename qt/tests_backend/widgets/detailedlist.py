import asyncio

from PySide6.QtCore import Qt
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
        return self.impl.refresh_enabled and self.scroll_position == 0

    async def non_refresh_action(self):
        # don't select the menu item... no-op
        pass

    async def refresh_action(self, active=True):
        if active:
            assert self.refresh_available()
            # ask for the menu
            await self._perform_action(0, -1)

            # A short pause to allow the click handler to be processed.
            await asyncio.sleep(0.1)
        else:
            assert not self.refresh_available()

    async def _perform_action(self, row, index):
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
            action.triggered.emit()
            if toga.App.app.run_slow:
                print("Action has been selected")
            menu.close()
            if toga.App.app.run_slow:
                print("Menu is closed")

        asyncio.get_running_loop().call_soon_threadsafe(trigger_action)
        self.impl.qt_context_menu(pos)
        await self.redraw("Action menu has been displayed")

    async def perform_primary_action(self, row, active=True):
        await self._perform_action(row, 0)

    async def perform_secondary_action(self, row, active=True):
        await self._perform_action(row, 1 if self.impl.primary_action_enabled else 0)
