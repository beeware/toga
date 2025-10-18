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
        print(f"[DEBUG REDRAW] Redraw called with message: {message}, delay: {delay}")
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

        print("[DEBUG REDRAW] Processing events to ensure UI is fully updated")
        events_processed = 0
        for i in range(15):
            if GTK_VERSION < (4, 0, 0):
                if Gtk.events_pending():
                    Gtk.main_iteration_do(blocking=False)
                else:
                    break
            else:
                context = GLib.main_context_default()
                if context.pending():
                    print(f"[DEBUG REDRAW] GTK4: Processing context iteration {i + 1}")
                    context.iteration(may_block=False)
                    events_processed += 1
                else:
                    print(
                        f"[DEBUG REDRAW] GTK4: "
                        f"No more events pending after {events_processed} iterations"
                    )
                    break

        # Always yield to let GTK catch up
        print("[DEBUG REDRAW] Yielding control with asyncio.sleep(0)")
        await asyncio.sleep(0)
        print("[DEBUG REDRAW] Redraw method complete")

        if toga.App.app.run_slow:
            delay = max(1, delay)
        if delay:
            print("Waiting for redraw" if message is None else message)
            await asyncio.sleep(delay)

    def assert_image_size(self, image_size, size, screen):
        assert image_size == size
