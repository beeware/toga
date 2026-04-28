import asyncio
from ctypes import c_wchar_p
from ctypes.wintypes import HWND, POINT

import System.Windows.Forms as WinForms

from toga.handlers import WeakrefCallable

from .libs import user32 as u32, win32constants as wc


class ContextMenu:
    """A Win32-based context menu.

    This Win32-based menu is preferred over the WinForms ContextMenuStrip since the
    style of the WinForms version has not been updated with recent version of Windows.
    This has been an unresolved issue since at least Dec 2019:
        - https://github.com/dotnet/winforms/issues/2476

    Attributes:
        widget: The Toga WinForms widget to be assigned to.
        actions: A function of the form actions(x: int, y: int) that returns a list that
            contains None values and pairs (label: str, action: Callable[[], None]).
            Each item is a row on the menu list, with None values defining a separators.
    """

    def __init__(self, widget, actions):
        self.widget = widget
        self.winforms_handle_created(None, None)
        widget.native.HandleCreated += WeakrefCallable(self.winforms_handle_created)
        widget.native.MouseClick += WeakrefCallable(self.winforms_mouse_click)

        self.actions = actions

    def winforms_handle_created(self, sender, e):
        """Create the menu when a the widget's handle is created."""
        self._native_hwnd = HWND(int(self.widget.native.Handle.ToString()))

    def winforms_mouse_click(self, sender, e):
        if e.Button != WinForms.MouseButtons.Right or e.Clicks != 1:
            return

        actions_list = self.actions(e.X, e.Y)
        pt = POINT(e.X, e.Y)
        u32.ClientToScreen(self._native_hwnd, pt)

        # Show the popup using the inner loop of the WinForms proactor.
        asyncio.get_event_loop().start_inner_loop(self._show, pt.x, pt.y, actions_list)

    def _show(self, x: int, y: int, actions_list):
        hmenu = u32.CreatePopupMenu()
        for index, action_pair in enumerate(actions_list, start=1):
            if action_pair is None:
                u32.AppendMenuW(hmenu, wc.MF_SEPARATOR, index, c_wchar_p(""))
            else:
                u32.AppendMenuW(hmenu, wc.MF_STRING, index, c_wchar_p(action_pair[0]))

        uFlags = (
            wc.TPM_LEFTALIGN
            | wc.TPM_TOPALIGN
            | wc.TPM_RIGHTBUTTON
            | wc.TPM_HORIZONTAL
            | wc.TPM_VERTICAL
            | wc.TPM_RETURNCMD
        )

        u32.SetForegroundWindow(self._native_hwnd)
        menu_selection = u32.TrackPopupMenuEx(
            hmenu, uFlags, x, y, self._native_hwnd, None
        )

        u32.DestroyMenu(hmenu)

        if menu_selection > 0:
            actions_list[menu_selection - 1][1]()
