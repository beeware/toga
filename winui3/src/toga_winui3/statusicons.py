from ctypes import byref, sizeof, wintypes as wt

from win32more.Microsoft.UI.Interop import GetWindowFromWindowId
from win32more.Microsoft.UI.Windowing import OverlappedPresenter
from win32more.Microsoft.UI.Xaml.Controls import (
    MenuFlyout,
    MenuFlyoutItem,
    MenuFlyoutSeparator,
    MenuFlyoutSubItem,
    RelativePanel,
)
from win32more.Windows.Foundation import Point
from win32more.Windows.Graphics import PointInt32, SizeInt32
from win32more.Windows.Win32.Foundation import POINT
from win32more.Windows.Win32.Graphics.Gdi import ScreenToClient
from win32more.Windows.Win32.UI.WindowsAndMessaging import (
    IDC_ARROW,
    WM_APP,
    WM_NCDESTROY,
    LoadCursorW,
    SetCursor,
    SetForegroundWindow,
)

from toga import App, Icon
from toga.command import Group, Separator

from .libs import win32constants as wc, win32structures as ws
from .libs.comctl32 import (
    DefSubclassProc,
    RemoveWindowSubclass,
    SetWindowSubclass,
)
from .libs.misc import get_x_lparam, get_y_lparam, loword
from .libs.nativeevents import events_handled
from .libs.shell import Shell_NotifyIconW


class StatusIcon:
    """The WinUI 3 backend implementation of the StatusIcon class.

    The WinUI 3 API does not provide a class that could be used as a StatusIcon (see
    for example https://github.com/microsoft/microsoft-ui-xaml/issues/2020), so a
    Win32 approach is used.
        Moreover, the needed subclassing functionality is not provided in the Win32
    metadata, so it does not appear in win32more. Hence the need to load it directly
    using ctypes.
    """

    def __init__(self, interface):
        self.interface = interface
        self.native_window = None

    def set_icon(self, icon: Icon):
        if self.native_window is not None:
            notify_icon_data = self._notify_icon_data(self._icon_handle(icon))
            Shell_NotifyIconW(wc.NIM_MODIFY, byref(notify_icon_data))

    def create(self):
        # Create a WinUI 3 Window instance to receive the messages.
        self.native_window = App.app._impl.native_instance.CreateWindow()

        # Hide the Window.
        self.native_window.AppWindow.Resize(SizeInt32(1, 1))
        self.native_window.AppWindow.Move(PointInt32(wc.SHRT_MAX - 1, wc.SHRT_MAX - 1))
        self.native_window.AppWindow.IsShownInSwitchers = False

        presenter = self.native_window.AppWindow.Presenter
        overlapped_presenter = OverlappedPresenter(value=presenter.value)
        overlapped_presenter.SetBorderAndTitleBar(False, False)

        # Setting "always on top" is needed for any menus will appear at the top.
        overlapped_presenter.IsAlwaysOnTop = True

        # Subclass the native_window to receive the WM_COMMAND messages.
        self._pfn_subclass = ws.SUBCLASSPROC(self._subclass_proc)
        SetWindowSubclass(self._hwnd, self._pfn_subclass, 0, 0)

        # Set the icon.
        icon_handle = self._icon_handle(self.interface.icon)
        notify_icon_data = self._notify_icon_data(icon_handle)
        Shell_NotifyIconW(wc.NIM_ADD, byref(notify_icon_data))

        # NOTIFYICON_VERSION_4 is the recommended version from Windows Vista onwards.
        notify_icon_data._.uVersion = wc.NOTIFYICON_VERSION_4
        Shell_NotifyIconW(wc.NIM_SETVERSION, byref(notify_icon_data))

    def _icon_handle(self, icon: Icon):
        return icon._impl.handle if icon else App.app.icon._impl.handle

    def _notify_icon_data(self, icon_handle):
        """Creates a NOTIFYICONDATAW instance for a given icon."""
        notify_icon_data = ws.NOTIFYICONDATAW()
        notify_icon_data.cbSize = sizeof(ws.NOTIFYICONDATAW)
        notify_icon_data.hWnd = self._hwnd
        notify_icon_data.uID = 1
        notify_icon_data.uCallbackMessage = WM_APP + 1
        notify_icon_data.uFlags = wc.NIF_ICON | wc.NIF_MESSAGE
        notify_icon_data.hIcon = icon_handle
        return notify_icon_data

    def remove(self):
        notify_icon_data = self._notify_icon_data(None)
        Shell_NotifyIconW(wc.NIM_DELETE, byref(notify_icon_data))
        self.native_window.Close()
        self.native_window = None

    @property
    def _hwnd(self):
        return GetWindowFromWindowId(self.native_window.AppWindow.Id)

    def _subclass_proc(
        self,
        hWnd: int,
        uMsg: int,
        wParam: int,
        lParam: int,
        uIdSubclass: int,
        dwRefData: int,
    ):
        # Remove the window subclass in the way recommended by Raymond Chen here:
        # https://devblogs.microsoft.com/oldnewthing/20031111-00/?p=41883
        if uMsg == WM_NCDESTROY:
            RemoveWindowSubclass(hWnd, self._pfn_subclass, uIdSubclass)

        elif uMsg == WM_APP + 1:
            message = loword(lParam)
            if message == wc.NIN_SELECT:
                self.native_event_click(get_x_lparam(wParam), get_y_lparam(wParam))

        # Call the original window procedure
        return DefSubclassProc(
            wt.HWND(hWnd),
            wt.UINT(uMsg),
            wt.WPARAM(wParam),
            wt.LPARAM(lParam),
        )

    def native_event_click(self, x, y): ...


class SimpleStatusIcon(StatusIcon):
    def native_event_click(self, x, y):
        self.interface.on_press()


class MenuStatusIcon(StatusIcon):
    def __init__(self, interface):
        super().__init__(interface)
        self._native_menu = None
        self.native_content = None

    def create(self):
        super().create()
        self.native_content = RelativePanel()
        self.native_window.Content = self.native_content

    @property
    def native_menu(self):
        return self._native_menu

    @native_menu.setter
    def native_menu(self, native_menu_instance: MenuFlyout):
        assert isinstance(native_menu_instance, MenuFlyout)

        native_menu_instance.event_handler.Closing += self.native_event_closing
        self._native_menu = native_menu_instance

    def native_event_closing(self, sender, args):
        # Hide the parent window immediately after a menu item is selected.
        self.native_window.AppWindow.Hide()

    def native_event_click(self, x, y):
        coords = POINT(x, y)
        ScreenToClient(self._hwnd, byref(coords))
        relative_coords = Point(coords.x / 2, coords.y / 2)

        # Show the menu. The parent window must be visible for the menu to be visible.
        self.native_window.AppWindow.Show()
        SetForegroundWindow(self._hwnd)
        self.native_menu.ShowAt(self.native_content, relative_coords)

        # Reload the standard cursor to prevent the busy cursor showing.
        h_cursor = LoadCursorW(None, IDC_ARROW)
        SetCursor(h_cursor)


class StatusIconSet:
    def __init__(self, interface):
        """The WinUI 3 implementation of an ordered collection of status icons."""
        self.interface = interface

    def _submenu(self, group, group_cache):
        try:
            return group_cache[group]
        except KeyError as exc:
            if group is None:
                raise ValueError("Unknown top level item") from exc
            else:
                parent_menu = self._submenu(group.parent, group_cache)

                submenu = MenuFlyoutSubItem()
                submenu.Text = group.text

                parent_menu.Items.Append(submenu)

            group_cache[group] = submenu
        return submenu

    def create(self):
        """Create

        This is called directly in App._startup() and also when the status icon command
        set is changed.
        """

        # Menu status icons are the only icons that have extra construction needs.
        # Clear existing menus
        for menu_status_icon in self.interface._menu_status_icons:
            menu_status_icon._impl.native_menu = events_handled(MenuFlyout)

        # Determine the primary status icon.
        primary_group = self.interface._primary_menu_status_icon
        if primary_group is None:  # pragma: no cover
            # If there isn't at least one menu status icon, then there aren't any menus
            # to populate. This can't be replicated in the testbed.
            return

        # Add the menu status items to the cache
        group_cache = {
            menu_status_icon: menu_status_icon._impl.native_menu
            for menu_status_icon in self.interface._menu_status_icons
        }
        # Map the COMMANDS group to the primary status icon's menu.
        group_cache[Group.COMMANDS] = primary_group._impl.native_menu

        for cmd in self.interface.commands:
            try:
                submenu = self._submenu(cmd.group, group_cache)
            except ValueError as exc:
                raise ValueError(
                    f"Command {cmd.text!r} does not belong to a current status icon "
                    "group."
                ) from exc
            else:
                if isinstance(cmd, Separator):
                    menu_item = MenuFlyoutSeparator()
                else:
                    menu_item = cmd._impl.create_menu_item(0, MenuFlyoutItem)

                submenu.Items.Append(menu_item)
