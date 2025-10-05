from pathlib import Path

import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication, QDialog
from toga_qt.keys import qt_to_toga_key, toga_to_qt_key
from toga_qt.libs import get_is_wayland

from .probe import BaseProbe


class AppProbe(BaseProbe):
    supports_key = True
    supports_key_mod3 = True
    supports_current_window_assignment = True
    supports_dark_mode = True
    edit_menu_noop_enabled = True

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.main_window = app.main_window
        self.native = self.app._impl.native
        self.impl = self.app._impl
        assert isinstance(QApplication.instance(), QApplication)
        assert self.native.style().objectName() == "breeze"
        # KWin supports this but not mutter which is used in CI.
        if get_is_wayland():
            self.supports_current_window_assignment = False

    @property
    def config_path(self):
        return Path.home() / ".config/testbed_qt"

    @property
    def data_path(self):
        return Path.home() / ".local/share/testbed_qt"

    @property
    def cache_path(self):
        return Path.home() / ".cache/testbed_qt"

    @property
    def logs_path(self):
        return Path.home() / ".local/state/testbed_qt/log"

    @property
    def is_cursor_visible(self):
        return self.native.overrideCursor() != QCursor(Qt.BlankCursor)

    def unhide(self):
        self.main_window._impl.native.show()

    def assert_app_icon(self, icon):
        raise pytest.skip("Not implemented in probe yet")

    def activate_menu_hide(self):
        pytest.xfail("KDE apps do not include a Hide in the menu bar")

    def activate_menu_exit(self):
        self._activate_menu_item(["File", "Quit"])

    def activate_menu_about(self):
        self._activate_menu_item(["Help", "About Toga Testbed"])

    async def close_about_dialog(self):
        self.impl._about_dialog.done(QDialog.DialogCode.Accepted)

    def activate_menu_visit_homepage(self):
        raise pytest.xfail("Qt apps do not have a Visit Homepage menu action")

    def assert_dialog_in_focus(self, dialog):
        active_window = QApplication.activeWindow()
        assert active_window.windowTitle() == dialog._impl.native.windowTitle()

    def assert_menu_item(self, path, *, enabled=True):
        item = self._menu_item(path)
        assert item.isEnabled() == enabled

    def assert_menu_order(self, path, expected):
        menu = self._menu_item(path)
        actual_titles = [
            action.text() if action.isSeparator() is False else "---"
            for action in menu.actions()
        ]
        assert actual_titles == expected

    def assert_system_menus(self):
        # Incomplete
        self.assert_menu_item(["File", "Quit"])
        self.assert_menu_item(["Help", "About Toga Testbed"])

    def activate_menu_close_window(self):
        pytest.xfail("KDE apps do not include a Close in the menu bar")

    def activate_menu_close_all_windows(self):
        pytest.xfail("KDE apps do not include a Close All in the menu bar")

    def activate_menu_minimize(self):
        pytest.xfail("KDE apps do not include a Minimize in the menu bar")

    def keystroke(self, combination):
        return qt_to_toga_key(toga_to_qt_key(combination))

    async def restore_standard_app(self):
        pytest.skip("not impld")

    async def open_initial_document(self, monkeypatch, document_path):
        pytest.skip("not impld")

    def open_document_by_drag(self, document_path):
        pytest.skip("Not impld")

    def has_status_icon(self, status_icon):
        pytest.skip("Status Icons not yet implemented on Qt")

    def status_menu_items(self, status_icon):
        pytest.skip("Status Icons not yet implemented on Qt")

    def activate_status_icon_button(self, item_id):
        pytest.skip("Status Icons not yet implemented on Qt")

    def activate_status_menu_item(self, item_id, title):
        pytest.skip("Status Icons not yet implemented on Qt")

    def perform_edit_action(self, action):
        self._activate_menu_item(["Edit", action])
