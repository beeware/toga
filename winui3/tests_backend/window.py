import asyncio
from ctypes import byref, sizeof, windll
from typing import Literal

from pytest import approx, skip
from win32more.Microsoft.UI.Interop import GetWindowFromWindowId
from win32more.Microsoft.UI.Windowing import (
    AppWindowPresenterKind,
    OverlappedPresenterState,
)
from win32more.Microsoft.UI.Xaml import Window as NativeWindow
from win32more.Windows.Win32.Foundation import RECT
from win32more.Windows.Win32.UI.WindowsAndMessaging import (
    MENUITEMINFOW,
    MFS_DISABLED,
    MIIM_STATE,
    SC_CLOSE,
    TITLEBARINFOEX,
    WM_DPICHANGED,
    WM_GETTITLEBARINFOEX,
    GetMenuItemInfo,
    GetSystemMenu,
    SetForegroundWindow,
)

from toga import Box, Size, Window
from toga.constants import REBECCAPURPLE

from .probe import BaseProbe


class WindowProbe(BaseProbe):
    supports_closable = True
    supports_minimizable = True
    supports_move_while_hidden = True
    supports_unminimize = True
    supports_minimize = True
    supports_placement = True
    supports_as_image = False
    supports_focus = True
    fullscreen_presentation_equal_size = True
    maximize_fullscreen_presentation_equal_size = False

    def __init__(self, app, window):
        self.app = app
        self.window = window
        self.impl = window._impl
        super().__init__(window._impl.native)
        assert isinstance(self.native, NativeWindow)

    @property
    def _hwnd(self):
        return GetWindowFromWindowId(self.impl.native.AppWindow.Id)

    async def wait_for_window(self, message, state=None):
        # A small delay to allow the window to resize.
        await self.redraw(message, delay=0.1)

        if state:
            timeout = 5
            polling_interval = 0.1
            exception = None
            loop = asyncio.get_running_loop()
            start_time = loop.time()
            while (loop.time() - start_time) < timeout:
                try:
                    assert self.instantaneous_state == state
                    return
                except AssertionError as e:
                    exception = e
                    await asyncio.sleep(polling_interval)
                    continue
                raise exception

    async def cleanup(self):
        self.window.close()
        await self.redraw("Closing window")

    def title_bar_object_midpoint(self, type: Literal["maximize", "minimize", "close"]):
        type_dict = {"maximize": 3, "minimize": 2, "close": 5}
        index = type_dict[type]

        info = TITLEBARINFOEX()
        info.cbSize = sizeof(TITLEBARINFOEX)
        windll.user32.SendMessageW(self._hwnd, WM_GETTITLEBARINFOEX, 0, byref(info))

        rect = info.rgrect[index]
        return (int((rect.left + rect.right) / 2), int((rect.top + rect.bottom) / 2))

    async def close(self):
        # The window Closing event is not triggered when self.native.Close() is
        # called directly. So click on the close button instead.
        midpoint = self.title_bar_object_midpoint("close")
        SetForegroundWindow(self._hwnd)
        await self._send_click(*midpoint)

    @property
    def content_size(self):
        actual_size = self.impl.container_native.ActualSize

        return Size(actual_size.X, actual_size.Y)

    @property
    def is_resizable(self):
        presenter, _ = self.impl._presenter
        return presenter.IsResizable

    ####################################################################################
    # State changing
    ####################################################################################

    @property
    def instantaneous_state(self):
        return self.impl.get_window_state(in_progress_state=False)

    async def maximize(self):
        midpoint = self.title_bar_object_midpoint("minimize")
        SetForegroundWindow(self._hwnd)
        await self._send_click(*midpoint)

    async def minimize(self):
        midpoint = self.title_bar_object_midpoint("minimize")
        SetForegroundWindow(self._hwnd)
        await self._send_click(*midpoint)

    @property
    def is_minimizable(self):
        presenter, _ = self.impl._presenter
        return presenter.IsMinimizable

    @property
    def is_minimized(self):
        presenter, _ = self.impl._presenter
        return (
            presenter.Kind == AppWindowPresenterKind.Overlapped
            and presenter.State == OverlappedPresenterState.Minimized
        )

    def unminimize(self):
        presenter, _ = self.impl._presenter
        presenter.Restore()

    def has_toolbar(self):
        skip("Toolbars are not implemented on on toga_winui3 yet.")

    def mock_dpi_change(self, window, mock_dpi):
        # There are no Microsoft supported ways to programmatically change monitor DPIs.
        # The method here is to calculate the bounding rectangle for the scaled window,
        # and send the WM_DPICHANGED message manually. The `self._dpi` property of the
        # window is monkeypatched to return the mock_dpi. This will allow the minimum
        # window size to be correctly calculated.

        dpi_ratio = mock_dpi / self.impl._dpi
        x = window.native.AppWindow.Position.X
        y = window.native.AppWindow.Position.Y

        # The overall window is scaled linearly.
        scaled_width = round(window.native.AppWindow.Size.Width * dpi_ratio)
        scaled_height = round(window.native.AppWindow.Size.Height * dpi_ratio)

        rect = RECT(x, y, x + scaled_width, y + scaled_height)

        # Monkeypatch the DPI property.
        type(window)._dpi = int(mock_dpi)

        windll.user32.SendMessageW(window._hwnd, WM_DPICHANGED, mock_dpi, byref(rect))

    async def assert_system_dpi_change(self, get_probe, mock_scale):
        # WinUI 3 uses CSS pixels for measurements for the layout _within_ a window, but
        # physical pixels for measurements _external_ to the window. From a Toga point
        # of view, DPI scaling is all handled internally except for minimum size
        # constraints. So this test only deals with the window size.

        mock_dpi = int(mock_scale * 96)
        if mock_dpi == self.impl._dpi:
            return
        dpi_ratio = mock_dpi / self.impl._dpi

        # Create a simple window for testing, and ensure that it is set to the minimum
        # size.
        box = Box(background_color=REBECCAPURPLE, width=400, height=300)
        window_interface = Window(content=box, size=(10, 10))
        window_interface.show()
        window = window_interface._impl

        original_dpi_property = type(window)._dpi
        original_size = window.native.AppWindow.Size

        self.mock_dpi_change(window, mock_dpi)

        # Check that the window size has been correctly resized.
        scaled_size = window.native.AppWindow.Size
        assert original_size.Width * dpi_ratio == approx(scaled_size.Width, abs=1)
        assert original_size.Height * dpi_ratio == approx(scaled_size.Height, abs=1)

        # Check that the window size still has the minimum size.
        window.size = Size(10, 10)
        min_size = window.native.AppWindow.Size
        assert min_size.Width == approx(scaled_size.Width, abs=1)
        assert min_size.Height == approx(scaled_size.Height, abs=1)

        # Restore the _dpi property of the Window class.
        type(window)._dpi = original_dpi_property

    @property
    def is_closable(self):
        hmenu = GetSystemMenu(self._hwnd, False)
        menu_item_info = MENUITEMINFOW()
        menu_item_info.cbSize = sizeof(MENUITEMINFOW)
        menu_item_info.fMask = MIIM_STATE

        GetMenuItemInfo(hmenu, SC_CLOSE, False, byref(menu_item_info))
        return menu_item_info.fState & MFS_DISABLED == 0
