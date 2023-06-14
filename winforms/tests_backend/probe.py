import asyncio

from System.Drawing import FontFamily, SystemFonts

from toga.fonts import CURSIVE, FANTASY, MONOSPACE, SANS_SERIF, SERIF, SYSTEM


class BaseProbe:
    def assert_font_family(self, expected):
        assert self.font.family == {
            CURSIVE: "Comic Sans MS",
            FANTASY: "Impact",
            MONOSPACE: FontFamily.GenericMonospace.Name,
            SANS_SERIF: FontFamily.GenericSansSerif.Name,
            SERIF: FontFamily.GenericSerif.Name,
            SYSTEM: SystemFonts.DefaultFont.FontFamily.Name,
        }.get(expected, expected)

    async def redraw(self, message=None, delay=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Winforms style changes always take effect immediately.

        # If we're running slow, wait for a second
        if self.app.run_slow:
            delay = 1

        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)
