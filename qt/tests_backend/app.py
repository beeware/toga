from pathlib import Path

import PIL.Image
import pytest
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication, QDialog, QSystemTrayIcon
from toga_qt.keys import qt_to_toga_key, toga_to_qt_key
from toga_qt.libs import IS_WAYLAND

import toga

from .probe import BaseProbe


class AppProbe(BaseProbe):
    formal_name = "Toga Testbed (Qt)"
    supports_key = True
    supports_key_mod3 = True
    supports_current_window_assignment = True
    supports_dark_mode = True
    edit_menu_noop_enabled = True
    supports_psutil = True

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.main_window = app.main_window
        self.native = self.app._impl.native
        self.impl = self.app._impl
        assert isinstance(QApplication.instance(), QApplication)
        # KWin supports this but not mutter which is used in CI.
        if IS_WAYLAND:
            self.supports_current_window_assignment = False

    @property
    def config_path(self):
        return Path.home() / ".config/testbed-qt"

    @property
    def data_path(self):
        return Path.home() / ".local/share/testbed-qt"

    @property
    def cache_path(self):
        return Path.home() / ".cache/testbed-qt"

    @property
    def logs_path(self):
        return Path.home() / ".local/state/testbed-qt/log"

    @property
    def is_cursor_visible(self):
        return self.native.overrideCursor() != QCursor(Qt.BlankCursor)

    def unhide(self):
        self.main_window._impl.native.show()

    def assert_app_icon(self, icon):
        for window in self.app.windows:
            # We have no real way to check we've got the right icon; use pixel peeping
            # as a guess. Construct a PIL image from the current icon.
            img = toga.Image(
                window._impl.native.windowIcon().pixmap(QSize(64, 64)).toImage()
            ).as_format(PIL.Image.Image)

            if icon:
                # The explicit alt icon has blue background, with green at a point 1/3
                # into the image
                assert img.getpixel((5, 5)) == (211, 230, 245)
                mid_color = img.getpixel((img.size[0] // 3, img.size[1] // 3))
                assert mid_color == (0, 204, 9)
            else:
                # The default icon is transparent background, and brown in the center.
                assert img.getpixel((5, 5))[3] == 0
                mid_color = img.getpixel((img.size[0] // 2, img.size[1] // 2))
                assert mid_color == (149, 119, 73, 255)

    def activate_menu_hide(self):
        pytest.xfail("KDE apps do not include a Hide in the menu bar")

    def activate_menu_exit(self):
        self._activate_menu_item(["File", "Quit"])

    def activate_menu_about(self):
        self._activate_menu_item(["Help", "About Toga Testbed (Qt)"])

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
        self.assert_menu_item(
            ["Settings", "Configure Toga Testbed (Qt)"],
            enabled=False,
        )
        self.assert_menu_item(["File", "Quit"], enabled=True)

        self.assert_menu_item(["File", "New Example Document"], enabled=True)
        self.assert_menu_item(["File", "New Read-only Document"], enabled=True)
        self.assert_menu_item(["File", "Open..."], enabled=True)
        self.assert_menu_item(["File", "Save"], enabled=True)
        self.assert_menu_item(["File", "Save As..."], enabled=True)
        self.assert_menu_item(["File", "Save All"], enabled=True)

        self.assert_menu_item(["Help", "About Toga Testbed (Qt)"], enabled=True)

        self.assert_menu_item(["Edit", "Undo"])
        self.assert_menu_item(["Edit", "Redo"])
        self.assert_menu_item(["Edit", "Cut"])
        self.assert_menu_item(["Edit", "Copy"])
        self.assert_menu_item(["Edit", "Paste"])

    def activate_menu_close_window(self):
        pytest.xfail("KDE apps do not include Close in the menu bar")

    def activate_menu_close_all_windows(self):
        pytest.xfail("KDE apps do not include Close All in the menu bar")

    def activate_menu_minimize(self):
        pytest.xfail("KDE apps do not include Minimize in the menu bar")

    def keystroke(self, combination):
        return qt_to_toga_key(toga_to_qt_key(combination))

    async def restore_standard_app(self):
        # No special handling needed to restore standard app.
        await self.redraw("Restore to standard app")

    async def open_initial_document(self, monkeypatch, document_path):
        pytest.xfail("Qt doesn't require initial document support")

    def open_document_by_drag(self, document_path):
        pytest.xfail("Qt doesn't support opening documents by drag")

    def has_status_icon(self, status_icon):
        return status_icon._impl.native is not None

    def status_menu_items(self, status_icon):
        menu = status_icon._impl.native.contextMenu()
        if menu is None:
            return None
        else:
            return [
                {
                    "": "---",
                    "About Toga Testbed (Qt)": "**ABOUT**",
                    "Quit": "**EXIT**",
                }.get(action.text(), action.text())
                for action in menu.actions()
            ]

    def activate_status_icon_button(self, item_id):
        self.app.status_icons[item_id]._impl.native.activated.emit(
            QSystemTrayIcon.ActivationReason.Trigger
        )

    def activate_status_menu_item(self, item_id, title):
        menu = self.app.status_icons[item_id]._impl.native.contextMenu()
        item = {action.text(): action for action in menu.actions()}[title]
        item.triggered.emit()

    def perform_edit_action(self, action):
        self._activate_menu_item(["Edit", action])
