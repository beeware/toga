import asyncio

from System.Windows.Forms import SendKeys

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
        if self.app.run_slow:
            delay = 1

        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    @property
    def scale_factor(self):
        return self.native.CreateGraphics().DpiX / 96

    async def type_character(self, char, *, ctrl=False):
        try:
            key_code = KEY_CODES[char]
        except KeyError:
            assert len(char) == 1, char
            key_code = char

        if ctrl:
            key_code = "^" + key_code

        SendKeys.SendWait(key_code)
