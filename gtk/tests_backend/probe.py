import asyncio

import toga
from toga_gtk.libs import GTK_VERSION, GLib, Gtk


class BaseProbe:

    def repaint_needed(self):
        if GTK_VERSION < (4, 0, 0):
            return Gtk.events_pending()
        else:
            return GLib.main_context_default().pending()

    async def redraw(self, message=None, delay=0):
        """Request a redraw of the app, waiting until that redraw has completed."""
        # Force a repaint
        while self.repaint_needed():
            if GTK_VERSION < (4, 0, 0):
                Gtk.main_iteration_do(blocking=False)
            else:
                GLib.main_context_default().iteration(may_block=False)

        # If we're running slow, wait for a second
        if toga.App.app.run_slow:
            delay = max(1, delay)

        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    def assert_image_size(self, image_size, size, screen):
        assert image_size == size
