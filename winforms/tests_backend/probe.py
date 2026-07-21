import asyncio

from pytest import approx
from System.Windows.Forms import SendKeys

import toga
from toga_winforms.libs.user32 import GetDpiForWindow

from .fonts import FontMixin

KEY_CODES = {
    f"<{name}>": f"{{{name.upper()}}}"
    for name in ["esc", "up", "down", "left", "right", "home", "end"]
}
KEY_CODES.update(
    {
        "\n": "{ENTER}",
    }
)


class BaseProbe(FontMixin):
    fixed_height = None

    def __init__(self, native=None):
        self.native = native

    def approx_width(self, width):
        return approx(width, rel=0.01)

    def approx_height(self, height):
        return approx(height, rel=0.01)

    async def redraw(self, message=None, delay=0, wait_for=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Winforms style changes always take effect immediately.

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

    @property
    def x(self):
        return round(self.native.Left / self.scale_factor)

    @property
    def y(self):
        return round(self.native.Top / self.scale_factor)

    @property
    def width(self):
        return round(self.native.Width / self.scale_factor)

    @property
    def height(self):
        return round(self.native.Height / self.scale_factor)

    def assert_width(self, min_width, max_width):
        assert min_width <= self.width <= max_width

    def assert_height(self, min_height, max_height):
        if self.fixed_height is not None:
            assert self.height == approx(self.fixed_height, rel=0.1)
        else:
            assert min_height <= self.height <= max_height

    @property
    def scale_factor(self):
        return GetDpiForWindow(int(self.native.Handle.ToString())) / 96

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

    def assert_image_size(self, image_size, size, screen, window=None):
        scale_factor = self.get_scale_factor(native_screen=screen._impl.native)
        assert image_size == (
            round(size[0] * scale_factor),
            round(size[1] * scale_factor),
        )
