import ctypes
from pathlib import Path
from time import sleep

import PIL.Image
import pytest
from System import EventArgs
from System.Drawing import Bitmap, Point
from System.Windows.Forms import Application, Cursor, ToolStripSeparator

import toga
from toga_winforms.keys import toga_to_winforms_key, winforms_to_toga_key

from .dialogs import DialogsMixin
from .probe import BaseProbe
from .window import WindowProbe


class AppProbe(BaseProbe, DialogsMixin):
    supports_key = True
    supports_key_mod3 = False
    supports_current_window_assignment = True

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

    def assert_app_icon(self, icon):
        for window in self.app.windows:
            # We have no real way to check we've got the right icon; use pixel peeping as a
            # guess. Construct a PIL image from the current icon.
            img = toga.Image(
                Bitmap.FromHicon(window._impl.native.Icon.Handle)
            ).as_format(PIL.Image.Image)

            if icon:
                # The explicit alt icon has blue background, with green at a point 1/3 into
                # the image
                assert img.getpixel((5, 5)) == (211, 230, 245, 255)
                mid_color = img.getpixel((img.size[0] // 3, img.size[1] // 3))
                assert mid_color == (0, 204, 9, 255)
            else:
                # The default icon is transparent background, and brown in the center.
                assert img.getpixel((5, 5))[3] == 0
                mid_color = img.getpixel((img.size[0] // 2, img.size[1] // 2))
                assert mid_color == (130, 100, 57, 255)

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
        await self.type_character("\n")

    def activate_menu_visit_homepage(self):
        self._activate_menu_item(["Help", "Visit homepage"])

    def assert_menu_item(self, path, *, enabled=True):
        item = self._menu_item(path)
        assert item.Enabled == enabled

        # Check some special cases of menu shortcuts
        try:
            shortcut = {
                ("Other", "Full command"): "Ctrl+1",
                ("Other", "Submenu1", "Disabled"): None,
                ("Commands", "No Tooltip"): "Ctrl+Down",
                ("Commands", "Sectioned"): "Ctrl+Space",
            }[tuple(path)]
        except KeyError:
            pass
        else:
            assert item.ShortcutKeyDisplayString == shortcut

    def assert_menu_order(self, path, expected):
        menu = self._menu_item(path)

        assert len(menu.DropDownItems) == len(expected)
        for item, title in zip(menu.DropDownItems, expected):
            if title == "---":
                assert isinstance(item, ToolStripSeparator)
            else:
                assert item.Text == title

    def assert_system_menus(self):
        self.assert_menu_item(["File", "New Example Document"], enabled=True)
        self.assert_menu_item(["File", "New Read-only Document"], enabled=True)
        self.assert_menu_item(["File", "Open..."], enabled=True)
        self.assert_menu_item(["File", "Save"], enabled=True)
        self.assert_menu_item(["File", "Save As..."], enabled=True)
        self.assert_menu_item(["File", "Save All"], enabled=True)
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

    async def restore_standard_app(self):
        # No special handling needed to restore standard app.
        await self.redraw("Restore to standard app")

    async def open_initial_document(self, monkeypatch, document_path):
        pytest.xfail("Winforms doesn't require initial document support")

    def open_document_by_drag(self, document_path):
        pytest.xfail("Winforms doesn't support opening documents by drag")

    def has_status_icon(self, status_icon):
        return status_icon._impl.native is not None

    def status_menu_items(self, status_icon):
        if status_icon._impl.native.ContextMenu:
            return [
                {
                    "-": "---",
                    "About Toga Testbed": "**ABOUT**",
                    "Exit": "**EXIT**",
                }.get(str(item.Text), str(item.Text))
                for item in status_icon._impl.native.ContextMenu.MenuItems
            ]
        else:
            # It's a button status item
            return None

    def activate_status_icon_button(self, item_id):
        # Winforms doesn't provide an OnClick to trigger clicks, so we have to fake it
        # at the level of the impl.
        self.app.status_icons[item_id]._impl.winforms_click(
            self.app.status_icons[item_id]._impl.native,
            EventArgs.Empty,
        )

    def activate_status_menu_item(self, item_id, title):
        menu = self.app.status_icons[item_id]._impl.native.ContextMenu
        item = {item.Text: item for item in menu.MenuItems}[title]
        item.OnClick(EventArgs.Empty)
