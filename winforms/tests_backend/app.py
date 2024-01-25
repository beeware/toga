import ctypes
from pathlib import Path
from time import sleep

import pytest
from System import EventArgs
from System.Drawing import Point
from System.Windows.Forms import Application, Cursor

from toga_winforms.keys import toga_to_winforms_key, winforms_to_toga_key

from .probe import BaseProbe
from .window import WindowProbe


class AppProbe(BaseProbe):
    supports_key = True
    supports_key_mod3 = False

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.main_window = app.main_window
        # The Winforms Application class is a singleton instance
        assert self.app._impl.native == Application

    @property
    def config_path(self):
        return (
            Path.home()
            / "AppData"
            / "Local"
            / "Tiberius Yak"
            / "Toga Testbed"
            / "Config"
        )

    @property
    def data_path(self):
        return Path.home() / "AppData/Local/Tiberius Yak/Toga Testbed/Data"

    @property
    def cache_path(self):
        return (
            Path.home()
            / "AppData"
            / "Local"
            / "Tiberius Yak"
            / "Toga Testbed"
            / "Cache"
        )

    @property
    def logs_path(self):
        return Path.home() / "AppData/Local/Tiberius Yak/Toga Testbed/Logs"

    @property
    def is_cursor_visible(self):
        # Despite what the documentation says, Cursor.Current never returns null in
        # Windows 10, whether the cursor is over the window or not.
        #
        # The following code is based on https://stackoverflow.com/a/12467292, but it
        # only works when the cursor is over the window.
        form = self.main_window._impl.native
        Cursor.Position = Point(
            form.Location.X + (form.Size.Width // 2),
            form.Location.Y + (form.Size.Height // 2),
        )

        # A small delay is apparently required for the new position to take effect.
        sleep(0.1)

        class POINT(ctypes.Structure):
            _fields_ = [
                ("x", ctypes.c_long),
                ("y", ctypes.c_long),
            ]

        class CURSORINFO(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_uint32),
                ("flags", ctypes.c_uint32),
                ("hCursor", ctypes.c_void_p),
                ("ptScreenPos", POINT),
            ]

        GetCursorInfo = ctypes.windll.user32.GetCursorInfo
        GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]

        info = CURSORINFO()
        info.cbSize = ctypes.sizeof(info)
        if not GetCursorInfo(ctypes.byref(info)):
            raise RuntimeError("GetCursorInfo failed")

        # `flags` is 0 or 1 in local testing, but the GitHub Actions runner always
        # returns 2 ("the system is not drawing the cursor because the user is providing
        # input through touch or pen instead of the mouse"). hCursor is more reliable.
        return info.hCursor is not None

    def is_full_screen(self, window):
        return WindowProbe(self.app, window).is_full_screen

    def content_size(self, window):
        return WindowProbe(self.app, window).content_size

    def _menu_item(self, path):
        item = self.main_window._impl.native.MainMenuStrip
        for i, label in enumerate(path):
            children = getattr(item, "Items" if i == 0 else "DropDownItems")
            child_labels = [child.Text for child in children]
            try:
                child_index = child_labels.index(label)
            except ValueError:
                raise AssertionError(
                    f"no item named {path[:i+1]}; options are {child_labels}"
                ) from None
            item = children[child_index]

        return item

    def _activate_menu_item(self, path):
        self._menu_item(path).OnClick(EventArgs.Empty)

    def activate_menu_exit(self):
        self._activate_menu_item(["File", "Exit"])

    def activate_menu_about(self):
        self._activate_menu_item(["Help", "About Toga Testbed"])

    async def close_about_dialog(self):
        await WindowProbe(self.app, self.main_window)._close_dialog("\n")

    def activate_menu_visit_homepage(self):
        self._activate_menu_item(["Help", "Visit homepage"])

    def assert_menu_item(self, path, *, enabled=True):
        assert self._menu_item(path).Enabled == enabled

    def assert_system_menus(self):
        self.assert_menu_item(["File", "Preferences"], enabled=False)
        self.assert_menu_item(["File", "Exit"])

        self.assert_menu_item(["Help", "Visit homepage"])
        self.assert_menu_item(["Help", "About Toga Testbed"])

    def activate_menu_close_window(self):
        pytest.xfail("This platform doesn't have a window management menu")

    def activate_menu_close_all_windows(self):
        pytest.xfail("This platform doesn't have a window management menu")

    def activate_menu_minimize(self):
        pytest.xfail("This platform doesn't have a window management menu")

    def keystroke(self, combination):
        return winforms_to_toga_key(toga_to_winforms_key(combination))
