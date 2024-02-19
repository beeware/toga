import asyncio

from System import IntPtr
from System.Drawing import Graphics
from System.Windows.Forms import SendKeys

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
    async def redraw(self, message=None, delay=0):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Winforms style changes always take effect immediately.

        # If we're running slow, wait for a second
        if toga.App.app.run_slow:
            delay = max(1, delay)

        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    @property
    def scale_factor(self):
        # Does the same thing as `return self.native.CreateGraphics().DpiX / 96`
        return Graphics.FromHdc(Graphics.FromHwnd(IntPtr.Zero).GetHdc()).DpiX / 96

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
        assert image_size == (size[0] * self.scale_factor, size[1] * self.scale_factor)
