import os
import sys
from pathlib import Path

import pytest
from textual.app import App as TextualApp

import toga

from .probe import BaseProbe

APP_ID = "org.beeware.toga.testbed-textual"
APP_NAME = "testbed-textual"
AUTHOR = "Tiberius Yak"
FORMAL_NAME = "Toga Testbed (Textual)"


class AppProbe(BaseProbe):
    supports_key = False
    supports_key_mod3 = False
    supports_current_window_assignment = True
    supports_dark_mode = False
    edit_menu_noop_enabled = False
    supports_psutil = True
    beep_delay = 0.1

    @classmethod
    def test_context(cls):
        """Establish the context required to safely run test code on the app's event
        loop.
        """
        return toga.App.app._impl.native._context()

    def __init__(self, app):
        super().__init__()
        self.app = app
        assert isinstance(self.app._impl.native, TextualApp)

    def _xdg_path(self, env_var, default_path):
        value = os.environ.get(env_var)
        if value:
            path = Path(value)
            if path.is_absolute():
                return path
        return Path.home() / default_path

    @property
    def _win32_app_dir(self):
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            base_dir = Path(local_app_data)
            if not base_dir.is_absolute():
                base_dir = Path.home() / "AppData/Local"
        else:
            base_dir = Path.home() / "AppData/Local"
        return base_dir / AUTHOR / FORMAL_NAME

    @property
    def config_path(self):
        if sys.platform == "darwin":
            return Path.home() / f"Library/Preferences/{APP_ID}"
        elif sys.platform == "win32":
            return self._win32_app_dir / "Config"
        else:
            return self._xdg_path("XDG_CONFIG_HOME", ".config") / APP_NAME

    @property
    def data_path(self):
        if sys.platform == "darwin":
            return Path.home() / f"Library/Application Support/{APP_ID}"
        elif sys.platform == "win32":
            return self._win32_app_dir / "Data"
        else:
            return self._xdg_path("XDG_DATA_HOME", ".local/share") / APP_NAME

    @property
    def cache_path(self):
        if sys.platform == "darwin":
            return Path.home() / f"Library/Caches/{APP_ID}"
        elif sys.platform == "win32":
            return self._win32_app_dir / "Cache"
        else:
            return self._xdg_path("XDG_CACHE_HOME", ".cache") / APP_NAME

    @property
    def logs_path(self):
        if sys.platform == "darwin":
            return Path.home() / f"Library/Logs/{APP_ID}"
        elif sys.platform == "win32":
            return self._win32_app_dir / "Logs"
        else:
            return self._xdg_path("XDG_STATE_HOME", ".local/state") / APP_NAME / "log"

    async def assert_event_loop(self):
        pytest.skip("Event loop assertions are not implemented on Textual.")

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
