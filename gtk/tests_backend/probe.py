import asyncio
import contextlib

import toga
from toga_gtk.libs import GTK_VERSION, GLib, Gtk

class BaseProbe:
    def _queue_draw(self, data):
        widget, event = data
        widget.queue_draw()
        event.set()

    async def redraw(self, message=None, delay=0):
        """Request a redraw of the app, waiting until that redraw has completed."""
        if (
            hasattr(self, "native")
            and self.native
            and hasattr(self.native, "queue_draw")
        ):
            draw_queued = asyncio.Event()
            GLib.idle_add(self._queue_draw, (self.native, draw_queued))
            await draw_queued

            if frame_clock := self.native.get_frame_clock():
                handler_id = None
                with contextlib.suppress(asyncio.TimeoutError):
                    redraw_complete = asyncio.Future()

                    def on_after_paint(*args):
                        if not redraw_complete.done():
                            redraw_complete.set_result(True)
                        return False

                    handler_id = frame_clock.connect("after-paint", on_after_paint)

                    await asyncio.wait_for(redraw_complete, 0.05)
                if handler_id is not None:
                    with contextlib.suppress(SystemError):
                        frame_clock.disconnect(handler_id)

        # Process events to ensure the UI is fully updated
        for _ in range(15):
            if GTK_VERSION < (4, 0, 0):
                if Gtk.events_pending():
                    Gtk.main_iteration_do(blocking=False)
                else:
                    break
            else:
                context = GLib.main_context_default()
                if context.pending():
                    context.iteration(may_block=False)
                else:
                    break

        # Always yield to let GTK catch up
        await asyncio.sleep(0)

        if toga.App.app.run_slow:
            delay = max(1, delay)
        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    def assert_image_size(self, image_size, size, screen):
        assert image_size == size
