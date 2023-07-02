import asyncio

from toga_gtk.libs import Gtk


class BaseProbe:
    supports_custom_fonts = True

    def assert_font_family(self, expected):
        assert self.font.family == expected

    def assert_font_options(self, weight, style, variant):
        assert self.font.weight == weight
        assert self.font.style == style
        assert self.font.variant == variant

    def repaint_needed(self):
        return Gtk.events_pending()

    async def redraw(self, message=None, delay=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a repaint
        while self.repaint_needed():
            Gtk.main_iteration_do(blocking=False)

        # If we're running slow, wait for a second
        if self.app.run_slow:
            print("Waiting for redraw" if message is None else message)
            delay = 1

        if delay:
            await asyncio.sleep(delay)
