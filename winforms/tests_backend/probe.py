import asyncio
from ctypes import byref, c_void_p, windll, wintypes

from System.Windows.Forms import Screen, SendKeys

import toga

KEY_CODES = {
    f"<{name}>": f"{{{name.upper()}}}"
    for name in ["esc", "up", "down", "left", "right"]
}
KEY_CODES.update(
    {
        "\n": "{ENTER}",
    }
)


class BaseProbe:
    async def redraw(self, message=None, delay=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Winforms style changes always take effect immediately.

        # If we're running slow, wait for a second
        if toga.App.app.run_slow:
            delay = 1

        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    @property
    def scale_factor(self):
        # For ScrollContainer
        if hasattr(self, "native_content"):
            return self.get_scale_factor(
                native_screen=Screen.FromControl(self.native_content)
            )
        # For Windows and others
        else:
            return self.get_scale_factor(native_screen=Screen.FromControl(self.native))

    def get_scale_factor(self, native_screen):
        screen_rect = wintypes.RECT(
            native_screen.Bounds.Left,
            native_screen.Bounds.Top,
            native_screen.Bounds.Right,
            native_screen.Bounds.Bottom,
        )
        windll.user32.MonitorFromRect.restype = c_void_p
        windll.user32.MonitorFromRect.argtypes = [wintypes.RECT, wintypes.DWORD]
        # MONITOR_DEFAULTTONEAREST = 2
        hMonitor = windll.user32.MonitorFromRect(screen_rect, 2)
        pScale = wintypes.UINT()
        windll.shcore.GetScaleFactorForMonitor(c_void_p(hMonitor), byref(pScale))
        return pScale.value / 100

    async def type_character(self, char, *, shift=False, ctrl=False, alt=False):
        try:
            key_code = KEY_CODES[char]
        except KeyError:
            assert len(char) == 1, char
            key_code = char

        if shift:
            key_code = "+" + key_code
        if ctrl:
            key_code = "^" + key_code
        if alt:
            key_code = "%" + key_code

        # This sends keys to the focused window, which isn't necessarily even in the
        # same app. Unfortunately that makes it difficult to run tests in the
        # background.
        SendKeys.SendWait(key_code)

    def assert_image_size(self, image_size, size, screen):
        scale_factor = self.get_scale_factor(native_screen=screen._impl.native)
        assert image_size == (size[0] * scale_factor, size[1] * scale_factor)
