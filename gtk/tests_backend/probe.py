import asyncio

import pytest

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
        if hasattr(self, "native"):
            self.native.queue_draw()

            frame_clock = self.native.get_frame_clock()
            if frame_clock:
                redraw_complete = asyncio.Future()

                def on_after_paint(clock, *args):
                    redraw_complete.set_result(True)
                    return False

                handler_id = frame_clock.connect("after-paint", on_after_paint)

                try:
                    await asyncio.wait_for(redraw_complete, 0.1)
                except asyncio.TimeoutError:
                    pass
                finally:
                    frame_clock.disconnect(handler_id)
        else:
            # Process a few events if frame clock isn't available
            for _ in range(10):
                if GTK_VERSION < (4, 0, 0):
                    Gtk.main_iteration_do(blocking=False)
                else:
                    GLib.main_context_default().iteration(may_block=False)

        # Always yield back to the event loop
        await asyncio.sleep(0)

        # Handle delay
        if toga.App.app.run_slow:
            delay = max(1, delay)

        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    def assert_image_size(self, image_size, size, screen):
        assert image_size == size
