import asyncio

import toga
from toga_gtk.libs import Gtk


class BaseProbe:
    GTK_VERSION = Gtk.MAJOR_VERSION, Gtk.MINOR_VERSION, Gtk.MICRO_VERSION

    def repaint_needed(self):
        return Gtk.events_pending()

    async def redraw(self, message=None, delay=0):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a repaint
        while self.repaint_needed():
            Gtk.main_iteration_do(blocking=False)

        # If we're running slow, wait for a second
        if toga.App.app.run_slow:
            delay = max(1, delay)

        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    def assert_image_size(self, image_size, size, screen):
        assert image_size == size
