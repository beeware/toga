import asyncio

from toga_gtk.libs import GLib


class BaseProbe:
    def assert_font_family(self, expected):
        assert self.font.family == expected

    def repaint_needed(self):
        return GLib.main_context_default().pending()

    async def redraw(self, message=None, delay=None):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a repaint
        while self.repaint_needed():
            GLib.main_context_default().iteration(may_block=False)

        # If we're running slow, wait for a second
        if self.app.run_slow:
            print("Waiting for redraw" if message is None else message)
            delay = 1

        if delay:
            await asyncio.sleep(delay)
