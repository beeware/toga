import asyncio
from ctypes import byref, sizeof

from pytest import approx
from win32more.Windows.Win32.Foundation import POINT
from win32more.Windows.Win32.UI.Input.KeyboardAndMouse import (
    INPUT,
    INPUT_KEYBOARD,
    INPUT_MOUSE,
    KEYBDINPUT,
    KEYEVENTF_KEYUP,
    MOUSEEVENTF_LEFTDOWN,
    MOUSEEVENTF_LEFTUP,
    MOUSEINPUT,
    VK_ESCAPE,
    VK_RETURN,
    SendInput,
)
from win32more.Windows.Win32.UI.WindowsAndMessaging import (
    GetCursorPos,
    SetCursorPos,
)

import toga


class BaseProbe:
    def __init__(self, native=None):
        self.native = native
        self._click_count = 0

    def approx_width(self, width):
        return approx(width, rel=0.01)

    def approx_height(self, height):
        return approx(height, rel=0.01)

    async def redraw_staging(self):
        """Wait until any property staging is finished."""
        widgets = toga.App.app.widgets.values()
        staging_areas = {widget._impl.container.staging_area for widget in widgets}

        def staging_complete():
            for staging_area in staging_areas:
                if len(staging_area._native_widgets) > 0:
                    return False

            return True

        for _ in range(50):
            if staging_complete():
                break
            await asyncio.sleep(0.02)

    async def redraw_resizing(self):
        """Wait until any resizing is finished."""
        try:
            width = self.native.Width
            height = self.native.Height
        except AttributeError:
            return

        def resizing_complete():
            return (
                width - 1 < self.native.ActualWidth < width + 1
                and height - 1 < self.native.ActualHeight < height + 1
            )

        for _ in range(50):
            if resizing_complete():
                break
            await asyncio.sleep(0.02)

    async def redraw(self, message=None, delay=0, wait_for=None):
        """Request a redraw of the app, waiting until that redraw has completed."""

        await self.redraw_staging()

        await self.redraw_resizing()

        # If we're running slow, or we have a wait condition,
        # wait for at least a second
        if toga.App.app.run_slow or wait_for:
            delay = max(1, delay)

        if delay or wait_for:
            print("Waiting for redraw" if message is None else message)
            if toga.App.app.run_slow or wait_for is None:
                await asyncio.sleep(delay)
            else:
                delta = 0.1
                interval = 0.0
                while not wait_for() and interval < delay:
                    await asyncio.sleep(delta)
                    interval += delta
        else:
            # Sleep even if the delay is zero: this allows any pending callbacks on the
            # event loop to run.
            await asyncio.sleep(0)

    def _set_cursor_position(self, x, y):
        # x and y are in screen coordinates.
        point = POINT()
        GetCursorPos(byref(point))

        # Only move the cursor if necessary.
        if x != point.x or y != point.y:
            SetCursorPos(x, y)

    def _send_input(self, input):
        return_value = SendInput(1, input, sizeof(input))
        if return_value != 1:
            raise OSError("SendInput failed.")

    async def _send_click(self, x, y):
        # x and y are in screen coordinates.

        # Move x to avoid double clicks.
        x_shifted = x - 3 + 6 * self._click_count
        self._click_count = (self._click_count + 1) % 2

        self._set_cursor_position(x_shifted, y)

        mouse_input = INPUT()
        mouse_input.type = INPUT_MOUSE
        mouse_input.Anonymous.mi = MOUSEINPUT()

        message_list = [MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP]

        async def click():
            for message in message_list:
                mouse_input.Anonymous.mi.dwFlags = message
                self._send_input(mouse_input)

        await click()

        await asyncio.sleep(0.05)

        # DEBUG ARM64
        await asyncio.sleep(1)

    async def _send_key(self, key_code, down=True, up=True):
        key_input = INPUT()
        key_input.type = INPUT_KEYBOARD
        key_input.Anonymous.ki = KEYBDINPUT()
        key_input.Anonymous.ki.wVk = key_code

        if down:
            self._send_input(key_input)

        if up:
            key_input.Anonymous.ki.dwFlags = KEYEVENTF_KEYUP
            self._send_input(key_input)

        await asyncio.sleep(0.1)

        # DEBUG ARM64
        await asyncio.sleep(1)

    async def _keyboard_select(self):
        await self._send_key(VK_RETURN)

    async def _keyboard_escape(self):
        await self._send_key(VK_ESCAPE)
