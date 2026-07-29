import asyncio
from ctypes import byref, sizeof, windll
from typing import Literal

from win32more.Microsoft.UI.Interop import GetWindowFromWindowId
from win32more.Microsoft.UI.Windowing import (
    AppWindowPresenterKind,
    OverlappedPresenterState,
)
from win32more.Microsoft.UI.Xaml import Window as NativeWindow
from win32more.Windows.Win32.UI.WindowsAndMessaging import (
    TITLEBARINFOEX,
    WM_GETTITLEBARINFOEX,
    SetForegroundWindow,
)

from toga import Size

from .probe import BaseProbe


class WindowProbe(BaseProbe):
    supports_closable = False  # FIXME: Use Win32
    supports_minimizable = True
    supports_move_while_hidden = True
    supports_unminimize = True
    supports_minimize = True
    supports_placement = True
    supports_as_image = True
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

    async def wait_for_window(
        self,
        message,
        state=None,
    ):
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
