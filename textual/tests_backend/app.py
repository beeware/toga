import sys
from pathlib import Path

import pytest
from textual.app import App as TextualApp

from .probe import BaseProbe


class AppProbe(BaseProbe):
    supports_key = False
    supports_key_mod3 = False
    supports_current_window_assignment = True
    supports_dark_mode = False
    edit_menu_noop_enabled = False
    supports_psutil = True

    def __init__(self, app):
        super().__init__()
        self.app = app
        assert isinstance(self.app._impl.native, TextualApp)

    @property
    def config_path(self):
        if sys.platform == "darwin":
            return Path.home() / f"Library/Preferences/{self.app.app_id}"
        elif sys.platform == "win32":
            return self._windows_app_dir / "Config"
        else:
            return Path.home() / f".config/{self.app.app_name}"

    @property
    def data_path(self):
        if sys.platform == "darwin":
            return Path.home() / f"Library/Application Support/{self.app.app_id}"
        elif sys.platform == "win32":
            return self._windows_app_dir / "Data"
        else:
            return Path.home() / f".local/share/{self.app.app_name}"

    @property
    def cache_path(self):
        if sys.platform == "darwin":
            return Path.home() / f"Library/Caches/{self.app.app_id}"
        elif sys.platform == "win32":
            return self._windows_app_dir / "Cache"
        else:
            return Path.home() / f".cache/{self.app.app_name}"

    @property
    def logs_path(self):
        if sys.platform == "darwin":
            return Path.home() / f"Library/Logs/{self.app.app_id}"
        elif sys.platform == "win32":
            return self._windows_app_dir / "Logs"
        else:
            return Path.home() / f".local/state/{self.app.app_name}/log"

    @property
    def _windows_app_dir(self):
        author = "Unknown" if self.app.author is None else self.app.author
        return Path.home() / f"AppData/Local/{author}/{self.app.formal_name}"

    @property
    def is_cursor_visible(self):
        pytest.skip("Cursor visibility is not implemented on Textual.")

    def unhide(self):
        pytest.xfail("Textual doesn't have app-level unhide.")

    def assert_app_icon(self, icon):
        pytest.skip("App icon assertions are not implemented on Textual.")

    def assert_dialog_in_focus(self, dialog):
        pytest.skip("Dialog focus assertions are not implemented on Textual.")

    def activate_menu_hide(self):
        pytest.skip("Menus are not implemented on Textual.")

    def activate_menu_exit(self):
        pytest.skip("Menus are not implemented on Textual.")

    def activate_menu_about(self):
        pytest.skip("Menus are not implemented on Textual.")

    async def close_about_dialog(self):
        pytest.skip("Menus are not implemented on Textual.")

    def activate_menu_visit_homepage(self):
        pytest.skip("Menus are not implemented on Textual.")

    def assert_system_menus(self):
        pytest.skip("Menus are not implemented on Textual.")

    def activate_menu_close_window(self):
        pytest.skip("Menus are not implemented on Textual.")

    def activate_menu_close_all_windows(self):
        pytest.skip("Menus are not implemented on Textual.")

    def activate_menu_minimize(self):
        pytest.skip("Menus are not implemented on Textual.")

    def assert_menu_item(self, path, enabled):
        pytest.skip("Menus are not implemented on Textual.")

    def assert_menu_order(self, path, expected):
        pytest.skip("Menus are not implemented on Textual.")

    def keystroke(self, combination):
        pytest.skip("Keystrokes are not implemented on Textual.")

    async def restore_standard_app(self):
        await self.redraw("Restore to standard app")

    async def open_initial_document(self, monkeypatch, document_path):
        pytest.xfail("Textual doesn't require initial document support.")

    def open_document_by_drag(self, document_path):
        pytest.xfail("Textual doesn't support opening documents by drag.")
