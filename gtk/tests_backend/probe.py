import asyncio
import contextlib

import toga
from toga_gtk.libs import GLib


class BaseProbe:
    def _queue_draw(self, data):
        widget, event = data
        widget.queue_draw()
        event.set()

    async def redraw(self, message=None, delay=0):
        # Queue a queue_draw, and use frame clock to wait for actual rendering
        if (
            hasattr(self, "native")
            and self.native
            and hasattr(self.native, "queue_draw")
        ):
            draw_queued = asyncio.Event()
            GLib.idle_add(self._queue_draw, (self.native, draw_queued))
            await draw_queued.wait()
            if frame_clock := self.native.get_frame_clock():
                handler_id = None
                # TimeoutError is suppressed because GDK only emits the
                # relevant signals when a frame is being requested.  If
                # the timing is off, after-paint may never get received;
                # protect against that by using a fixed (0.05s) timeout
                # and then ignoring any errors that results from it.
                with contextlib.suppress(asyncio.TimeoutError):
                    redraw_complete = asyncio.Future()

                    def on_after_paint(*args):
                        if not redraw_complete.done():
                            redraw_complete.set_result(True)
                        return False

                    handler_id = frame_clock.connect("after-paint", on_after_paint)

                    await asyncio.wait_for(redraw_complete, 0.05)
                if handler_id is not None:
                    frame_clock.disconnect(handler_id)

        # Process events to ensure the UI is fully updated
        context = GLib.main_context_default()
        while context.pending():
            context.iteration(may_block=False)

        # Always yield to let GTK catch up
        await asyncio.sleep(0)

        if toga.App.app.run_slow:
            delay = max(1, delay)
        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    def assert_image_size(self, image_size, size, screen):
        assert image_size == size
