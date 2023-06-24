import asyncio

from System.Drawing import FontFamily, SystemFonts

from toga.fonts import (
    CURSIVE,
    FANTASY,
    ITALIC,
    MONOSPACE,
    OBLIQUE,
    SANS_SERIF,
    SERIF,
    SMALL_CAPS,
    SYSTEM,
)


class BaseProbe:
    def assert_font_options(self, weight, style, variant):
        assert self.font.weight == weight

        if style == OBLIQUE:
            print("Intepreting OBLIQUE font as ITALIC")
            assert self.font.style == ITALIC
        else:
            assert self.font.style == style

        if variant == SMALL_CAPS:
            print("Ignoring SMALL CAPS font test")
        else:
            assert self.font.variant == variant

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
