import asyncio
from ctypes import byref, sizeof, windll
from typing import Literal
from unittest.mock import Mock

from pytest import approx, skip
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
from toga.constants import WindowState

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

    async def assert_system_dpi_change_for_state(self, mock_scale):
        # WinUI 3 uses CSS pixels for measurements for the layout within a window, but
        # physical pixels for measurements external to the window. From a Toga point of
        # view, DPI scaling is all handled internally except for minimum size
        # constraints. So this test only deals with the window size.
        #   There are no Microsoft supported ways to programmatically change monitor
        # DPIs. The method here is to monkeypatch the window's DPI and then manually
        # fire the DPI changed event.
        mock_dpi = int(mock_scale * 96)
        if mock_dpi == self.impl._dpi:
            return

        # Store the original values
        dpi_ratio = mock_dpi / self.impl._dpi
        original_size = self.window.size
        original_dpi_property = type(self.impl)._dpi

        # Monkeypatch the DPI property.
        type(self.impl)._dpi = int(mock_scale * 96)

        # Add a `on_resize` handler.
        on_resize_handler = Mock()
        self.window.on_resize_handler = on_resize_handler

        # Manually trigger the DPI changed event.
        self.impl.native_event_xaml_root_changed(None, None)
        await self.redraw(
            f"Simulated DPI change: Window should be {dpi_ratio}x its original size",
            delay=0.1,
        )

        # Save the scaled size. There is an adjustment for the normal state, since the
        # DPI has not actually been changed.
        if self.window.state == WindowState.NORMAL:
            scaled_size = self.window.size * float(1 / dpi_ratio)
        elif self.window.state == WindowState.MAXIMIZED:
            scaled_size = self.window.size

        # Restore the DPI property.
        type(self.impl)._dpi = original_dpi_property

        # Manually trigger the DPI changed event.
        self.impl.native_event_xaml_root_changed(None, None)

        await self.redraw(
            "Simulated DPI change: Window should be its original size",
            delay=0.1,
        )

        # There are difference in decor, etc. for the different scales which isn't
        # tested here. Accept within 10% of the size.
        assert scaled_size == approx(original_size, rel=0.1)

        # The original size should be restored.
        assert original_size == self.window.size

        # A DPI event should not trigger a on_resize event since the Toga size never
        # changes.
        on_resize_handler.assert_not_called()

    async def assert_system_dpi_change(self, get_probe, mock_scale):
        # Test DPI change for the normal window state.
        await self.assert_system_dpi_change_for_state(mock_scale)

        # Test DPI change while maximized.
        self.window.state = WindowState.MAXIMIZED
        await self.wait_for_window(
            "Maximizing window before simulating another DPI change."
        )

        await self.assert_system_dpi_change_for_state(mock_scale)

        self.window.state = WindowState.NORMAL
        await self.wait_for_window("Returning window to the normal state.")
