import _overlapped
import asyncio
from ctypes import byref, sizeof, windll, wintypes as wt
from pathlib import Path
from time import sleep

import PIL.Image
import pytest
import toga_winui3.libs.win32structures as ws
from toga_winui3.libs.gdiplus import icon_pixels
from toga_winui3.libs.nativeapp import NativeApp
from toga_winui3.libs.shell import Shell_NotifyIconGetRect
from win32more.Microsoft.UI.Input import InputCursor
from win32more.Microsoft.UI.Interop import GetWindowFromWindowId
from win32more.Microsoft.UI.Xaml import FocusState, Window
from win32more.Microsoft.UI.Xaml.Controls import (
    MenuBarItem,
    MenuFlyout,
    MenuFlyoutItem,
    MenuFlyoutSeparator,
    MenuFlyoutSubItem,
)
from win32more.Windows.Win32.UI.Input.KeyboardAndMouse import (
    VK_B,
    VK_RETURN,
    VK_RWIN,
)
from win32more.Windows.Win32.UI.WindowsAndMessaging import (
    CURSORINFO,
    TITLEBARINFOEX,
    WM_GETICON,
    WM_GETTITLEBARINFOEX,
    GetCursorInfo,
    SendMessageW,
)

import toga

from .probe import BaseProbe


class AppProbe(BaseProbe):
    formal_name = "Toga Testbed (WinUI 3)"
    supports_key = True
    supports_key_mod3 = False
    supports_current_window_assignment = True
    supports_dark_mode = True
    edit_menu_noop_enabled = False
    supports_psutil = True
    beep_delay = 0.1

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.main_window = app.main_window

        # The NativeApp class is a descendant class of the Microsoft.UI.Xaml.Application
        # class, which is a singleton instance.
        assert self.app._impl.native == NativeApp
        assert isinstance(self.app._impl.native_instance, NativeApp)

    @property
    def _hwnd(self):
        """The handle of the main window."""
        return GetWindowFromWindowId(self.main_window._impl.native.AppWindow.Id)

    ####################################################################################
    # Paths
    ####################################################################################

    @property
    def config_path(self):
        return Path.home() / "AppData/Local/Tiberius Yak/Toga Testbed (WinUI 3)/Config"

    @property
    def data_path(self):
        return Path.home() / "AppData/Local/Tiberius Yak/Toga Testbed (WinUI 3)/Data"

    @property
    def cache_path(self):
        return Path.home() / "AppData/Local/Tiberius Yak/Toga Testbed (WinUI 3)/Cache"

    @property
    def logs_path(self):
        return Path.home() / "AppData/Local/Tiberius Yak/Toga Testbed (WinUI 3)/Logs"

    ####################################################################################
    # Menu tests
    ####################################################################################

    def _menu_children(self, menu):
        children = [self._menu_item_casted(child) for child in menu.Items]
        child_labels = [self._menu_item_label(child) for child in children]
        return children, child_labels

    async def _menu_item_open_or_select(self, item, select: bool):
        # Wait to enure that the item can receive the input focus.
        for _ in range(50):
            item.Focus(FocusState.Programmatic)

            if item.FocusState != FocusState.Unfocused:
                break
            await asyncio.sleep(0.01)
        else:
            raise ValueError(f"{item} was never given the input focus.")

        if not select:
            await self._keyboard_select()
            return

        # Make a mutable boolean.
        item_selected = [False]

        def callback(sender, args, item_selected=item_selected):
            item_selected[0] = True

        # A selectable final menu item is always of type MenuFlyoutItem
        selectable_item: MenuFlyoutItem = self._menu_item_casted(item)
        token = selectable_item.add_Click(callback)

        await self._keyboard_select()

        # Wait to enure that the item has been selected.
        for _ in range(50):
            if item_selected[0]:
                selectable_item.remove_Click(token)
                break
            await asyncio.sleep(0.01)
        else:
            selectable_item.remove_Click(token)
            raise ValueError(f"{item} was never selected.")

    async def _menu_item(self, path, open_menus=False):
        """Select a menu item with the given path."""
        # Note that retrieving a submenu's items via menu.Items gives a list of
        # MenuFlyoutItemBase objects. These need to be casted manually to the
        # appropriate types.

        item = self.main_window._impl.menu_native
        for i, label in enumerate(path):
            children, child_labels = self._menu_children(item)

            try:
                child_index = child_labels.index(label)
            except ValueError:
                raise AssertionError(
                    f"no item named {path[: i + 1]}; options are {child_labels}"
                ) from None

            item = children[child_index]

            if open_menus:
                await self._menu_item_open_or_select(item, len(path) == i + 1)

        return item

    def _menu_item_label(self, menu_item):
        if isinstance(menu_item, MenuBarItem):
            return menu_item.Title

        elif type(menu_item) in (MenuFlyoutItem, MenuFlyoutSubItem):
            return menu_item.Text

        return "---"

    def _menu_item_casted(self, menu_item):
        # Note that retrieving a submenu's items via menu.Items gives a list of
        # MenuFlyoutItemBase objects. The actual type of this object could be one of:
        #    - MenuFlyoutSubItem: Has both the Items and the Text attributes.
        #    - MenuFlyoutItem:  Has the Items attribute but not the Text attribute.
        #    - MenuFlyoutSeparator: Doesn't have the Items or the Text attributes.

        # Attempt to cast as MenuFlyoutSubItem
        if isinstance(menu_item, MenuBarItem):
            return menu_item

        try:
            casted = MenuFlyoutSubItem(value=menu_item.value)
            casted.Items  # noqa B018
            return casted
        except OSError:
            pass

        # Attempt to cast as MenuFlyoutItem
        try:
            casted = MenuFlyoutItem(value=menu_item.value)
            casted.Text  # noqa B018
            return casted
        except OSError:
            pass

        # Fallback to MenuFlyoutSeparator
        return MenuFlyoutSeparator(value=menu_item.value)

    async def _activate_menu_item(self, path):
        await self._menu_item(path, open_menus=True)

    async def activate_menu_visit_homepage(self):
        await self._activate_menu_item(["Help", "Visit homepage"])

    async def assert_menu_item(self, path, *, enabled=True):
        item = await self._menu_item(path)
        assert item.IsEnabled == enabled

    async def assert_menu_order(self, path, expected):
        menu = await self._menu_item(path)
        _, child_labels = self._menu_children(menu)

        assert child_labels == expected

    async def assert_system_menus(self):
        await self.assert_menu_item(["File", "New Example Document"], enabled=True)
        await self.assert_menu_item(["File", "New Read-only Document"], enabled=True)
        await self.assert_menu_item(["File", "Open..."], enabled=True)
        await self.assert_menu_item(["File", "Save"], enabled=True)
        await self.assert_menu_item(["File", "Save As..."], enabled=True)
        await self.assert_menu_item(["File", "Save All"], enabled=True)
        await self.assert_menu_item(["File", "Preferences"], enabled=False)
        await self.assert_menu_item(["File", "Exit"])

        await self.assert_menu_item(["Help", "Visit homepage"])
        await self.assert_menu_item(["Help", "About Toga Testbed (WinUI 3)"])

    async def activate_menu_exit(self):
        await self._activate_menu_item(["File", "Exit"])

    async def activate_menu_about(self):
        await self._activate_menu_item(["Help", "About Toga Testbed"])

    def activate_menu_close_window(self):
        pytest.xfail("This platform doesn't have a window management menu")

    def activate_menu_hide(self):
        pytest.xfail("This platform doesn't present a app level hide option in menu.")

    def activate_menu_minimize(self):
        pytest.xfail("This platform doesn't have a window management menu")

    ####################################################################################
    # Cursor visablity
    ####################################################################################

    @property
    def _is_cursor_visible_non_client(self):
        # This method used code from the toga_winforms probe which is based off:
        # https://stackoverflow.com/a/12467292.
        #
        # The documentation recommends using GetCursorInfo to test the visibility of
        # cursors shown/hidden with ShowCursor.
        # https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-showcursor
        # https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-getcursorinfo

        # First, place the cursor in the non-client area. Use SendMessageW from windll
        # to treat LPARAM as a pointer.
        SendMessage = windll.user32.SendMessageW

        # Get the bounding rectangle of the close button.
        title_bar_info = TITLEBARINFOEX()
        title_bar_info.cbSize = sizeof(TITLEBARINFOEX)
        SendMessage(self._hwnd, WM_GETTITLEBARINFOEX, 0, byref(title_bar_info))
        close_rect = title_bar_info.rgrect[5]

        self._set_cursor_position(
            int((close_rect.left + close_rect.right) / 2),
            int((close_rect.top + close_rect.bottom) / 2),
        )

        # A sleep to allow the window messages to propagate.
        sleep(0.1)

        cursor_info = CURSORINFO()
        cursor_info.cbSize = sizeof(CURSORINFO)
        if not GetCursorInfo(byref(cursor_info)):
            raise RuntimeError("GetCursorInfo failed")

        # Visibility *should* be exposed by CursorInfo.flags; but in CI,
        # CursorInfo.flags returns 2 ("the system is not drawing the cursor
        # because the user is providing input through touch or pen instead of
        # the mouse"). In that case, we have to fall back to the backend's
        # boolean representation, because there doesn't appear to be any
        # more reliable mechanism for determining cursor state.
        if cursor_info.flags == 2:
            return self.app._impl._cursor_visible
        else:
            return cursor_info.flags == 1

    @property
    def is_cursor_visible(self):
        # The cursor visibility if has two parts:
        #   1. ShowCursor for the non-client area
        #   2. ProtectedCursor for the client area.

        # Get the cursor visibility of the non-client area.
        is_cursor_visible_non_client = self._is_cursor_visible_non_client

        # Confirm that the cursor visibilities of the client and non-client areas match.
        protected_cursor = self.main_window._impl.native.Content.ProtectedCursor
        if is_cursor_visible_non_client:
            assert protected_cursor is None
        else:
            assert isinstance(protected_cursor, InputCursor)

        return is_cursor_visible_non_client

    ####################################################################################
    # Miscellaneous
    ####################################################################################

    async def assert_event_loop_unregistering(self, loop):
        """Test that events can be unregistered."""
        event = _overlapped.CreateEvent(None, True, False, None)
        fut = loop._proactor.wait_for_handle(event, 10)
        fut.cancel()

        # Wait for the future to be removed from the unregistered list.
        await asyncio.sleep(0.2)
        assert len(loop._proactor._unregistered) == 0

    async def assert_event_loop(self):
        loop = self.app.loop

        await self.assert_event_loop_unregistering(loop)

    async def restore_standard_app(self):
        # No special handling needed to restore standard app.
        await self.redraw("Restore to standard app")

    def assert_app_icon(self, icon):
        # Compare the pixels of `icon` using Pillow to those from the registered icon
        # using GDI+.
        path = toga.Icon(icon if icon else "")._impl.path

        with PIL.Image.open(path).convert("RGBA") as pil_image:
            width_pil, height_pil = pil_image.size
            pixels_pil = pil_image.load()

        for window in self.app.windows:
            hwnd = GetWindowFromWindowId(window._impl.native.AppWindow.Id)
            hicon = SendMessageW(hwnd, WM_GETICON, 0, 0)
            pixels_gdip = icon_pixels(hicon)

            assert width_pil == len(pixels_gdip)
            assert height_pil == len(pixels_gdip[0])

            count = 0
            for x in range(width_pil):
                for y in range(height_pil):
                    if pixels_pil[x, y] == pixels_gdip[x][y]:
                        count += 1

            # There are some difference in how alpha is treated. Accept 97% match
            assert count / (width_pil * height_pil) > 0.97

    def unhide(self):
        pytest.xfail("This platform doesn't have an app level unhide.")

    async def open_initial_document(self, monkeypatch, document_path):
        pytest.xfail("Winforms doesn't require initial document support")

    def open_document_by_drag(self, document_path):
        pytest.xfail("Winforms doesn't support opening documents by drag")

    ####################################################################################
    # Methods relating to StatusIcon
    ####################################################################################

    def has_status_icon(self, status_icon):
        return isinstance(status_icon._impl.native_window, Window)

    async def _get_status_icon_midpoint(self, status_icon) -> tuple[int, int]:
        # `Winkey + B` then `Enter` opens the notification icon overflow tray.
        await self._send_key(VK_RWIN, up=False)
        await self._send_key(VK_B)
        await self._send_key(VK_RWIN, down=False)
        await self._send_key(VK_RETURN)

        notify_icon_identifier = ws.NOTIFYICONIDENTIFIER()
        notify_icon_identifier.cbSize = sizeof(ws.NOTIFYICONIDENTIFIER())
        notify_icon_identifier.hWnd = status_icon._impl._hwnd
        notify_icon_identifier.uID = 1

        def get_midpoint():
            rect = wt.RECT()
            Shell_NotifyIconGetRect(byref(notify_icon_identifier), byref(rect))

            x = int((rect.left + rect.right) / 2)
            y = int((rect.top + rect.bottom) / 2)
            return (x, y)

        # Make sure the overflow tray is fully open by tracking when the midpoint stops
        # moving.
        midpoint = get_midpoint()
        for _ in range(10):
            await asyncio.sleep(0.05)

            new_midpoint = get_midpoint()

            if midpoint == new_midpoint:
                break
            midpoint = new_midpoint

        return midpoint

    def _get_status_menu_items(self, status_icon):
        native_menu = getattr(status_icon._impl, "native_menu", None)

        if native_menu:
            assert isinstance(native_menu, MenuFlyout)
            return [self._menu_item_casted(child) for child in native_menu.Items]

    def status_menu_items(self, status_icon):
        items = self._get_status_menu_items(status_icon)

        if items is None:
            return

        def process_text(text):
            return {
                "About Toga Testbed (WinUI 3)": "**ABOUT**",
                "Exit": "**EXIT**",
            }.get(text, text)

        return [
            "---"
            if isinstance(child, MenuFlyoutSeparator)
            else process_text(child.Text)
            for child in items
        ]

    async def activate_status_icon_button(self, item_id):
        # Click on the status icon.
        status_icon = self.app.status_icons[item_id]

        # There is an issue on the x86_64 CI runner where the method used here to open
        # the system tray overflow menu doesn't work properly the first time. So, open
        # it twice.
        midpoint = await self._get_status_icon_midpoint(status_icon)
        await self._keyboard_escape()

        midpoint = await self._get_status_icon_midpoint(status_icon)
        await self._send_click(*midpoint)

        # Close the overflow tray
        await self._keyboard_escape()

    async def activate_status_menu_item(self, item_id, title):
        # Click on the status icon.
        status_icon = self.app.status_icons[item_id]
        midpoint = await self._get_status_icon_midpoint(status_icon)
        await self._send_click(*midpoint)

        items = self._get_status_menu_items(status_icon)
        index = self.status_menu_items(status_icon).index(title)

        # Make sure that the menu item is selected before sending select command.
        for _ in range(100):
            items[index].Focus(FocusState.Programmatic)
            if items[index].FocusState != 0:
                break
            await asyncio.sleep(0.01)

        await self._keyboard_select()

        # Close the overflow tray
        await self._keyboard_escape()
